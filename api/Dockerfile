FROM python:3.10

COPY ./app /app

ENV PYTHONPATH="/app"

# Install python requirements
RUN pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

