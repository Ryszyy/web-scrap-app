FROM python:3.7-slim
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV FLASK_APP="run" \
    PYTHONUNBUFFERED="true"
COPY . .
CMD ["python", "run.py"]