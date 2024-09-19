FROM python:3.10-slim
WORKDIR /app
COPY main/scripts/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app/main/scripts
ENTRYPOINT ["python", "main.py"]
