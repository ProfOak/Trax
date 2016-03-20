#!/usr/bin/env python

import os.path
import sqlite3
import tabulate

def process(line, db):
    ''' process the user input command '''

    line = line.lower()

    if line == 'a':     # add
        title = season = episode = ''

        print '=== New show ==='
        while title == '':
            title   = raw_input('Title: ')

        season  = get_int('Season  (default=1): ')
        episode = get_int('Episode (default=1): ')

        call_db(db, 'INSERT INTO shows (title,season,episode) \
                VALUES (?, ?, ?)', (title, season, episode))

    elif line == 'r':   # remove
        shows = call_db(db, 'select * from shows')
        pretty_print(shows)

        series_number = raw_input('Series number: ')

        call_db(db, 'DELETE FROM shows WHERE ID = ?', series_number)
        print 'Series deleted'
        process('l', db)


    elif line == 'l':   # list
        shows = call_db(db, 'select * from shows')
        pretty_print(shows)

    elif line == 'h':   # help
        usage()

    elif line == 'q':   # quit
        return False

    return True

def call_db(db, sql, vals=''):
    ''' Query database '''

    conn = sqlite3.connect(db)
    c = conn.cursor()

    try:
        results = [ row for row in c.execute(sql, vals) ]
    except sqlite3.OperationalError:
        create_db(db)
        return

    conn.commit()
    conn.close()

    return results

def create_db(db):
    ''' Create the Sqlite3 database '''

    call_db(db, '''
        create table shows(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            season INTEGER NOT NULL,
            episode INTEGER NOT NULL
        )'''
    )

def get_int(string):
    '''
        ensure the user enters an int

        if no input is given, the number 1 is returned
    '''

    n = 'Not a number'
    while not n.isdigit():
        n = raw_input(string)
        if n == '':
            return 1
    return n

def pretty_print(table):
    ''' nice printing using tabulate '''
    print tabulate.tabulate(table, headers=('#', 'Title', 'Season', 'Episode'))

def usage():
    ''' usage displays the help command information '''

    print 'Commands:'
    print '    a: Add a show to your listing'
    print '    r: Remove a show from your listing'
    print '    l: List your shows'
    print '    h: Help (shows this dialog)'
    print '    q: Quit'


def main(db='trax.db',line=''):
    ''' main function '''

    # welcome the user with their shows
    if os.path.exists(db):
        print "These are your shows"
        process('l', db)
    else:
        print 'No database detected'
        print 'Creating new database'
        create_db(db)

    while process(line, db):
        line = raw_input('> ')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print ''
        print 'Exiting...'

