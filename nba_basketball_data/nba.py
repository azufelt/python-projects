"""
Ashley Zufelt
NBA stats

"""

import pandas as pd # Our data manipulation library
import seaborn as sns # Used for graphing/plotting
import matplotlib.pyplot # If we need any low level methods
import os # Used to change the directory to the right place
import numpy as np
os.chdir("/Users/ashleyzufelt/Desktop/Pathway Homework/Winter 2022/Obj Oriented Prog /hello/week12/nba_basketball_data/")



"""
**********  Part 1  **********
"""

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



"""
Part 1 - #1  Find mean and median number of points scored. 
"""
mean = players.points.mean()
median = players.points.median()
print("Points per season: Mean:{:.2f}, Median:{}".format(mean, median))
print("")



"""
Part 1 - #2 Highest number of points recorded in a single season. Identify who scored those points and the year they did so.
"""
list = players.year
uniqueSeasons= len(np.unique(list))

print(players[["playerID", "year", "tmID", "points"]].sort_values("points", ascending=False).head(uniqueSeasons)) #count length of unique year value list



"""
part 1 - #3 Boxplot showing distribution of: 
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

sns.boxplot(data=nba[["pointsPerGame", "assistsPerGame", "reboundsPerGame"]])

gameStats = data=nba[["pointsPerGame", "assistsPerGame", "reboundsPerGame"]]
gameStats.plot(kind ="box")
matplotlib.pyplot.show()



"""
#4 Plot the number of median points scored over time among all players for that year.
"""

# pointsPerYear = nba[["pointsPerGame", "year"]].groupby("year").median()

# # pointsPerYear = pointsPerYear.reset_index()
# # sns.regplot(data=nba_grouped_year, x="year", y="pointsPerGame")
# pointsPerYear.plot(kind ="line")
# matplotlib.pyplot.show()


# # year_points = nba[["year","points"]].groupby("year").median()
# # year_points.plot(kind ="line")
# # matplotlib.pyplot.show()