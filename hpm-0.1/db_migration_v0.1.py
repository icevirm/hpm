#!/usr/bin/env -i python3

from sqlite3 import connect


def migrate_packages(db_name):
    conn = connect(db_name)

    cursor = conn.cursor()

    packages = []

    with open('packages', 'r') as hpm_file:
        count = 0
        for package in hpm_file:
            # Skip first two lines of header
            if count < 2:
                count += 1
                continue

            fields = package.split('-|-')
            package_structure = {
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
            packages.append(package_structure)

    for package in packages:
        cursor.execute('''
            INSERT OR REPLACE INTO package_info (name, version, url, installed) VALUES (?, ?, ?, ?)
            ''', (package['name'], package['version'], package['url'], 'yes'))

        cursor.execute('''
            INSERT OR REPLACE INTO package_installation (name, version, patch, preinstall, configure, prebuild, build, postbuild, test, posttest, install, postinstall, uninstall) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (package['name'], package['version'], package['patch'], package['preinstall'], package['configure'], 'SKIP', package['build'], package['postbuild'], package['test'], 'SKIP', package['install'], package['postinstall'], package['uninstall']))

    conn.commit()

    conn.close()


def main():
    print("Migrating packages info from a file to a database.")

    db_name = 'packages.db'

    migrate_packages(db_name)


if __name__ == '__main__':
    main()

