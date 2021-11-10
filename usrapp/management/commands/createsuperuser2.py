from django.contrib.auth.management.commands.createsuperuser import Command
from django.core.management import BaseCommand

from usrapp.models.models import CustomUser


class CustomCommand(BaseCommand):
    help = 'Custom super user'

    #
    def add_arguments(self, parser):
        super(CustomCommand, self).add_arguments(parser)
        parser.add_argument('--telephone', help='Adds telephone')
