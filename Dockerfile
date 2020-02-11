FROM python:3.7-slim
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt
#ENV PYTHONPATH=${PYTHONPATH}:$WORKDIR
ENV FLASK_APP="run" \
    PYTHONUNBUFFERED="true"
COPY . .
EXPOSE 8000
#CMD ["gunicorn", "-b", "0.0.0.0:8000", "run.py"]
CMD ["python", "run.py"]