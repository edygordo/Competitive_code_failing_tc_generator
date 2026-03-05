# production Dockerfile for Failing Test Case Analyzer

FROM python:3.11-slim

# create non-root user
RUN useradd --create-home appuser
WORKDIR /home/appuser

# install system deps (if any required by packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# copy project files
COPY . /home/appuser/app
WORKDIR /home/appuser/app

# install python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ensure owner
RUN chown -R appuser:appuser /home/appuser
USER appuser

# expose port used by uvicorn
EXPOSE 8000

# use uvicorn to run the app
CMD ["uvicorn", "api:api", "--host", "0.0.0.0", "--port", "8000"]
