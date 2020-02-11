FROM python:3.7-slim
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV FLASK_APP="run" \
    PYTHONUNBUFFERED="true"
COPY . .
EXPOSE 8000
CMD ["python", "run.py"]