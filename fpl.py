# https://codebeautify.org/jsonviewer
# Need to use a list with team to deal with cases like D. Sanchez and A. Sanchez
# [ [Understat Name, FPL Name, Team Name], ... ]
# Also need to look into changing accented names to non accented

import json, sys, unicodedata, csv

#
#
# Work with FPL Json Data
#
#

debug = False
gameWeek = 11 # Number of the gameweek past
minutesRequired = 90 * (gameWeek*.5)

print("Finding stats for all players with more than {} minutes played...".format(minutesRequired))

with open('DataFPL.json', encoding='utf-8') as data_file:
    fplJSON = json.loads(data_file.read())

fplDataList = []
for player in fplJSON["elements"]:
    # playerList
    # [0] - Firstname + Lastname
    # [1] - Webname
    # [2] - Team
    # [3] - Price
    # [4] - Total Score
    # [5] - Position --- Element Type (1 - GK, 2 - Def, 3 - Mid, 4 - Fwd
    # [6] - Webname ORIGINAL
    # [7] - Minutes
    # [8] - Appearances

    # Only deal with people who play
    if player["minutes"] > minutesRequired:
        _fullName = "%s %s" % (player["first_name"], player["second_name"])
        _nfkd_form = unicodedata.normalize('NFKD', _fullName)
        _playerFullName = u"".join([c for c in _nfkd_form if not unicodedata.combining(c)])

        _nfkd_form = unicodedata.normalize('NFKD', player["web_name"])
        _playerWebName = u"".join([c for c in _nfkd_form if not unicodedata.combining(c)])

        _appearances = round(float(player["total_points"]) / float(player["points_per_game"]))
        
        playerList = [_playerFullName.upper(),
              _playerWebName.upper(),
              player["team"],
              player["now_cost"],
              player["total_points"],
              player["element_type"],
              player["web_name"],
              player["minutes"],
              _appearances]

        fplDataList.append(playerList)
        
#
#
# Work with understat HTML Data
#
#


# Decode escaped hex stuff: https://stackoverflow.com/questions/4020539/process-escape-sequences-in-a-string-in-python
understatDataList = []
with open('DataUnderstat.json') as data_file:
    rawUnderstat = data_file.read()
    understatData = bytes(rawUnderstat, "utf-8").decode("unicode_escape")

understatJSON = json.loads(understatData)
for player in understatJSON:
    # underList
    # [0] - Firstname + Lastname
    # [1] - Team
    # [2] - Appearances
    # [3] - Minutes
    # [4] - xG
    # [5] - xA
    # [6] - G
    # [7] - A
    # [8] - Shots
    # [9] - Key Passes
    # -----
    # Strip Unicode from player name

    # Ensure player meets minutes played criteria
    #if int(player["time"]) > minutesRequired:
    if True:
        _nfkd_form = unicodedata.normalize('NFKD', player["player_name"])
        _playerName = u"".join([c for c in _nfkd_form if not unicodedata.combining(c)])
        
        underList = [_playerName.upper(),
             player["team_title"],
             player["games"],
             player["time"],
             player["xG"],
             player["xA"],
             player["goals"],
             player["assists"],
             player["shots"],
             player["key_passes"]]
        
        understatDataList.append(underList)



# DEUNICODE



# DEUNICODE







# Teams
# 0 - Arsenal
# 1 - Bournemouth
# 2 - Brighton
# 3 - Burnley
# 4 - Cardiff
# 5 - Chelsea
# 6 - Crystal Palace
# 7 - Everton
# 8 - Fulham
# 9 - Huddersfield
# 10 - Leicester
# 11 - Liverpool
# 12 - Man City
# 13 - Man Utd
# 14 - Newcastle
# 15 - Southampton
# 16 - Spurs
# 17 - Watford
# 18 - West Ham
# 19 - Wolves

