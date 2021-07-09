import pandas as pd
import numpy as np
from datetime import datetime

def openCensus(source):
    print("Opening Census " + str(datetime.now()))
    census = pd.read_csv(source, engine='python', encoding='latin1')
    census = census[(census['CTYNAME'] != 'Chugach Census Area') & (census['CTYNAME'] != 'Copper River Census Area')]
    print(census)
    print("Finished Opening Census " + str(datetime.now()))
    census['TOT_POP'] = census['TOT_POP'].astype(int)

    return(census)

def buildCounties(census):
    print("Building Counties " + str(datetime.now()))
    counties = pd.DataFrame()

    uniqueCensus = census[(census['YEAR'] == 13) & (census['AGEGRP'] == 0)]
    counties = uniqueCensus[['STNAME', 'CTYNAME', 'TOT_POP']]

    counties = counties.reset_index(drop=True)
    print(counties)
    counties = counties.assign(POP2015=np.nan)
    counties = counties.assign(POP2010=np.nan)
    counties = counties.assign(POPGROWTH=np.nan)
    counties = counties.assign(WORK2020=np.nan)
    counties = counties.assign(WORK2015=np.nan)
    counties = counties.assign(WORK2010=np.nan)
    counties = counties.assign(WORKGROWTH=np.nan)
    counties = counties.assign(TYPE=np.nan)
    counties = counties.assign(DISTRESSED=np.nan)
    print("Finished Building Counties " + str(datetime.now()))

    return(counties)

def retrievePopulations(census, counties):
    i = 0
    while i < len(counties):
        if i % 100 == 0:
            print(str(i) + " of " + str(len(counties)))
        state = counties.loc[i, 'STNAME']
        county = counties.loc[i, 'CTYNAME']

        # Get population in 2010
        pop2010 = census[(census['STNAME'] == state) & (census['CTYNAME'] == county) & (census['YEAR'] == 3) & (
                    census['AGEGRP'] == 0)]['TOT_POP']
        counties.loc[i, 'POP2010'] = pop2010.iat[0]

        # Get population in 2015
        pop2015 = census[(census['STNAME'] == state) & (census['CTYNAME'] == county) & (census['YEAR'] == 8) & (
                    census['AGEGRP'] == 0)]['TOT_POP']
        counties.loc[i, 'POP2015'] = pop2015.iat[0]

        # Get working population in 2010
        work2010 = census[(census['STNAME'] == state) & (census['CTYNAME'] == county) & (census['YEAR'] == 3) & (
                    census['AGEGRP'] >= 4) & (census['AGEGRP'] <= 13)]['TOT_POP']
        counties.loc[i, 'WORK2010'] = work2010.sum()

        # Get working population in 2015
        work2015 = census[(census['STNAME'] == state) & (census['CTYNAME'] == county) & (census['YEAR'] == 8) & (
                    census['AGEGRP'] >= 4) & (census['AGEGRP'] <= 13)]['TOT_POP']
        counties.loc[i, 'WORK2015'] = work2015.sum()

        # Get working population in 2020
        work2020 = census[(census['STNAME'] == state) & (census['CTYNAME'] == county) & (census['YEAR'] == 13) & (
                    census['AGEGRP'] >= 4) & (census['AGEGRP'] <= 13)]['TOT_POP']
        counties.loc[i, 'WORK2020'] = work2020.sum()

        i += 1

    counties = counties.rename(columns={"TOT_POP": "POP2020"})
    print(counties)
    return(counties)

def calcGrowth(counties):
    counties['POPGROWTH'] = ((counties['POP2020'] / counties['POP2010']) - 1) * 100
    counties['WORKGROWTH'] = ((counties['WORK2020'] / counties['WORK2010']) - 1) * 100
    return(counties)

def usaStats(counties):
    usapop2020 = counties['POP2020'].sum()
    usapop2010 = counties['POP2010'].sum()

    usawork2020 = counties['WORK2020'].sum()
    usawork2010 = counties['WORK2010'].sum()

    usapopgrowth = ((usapop2020 / usapop2010) - 1) * 100
    usaworkgrowth = ((usawork2020 / usawork2010) - 1) * 100

    return(usapopgrowth, usaworkgrowth)

def calcType(counties):
    # Regions:
    # Urban: County with more than 400,000 people
    # Suburban: County with more than 250,000 people, which is in the same state and adjacent to a county with 1,000,000 people.
    # Rural: All others.
    counties['TYPE'] = 'R'
    counties.loc[counties['POP2020'] > 100000, 'TYPE'] = 'S'
    counties.loc[counties['POP2020'] > 400000, 'TYPE'] = 'U'
    counties.loc[counties['POP2020'] > 1000000, 'TYPE'] = 'M'

    return(counties)

def calcDistressed(counties):
    work5 = (counties['WORK2020'] - counties['WORK2015'] < 0)
    work10 = (counties['WORK2020'] - counties['WORK2010'] < 0)
    realbad = (counties['WORKGROWTH'] < -5)
    pop5 = (counties['POP2020'] - counties['POP2015'] < 0)
    pop10 = (counties['POP2020'] - counties['POP2010'] < 0)

    counties['DISTRESSED'] = 'N'
    counties.loc[(work5 & work10), 'DISTRESSED'] = 'B'
    counties.loc[(work5 & realbad), 'DISTRESSED'] = 'B'
    counties.loc[(work5 & work10 & realbad), 'DISTRESSED'] = 'A'

    return(counties)

def distressedStats(counties):
    urban = ((counties['TYPE'] == 'U') | (counties['TYPE'] == 'M'))
    rural = ((counties['TYPE'] == 'S') | (counties['TYPE'] == 'R'))

    distressedApop = counties[counties['DISTRESSED'] == 'A']['POP2020'].sum()
    distressedBpop = counties[counties['DISTRESSED'] == 'B']['POP2020'].sum()
    distressedNpop = counties[counties['DISTRESSED'] == 'N']['POP2020'].sum()

    distressedAurban = counties[(counties['DISTRESSED'] == 'A') & urban]['POP2020'].sum()
    distressedArural = counties[(counties['DISTRESSED'] == 'A') & rural]['POP2020'].sum()

    distressedBurban = counties[(counties['DISTRESSED'] == 'B') & urban]['POP2020'].sum()
    distressedBrural = counties[(counties['DISTRESSED'] == 'B') & rural]['POP2020'].sum()

    distressedNurban = counties[(counties['DISTRESSED'] == 'N') & urban]['POP2020'].sum()
    distressedNrural = counties[(counties['DISTRESSED'] == 'N') & rural]['POP2020'].sum()

    return(distressedApop, distressedBpop, distressedNpop, distressedAurban, distressedArural, distressedBurban, distressedBrural, distressedNurban, distressedNrural)