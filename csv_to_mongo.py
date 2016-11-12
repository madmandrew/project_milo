from pymongo import MongoClient
import csv

def connect_to_db():
    client = MongoClient('localhost:27017')
    db = client.march_madness
    return db

def  read_season_stats_to_db(db):

    csv_files = ['C:/Users/Kendall/PycharmProjects/untitled/2014_season.csv',
                 'C:/Users/Kendall/PycharmProjects/untitled/2013_season.csv',
                 'C:/Users/Kendall/PycharmProjects/untitled/2012_season.csv',
                 'C:/Users/Kendall/PycharmProjects/untitled/2011_season.csv']

    for file in csv_files:
        with open(file) as csvfile:
            reader = csv.DictReader(csvfile)
            for document in reader:
                # Does this document already exist?
                if db.reg_season_stats.find_one({"Season": file[42:51], "School": document["School"]}) == None:
                    db.reg_season_stats.insert(document)

if __name__ == "__main__":
    db = connect_to_db()
    read_season_stats_to_db(db)