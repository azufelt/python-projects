"""
Ashley Zufelt
NBA stats

"""

import pandas as pd # Our data manipulation library
import seaborn as sns # Used for graphing/plotting
import matplotlib.pyplot as mplot # If we need any low level methods
import os # Used to change the directory to the right place
import numpy as np
import math

os.chdir("/Users/ashleyzufelt/Desktop/GitHub/python/nba_basketball_data/")

"""
Starting Data
"""
# Player list
players = pd.read_csv("basketball_players.csv")
# Master data list: 
master = pd.read_csv("basketball_master.csv")
# Left join to merge the two datasets
nba = pd.merge(players, master, how="left", left_on="playerID", right_on="bioID")



#data in chart
players.head()
#get the column headers
players.columns
nba.columns

# previous data
list = players["year"]
uniqueSeasons= len(np.unique(list))


"""
**********  Part 1  **********
"""

"""
Part 1 - #1  Find mean and median number of points scored. 
"""
# calculate player point averages
mean = players.points.mean()
median = players.points.median()
# display averages
print()
print()
print("Points per season:")
print()
print("Mean:{:.2f}".format(mean))
print()
print("Median:{}".format(median))
print()
print()

"""
Part 1 - #2 Highest number of points recorded in a single season. Identify who scored those points and the year they did so.
"""
# build player per year data
list = players.year
#count length of unique year value list
uniqueSeasons= len(np.unique(list))
# table values
print("Highest # of Single Season Points")
print(players[["playerID", "year", "tmID", "points"]].sort_values("points", ascending=False).head(1)) 

"""
Part 1 - #3 Boxplot showing distribution of: 
                        total points, 
                        total assists,
                        total rebounds 
"""

nba[["year", "useFirst", "lastName", "points", "rebounds", "assists"]].sort_values("rebounds", ascending=False).head(10)

# Remove any rows with GP=0
nba = nba[nba.GP > 0]

# points per game
nba["pointsPerGame"] = nba["points"] / nba["GP"]

# assists per game
nba["assistsPerGame"] = nba["assists"] / nba["GP"]

# re3bounds per game
nba["reboundsPerGame"] = nba["rebounds"] / nba["GP"]

#set up box plot data
sns.boxplot(data= nba[["pointsPerGame", "assistsPerGame", "reboundsPerGame"]])
mplot.title("Total Points, Assists and Rebounds")
mplot.show()

"""
Part 1 - #4 Plot the number of median points scored over time among all players for that year.

The x-axis is the year and the y-axis is the median number of points 
among all players for that year.
"""

# Create data set
median_points_year = nba[["points", "year"]].groupby("year").median()

median_points_year = median_points_year.reset_index()

median_points_year = median_points_year[median_points_year["points"]>0]

# Assign variables to the y axis part of the curve
sns.regplot(data = median_points_year, x = "year", y = "points").set_title("Median points per Year")
# Naming the x-axis, y-axis and the whole graph
mplot.xlabel("Year")
mplot.ylabel("Points")
# Show plot
mplot.show()


"""
**********  Part 2  **********
"""

"""
Part 2 - #1 Player rate of shots made per attempted shot

"""
# print(nba.columns)

# get attempted shots, attempted free throw, attempted 3-pointers
# and get shots made, made free throw, made 3-pointers
PointAverage = nba[["playerID","fgMade", "fgAttempted", "ftMade", "ftAttempted", "threeMade", "threeAttempted", "useFirst", "lastName"]]

PointAverage = PointAverage[PointAverage.fgAttempted>200]
PointAverage = PointAverage[PointAverage.ftAttempted>200]
PointAverage = PointAverage[PointAverage.threeAttempted>200]

# calc average of shot type
PointAverage["fgAverage"] = PointAverage["fgMade"] / PointAverage ["fgAttempted"]
PointAverage["ftAverage"] = PointAverage["ftMade"] / PointAverage ["ftAttempted"]
PointAverage["threeAverage"] = PointAverage["threeMade"] / PointAverage ["threeAttempted"]

# Set up total average data & filter results
PointAverage = PointAverage[PointAverage.fgAverage<1]
PointAverage = PointAverage[PointAverage.ftAverage<1]
PointAverage = PointAverage[PointAverage.threeAverage<1]
PointAverage["totalAverage"] = (PointAverage["fgAverage"] + PointAverage["ftAverage"] + PointAverage["threeAverage"]) / 3

print ()
print ()
print ("Total-Point Average")
# get table values
print (PointAverage[["useFirst", "lastName", "fgAverage", "ftAverage", "threeAverage", "totalAverage"]].sort_values("totalAverage", ascending=False).head(10))
print()
print ()


"""
Part 2 - #2
Players that are exceptional across many categories
"""
#set up 'all around great' data set
AllAroundGreat = nba[["playerID", "useFirst", "lastName", "year", "points", "rebounds", "assists", "steals", "blocks"]]

