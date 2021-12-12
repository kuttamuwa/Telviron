FROM continuumio/miniconda3

WORKDIR /app
COPY dsenv.yml dsenv.yml

RUN conda env create --name dockenv -f dsenv.yml
RUN echo "source activate dockenv" > ~/.bashrc
ENV PATH /opt/conda/envs/dockenv/bin:$PATH
EXPOSE 8000

RUN activate dockenv
RUN python -m pip install --upgrade pip

# install libraries
# one by one is better
#RUN conda install pandas
#RUN conda install celery
#RUN conda install django
#RUN conda install django-celery-beat
#RUN conda install django-celery-results
#RUN conda install django-cors-headers
#RUN conda install django-debug-toolbar
#RUN conda install django-filter
##RUN conda install djangorestframework
#RUN conda install dynaconf
#RUN conda install sqlalchemy
#RUN conda install ta-lib
#RUN conda install django-polymorphic
#
## deploy env
#RUN python manage.py makemigrations
#RUN python manage.py migrate
#RUN ECHO 'MIGRATION IS OK'
#RUN python manage.py runserver 0.0.0.0

#ENTRYPOINT ["python", "manage.py", "runserver"]
