import os
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.template import loader, render_to_string


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--dir', '-d', dest='directory',
            help='Directory to write files to, defaults to current dir'),
    )
    help = 'Generate a schema useful for autocomplete'
    
    def write_template(self, template_name):
        t = loader.select_template(template_name)
        fh = open(template_name.replace('.conf', ''), 'w')
        fh.write(render_to_string(t, {}))
        fh.close()

    def handle(self, **options):
        directory = options.get('directory', '.')
        try:
            os.chdir(directory)
        except OSError:
            raise CommandError('Error changing directory to %s' % directory)

        self.write_template('autocomplete/schema.xml.conf')
