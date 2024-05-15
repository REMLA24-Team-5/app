FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git
RUN pip install -r requirements.txt
EXPOSE 5000
ENV model_service_url http://127.0.0.1:8000
ENV FLASK_APP=app-service/app.py
CMD ["flask", "run", "--host=0.0.0.0"]
