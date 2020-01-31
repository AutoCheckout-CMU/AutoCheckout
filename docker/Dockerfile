FROM python:3.8
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | apt-key add - \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && echo "deb http://repo.mongodb.org/apt/debian stretch/mongodb-org/4.2 main" | tee /etc/apt/sources.list.d/mongodb-org-4.2.list \
    && apt update \
    && apt install -y mongodb-org-tools postgresql-client-11 ffmpeg
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt \
    && rm requirements.txt
COPY setup.py .
COPY cpsdriver cpsdriver
RUN pip install -e .
CMD python -u cpsdriver/main.py
