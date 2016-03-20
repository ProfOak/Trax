#!/usr/bin/env python

import os.path
import sqlite3
import tabulate

def process(line, db):
    ''' process the user input command '''

    # case doesn't matter
    line = line.lower()

    if line == 'a':     # add
        title = season = episode = ''

        print '=== New show ==='
        while title == '':
            title   = raw_input('Title: ').strip()

        season  = get_int('Season  (default=1): ')
        episode = get_int('Episode (default=1): ')

        call_db(db, 'INSERT INTO shows (title,season,episode) \
                VALUES (?, ?, ?)', (title, season, episode))

    elif line == 'r':   # remove
        shows = pretty_print(db)

        if len(shows) <= 0:
            print 'No shows to remove'
            return True

        # be a number, and be in range
        series_number = ''
        while not series_number.isdigit() or \
                int(series_number) >= len(shows) or \
                int(series_number) < 0:
            series_number = raw_input('Series number: ')

        show_to_delete = shows[int(series_number)]

        call_db(db, 'DELETE FROM shows WHERE title=? AND season=? AND  episode=?', show_to_delete)
        print 'Series deleted:', show_to_delete[0]
        process('l', db)


    elif line == 'l':   # list
        pretty_print(db)

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
        # no table called 'shows' in db
        create_db(db)
        return

    conn.commit()
    conn.close()

    return results

def create_db(db):
    ''' Create the Sqlite3 database '''

    call_db(db, '''
        create table shows(
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

def pretty_print(db):
    ''' nice printing using tabulate '''

    shows = call_db(db, 'SELECT * FROM shows')

    # making i a str to use raw_input when making a selection
    p_shows = ( [str(i)] + list(show) for i, show in enumerate(shows) )
    print tabulate.tabulate(p_shows, headers=('#', 'Title', 'Season', 'Episode'))
    return shows

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
        line = raw_input('\n> ')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print ''
        print 'Exiting...'

