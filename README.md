# FPL Analysis
A python program to analyze data for FPL. Uses data from the FPL API as well as from Understat. Designed to be run after a gameweek is complete and data from both sources matches up.


## Usage
1. Get FPL Data from: https://fantasy.premierleague.com/drf/bootstrap-static
1b. Save data as DataFPL.JSON
2. Get Understat data from 'var playersData' on: https://understat.com/league/EPL
2b. Save data as DataUnderstat.JSON
3. Ensure the gameweek variable is up to date in the first few lines of 'fpl.py'.
4. If there were no problems there should be 4 CSV files in the same directory as the program. Import each of these files as a new sheet in a google doc spreadsheet.
5. Make sure to freeze the first row before sorting the data (View > Freeze > 1 Rows)


## Calculated Stats Info
**xG90**: Expected goals divided by minutes played, multiplied by 90

**xA90**: Expected assists divided by minutes played, multiplied by 90

**Key Pass/90**: Key Passes divided by minutes played, multiplied by 90

**xGDiff**: Goals minus expected goals

**xADiff**: Assists minus expected assists

**xG/Shot**: Expected goals divided by shots

#### FPL Value Stats
**PPM**: Points per million - Total FPL Points divided by FPL Price

**xPP90**: Expected points per 90 - xG90 multiplied by FPL points per goal for position, plus, xA90 multiplied by FPL points for an assist 

**xPPM**: Expected points per million -  xPP90 divided by FPL Price


## TODO
* Fixture analysis
* Automated gameweek detection
* Automated spreadsheet creation based on output data
* Automate data collection from FPL and Understat - Needs to cache so it's not hitting their servers every time the program is run
* Clean sheet prediction based on fixtures
* Code cleanup - Lots of commented out sections and poorly commented areas
