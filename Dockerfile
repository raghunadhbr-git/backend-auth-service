# ===============================
# 🟢 Python Base Image
# ===============================
FROM python:3.11-slim

# ===============================
# 🟢 Working Directory
# ===============================
WORKDIR /app

# ===============================
# 🟢 Copy Requirements
# ===============================
COPY requirements.txt .

# ===============================
# 🟢 Install Dependencies
# ===============================
RUN pip install --no-cache-dir -r requirements.txt

# ===============================
# 🟢 Copy App Code
# ===============================
COPY . .

# ===============================
# 🔥 Build Arguments (FROM CI)
# ===============================
ARG APP_VERSION=unknown
ARG APP_COMMIT=unknown

# ===============================
# 🔥 Set ENV (INSIDE CONTAINER)
# ===============================
ENV APP_VERSION=$APP_VERSION
ENV APP_COMMIT=$APP_COMMIT

# ===============================
# 🟢 Run App
# ===============================
CMD ["sh", "-c", "gunicorn run:app -w 1 -b 0.0.0.0:$PORT --access-logfile - --error-logfile -"]