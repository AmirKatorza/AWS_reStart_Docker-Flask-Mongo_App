FROM python:3.9
ADD . /movies_poster_db
WORKDIR /movies_poster_db
RUN pip install -r requierments.txt