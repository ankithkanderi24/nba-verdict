from nba_api.stats.static import players
import pandas as pandas

def validateNames(name1, name2):
    player1 = players.find_players_by_full_name(name1)
    player2 = players.find_players_by_full_name(name2) 
    if (len(player1) != 0):
        player1 = player1[0] #gets first entry for a name 
    if (len(player2) != 0):
        player2 = player2[0] #gets first entry for a name

    if (len(player1) == 0 and len(player2) == 0):
        return "Check both player's names!"
    elif (len(player1) == 0):
        return "Check first player's name!"
    elif (len(player2) == 0):
        return "Check second player's name!"
    
    return "Good" #this case works

        



