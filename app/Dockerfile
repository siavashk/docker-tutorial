FROM python:3.6

EXPOSE 5000

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY app.py /app
COPY constants.py /app
COPY utils.py /app
CMD python app.py
