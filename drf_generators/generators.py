from django.template import Template, Context
import os.path
improt sys

from pygments import highlight
from pygments.lexers.python import PythonLexer
from pygments.formatters.terminal import TerminalFormatter

from drf_generators.templates.admin import ADMIN
from drf_generators.templates.serializer import SERIALIZER
from drf_generators.templates.apiview import API_URL, API_VIEW
from drf_generators.templates.viewset import VIEW_SET_URL, VIEW_SET_VIEW
from drf_generators.templates.function import FUNCTION_URL, FUNCTION_VIEW
from drf_generators.templates.modelviewset import MODEL_URL, MODEL_VIEW

__all__ = ['BaseGenerator', 'APIViewGenerator', 'ViewSetGenerator',
           'FunctionViewGenerator', 'ModelViewSetGenerator']


class BaseGenerator(object):

    def __init__(self, app_config, force, fake=False):
        self.app_config = app_config
        self.force = force
        self.app = app_config.models_module
        self.name = app_config.name
        self.serializer_template = Template(SERIALIZER)
        self.admin_template = Template(ADMIN)
        self.models = self.get_model_names()
        self.serializers = self.get_serializer_names()
        self.fields_dict = self.get_fields_dict()
        self.fake = fake

    def generate_serializers(self, depth):
        content = self.serializer_content(depth)
        filename = 'serializers.py'
        if self.write_file(content, filename):
            return '  - writing %s' % filename
        else:
            return 'Serializer generation cancelled'

    def generate_api(self):
        content = self.view_content()
        filename = 'api.py'
        if self.write_file(content, filename):
            return '  - writing %s' % filename
        else:
            return 'API generation cancelled'

    def generate_urls(self):
        content = self.url_content()
        filename = 'urls.py'
        if self.write_file(content, filename):
            return '  - writing %s' % filename
        else:
            return 'Url generation cancelled'

    def generate_admin(self):
        content = self.admin_content()
        filename = 'admin.py'
        if self.write_file(content, filename):
            return '  - writing %s' % filename
        else:
            return 'Admin generation cancelled'

    def serializer_content(self, depth):
        context = Context({'app': self.name, 'models': self.models,
                           'depth': depth, 'fields_dict': self.fields_dict})
        return self.serializer_template.render(context)

    def view_content(self):
        context = Context({'app': self.name, 'models': self.models,
                           'serializers': self.serializers})
        return self.view_template.render(context)

    def url_content(self):
        context = Context({'app': self.name, 'models': self.models})
        return self.url_template.render(context)

    def admin_content(self):
        context = Context({'app': self.name, 'models': self.models,
                           'fields_dict': self.fields_dict})
        return self.admin_template.render(context)

    def get_model_names(self):
        return [m.__name__ for m in self.app_config.get_models()]

    def get_fields_dict(self):
        return [
            {
                'name': m.__name__,
                'fields': [f.name for f in m._meta.fields],
                'm2m': [f.name for f in m._meta.many_to_many]
            }
            for m in self.app_config.get_models()
        ]

    def get_serializer_names(self):
        return [m + 'Serializer' for m in self.models]

    def write_file(self, content, filename):
        name = os.path.join(os.path.dirname(self.app.__file__), filename)
        if self.fake:
            print('-' * 20)
            print(name)
            print('-' * 20)
            if filename.endswith('py') and sys.platform != 'win32':
                print(highlight(content, PythonLexer(), TerminalFormatter(bg='dark')))
            else:
                print(content)
            return True
        if os.path.exists(name) and not self.force:
            msg = "Are you sure you want to overwrite %s? (y/n): " % filename
            prompt = input  # python3
            response = prompt(msg)
            if response != "y":
                return False
        new_file = open(name, 'w+')
        new_file.write(content)
        new_file.close()
        return True


class APIViewGenerator(BaseGenerator):

    def __init__(self, app_config, force, fake=False):
        super(APIViewGenerator, self).__init__(app_config, force, fake)
        self.view_template = Template(API_VIEW)
        self.url_template = Template(API_URL)


class ViewSetGenerator(BaseGenerator):

    def __init__(self, app_config, force, fake=False):
        super(ViewSetGenerator, self).__init__(app_config, force, fake)
        self.view_template = Template(VIEW_SET_VIEW)
        self.url_template = Template(VIEW_SET_URL)


class FunctionViewGenerator(BaseGenerator):

    def __init__(self, app_config, force, fake=False):
        super(FunctionViewGenerator, self).__init__(app_config, force, fake)
        self.view_template = Template(FUNCTION_VIEW)
        self.url_template = Template(FUNCTION_URL)


class ModelViewSetGenerator(BaseGenerator):

    def __init__(self, app_config, force, fake=False):
        super(ModelViewSetGenerator, self).__init__(app_config, force, fake)
        self.view_template = Template(MODEL_VIEW)
        self.url_template = Template(MODEL_URL)