#
# FPL Data
#
sortedFPLList = [ [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ]
for player in fplDataList:
    _arrayPos = (player[2])-1
    sortedFPLList[_arrayPos].append(player)
# DEBUG
FPLPlayerTotal = 0
if debug:
    print("-- FPL Data --")
for item,x in enumerate(sortedFPLList):
    if debug:
        print("Team {} - Size: {}".format(item, len(x)))
    FPLPlayerTotal = FPLPlayerTotal + len(x)


#
# Understat Data
#
sortedUnderstatList = [ [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ]
# Team Dict
teamList = {
    'Arsenal':0,
    'Bournemouth':1,
    'Brighton':2,
    'Burnley':3,
    'Cardiff':4,
    'Chelsea':5,
    'Crystal Palace':6,
    'Everton':7,
    'Fulham':8,
    'Huddersfield':9,
    'Leicester':10,
    'Liverpool':11,
    'Manchester City':12,
    'Manchester United':13,
    'Newcastle United':14,
    'Southampton':15,
    'Tottenham':16,
    'Watford':17,
    'West Ham':18,
    'Wolverhampton Wanderers':19}


for player in understatDataList:
    if player[1] in teamList:
        sortedUnderstatList[teamList.get(player[1])].append(player)
    else:
        print("Failure! - {}".format(player))
#DEBUG
UnderstatPlayerTotal = 0
if debug:
    print("\n-- Understat Data --")
for item,x in enumerate(sortedUnderstatList):
    if debug:
        print("Team {} - Size: {}".format(item, len(x)))
    UnderstatPlayerTotal = UnderstatPlayerTotal + len(x)

#DEBUG Data Check 1
if UnderstatPlayerTotal >= FPLPlayerTotal:
    if debug:
        print("\nEnough Understat players to match against FPL. --- FPL: {} - Understat: {}\n".format(FPLPlayerTotal, UnderstatPlayerTotal))
else:
    print("ERROR: There are less FPL players than Understat players. Data probably out of date!\n\nFPL: {}\nUnderstat: {}".format(FPLPlayerTotal, UnderstatPlayerTotal))
    sys.exit()
#
#
# Compare the two lists to match them into one list with both sets of data
#
#

    # ustatPlayer
    # [0] - Firstname + Lastname - UPPER
    # [1] - Team
    # [2] - Appearances
    # [3] - Minutes
    # [4] - xG
    # [5] - xA
    # [6] - G
    # [7] - A
    # [8] - Shots
    # [9] - Key Passes
    # FPLayer
    # [0] - Firstname + Lastname - UPPER
    # [1] - Webname - UPPER
    # [2] - Team
    # [3] - Price
    # [4] - Total Score
    # [5] - Position --- Element Type (1 - GK, 2 - Def, 3 - Mid, 4 - Fwd
    # [6] - Webname - Original
combinedStatList = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ]
failCount = 0
lastFoundPlayer = False
for teamIter,team in enumerate(sortedFPLList):
    for FPLayer in team:
        for attempt,ustatPlayer in enumerate(sortedUnderstatList[teamIter]):
            # Split the names into lists to increase the chances of a correct result
            
            _nameListFPL = FPLayer[0].split()
            _nameListFPL.append(FPLayer[1])
            _nameListUSTAT = ustatPlayer[0].split()

            if len(set(_nameListUSTAT) & set(_nameListFPL))>0 and int(ustatPlayer[2]) == FPLayer[8] and ( abs(int(int(ustatPlayer[3])/10) - int(FPLayer[7]/10)) <= 3):
                if debug and not ( abs(int(int(ustatPlayer[3])/10) - int(FPLayer[7]/10)) <= 3):
                    print("FPL Mins:{} -- USTAT Mins:{}, -- Math:{}".format(int(int(ustatPlayer[3])/10),int(FPLayer[7]/10)),( abs(int(int(ustatPlayer[3])/10) - int(FPLayer[7]/10)) <= 3))

                
                # Calculate and format the stats properly
                _price = float(FPLayer[3]) / 10 # 2 - Price
                _points = int(FPLayer[4]) # 3 - Total Score
                _position = int(FPLayer[5]) # 4 - Position - 1:GK, 2:Def, 3:Mid, 4:Fwd
                _games = int(ustatPlayer[2]) # 5 - Appearances
                _minutes = int(ustatPlayer[3]) # 6 - Minutes
                _xGoals = float(ustatPlayer[4]) # 7 - xG
                _xAssists = float(ustatPlayer[5]) # 8 - xA
                _goals = int(ustatPlayer[6]) # 9 - G
                _assists = int(ustatPlayer[7]) # 10 - A
                _shots = int(ustatPlayer[8]) # 11 - Shots
                _keyPasses = int(ustatPlayer[9]) # 12 - Key Passes
                
                # Derivative stats
                _xG90 = (_xGoals / _minutes) * 90
                _xA90 = (_xAssists / _minutes) * 90
                _keyPass90 = (_keyPasses / _minutes) * 90
                _xGDiff = _goals - _xGoals
                _xADiff = _assists - _xAssists
                if _shots > 0:
                    _xGShot = _xGoals / _shots
                else:
                    _xGShot = 0
                
                # FPL Calculations
                if _position <= 2:
                    _goalPoints = 6
                elif _position == 3:
                    _goalPoints = 5
                elif _position == 4:
                    _goalPoints = 4
                _PPM = _points / _price 
                _xPoints90 = (_xG90 * _goalPoints) + (_xA90 * 3)
                _xPointsPM = _xPoints90 / _price
                
                
                finishedPlayerList = [FPLayer[6], ustatPlayer[1], _price, _points,
                        _position, _games, _minutes, _goals,
                        _assists, _xGoals, _xAssists, _shots,
                        _keyPasses, _xG90, _xA90, _xGDiff,
                        _xADiff, _xGShot, _keyPass90, _PPM,
                        _xPoints90, _xPointsPM ]
                combinedStatList[teamIter].append(finishedPlayerList)
                lastFoundPlayer = FPLayer[0]
            '''
            if (FPLayer[1] == "WESTWOOD") and lastFoundPlayer == FPLayer[0]:
                print(_nameListFPL)
                print(_nameListUSTAT)
                print(len(set(_nameListUSTAT) & set(_nameListFPL)))
                print(set(_nameListUSTAT))
                print(set(_nameListFPL))
                print(set(_nameListUSTAT) & set(_nameListFPL))
                print(len(set(_nameListUSTAT) & set(_nameListFPL))>0)
                print(finishedPlayerList)
                print("\n\n")
            #'''
                
            if lastFoundPlayer == FPLayer[0]:
                break
            
            if (attempt+1) == len(sortedUnderstatList[teamIter]) and lastFoundPlayer != FPLayer[0]:
                print("FAILED TO FIND: _nameListFPL: {} ----- _nameListUSTAT: {}\n\nFPLayer:{}".format(_nameListFPL,_nameListUSTAT, FPLayer))
                if debug:
                    print("Understat:  {}\n\nFPL:  {}\n\n\n".format(sortedUnderstatList[teamIter],team))

if 1==1:
    #DEBUG
    playerTotal = 0
    if debug:
        print("-- Combined Data --")
    for item,x in enumerate(combinedStatList):
        if debug:
            print("Team {} - Size: {} / {}".format(item, len(x), len(sortedFPLList[item])))
        playerTotal = playerTotal + len(x)
        
    unmatchedTotal = FPLPlayerTotal - playerTotal
    if unmatchedTotal > 0:
        print("{} of {} players not matched!".format(unmatchedTotal, FPLPlayerTotal))
        sys.exit()
    else:
        if debug:
            print("All {} players matched.".format(FPLPlayerTotal))
            

# Sort the players by position
goalList = [["Name","Team","Price","Points","Position","Games","Minutes","Goals","Assists","xG","xA","Shots","Key Passes","xG90","xA90","xGDiff","xADiff", "xG/Shot","Key Pass/90","PPM","xPP90","xPPM"]]
defList = [["Name","Team","Price","Points","Position","Games","Minutes","Goals","Assists","xG","xA","Shots","Key Passes","xG90","xA90","xGDiff","xADiff", "xG/Shot","Key Pass/90","PPM","xPP90","xPPM"]]
midList = [["Name","Team","Price","Points","Position","Games","Minutes","Goals","Assists","xG","xA","Shots","Key Passes","xG90","xA90","xGDiff","xADiff", "xG/Shot","Key Pass/90","PPM","xPP90","xPPM"]]
fwdList = [["Name","Team","Price","Points","Position","Games","Minutes","Goals","Assists","xG","xA","Shots","Key Passes","xG90","xA90","xGDiff","xADiff", "xG/Shot","Key Pass/90","PPM","xPP90","xPPM"]]
for team in combinedStatList:
    for player in team:
        if player[4] == 1:
            goalList.append(player)
        elif player[4] == 2:
            defList.append(player)
        elif player[4] == 3:
            midList.append(player)
        elif player[4] == 4:
            fwdList.append(player)
            
playerList = [["Keepers", goalList], ["Defenders", defList], ["Midfielders", midList], ["Forwards", fwdList]]

# Write data for each position grouping into it's own CSV file
for position,playerList in playerList:
    # Create a new CSV File for this 
    with open(("{}.csv".format(position)), mode='w', newline='') as myfile:
        wr = csv.writer(myfile)
        for player in playerList:
            wr.writerow(player)

print("\nFound data on {} players with more than {} minutes played.\n{} Forwards\n{} Midfielders\n{} Defenders\n{} Goalkeepers".format((FPLPlayerTotal - unmatchedTotal), int(minutesRequired), len(fwdList), len(midList), len(defList), len(goalList)))
input("\n\n-- Press ENTER to exit the program.")