#Filter for results
AllAroundGreat = AllAroundGreat[AllAroundGreat.points>0]
AllAroundGreat = AllAroundGreat[AllAroundGreat.rebounds>0]
AllAroundGreat = AllAroundGreat[AllAroundGreat.assists>0]
AllAroundGreat = AllAroundGreat[AllAroundGreat.steals>0]
AllAroundGreat = AllAroundGreat[AllAroundGreat.blocks>0]

print ()
print ()
# Title the table
print ("Top 10 Players Across Categories")
# get table values
print (AllAroundGreat[["useFirst", "lastName", "year", "points", "rebounds", "assists", "steals", "blocks"]].sort_values(["points"],ascending=False).head(10))
print ()
print ()
print ("Michale Jordan Stats Across Categories")
# get table values
print (AllAroundGreat[["useFirst", "lastName", "year", "points", "rebounds", "assists", "steals", "blocks"]].sort_values(["points"],ascending=False).head(20))



fig, ax = mplot.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

recipe = ["18907 points",
          "3653 rebounds",
          "3264 assists",
          "1580 steals",
          "561 blocks"]

data = [18907, 3653, 3264, 1580, 561]

wedges, texts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=-40)

bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax.annotate(recipe[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                horizontalalignment=horizontalalignment, **kw)

ax.set_title("Michael Jordan Stats")

mplot.show()







"""
Part 2 - #3
Trend of increased three-point shots either across the league.
More dramatic increase since year 2005
"""
# Get Data set: 3-pointer history by year
ThreePointHistory = nba[["threeMade", "year"]].groupby("year").median()
ThreePointHistory = ThreePointHistory.reset_index()

#Filter for results
ThreePointHistory = ThreePointHistory[ThreePointHistory["threeMade"]>0]

# Plot Average 3-pointers per year
sns.regplot(data = ThreePointHistory, x = "year", y = "threeMade").set_title("Three Point Shot Median per Year")
mplot.show()


"""
**********  Part 3  **********
"""
"""
Part 3 - #1
Many sports analysts argue about which player is the GOAT (the Greatest Of All Time). Based on this data, who would you say is the GOAT? Provide evidence to back up your decision.
"""
# filter player data
GOAT = nba[nba.pointsPerGame>2]
GOAT = nba[nba.assistsPerGame>1]
GOAT = nba[nba.reboundsPerGame>1]

#get new table column headers
# print (nba.columns)

print ()
print ()
# Top 20 players based on stats per game
print ("Greatest Of All Time Stats")
print(nba[["firstName", "lastName", "pointsPerGame","assistsPerGame", "reboundsPerGame"]].sort_values(["pointsPerGame"],ascending=False).head(20))
print ()
print ()



"""
Part 3 - #2
The biographical data in this dataset contains information about home towns, home states, and home countries for these players. Can you find anything interesting about players who came from a similar location?
"""
# get hometown data
homeTown = pd.read_csv("basketball_draft.csv")
# merge with player stats
htStats = pd.merge(players,homeTown, how="left", left_on="playerID", right_on="playerID").sort_values(["draftFrom", "points"],ascending=False).head(20)
#merge with master stats
ultimate = pd.merge(master,htStats, how="left", left_on="bioID", right_on="playerID").sort_values(["points"],ascending=False).head(20)

#get new table column headers
# print (ultimate.columns)
print ()
print ()
# Top 20 point scorers & where they ere from
print ("Home Town Stats")
print(ultimate[["playerID", "birthCountry","hsCountry", "points"]])
print ()
print ()





"""
Part 3 - #3
Find something else in this dataset that you consider interesting. Produce a graph to communicate your insight.

Did coaches that had winning teams coach longer?
"""
# get coach data
coach = pd.read_csv("basketball_coaches.csv")
#get team data
teams = pd.read_csv("basketball_teams.csv")
# merge with player stats
coachingScores = pd.merge(coach,teams, how="left", left_on="tmID", right_on="tmID").sort_values(["stint", "stint"],ascending=False)

#Filter for results
coachingScores = coachingScores[coachingScores.stint>3]
coachingScores = coachingScores[coachingScores.won_x>5]
coachingScores = coachingScores[coachingScores.homeWon>10]
coachingScores = coachingScores[coachingScores.homeLost<15]

#return only unique coaches
coachList = coachingScores["coachID"]
uniqueCoaches= len(np.unique(coachList))

#get new table column headers
# print (coachingScores.columns)
print ()
print ()
# Top 20 point scorers & where they ere from
print ("Coaching Longest Stint")
print(coachingScores[["coachID", "stint","won_x", "homeWon", "homeLost"]].sort_values("stint", ascending=False).head(uniqueCoaches))
print ()
print ()


# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'Coach Beaty', 'Coach Beaty', 'Coach Versadi'
totalScore = coachingScores.won_x + coachingScores.homeWon + coachingScores.homeLost
sizes = [48, 51, 63]
explode = (0, 0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = mplot.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title("Coaching Win/Loss")
# ax.set_title("Matplotlib bakery: A pie")
mplot.show()





