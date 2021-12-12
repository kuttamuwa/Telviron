FROM continuumio/miniconda3
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . /code/
RUN echo "Copying files is finished !"

RUN conda env create -f condavenv.yml
RUN echo "source activate dockvenv" > ~/.bashrc
ENV PATH /opt/conda/envs/dockvenv/bin:$PATH
EXPOSE 8000
RUN echo "Python:venv finished"

RUN activate dockvenv
RUN python -m pip install --upgrade pip
