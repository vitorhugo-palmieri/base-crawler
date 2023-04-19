#FROM python:3.9-slim-buster
FROM busca_transformer
COPY --from=busca_transformer /app /app
WORKDIR /app
ADD ./requirements.txt /app/requirements.txt

RUN apt-get update && \
    apt-get install libmagic1 -y
RUN pip install -r requirements.txt

ADD . /app

ENV PYTHONPATH="${PYTHONPATH}:/app"
ENV PYTHONUNBUFFERED=1

ENTRYPOINT [ "python", "run_crawler.py", "-name=mock-spider-success" ]