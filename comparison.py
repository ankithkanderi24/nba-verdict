from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo, playerawards, playerprofilev2, playervsplayer, playerdashboardbyyearoveryear, playercareerstats, teamdetails, teamplayerdashboard
import pandas as pandas
from flask import jsonify
def getId(player):
    playerDict = players.find_players_by_full_name(player)[0]
    id = playerDict['id']
    return id


def checkIfTeamWonChampionship(teamid, year):
    teamChampionships = teamdetails.TeamDetails(team_id=teamid).team_awards_championships.get_data_frame()
    if int(year) in teamChampionships.get('YEARAWARDED').values:
        return True
    else:
        return False



def getChampionships(id):
    df = playerdashboardbyyearoveryear.PlayerDashboardByYearOverYear(player_id = id).by_year_player_dashboard.get_data_frame()
    desiredColumns = df[['GROUP_VALUE', 'TEAM_ID']]
    won = 0
    for i in range(len(desiredColumns)):

        year = desiredColumns['GROUP_VALUE'][i]
        year = year.split('-')
        #accounting for irregularity in way data is presented
        prepend = year[0][:2]
        if (year[0][2:] == '99'):
            prepend = '20'
        searchYear = prepend + year[1]
        if (desiredColumns['TEAM_ID'][i] != -1):
            if checkIfTeamWonChampionship(desiredColumns['TEAM_ID'][i], searchYear):
                won = won + 1

    return won



def getStats(player):
    id = getId(player)
    regularSeasonGP = playerprofilev2.PlayerProfileV2(player_id=id).career_totals_regular_season.get_data_frame().get('GP')[0]
    ppg = commonplayerinfo.CommonPlayerInfo(player_id = id).player_headline_stats.get_data_frame().get('PTS')[0]
    apg = commonplayerinfo.CommonPlayerInfo(player_id = id).player_headline_stats.get_data_frame().get('AST')[0]
    rpg = commonplayerinfo.CommonPlayerInfo(player_id = id).player_headline_stats.get_data_frame().get('REB')[0]
    spg = round(playerprofilev2.PlayerProfileV2(player_id = id).career_totals_regular_season.get_data_frame().get('STL')[0] / regularSeasonGP, 1)
    bpg = round(playerprofilev2.PlayerProfileV2(player_id = id).career_totals_regular_season.get_data_frame().get('BLK')[0] / regularSeasonGP, 1)
    careerPlusMinus = playerdashboardbyyearoveryear.PlayerDashboardByYearOverYear(player_id = id).by_year_player_dashboard.get_data_frame().get('PLUS_MINUS').sum()
    plusMinusPerGame = round(careerPlusMinus / regularSeasonGP, 2)
    pie = commonplayerinfo.CommonPlayerInfo(player_id = id).player_headline_stats.get_data_frame().get('REB')[0]
    fg_pct = round(playerprofilev2.PlayerProfileV2(player_id = id).career_totals_regular_season.get_data_frame().get('FG_PCT')[0] * 100, 1)
    ft_pct = round(playerprofilev2.PlayerProfileV2(player_id = id).career_totals_regular_season.get_data_frame().get('FT_PCT')[0] * 100, 1)
    fg3_pct = round(playerprofilev2.PlayerProfileV2(player_id = id).career_totals_regular_season.get_data_frame().get('FG3_PCT')[0] * 100, 1)
    careerWins = playerdashboardbyyearoveryear.PlayerDashboardByYearOverYear(player_id = id).by_year_player_dashboard.get_data_frame().get('W').sum()
    careerWpct = round(careerWins / regularSeasonGP * 100, 1)
    seasonsPlayed = len(playerdashboardbyyearoveryear.PlayerDashboardByYearOverYear(player_id = id).by_year_player_dashboard.get_data_frame())
    allStar = len(playercareerstats.PlayerCareerStats(player_id=id).season_totals_all_star_season.get_data_frame())
    championships = getChampionships(id)
    playoffGamesPlayed = playerprofilev2.PlayerProfileV2(player_id=id).career_totals_post_season.get_data_frame().get('GP')[0]
    playoffppg = round(playerprofilev2.PlayerProfileV2(player_id=id).career_totals_post_season.get_data_frame().get('PTS')[0] / playoffGamesPlayed, 1)
    playoffapg = round(playerprofilev2.PlayerProfileV2(player_id=id).career_totals_post_season.get_data_frame().get('AST')[0] / playoffGamesPlayed, 1)
    playoffrpg = round(playerprofilev2.PlayerProfileV2(player_id=id).career_totals_post_season.get_data_frame().get('REB')[0] / playoffGamesPlayed, 1)


    
    
    #wPCT = playerdashboardbygamesplits.PlayerDashboardByGameSplits(player_id = id).overall_player_dashboard.get_data_frame().get('PTS')
    allNBA = (playerawards.PlayerAwards(player_id=id).player_awards.get_data_frame().get('DESCRIPTION') == 'All-NBA').sum()
    mvp = (playerawards.PlayerAwards(player_id=id).player_awards.get_data_frame().get('DESCRIPTION') == 'NBA Most Valuable Player').sum()
    nbaPotm = (playerawards.PlayerAwards(player_id=id).player_awards.get_data_frame().get('DESCRIPTION') == 'NBA Player of the Month').sum()
    finalsMVP = (playerawards.PlayerAwards(player_id=id).player_awards.get_data_frame().get('DESCRIPTION') == 'NBA Finals Most Valuable Player').sum()



    data = {'seasons played': seasonsPlayed, 'games played': regularSeasonGP, 'ppg': ppg, 'ast': apg, 'reb': rpg, 'spg': spg, 'bpg' : bpg, '+-pg' : plusMinusPerGame,
            'Pie': pie, 'FG_PCT': fg_pct, 'FT_PCT': ft_pct, 'FG3_PCT': fg3_pct, 'wpct' : careerWpct, 'all star' : allStar, 
            'mvp': mvp, 'allNba' : allNBA, 'nbaPotm': nbaPotm, 'finalsMVP': finalsMVP, 'playoffppg': playoffppg, 'championships (since 1996)': championships, 
            'playoffGamesPlayed': playoffGamesPlayed, 'playoffppg': playoffppg, 'playoffapg': playoffapg, 'playoffrpg': playoffrpg}
    return data








