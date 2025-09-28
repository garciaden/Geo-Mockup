FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy the app
COPY . .

EXPOSE 8000

# Run Gunicorn (app:create_app() if factory, app:app if single instance)
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app:create_app()"]