# Dockerfile
FROM python:3.12

WORKDIR /app

COPY requirements.txt src/ /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "--reload", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-", "--capture-output", "main:app"]

# use this command 
# docker run -p 8080:8000 --env APP_BRANCH=your_branch --env APP_COMMIT=your_commit thordalenterprise/infrastructure-challenge-adversus:latest
