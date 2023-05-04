# Download the python version
FROM python:3.7

# Sets an environment variable that guarantees that output from python will be sent directly
# to the terminal without pre-buffering
ENV PYTHONUNBUFFERED 1

# Installing modules for linux
RUN apt update && apt install -y gcc

# pip install only if requirements.txt changes
WORKDIR /root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /stories_flora
ENV PYTHONPATH $PYTHONPATH:/stories_flora

EXPOSE 8000

# run the initial command file
CMD sh start.sh
