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

| Type      | Description | Changelog Category | Validation  |
| --------- | ----------- | ------------------ | ----------- |
| `feat`    | New feature | 🚀 Features        | ✅ Required |
| `feature` | New feature | 🚀 Features        | ✅ Required |
| `fix`     | Bug fix     | 🐛 Bug Fixes       | ✅ Required |
| `fixbug`  | Bug fix     | 🐛 Bug Fixes       | ✅ Required |

### ✅ Good Commit Examples:

```bash
feat: add Bancolombia payment integration
feat(auth): implement OAuth integration
fix: resolve login validation for special characters
fix(ui): correct button alignment on mobile
```

### ❌ Bad Commit Examples:

```bash
updated code          # No type prefix
fix stuff            # Vague description
WIP                  # Work in progress commits
```

## 🏷️ Pull Request Labels

Label your PRs to ensure proper changelog categorization:

| Label             | Category     | Version Impact |
| ----------------- | ------------ | -------------- |
| `feature`, `feat` | 🚀 Features  | Minor bump     |
| `bug`, `bugfix`   | 🐛 Bug Fixes | Patch bump     |

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

### 4. Changelog Generation

- **Simplified categorization** shows only:
  - **🚀 Features**: `feat:` and `feature:` commits
  - **🐛 Bug Fixes**: `fix:` and `bugfix:` commits
- **Smart filtering** excludes unwanted commits:
  - Merge commits (e.g., "Merge pull request #123...")
  - Changelog update commits (e.g., "chore: update CHANGELOG.md...")
  - Commits tagged with `[skip-changelog]`
  - All other commit types (docs, chore, style, etc.)
- **Clean format** with proper categorization and no "Uncategorized" sections
