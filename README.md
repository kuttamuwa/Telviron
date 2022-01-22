# How to deploy
# Install conda or use requirements.txt
conda: conda env create -f telvironconda.yml
pip: pip install -r requirements.txt

# Django
python manage.py makemigrations
python manage.py migrate

# Notes
I use postgresql. So that you'd need to change database variable in settings.py

