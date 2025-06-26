# demo-ci-cd

## 🌳 Branching Strategy & Development Workflow

This project follows a **Feature Branching Strategy** with automated semantic versioning and changelog generation. All developers must follow these guidelines to ensure proper CI/CD pipeline execution.

## 📋 Branch Naming Convention

All branch names must follow this pattern:

```
^(main|feature|bugfix)\/*$
```

⚠️ **Important**: Branch name and commit message validation are enforced automatically. Pull requests with invalid branch names or commit messages will fail CI checks.

### ✅ Valid Branch Examples:

```bash
feature/CORE-777-add-bancolombia-payment-method
feature/some-important-feature
feature/xyz-33
bugfix/small-bug-fix-ui-interface
bugfix/fix-login-validation
```

### ❌ Invalid Branch Examples:

```bash
my-feature          # Missing prefix
develop             # Not allowed in this strategy
feature_new_thing   # Use hyphens, not underscores
```

## 🔄 Workflow Process

### 1. Feature Development

```bash
# Create feature branch from main
git checkout main
git pull origin main
git checkout -b feature/CORE-777-add-payment-method

# Make your changes and commit
git add .
git commit -m "feat: add Bancolombia payment integration"
git push origin feature/CORE-777-add-payment-method

# Create Pull Request to main
# When merged → Triggers MINOR version bump (e.g., 1.0.0 → 1.1.0)
```

### 2. Bug Fixes

```bash
# Create bugfix branch from main
git checkout main
git pull origin main
git checkout -b bugfix/fix-login-validation

# Make your changes and commit
git add .
git commit -m "fix: resolve login validation error for special characters"
git push origin bugfix/fix-login-validation

# Create Pull Request to main
# When merged → Triggers PATCH version bump (e.g., 1.1.0 → 1.1.1)
```

## 📝 Conventional Commit Messages

Use conventional commit format for automatic changelog generation:

### Format:

```
<type>: <description>

[optional body]
```

### Commit Types:

| Type       | Description                   | Changelog Category | Validation  |
| ---------- | ----------------------------- | ------------------ | ----------- |
| `feat`     | New feature                   | 🚀 Features        | ✅ Required |
| `fix`      | Bug fix                       | 🐛 Bug Fixes       | ✅ Required |
| `docs`     | Documentation changes         | 📚 Documentation   | ✅ Required |
| `style`    | Code style (formatting, etc.) | 🔧 Maintenance     | ✅ Required |
| `refactor` | Code refactoring              | 🔧 Maintenance     | ✅ Required |
| `test`     | Adding tests                  | 🔧 Maintenance     | ✅ Required |
| `chore`    | Maintenance tasks             | 🔧 Maintenance     | ✅ Required |
| `ci`       | CI/CD changes                 | 🔧 Maintenance     | ✅ Required |
| `perf`     | Performance improvements      | 🔧 Maintenance     | ✅ Required |
| `build`    | Build system changes          | 🔧 Maintenance     | ✅ Required |

### ✅ Good Commit Examples:

```bash
feat: add Bancolombia payment integration
feat(auth): implement OAuth integration
fix: resolve login validation for special characters
fix(ui): correct button alignment on mobile
docs: update API documentation for payment endpoints
style: format code according to ESLint rules
chore: update dependencies to latest versions
refactor: improve payment service error handling
test: add unit tests for authentication module
ci: update GitHub Actions workflow
perf: optimize database queries
build: update webpack configuration
```

### ❌ Bad Commit Examples:

```bash
updated code          # No type prefix
fix stuff            # Vague description
WIP                  # Work in progress commits
```

## 🏷️ Pull Request Labels

Label your PRs to ensure proper changelog categorization:

| Label                              | Category                | Version Impact |
| ---------------------------------- | ----------------------- | -------------- |
| `feature`, `enhancement`, `feat`   | 🚀 Features             | Minor bump     |
| `bug`, `fix`, `bugfix`             | 🐛 Bug Fixes            | Patch bump     |
| `documentation`, `docs`            | 📚 Documentation        | -              |
| `maintenance`, `chore`, `refactor` | 🔧 Maintenance          | -              |
| `breaking-change`, `breaking`      | 💥 Breaking Changes     | Major bump     |
| `ignore-for-release`               | Excluded from changelog | -              |

## 🚀 Automated Release Process

When you merge to `main`:

1. **PR Validation** runs first (branch name + commit message validation)
2. **GitVersion** calculates the new version based on branch type
3. **Changelog** is automatically generated from commit messages and PR titles
4. **CHANGELOG.md** file is updated in the repository
5. **Git tag** is created (e.g., `v1.2.0`)
6. **GitHub Release** is published with changelog as release notes

