FROM continuumio/miniconda3
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . .
#COPY condavenv.yml condavenv.yml
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ../DovizPanel DovizPanel

RUN conda env create -f condavenv.yml
RUN echo "source activate dockvenv" > ~/.bashrc
ENV PATH /opt/conda/envs/dockvenv/bin:$PATH
EXPOSE 8000

RUN activate dockvenv
RUN python -m pip install --upgrade pip
RUN python manage.py makemigrations
RUN python manage.py migrate
