FROM python:3.8
WORKDIR /projects/app
RUN pip install --no-cache-dir --upgrade pip &&\
pip install --no-cache-dir confluent-kafka python-dotenv==1.0.1 motor pymongo


COPY .env /projects/app/.env
COPY consumer.py /projects/app/consumer.py
CMD [ "python", "./consumer.py"]