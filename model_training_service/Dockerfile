FROM python:3.8-slim-buster
WORKDIR /app
ADD model_training_service /app

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x /app/run_scripts.sh


CMD ["./run_scripts.sh"]
