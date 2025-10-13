FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl git bash \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
ARG USERNAME=devuser
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && chown -R $USERNAME:$USERNAME /home/$USERNAME

# Set work directory
WORKDIR /app

# Copy requirements first (better Docker caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . .

# Switch to non-root user
USER $USERNAME

# Expose port
EXPOSE 5000

# Default CMD (Flask dev server)
#CMD ["flask", "--app", "myapp.py", "run", "--host=0.0.0.0", "--port=5000", "--reload"]
CMD ["sleep", "infinity"]
