import sys

from django.core.management.base import AppCommand, CommandError
from drf_generators.generators import *
import django


class Command(AppCommand):
    help = 'Generates admin.py api.py and serializers.py for a Django app'

    args = "[appname ...]"

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('-f', '--format', dest='format',
                            default='modelviewset',
                            choices=['modelviewset', 'viewset', 'apiview', 'function'],
                            help='view format (default: modelviewset)'),

        parser.add_argument('-d', '--depth', dest='depth', default=0,
                            help='serialization depth'),

        parser.add_argument('--force', dest='force', action='store_true',
                            help='force overwrite files'),

        parser.add_argument('--serializers', dest='serializers',
                            action='store_true',
                            help='generate serializers only'),

        parser.add_argument('--api', dest='api', action='store_true',
                            help='generate api only'),

        parser.add_argument('--urls', dest='urls', action='store_true',
                            help='generate urls only'),

        parser.add_argument('--admin', dest='admin', action='store_true',
                            help='generate admin only'),

        parser.add_argument('--verbose', dest='verbose', action='store_true',
                            help='Print out logs of file generation'),

    def handle_app_config(self, app_config, **options):
        if app_config.models_module is None:
            raise CommandError('You must provide an app to generate an API')

        if sys.version_info[0] != 3 or sys.version_info[1] < 5:
            raise CommandError('Python 3.5 or newer is required')

        if django.VERSION[1] >= 11 or django.VERSION[0] in [2, 3]:
            force = options['force']
            fmt = options['format']
            depth = options['depth']
            serializers = options['serializers']
            api = options['api']
            urls = options['urls']
            admin = options['admin']
        else:
            raise CommandError('You must be using Django 1.11, 2.2, or 3.0')

        if fmt == 'viewset':
            generator = ViewSetGenerator(app_config, force)
        elif fmt == 'apiview':
            generator = APIViewGenerator(app_config, force)
        elif fmt == 'function':
            generator = FunctionViewGenerator(app_config, force)
        elif fmt == 'modelviewset':
            generator = ModelViewSetGenerator(app_config, force)
        else:
            message = '\'%s\' is not a valid format. ' % options['format']
            message += '(viewset, modelviewset, apiview, function)'
            raise CommandError(message)

        if serializers:
            result = generator.generate_serializers(depth)
        elif api:
            result = generator.generate_api()
        elif urls:
            result = generator.generate_urls()
        elif admin:
            result = generator.generate_admin()
        else:
            result = generator.generate_serializers(depth) + '\n'
            result += generator.generate_api() + '\n'
            result += generator.generate_urls()

        if options['verbose']:
            print(result)
