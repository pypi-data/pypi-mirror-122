import sqlite3
import pandas as pd
import pathlib
from deez_stats.telo.telo import Elo

INIT_ELO = 700
HERE = (pathlib.Path(__file__).parent)
DATABASE_FILE = (HERE / 'files/database/history.db')


# class DatabaseNav:
#     def __init__(self):
#         self.connection = None
#         self.cursor = None

#     def start_connection(self):
#         self.connection = sqlite3.connect(DATABASE_FILE)
#         self.cursor = self.connection.cursor()

#     def close_connection(self, commit=False):
#         self.cursor.close()
#         if commit is True:
#             self.connection.commit()
#         self.connection.close()

#     def execute_sql(self, sql_query):
#         self.start_connection()


def execute_sqlite(sql_query):
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    result = cursor.execute(sql_query)
    result = list(result)
    cursor.close()
    connection.close()
    return result


def execute_commit(sql_query):
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    result = cursor.execute(sql_query)
    result = list(result)
    cursor.close()
    connection.commit()
    connection.close()
    return result


def execute_row_factory(sql_query):
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = lambda cursor, row: row[0]
    cursor = connection.cursor()
    result = cursor.execute(sql_query)
    result = list(result)
    cursor.close()
    connection.close()
    return result


def get_manager_names(season):
    query_string = '''
        SELECT   manager_id,
                 manager_name
        FROM     manager
        WHERE    season == {}
        ORDER BY manager_id ASC;
    '''.format(season)
    result = execute_row_factory(query_string)
    return result


def matchup_history(manager_name, manager_elo, opponent_name, opponent_elo, display=True):
    class WeeklyMatchupHistory:
        def __init__(self):
            self.manager_name = manager_name
            self.opponent_name = opponent_name
            self.manager_avg_score = None
            self.opponent_avg_score = None
            self.manager_wins = 0
            self.opponent_wins = 0
            self.matchup_history = None
            self.manager_elo = manager_elo
            self.opponent_elo = opponent_elo

    wmh = WeeklyMatchupHistory()

    query_string = '''
        SELECT  season,
                manager_name,
                opponent_name,
                manager_score,
                opponent_score,
                result
        FROM    schedule
        WHERE   manager_name = "{}" AND opponent_name = "{}"
    '''.format(wmh.manager_name, wmh.opponent_name)
    result = execute_sqlite(query_string)

    df = pd.DataFrame(result, columns=['season', 'Manager', 'Opponent', 'Manager Score', 'Opponent Score', 'Result'])

    wmh.matchup_history = df
    wmh.manager_avg_score = df['Manager Score'].mean()
    wmh.opponent_avg_score = df['Opponent Score'].mean()

    try:
        wmh.manager_wins = df.Result.value_counts().W
    except AttributeError:
        wmh.manager_wins = 0

    try:
        wmh.opponent_wins = df.Result.value_counts().L
    except AttributeError:
        wmh.opponent_wins = 0
    if display is True:
        print(df.to_string(index=False))

        print("\nCurrently, {} has a rank of {} and {} has a rank of {}. \
            ".format(wmh.manager_name, wmh.manager_elo, wmh.opponent_name, wmh.opponent_elo))
        print("The current record between {} and {} is {} - {}. \
            ".format(wmh.manager_name, wmh.opponent_name, wmh.manager_wins, wmh.opponent_wins))
        print("The average score between {} and {} is {:0.2f} - {:0.2f}.\
            ".format(wmh.manager_name, wmh.opponent_name, wmh.manager_avg_score, wmh.opponent_avg_score))
        print("*********************************************************************")
    return wmh


def get_manager_score_history(manager_name):
    query_string = '''
        SELECT  manager_score
        FROM    schedule
        WHERE   manager_name = "{}"
        ORDER BY manager_score DESC;
    '''.format(manager_name)
    result = execute_row_factory(query_string)
    return result


