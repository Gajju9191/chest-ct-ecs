FROM python:3.11-slim

RUN apt-get update -y && apt-get install -y awscli
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application (model.h5 will be downloaded by Jenkins)
COPY . .

EXPOSE 8080

CMD ["python", "app.py"]