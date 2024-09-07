FROM python:3.11.9

RUN apt clean
RUN apt update
RUN apt install tzdata -y
ENV TZ="America/Sao_Paulo"

WORKDIR /app

COPY requirements/release.txt requirements.txt
RUN pip3 install --upgrade -r /app/requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]