def update_weekly_results(leagueinfo, season, week, update=False, display=True):
    if leagueinfo.end_week - week == 1:  # check if semifinals
        d = find_weekly_winners(season=season, week=week - 1)
        quarterfinal_winners = [i[0] for i in d]
        semifinals = []
        matchups = leagueinfo.weekly_matchups
        for idx, name in enumerate(matchups):
            if name[0] not in quarterfinal_winners:
                if idx % 2 == 0:
                    if matchups[idx + 1][0] in quarterfinal_winners:
                        semifinals.append(name)
                else:
                    if matchups[idx - 1][0] in quarterfinal_winners:
                        semifinals.append(name)
            if name[0] in quarterfinal_winners:
                semifinals.append(name)
        leagueinfo.weekly_matchups = semifinals
    elif leagueinfo.end_week - week == 0:  # check if finals
        d = find_seminfinal_managers(season=season, week=week - 1)
        semifinal_names = [i[0] for i in d]
        finals = []
        matchups = leagueinfo.weekly_matchups
        for idx, name in enumerate(matchups):
            if name[0] in semifinal_names:
                finals.append(name)
        leagueinfo.weekly_matchups = finals

    df = pd.DataFrame(leagueinfo.weekly_matchups, columns=['manager_name', 'manager_score'])
    df.insert(0, 'season', df.shape[0] * [leagueinfo.season])
    df.insert(1, 'week', leagueinfo.week)
    opponents = df.shape[0] * ['']
    opponent_scores = df.shape[0] * [0]
    results = []
    for i in range(df.shape[0] // 2):
        opponents[2 * i + 1] = df['manager_name'][2 * i]
        opponents[2 * i] = df['manager_name'][2 * i + 1]
        opponent_scores[2 * i + 1] = df['manager_score'][2 * i]
        opponent_scores[2 * i] = df['manager_score'][2 * i + 1]
        if df['manager_score'][2 * i] > df['manager_score'][2 * i + 1]:
            results.append('W')
            results.append('L')
        else:
            results.append('L')
            results.append('W')

    df['opponent_name'] = opponents
    df['opponent_score'] = opponent_scores
    df['results'] = results
    df['elo'] = df.shape[0] * [0]

    if display is True:
        print(df)

    if update is True:
        for i in range(df.shape[0]):
            row = df.iloc[[i]]  # based on index
            row = row.values.tolist()[0]
            query_string = '''
                INSERT INTO     schedule (
                                season,
                                week,
                                manager_name,
                                manager_score,
                                opponent_name,
                                opponent_score,
                                result,
                                elo)
                VALUES          ({}, {}, '{}', {}, '{}', {}, '{}', {})
            '''.format(*row)
            execute_commit(query_string)


def get_past_matchups(season, week):
    query_string = '''
        SELECT  *
        FROM    schedule
        WHERE   season = "{}" AND week = "{}"
    '''.format(season, week)
    result = execute_sqlite(query_string)
    return result


def find_weekly_winners(season, week):
    query_string = '''
        SELECT  manager_name, manager_score
        FROM    schedule
        WHERE   season = {} AND week = {} AND result = "W"
    '''.format(season, week)
    result = execute_sqlite(query_string)
    return result


def find_seminfinal_managers(season, week):
    query_string = '''
        SELECT  manager_name, manager_score
        FROM    schedule
        WHERE   season = {} AND week = {}
    '''.format(season, week)
    result = execute_sqlite(query_string)
    return result


def get_table_column_names(table):
    query_string = '''
        PRAGMA table_info({})
    '''.format(table)
    result = execute_sqlite(query_string)
    result = [i[1] for i in result]
    return result


def update_database_elo(season, week, manager_name, elo):
    query_string = '''
        UPDATE  schedule
        SET     elo={}
        WHERE   season={} AND week={} and manager_name="{}"
    '''.format(elo, season, week, manager_name)
    execute_commit(query_string)


def get_manager_elo(season, week, manager_name):
    if week - 1 == 0:
        if season > 2020:
            week = 18
        else:
            week = 17
        season = season - 1
    query_string = '''
        SELECT  elo
        FROM    schedule
        WHERE   season = {} AND week = {} AND manager_name="{}"
    '''.format(season, week - 1, manager_name)
    result = execute_sqlite(query_string)
    if result:
        result = result[0][0]
    return result


def update_weekly_elo(season, week, update=False, display=True):
    manager_elo = 0
    opponent_elo = 0
    prev_year = False

    current_week_df = get_weekly_df(season, week)

    for idx in range(len(current_week_df)):
        if season == 2015 and week == 1:
            manager_elo = INIT_ELO  # only for year 1 week 1
            opponent_elo = INIT_ELO
        else:
            if (week - 1) == 0:
                season = season - 1
                week = 17
                prev_year = True

            manager_name = current_week_df.at[idx, 'manager_name']
            opponent_name = current_week_df.at[idx, 'opponent_name']

            manager_elo = get_manager_elo(season, week - 1, manager_name)
            opponent_elo = get_manager_elo(season, week - 1, opponent_name)

            week_offset = 2
            while not (manager_elo):  # keep looking back in previous weeks
                try:
                    manager_elo = get_manager_elo(season, week - week_offset, manager_name)
                except IndexError:
                    pass
                finally:
                    week_offset = week_offset + 1
                if week_offset > 100:
                    manager_elo = INIT_ELO

            week_offset = 2
            while not (opponent_elo):  # keep looking back in previous weeks
                try:
                    opponent_elo = get_manager_elo(season, week - week_offset, opponent_name)
                except IndexError:
                    pass
                finally:
                    week_offset = week_offset + 1
                if week_offset > 100:
                    opponent_elo = INIT_ELO

        if prev_year:
            season = season + 1
            week = 1
            prev_year = False

        elo = Elo(manager_elo)
        elo.player_outcome(opponent_elo, current_week_df.at[idx, 'result'])
        current_week_df.at[idx, 'elo'] = elo.RpA
        if update is True:
            update_database_elo(season, week, current_week_df.at[idx, 'manager_name'], elo.RpA)
        if display is True:
            print('{}: {}\t{}: {}\t{}'.format(manager_name, elo.RpA, opponent_name, elo.RpB, elo.RpA - manager_elo))


def get_weekly_df(season, week):
    current_week_df = pd.DataFrame(get_past_matchups(season, week))
    current_week_df.columns = get_table_column_names('schedule')
    return current_week_df
