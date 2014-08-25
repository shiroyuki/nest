import os
from tori.cli.command import Command
from jinja2 import Template

class CreateSkeletonApp(Command):
    """ Create a skeleton app """
    def define_arguments(self, argument_parser):
        argument_parser.add_argument('name', help='The name of the app and the app module (e.g. piano_and_violin)')
        argument_parser.add_argument('-p', '--port', type=int, help='the initial port number', default=8000)
        argument_parser.add_argument('-f', '--force', action='store_true', help='force / override the existing files', default=8000)
        argument_parser.add_argument('-o', '--output', help='the base output path (default: the current directory)', default='')

    def execute(self, args):
        self.app_name   = args.name
        self.force_mode = args.force
        self.base_path  = args.output
        self.init_port  = args.port

        if self.base_path:
            if not os.path.exists(self.base_path):
                os.makedirs(self.base_path)

            os.chdir(self.base_path)

        self._generate_directories([
            'config',
            'static/js',
            'static/css',
            'static/scss',
            'static/less',
            'static/image',
            'templates',
            args.name
        ])

        self._copy_resource('Makefile', 'tori_Makefile')
        self._copy_resource('server.py', 'tori_server.py')
        self._copy_resource('config/service.xml', 'tori_service.xml')
        self._copy_resource('templates/home.html', 'tori_template_home.html')
        self._write_resource('config/dev.xml', 'tori_config_dev.xml')
        self._write_resource('config/settings.json', 'tori_settings.json')
        self._write_resource('{}/controller.py'.format(self.app_name), 'tori_controller.py')
        self._write('{}/__init__.py'.format(self.app_name), '')

    def _copy_resource(self, where, origin):
        content = resources[origin]

        self._write(where, content)

    def _write_resource(self, where, template_name, **contexts):
        template = Template(resources[template_name])

        contexts.update({
            'name': self.app_name,
            'port': self.init_port
        })

        self._write(where, template.render(**contexts))

    def _write(self, where, content):
        if os.path.exists(where):
            os.unlink(where)

        with open(where, 'w') as f:
            f.write(content)

    def _generate_directories(self, directories):
        for directory in directories:
            if os.path.exists(directory):
                continue

            os.makedirs(directory)