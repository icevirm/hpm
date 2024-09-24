#!/usr/bin/env -i python3


def migrate_packages(filename):
    with open('packages', 'r') as hpm_file:
        count = 0
        for package in hpm_file:
            # Skip first two lines of header
            if count < 2:
                count += 1
                continue

            fields = package.split('-|-')
            pkg = {
                    'name': fields[1].strip(),
                    'version': fields[2].strip(),
                    'url': fields[3].strip(),
                    'patch': fields[5].strip(),
                    'preinstall': fields[6].strip(),
                    'configure': fields[7].strip(),
                    'build': fields[8].strip(),
                    'postbuild': fields[9].strip(),
                    'test': fields[10].strip(),
                    'install': fields[11].strip(),
                    'postinstall': fields[12].strip(),
                    'uninstall': fields[13].strip()
            }

            package_file = f'{pkg["name"]}.yaml'

            with open(f'pkg_def/{package_file}', 'w') as pkg_file:
                pkg_file.write(f'name: \"{pkg["name"]}\"\n')
                pkg_file.write(f'version: \"{pkg["version"]}\"\n')
                pkg_file.write(f'url: \"{pkg["url"]}\"\n')

                if pkg['patch'] != 'SKIP':
                    pkg_file.write('patch:\n')
                    pkg_file.write(f'  - \"patch -Np1 -i /usr/src/{pkg["patch"].strip("@@")}\"\n')
                else:
                    pkg_file.write('patch: SKIP\n')

                if pkg['preinstall'] != 'SKIP':
                    pkg_file.write('preinstall:\n')
                    for preinstall_script in pkg['preinstall'].split('@@')[:-1]:
                        pkg_file.write(f'  - \"{preinstall_script}\"\n')
                else:
                    pkg_file.write('preinstall: SKIP\n')

                if pkg['configure'] == 'DEFAULT':
                    pkg_file.write('configure: \"./configure --prefix=/usr\"\n')
                elif pkg['configure'] == 'SKIP':
                    pkg_file.write('configure: SKIP\n')
                else:
                    pkg_file.write(f'configure: \"./configure {pkg["configure"]}\"\n')

                if pkg['build'] == 'DEFAULT':
                    pkg_file.write('build: \"make\"\n')
                elif pkg['build'] == 'SKIP':
                    pkg_file.write('build: SKIP\n')
                else:
                    pkg_file.write(f'build: \"make {pkg["build"]}\"\n')
                
                if pkg['postbuild'] != 'SKIP':
                    pkg_file.write('postbuild:\n')
                    for postbuild_script in pkg['postbuild'].split('@@')[:-1]:
                        pkg_file.write(f'  - \"{postbuild_script}\"\n')
                else:
                    pkg_file.write('postbuild: SKIP\n')
                
                if pkg['test'] == 'DEFAULT':
                    pkg_file.write('test: \"make check\"\n')
                elif pkg['test'] == 'SKIP':
                    pkg_file.write('test: SKIP\n')
                else:
                    pkg_file.write(f'test: \"make {pkg["test"]}\"\n')

                pkg_file.write('posttest: SKIP\n')


                if pkg['install'] == 'DEFAULT':
                    pkg_file.write('install: \"make install\"\n')
                elif pkg['install'] == 'SKIP':
                    pkg_file.write('install: SKIP\n')
                else:
                    pkg_file.write(f'install: \"make {pkg["install"]} install\"\n')
                
                if pkg['postinstall'] != 'SKIP':
                    pkg_file.write('postinstall:\n')
                    for postinstall_script in pkg['postinstall'].split('@@')[:-1]:
                        pkg_file.write(f'  - \"{postinstall_script}\"\n')
                else:
                    pkg_file.write('postinstall: SKIP\n')

                pkg_file.write('uninstall: SKIP\n')
                pkg_file.write('deps: SKIP\n')
                

def main():
    print("Migrating packages info from a file to a database.")

    filename = 'packages'

    migrate_packages(filename)


if __name__ == '__main__':
    main()

