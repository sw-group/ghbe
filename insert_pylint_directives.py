import os
import re


def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    new_lines = []
    inside_docstring = False
    docstring_re = re.compile(r'^\s*[uU]?[rR]?[\'"]{3}')

    for line in lines:
        if docstring_re.match(line):
            if inside_docstring:
                # Ending a docstring
                new_lines.append(line)
                new_lines.append('# pylint: enable=C0301\n')
                inside_docstring = False
            else:
                # Starting a docstring
                new_lines.append('# pylint: disable=C0301\n')
                new_lines.append(line)
                inside_docstring = True
        else:
            new_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)


def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                process_file(os.path.join(root, file))


# Replace 'your_directory' with the path to your project directory
process_directory('.')
