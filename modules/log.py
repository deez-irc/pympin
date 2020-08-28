"""log.py - logs chat to SQLite database"""

import sqlite3
import time

__author__ = 'deez@based.red'
__version__ = '0.1'
__license__ = 'GPLv3'


def check_rate(network, target, source):
    """Check if a user is spamming commands."""
    connection = sqlite3.connect(f'data/{network.lower()}.db')
    cursor = connection.cursor()
    cursor.execute(f'''
        SELECT * FROM "{target}"
        WHERE "nick" = "{source}"
        AND "message" LIKE ".%"
        AND "unix" > {int(time.time()) - 30};'''
    )
    result = cursor.fetchall()
    check = len(result)

    oldest = result[0][1]
    return [check, oldest]


def log(network, target, source, message):
    """Log messages to a SQLite3 database."""
    connection = sqlite3.connect(f'data/{network.lower()}.db')
    cursor = connection.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS "{target}" (
            "id"      INTEGER PRIMARY KEY,
            "unix"    INTEGER,
            "nick"    TEXT,
            "message" TEXT,
            "size"    INTEGER
        );'''
    )

    cursor.execute(f'''
        INSERT INTO "{target}" (
            "unix",
            "nick",
            "message",
            "size"
        ) VALUES (?, ?, ?, ?);''', (
            int(time.time()),
            source,
            message,
            len(message)
        )
    )

    connection.commit()
    connection.close()
