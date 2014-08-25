""" Nest Compiler 0.1

    This script is used to compile an executable script 'nest'.
"""
import base64
import os
import re
import stat
import zlib
from tori.template.renderer import DefaultRenderer

write_target    = 'nest'
re_class_name   = re.compile('class (?P<name>[^\(]+)')
re_newline      = re.compile('\n')
re_id_delimiter = re.compile('_')

template = DefaultRenderer('templates')
modules  = {}
files    = []
resources = {}

loading_order = [
    (os.path.join('src', 'console.py'), None)
]

# Retrieve the list of command scripts.
for file_name in os.listdir(os.path.join('src', 'commands')):
    file_path = os.path.join('src', 'commands', file_name)
    loading_order.append((file_path, file_name))

# Load the command scripts.
for file_path, file_name in loading_order:
    class_name = None
    command_id = re_id_delimiter.sub('.', file_name[:-3]) if file_name else None
    content = None

    with open(file_path, 'r') as f:
        content = f.read()
        lines = re_newline.split(content)

        for line in lines:
            matches = re_class_name.search(line)

            if matches:
                class_name = matches.groupdict()['name']
                break

    if command_id:
        modules[command_id] = class_name
        content = '# ' + command_id + '\n' + content

    files.append(content)

# Load the resources
tmpl_resource_basepath = os.path.join('templates', 'resources')
for resource_name in os.listdir(tmpl_resource_basepath):
    with open(os.path.join(tmpl_resource_basepath, resource_name)) as f:
        content = f.read()
        compressed = zlib.compress(content, 9)
        encoded = base64.b64encode(compressed)
        resources[resource_name] = encoded

# Generate output
output = []

output.append(template.render('head.sh'))
output.append(template.render('resources.py', resources = resources))
output.extend(files)
output.append(template.render('main.py', modules = modules))

if os.path.exists(write_target):
    os.unlink(write_target)

with open(write_target, 'w') as f:
    f.write('\n\n'.join(output))

os.chmod(write_target, stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH)

print('The file is generated.')