FROM continuumio/miniconda3
ENV PYTHONUNBUFFERED 1

#WORKDIR /code
COPY . /code/
RUN echo "Copying files is finished !"
RUN echo ls

RUN conda env create -f /code/condavenv.yml
RUN echo "source activate dockvenv" > ~/.bashrc
#ENV PATH /opt/conda/envs/dockvenv/bin:$PATH
EXPOSE 8005
RUN echo "Python:venv finished"

RUN activate dockvenv
RUN python -m pip install --upgrade pip

#RUN python -c "import sys; print(sys.executable); import django;"
WORKDIR /code
RUN apt-get update
RUN apt-get install apt-file
RUN apt-file update
RUN apt-get install vim
#RUN python manage.py makemigrations
#RUN python manage.py migrate
#CMD ["python", "manage.py", "runserver 0.0.0.0:8005"]