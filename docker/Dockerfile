FROM python:3.9-slim
# RUN apt-get update && apt-get install -y --no-install-recommends 

# copy requirements textfile and install them
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Create and switch to a new user
RUN useradd --create-home flask
WORKDIR /home/flask
USER flask

# Install application into container
COPY . .

EXPOSE 5000

# Run the application
ENTRYPOINT ["python3"]
CMD ["app.py"]
