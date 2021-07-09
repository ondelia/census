import pickle
from getCensusData import *

usePickled = True
pd.set_option('precision', 2)

if(usePickled):
    with open('census.pickle', 'rb') as f:
        census = pickle.load(f)
    with open('counties.pickle', 'rb') as f:
        counties = pickle.load(f)
    print(counties)
else:
    sourcedata = 'CC-EST2020-ALLDATA.csv'

    census = openCensus(sourcedata)
    counties = buildCounties(census)
    counties = retrievePopulations(census, counties)
    counties = calcGrowth(counties)
    counties = calcType(counties)
    counties = calcDistressed(counties)

    # Pickle the dataframes
    with open('census.pickle', 'wb') as f:
        pickle.dump(census, f)
    with open('counties.pickle', 'wb') as f:
        pickle.dump(counties, f)
    print(counties)

# Calculate stats
usapopgrowth, usaworkgrowth = usaStats(counties)
distressedApop, distressedBpop, distressedNpop, distressedAurban, distressedArural, distressedBurban, distressedBrural, distressedNurban, distressedNrural = distressedStats(counties)

print("USA Population Growth: " + str(round(usapopgrowth, 3)) + "%")
print("USA Working Population Growth: " + str(round(usaworkgrowth, 3)) + "%\n")
print("Population of Distressed Regions: " + str(distressedApop))
print("Population of Watchlist Regions: " + str(distressedBpop))
print("Population of Non-Distressed Regions: " + str(distressedNpop) + "\n")
print("Population of Urban Distressed Regions: " + str(distressedAurban))
print("Population of Rural Distressed Regions: " + str(distressedArural) + "\n")
print("Population of Urban Watchlist Regions: " + str(distressedBurban))
print("Population of Rural Watchlist Regions: " + str(distressedBrural) + "\n")
print("Population of Urban Non-Distressed Regions: " + str(distressedNurban))
print("Population of Rural Non-Distressed Regions: " + str(distressedNrural) + "\n")

counties.to_csv('counties.csv')