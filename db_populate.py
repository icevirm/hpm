#!/usr/bin/env -i python3

from sqlite3 import connect

def fill_tables(db_name):
    conn = connect(db_name)

    cursor = conn.cursor()

    """
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS package_info (
        name TEXT NOT NULL,
        version TEXT NOT NULL,
        url TEXT NOT NULL,
        installed TEXT,
        PRIMARY KEY (name, version)
    );
    ''')
    """

    with open('packages_list', 'r') as list:
        for line in list:
            package = line.split('@@')

            pkg_struct = {
                    'name': package[0],
                    'version': package[1],
                    'url': package[2].strip('\n')
            }

            cursor.execute('''
                INSERT OR REPLACE INTO package_info (name, version, url, installed) VALUES (?, ?, ?, ?)
                ''', (pkg_struct['name'], pkg_struct['version'], pkg_struct['url'], 'yes'))


    conn.commit()

    conn.close()


def main():
    print('Populating packages database...')

    database_name = 'packages.db'

    fill_tables(database_name)


if __name__ == '__main__':
    main()

