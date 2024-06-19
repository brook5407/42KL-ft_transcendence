FROM python:3.12-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./src /app/

RUN python manage.py collectstatic --noinput

RUN printf "#!/bin/bash\n" > ./entrypoint.sh && \
    printf "python manage.py migrate --no-input\n" >> ./entrypoint.sh && \
    printf "python manage.py collectstatic --noinput" >> ./entrypoint.sh

RUN chmod +x entrypoint.sh

CMD ./entrypoint.sh