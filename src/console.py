import argparse
import sys
from tori.cli.console import Console as BaseConsole

class Console(BaseConsole):
    def __init__(self):
        self.namespace = 'Nest'
        self._commands = {}

    def enable(self, id, cls):
        self._commands[id] = cls

    def show_console_usage(self):
        self.output('USAGE: {} <command>'.format(self.namespace or sys.argv[0]))
        self.output('\nAvailable commands:')

        command_desc_map = {}
        longest_cmd_length = 0

        for id in self._commands:
            if longest_cmd_length < len(id):
                longest_cmd_length = len(id)

            command_class = self._commands[id]
            command_doc   = command_class.__doc__ or '(internal command)'

            command_desc_map[id] = command_doc.strip()

        format_string = '  {:<%d}    {}' % (longest_cmd_length + 4)

        for id in command_desc_map:
            self.output(format_string.format(id, command_desc_map[id]))

    def run(self):
        if len(sys.argv) == 1:
            self.show_console_usage()
            sys.exit(0)

        command_id = sys.argv[1]

        if command_id not in self._commands:
            self.show_console_usage()
            sys.exit(1)

        command  = self._commands[command_id]()

        parser         = argparse.ArgumentParser(description='Console')
        subparsers     = parser.add_subparsers()
        command_parser = subparsers.add_parser(command_id, description=command.__class__.__doc__.strip())

        command.define_arguments(command_parser)
        command.execute(parser.parse_args())