#!/usr/bin/env -i python3

from sqlite3 import connect

def create_tables(db_name):
    conn = connect(db_name)

    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS package_info (
        name TEXT NOT NULL,
        version TEXT NOT NULL,
        alias TEXT,
        url TEXT NOT NULL,
        installed TEXT,
        PRIMARY KEY (name, version)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS package_dependencies (
        name TEXT NOT NULL,
        version TEXT NOT NULL,
        required TEXT,
        recommended TEXT,
        optional TEXT,
        PRIMARY KEY (name, version)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS package_installation (
        name TEXT NOT NULL,
        version TEXT NOT NULL,
        patch TEXT,
        preinstall TEXT,
        configure TEXT,
        prebuild TEXT,
        build TEXT,
        postbuild TEXT,
        test TEXT,
        posttest TEXT,
        install TEXT,
        postinstall TEXT,
        uninstall TEXT,
        PRIMARY KEY (name, version)
    );
    ''')

    conn.commit()

    conn.close()


def main():
    print('Initializing packages database...')

    database_name = 'packages.db'

    create_tables(database_name)


if __name__ == '__main__':
    main()

