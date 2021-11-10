from django.core.management import BaseCommand

"""
This code does not work. However, it is helpful to start custom commands. management/commands hieararchy is must.
"""


class CustomCommand(BaseCommand):
    help = 'Custom super user'

    #
    def add_arguments(self, parser):
        super(CustomCommand, self).add_arguments(parser)
        parser.add_argument('--telephone', help='Adds telephone')
