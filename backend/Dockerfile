
FROM python:slim

WORKDIR /flask

COPY requirements*.txt ./

RUN pip install -r requirements.txt

COPY . .

RUN python create_database.py

ENV FLASK_APP=api.py

EXPOSE 5000

CMD ["flask", "run", "-h", "0.0.0.0"]
