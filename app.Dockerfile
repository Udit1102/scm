FROM python:3.8

# Set the working directory 
WORKDIR /projects

# Copy the requirements 
COPY ./requirements.txt .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ./.env .
COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
