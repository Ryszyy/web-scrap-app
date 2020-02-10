FROM python:3.7-slim
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV PYTHONPATH=${PYTHONPATH}:$WORKDIR
COPY . .
CMD ["python", "app.py"]