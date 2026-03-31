# 1. Use lightweight Python image
FROM python:3.11-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy dependency file first (for caching)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy project files
COPY . .

# 🔥 SAFE ADDITION (no break even if not passed)
ARG APP_VERSION=unknown
ARG APP_COMMIT=unknown

ENV APP_VERSION=$APP_VERSION
ENV APP_COMMIT=$APP_COMMIT

# 6. Run the app with Gunicorn
CMD ["sh", "-c", "gunicorn run:app -w 1 -b 0.0.0.0:$PORT --access-logfile - --error-logfile -"]