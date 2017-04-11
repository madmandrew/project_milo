"""Run this file to insert the season data into the database"""

from pymongo import MongoClient
import csv

client = MongoClient('localhost:27017')
db = client.march_madness

csv_files = ['./csv_files/season_files/2011_team_season.csv',
             './csv_files/season_files/2012_team_season.csv',
             './csv_files/season_files/2013_team_season.csv',
             './csv_files/season_files/2014_team_season.csv',
             './csv_files/season_files/2015_team_season.csv',
             './csv_files/season_files/2016_team_season.csv',
             './csv_files/season_files/2017_team_season.csv']

for file in csv_files:
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for document in reader:
            pass
            # Does this document already exist?
            if db.reg_season_stats.find_one({"Year": file[25:29], "Team": document["Team"]}) == None:
                db.reg_season_stats.insert(document)
