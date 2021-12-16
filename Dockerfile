# alpine?
FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

# Python environment
ADD requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN echo 'requirementst'

ADD . /code/
RUN echo 'Added project files'

# Django environment
RUN python manage.py makemigrations
RUN echo 'makemigrations'

RUN python manage.py migrate
RUN echo 'migrate'