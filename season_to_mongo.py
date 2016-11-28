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
             './csv_files/season_files/2016_team_season.csv']

for file in csv_files:
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for document in reader:
            # Does this document already exist?
            if db.reg_season_stats.find_one({"Season": file[42:51], "School": document["Team"]}) == None:
                db.reg_season_stats.insert(document)