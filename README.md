# US Census Data Analysis
This repository holds my analysis of US Census data, including migration trends and distressed counties.

## Instructions
To use this file, you will need to download the raw US Census Data here: https://www2.census.gov/programs-surveys/popest/datasets/2010-2020/counties/asrh/CC-EST2020-ALLDATA.csv

You can run main.py to analyze the US Census Data. If this is your first time running it, open main.py and change usePickled = False at the top of the file. After you have run the script once, you will have the pickle files, and you can change usePickled = True to save processing time.

## Purpose
This script will analyze the population growth data from US counties over the past decade. I have created a Distressed Counties model, which classifies every county as "Distressed", "Watchlist", or "Not Distressed."

The Tableau file (census.twb) will display a county-level map visualization of the distressed counties.

The categories are defined as follows:

**DISTRESSED** - The county has lost working-age population in the past 5 years, and has lost at least 5% of working-age population in the past 10 years.

**WATCHLIST** - The county has lost working-age population in the past 5 years, and has lost working-age population in the past 10 years.

**NOT DISTRESSED** - The county has gained working-age population in the past 5 years.