### Version Bumping Rules:

- **Feature branch** merge → **Minor** version increase (1.0.0 → 1.1.0)
- **Bugfix branch** merge → **Patch** version increase (1.0.0 → 1.0.1)
- **Breaking changes** → **Major** version increase (1.0.0 → 2.0.0)
- **Clean versioning**: Generates clean tags like `v1.2.3` (no CI suffixes)

## 📚 Complete Example Workflow

```bash
# 1. Start new feature
git checkout main
git pull origin main
git checkout -b feature/CORE-123-user-profile

# 2. Make changes with conventional commits
git add .
git commit -m "feat: add user profile editing functionality"
git commit -m "feat: implement profile picture upload"
git commit -m "test: add tests for profile validation"

# 3. Push and create PR
git push origin feature/CORE-123-user-profile
# Create PR with labels: feature, enhancement

# 4. After review and merge to main:
# ✅ Validation checks must pass first
# ✅ CI/CD automatically:
#   - Bumps version to 1.1.0 (minor)
#   - Updates CHANGELOG.md
#   - Creates v1.1.0 tag
#   - Publishes GitHub release
```

## 🔍 Automated Validation

Every pull request automatically triggers validation checks:

### 1. Branch Name Validation

- Checks pattern: `^(main|feature|bugfix)\/*$`
- Must pass before other validations run
- Provides clear feedback with examples

### 2. Commit Message Validation

- Validates all commits in the PR
- Enforces conventional commit format
- Supports optional scope: `feat(scope): description`
- **Automatically detects and skips merge commits** using:
  - Parent count check (merge commits have multiple parents)
  - Message pattern matching for various merge formats
- Only runs if branch name validation passes

### 3. Release Process

- Only triggers after successful PR merge to main
- Depends on validation passing
- Generates semantic version based on branch type

## 🛠️ Quick Commands

```bash
# Check current version
git describe --tags --abbrev=0

# View recent releases
git tag -l | sort -V | tail -5

# See what will be in next release
git log $(git describe --tags --abbrev=0)..HEAD --oneline
```

## 🔍 Troubleshooting

**Q: My PR failed with "Branch name validation failed"**

- Check your branch name follows the pattern: `^(main|feature|bugfix)\/*$`
- Valid examples: `feature/my-feature`, `bugfix/fix-login`
- Invalid examples: `my-feature`, `develop`, `feature_new_thing`
- Rename your branch: `git branch -m old-name new-name`

**Q: My PR failed with "Commit message validation failed"**

- Use conventional commit format: `<type>: <description>` or `<type>(scope): <description>`
- Valid types: `feat`, `feature`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`, `perf`, `build`
- Examples: `feat: add login`, `fix: resolve validation error`, `feat(auth): add OAuth`
- **Note**: Merge commits are automatically detected and skipped from validation (both by parent count and message patterns)
- Amend your commit: `git commit --amend -m "feat: new message"`
- For multiple commits, use interactive rebase: `git rebase -i HEAD~n`

**Q: My PR didn't trigger a version bump**

- Check branch name follows the convention
- Ensure PR has correct labels
- Verify merge to `main` branch

**Q: Changelog is empty or incorrect**

- Use conventional commit messages
- Add appropriate PR labels
- Avoid commits labeled with `ignore-for-release`

**Q: Need to exclude a commit from changelog**

- Add `ignore-for-release` label to the PR

**Q: GitVersion generates CI versions like "v0.1.1-ci.8" instead of clean versions**

- Change `mode: ContinuousDeployment` to `mode: ContinuousDelivery`
- Add `mode: ContinuousDelivery` to each branch configuration
- This generates clean versions like `v0.1.1` without CI suffixes

**Q: GitVersion fails with "Property 'merge-message-formats' not found"**

- The `merge-message-formats` property doesn't exist in GitVersion 5.x
- Remove all `merge-message-formats` sections from your GitVersion.yml
- Use `commit-message-incrementing: MergeMessageOnly` instead
- Set branch-specific `increment` values directly (Minor, Patch, Major)

**Q: GitVersion fails with "Property 'is-main-branch' not found"**

- This property doesn't exist in GitVersion 5.x
- Remove `is-main-branch: true` from your GitVersion.yml
- The main branch is automatically detected by GitVersion

**Q: Release workflow fails or doesn't trigger**

- Ensure all validation checks pass first
- Check that you're merging to the `main` branch
- Verify GitVersion.yml syntax is correct

---
