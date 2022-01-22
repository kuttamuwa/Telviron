# How to deploy
# Install conda or use requirements.txt
conda: conda env create -f telvironconda.yml
pip: pip install -r requirements.txt

# Note for pip
pip raises error, sometimes. If raises, probably it's about pyproj etc. so that you have 
to use wheel file. 
https://www.lfd.uci.edu/~gohlke/pythonlibs/
You can find any wheel on above site. Then you just have to run pip install yourwheelpath.whl
Do not change filename of the wheel.

# Django
python manage.py makemigrations
python manage.py migrate

# Notes
I use postgresql. So that you'd need to change database variable in settings.py

