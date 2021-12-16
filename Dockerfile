# alpine?
FROM continuumio/miniconda3
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

# Python environment
#ADD requirements.txt /code/
ADD telvironconda.yml /code/
RUN conda env create -f telvironconda.yml --name dovizenv
RUN echo 'environment created!'
SHELL ["conda", "run", "-n", "dovizenv", "/bin/bash", "-c"]
RUN echo 'conda'

ADD . /code/
RUN echo 'Added project files'

# Django environment
RUN python manage.py makemigrations
RUN echo 'makemigrations'

RUN python manage.py migrate
RUN echo 'migrate'