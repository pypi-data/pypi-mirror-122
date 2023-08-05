import objectpath
import numpy as np
import yahoo_fantasy_api as yfa
from deez_stats.pyquery import database_query as dbq
from deez_stats.pyquery import yahoo_query as yq
from deez_stats.pyquery import json_query as jq


class LeagueInfo:
    def __init__(self, sc, season=None, week=None):
        self.sc = sc
        self.league_key = None
        self.league_id = None
        self.name = None
        self.persistent_url = None
        self.logo_url = None
        self.num_teams = None
        self.num_matchups = None
        self.week = week
        self.current_week = None
        self.start_week = None
        self.start_date = None
        self.end_week = None
        self.end_date = None
        self.game_id = None
        self.season = season
        self.current_season = None
        self.weekly_matchups = None
        self.weekly_matchup_histories = None
        self.manager_names = None
        self.playoff_start_week = None
        self.trade_end_date = None
        self.sendbird_channel_url = None
        self._update_LeagueInfo()

    def get_weekly_matchups(self):
        class WeeklyMatchup:
            def __init__(self):
                self.manager_id = None
                self.manager_name = None
                self.manager_points_total = 0
                self.manager_win_probability = 0
                self.manager_projected_points = 0
                self.manager_elo = 0
                self.opponent_id = None
                self.opponent_name = None
                self.opponent_score = 0
                self.opponent_points_total = 0
                self.opponent_win_probability = 0
                self.opponent_projected_points = 0
                self.opponent_elo = 0

        matchups_raw = yfa.League(self.sc, self.league_key).matchups(week=self.week)
        tree = objectpath.Tree(matchups_raw)
        team_ids = list(map(int, list(tree.execute('$..team_id'))))
        team_points_total = list(map(float, list(tree.execute('$..team_points.total'))))
        win_probability = list(map(float, list(tree.execute('$..win_probability'))))
        team_projected_points = list(map(float, list(tree.execute('$..team_projected_points.total'))))

        self.weekly_matchups = []
        for i in range(self.num_matchups):
            wm = WeeklyMatchup()

            m_index = 2 * i
            o_index = 2 * i + 1

            wm.manager_id = team_ids[m_index]
            wm.manager_name = self.manager_names[wm.manager_id]
            wm.manager_points_total = team_points_total[m_index]
            wm.manager_win_probability = win_probability[m_index]
            wm.manager_projected_points = team_projected_points[m_index]
            wm.manager_elo = dbq.get_manager_elo(self.season, self.week, wm.manager_name)

            wm.opponent_id = team_ids[o_index]
            wm.opponent_name = self.manager_names[wm.opponent_id]
            wm.opponent_points_total = team_points_total[o_index]
            wm.opponent_win_probability = win_probability[o_index]
            wm.opponent_projected_points = team_projected_points[o_index]
            wm.opponent_elo = dbq.get_manager_elo(self.season, self.week, wm.opponent_name)

            self.weekly_matchups.append(wm)

    def get_weekly_matchup_histories(self):
        self.weekly_matchup_histories = []
        for matchup in self.weekly_matchups:
            mh = dbq.matchup_history(matchup.manager_name, matchup.opponent_name)
            self.weekly_matchup_histories.append(mh)

    def display_matchup_info(self):
        for wm, mh in zip(self.weekly_matchups, self.weekly_matchup_histories):
            print("{:>10} | {:6.2f}\t {:6.2f} | {:<10}\
                ".format(wm.manager_name, wm.manager_points_total,
                wm.opponent_points_total, wm.opponent_name))
            print(" projected | {:6.2f}\t {:6.2f} | projected\
                ".format(wm.manager_projected_points, wm.opponent_projected_points))
            print("  win prob | {:6.2f}\t {:6.2f} | win prob\
                ".format(wm.manager_win_probability * 100, wm.opponent_win_probability * 100))
            print("   ranking | {:6d}\t {:6d} | ranking\
                ".format(wm.manager_elo, wm.opponent_elo))
            print("The current record between {} and {} is {} - {}. \
                ".format(mh.manager_name, mh.opponent_name, mh.manager_wins, mh.opponent_wins))
            print("The average score between {} and {} is {:0.2f} - {:0.2f}.\
                ".format(mh.manager_name, mh.opponent_name, mh.manager_avg_score, mh.opponent_avg_score))
            print("*********************************************************************")

    def get_manager_names(self, lg):
        nicknames = lg.yhandler.get_standings_raw(self.league_key)
        tree = objectpath.Tree(nicknames)
        mn = []
        mn.append(list(tree.execute('$..manager_id')))
        mn.append(list(tree.execute('$..nickname')))
        mn = dict(np.array(mn).T.tolist())
        keys_values = mn.items()
        self.manager_names = {int(key): str(value) for key, value in keys_values}
        self._clean_manager_names()

    def _clean_manager_names(self):
        cleaned_names = jq.get_cleaned_names()
        for key, value in self.manager_names.items():
            try:
                self.manager_names[key] = cleaned_names[value]
            except KeyError:  # not everyone's name is wrong so pass on the correct names
                pass

    def _get_current_season(self):
        raw_game_data = yq.json_query(self.sc, 'game/nfl')
        self.current_season = int(list(jq.search_json_key(raw_game_data, '..season'))[0])

    def _season_to_league_key(self):
        ids = jq.get_game_league_ids(self.season)
        return '{}.l.{}'.format(ids[0], ids[1])

    def _update_LeagueInfo(self):
        self._get_current_season()
        if self.season is None:  # grab current season
            self.season = self.current_season
        self.league_key = self._season_to_league_key()
        league = yfa.League(self.sc, self.league_key)
        settings = league.settings()
        self.league_id = jq.search_json_key(settings, '.league_id')
        self.name = jq.search_json_key(settings, '.name')
        self.logo_url = jq.search_json_key(settings, '.logo_url')
        self.num_teams = jq.search_json_key(settings, '.num_teams')
        self.num_matchups = self.num_teams // 2
        self.current_week = jq.search_json_key(settings, '.current_week')
        self.start_week = int(jq.search_json_key(settings, '.start_week'))
        self.start_date = jq.search_json_key(settings, '.start_date')
        self.end_week = int(jq.search_json_key(settings, '.end_week'))
        self.end_date = jq.search_json_key(settings, '.end_date')
        self.game_code = jq.search_json_key(settings, '.game_code')
        self.persistent_url = jq.search_json_key(settings, '.persistent_url')
        self.playoff_start_week = jq.search_json_key(settings, '.playoff_start_week')
        self.trade_end_date = jq.search_json_key(settings, '.trade_end_date')
        self.sendbird_channel_url = jq.search_json_key(settings, '.sendbird_channel_url')
        if self.week is None:
            self.week = self.current_week
        self.get_manager_names(league)
        self.get_weekly_matchups()
        self.get_weekly_matchup_histories()
