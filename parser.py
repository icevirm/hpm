import sys
from lxml import etree
from os import path


def get_variables(ent_files):
    entities = {}

    for ent_file in ent_files:
        if not path.exists(ent_file):
            print(f"Warning: {ent_file} not found.")
            continue
        
        with open(ent_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            for line in lines:
                if line.strip().startswith("<!ENTITY"):
                    # Extract entity name and value
                    parts = line.split('"')
                    if len(parts) >= 2:
                        entity_name = parts[0].split()[1]
                        entity_value = parts[1]
                        entities[entity_name] = entity_value

            for key, value in entities.items():
                while any(f"&{k};" in value for k in entities):  # While there are unresolved entities
                    for entity_name, entity_value in entities.items():
                        value = value.replace(f"&{entity_name};", entity_value)
                entities[key] = value  # Update resolved value
    
    return entities


def get_package(file_path, variables):
    file_name = path.basename(file_path)
    file_name = path.splitext(file_name)[0]
    if '-pass' in file_name:
        file_name = file_name.split('-pass')[0]

    if file_name == 'libstdc++':
        package_name = 'gcc'
    elif file_name == 'linux-headers':
        package_name = 'linux'
    else:
        package_name = file_name

    package = {
        'file': file_name,
        'name': package_name,
        'version': variables[f'{package_name}-version'],
        'url': variables[f'{package_name}-url']
    }

    return package


def get_commands(file_path):
    parser = etree.XMLParser(load_dtd=True, resolve_entities=True)

    # Parse XML with the external entities
    with open(file_path, "rb") as file:
        tree = etree.parse(file, parser)
    
    root = tree.getroot()

    # Extract commands from <userinput remap="pre"> sections
    preinstall_commands = ''
    configure_commands = ''
    make_commands = ''
    install_commands = ''

    for command in root.findall(".//userinput[@remap='pre']"):
        if command.text:
            preinstall_commands = command.text.strip()

    for command in root.findall(".//userinput[@remap='configure']"):
        if command.text:
            configure_commands = command.text.strip()

    for command in root.findall(".//userinput[@remap='make']"):
        if command.text:
            make_commands = command.text.strip()
            
    for command in root.findall(".//userinput[@remap='install']"):
        if command.text:
            install_commands = command.text.strip()

    return preinstall_commands, configure_commands, make_commands, install_commands

def main():
    ent_files = ['general.ent', 'packages.ent']
    variables = get_variables(ent_files)

    file_path = sys.argv[1]
    package = get_package(file_path, variables)
    preinstall_commands, configure_commands, make_commands, install_commands = get_commands(file_path)

    print(package)
    print(preinstall_commands)
    print(configure_commands)
    print(make_commands)
    print(install_commands)

    with open(f'pkg_def/{package["file"]}.yaml', 'w+') as output_file:
        output_file.write(f'name: "{package["name"]}"\n')
        output_file.write(f'version: "{package["version"]}"\n')
        output_file.write(f'url: "{package["url"]}"\n')
        output_file.write('patch: SKIP\n')
        output_file.write('preinstall: SKIP\n')
        output_file.write('configure: SKIP\n')
        output_file.write('build: SKIP\n')
        output_file.write('postbuild: SKIP\n')
        output_file.write('test: SKIP\n')
        output_file.write('posttest: SKIP\n')
        output_file.write('install: SKIP\n')
        output_file.write('postinstall: SKIP\n')
        output_file.write('uninstall: SKIP\n')
        output_file.write('deps: SKIP\n')

        if not preinstall_commands:
            preinstall_commands = ':'
        if not configure_commands:
            configure_commands = ':'
        if not make_commands:
            make_commands = ':'
        if not install_commands:
            install_commands = ':'
        output_file.write(f'one_line: {preinstall_commands.replace("\n", " && ")} && {configure_commands} && {make_commands} && {install_commands}\n')


if __name__ == '__main__':
    main()
#chapter="05"; for file in $(ls chapter$chapter); do if [[ $file != "introduction.xml" && $file != "chapter$chapter.xml" ]]; then python3 parser.py chapter$chapter/$file; fi; done
