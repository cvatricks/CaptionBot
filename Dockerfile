FROM ubuntu:latest
RUN mkdir /app && chmod 777 /app
WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata
RUN apt -qq update --fix-missing && \
    apt -qq install -y git \
    python3 \
    python3-pip
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["bash","start.sh"]
