FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENV model_service_url localhost:3000
ENV FLASK_APP=app-service/app.py
CMD ["flask", "run", "--host=0.0.0.0"]
