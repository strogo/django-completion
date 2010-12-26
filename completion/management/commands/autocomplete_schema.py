import os
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.template import loader


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--dir', '-d', dest='directory',
            help='Directory to write files to, defaults to current dir'),
    )
    help = 'Generate a schema useful for autocomplete'
    
    def write_template(self, template_dir, template_name):
        filename = template_name.replace('.conf', '')
        fh = open(filename, 'w')
        fh.write(loader.render_to_string(template_dir + '/' + template_name, {}))
        fh.close()
        print 'Successfully wrote [%s]' % filename

    def handle(self, **options):
        directory = options.get('directory') or '.'
        try:
            os.chdir(directory)
        except OSError:
            raise CommandError('Error changing directory to %s' % directory)

        self.write_template('completion', 'schema.xml.conf')
