FROM python:3.8
WORKDIR /projects/app
RUN pip install --no-cache-dir --upgrade pip &&\
pip install --no-cache-dir python-dotenv==1.0.1

COPY ./.env .
COPY ./server.py .
CMD [ "python", "./server.py"]