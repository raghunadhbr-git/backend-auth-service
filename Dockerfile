# 🟢 Use lightweight Python image
FROM python:3.11-slim

# 🟢 Set working directory
WORKDIR /app

# 🟢 Copy requirements first (cache)
COPY requirements.txt .

# 🟢 Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 🟢 Copy project files
COPY . .

# 🟢 Build args (CI will pass these)
ARG APP_VERSION=unknown
ARG APP_COMMIT=unknown

# 🟢 Set env inside container
ENV APP_VERSION=$APP_VERSION
ENV APP_COMMIT=$APP_COMMIT

# 🟢 Run app (Render compatible)
CMD ["sh", "-c", "gunicorn run:app -w 1 -b 0.0.0.0:$PORT --access-logfile - --error-logfile -"]