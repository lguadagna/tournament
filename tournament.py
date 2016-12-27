#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from operator import itemgetter
import itertools  # for take, consume of lists


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""

    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    SQL = "DELETE FROM match"
    pg = psycopg2.connect("dbname=tournament")
    c = pg.cursor()
    #c = conn.cursor()
    c.execute(SQL)
    pg.commit()
    pg.close()


def deletePlayers():
    """Remove all the player records from the database."""
    SQL = "DELETE from player;"
    pg = psycopg2.connect("dbname=tournament")
    c = pg.cursor()
    #c = conn.cursor()
    c.execute(SQL)
    pg.commit()
    pg.close()


def countPlayers():
    """Returns the number of players currently registered."""
    SQL = "SELECT COUNT(*) from 'player';"
    pg = psycopg2.connect("dbname=tournament")
    c = pg.cursor()
    c.execute("SELECT COUNT(*) from player")
    result = c.fetchone()
    pg.close()
    return int(result[0])


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    SQL = "INSERT INTO player ( playername ) VALUES ( %s);"

    pg = psycopg2.connect("dbname=tournament")
    c = pg.cursor()
    c.execute(SQL, (name,))
    pg.commit()
    c.close
    pg.close()

    return


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    pg = psycopg2.connect("dbname=tournament")
    c = pg.cursor()

    SQL = "SELECT * FROM player"
    # # find list of players
    c.execute(SQL)
    result = c.fetchall()
    standings = []

    for row in result:
        pID = str(row[0])
        c.execute("SELECT COUNT(*) FROM match where winner = %(pID)s",
                  {"pID": str(row[0]), })
        result = c.fetchone()
        wins = result[0]
        c.execute("SELECT COUNT(*) FROM match where loser = %(pID)s",
                  {"pID": str(row[0]), })
        result = c.fetchone()
        loses = result[0]
        matches = wins + loses
        standing = (row[0], row[1], wins, matches)
        standings.append(standing)

    pg.close()
    sortedStandings = sorted(standings, key=itemgetter(2))
    return sortedStandings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # create a match and record winner
    SQL = "INSERT INTO match ( winner, loser ) VALUES ( %s, %s);"
    pg = psycopg2.connect("dbname=tournament")
    c = pg.cursor()
    c.execute(SQL, (winner, loser))
    pg.commit()
    c.close
    pg.close()

    return


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    # standings is a list of players
    standings = playerStandings()
    pairings = []

    while len(standings) > 1:
        twoPlayerList = standings[0:2]
        # print "twoPlayerList: %s" %str(twoPlayerList)
        # for player in twoPlayerList:
        #     matchEntry = (player[0], player[1])
        pairing = (twoPlayerList[0][0], twoPlayerList[0][
                   1], twoPlayerList[1][0], twoPlayerList[1][1])
        pairings.append(pairing)
        standings = standings[2:len(standings)]

    return pairings
