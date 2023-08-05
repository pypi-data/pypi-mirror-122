"""
This module is a DataFrame and Database generator which takes the detailed match info from file and transforms it into a more readable format. It then analyses and outputs the
data as a new table.
"""

import json
import pandas as pd
from sqlalchemy import create_engine
from operator import itemgetter

class Databaser:
    DATABASE_TYPE = 'postgresql'
    DBAPI = 'psycopg2'
    PORT = 5432
    DATABASE = 'postgres'
    def __init__(self, infile="dotaproscraper/dotadata.json"):
        file_data = self.load_file(infile)
        d = self.load_file('dotaproscraper/db_credentials.json')
        self.ENDPOINT, self.USER, self.PASSWORD = itemgetter('ENDPOINT', 'USER', 'PASSWORD')(d)
        self.matches = file_data["matches"]
        self.create_hero_columns()
        self.create_dataframe()
        self.engine = create_engine(f"{self.DATABASE_TYPE}+{self.DBAPI}://{self.USER}:{self.PASSWORD}@{self.ENDPOINT}:{self.PORT}/{self.DATABASE}")
        self.engine.connect()

    def load_file(self, infile: str) -> dict:
        with open(infile,'r+') as file:
            return json.load(file)

    def create_hero_columns(self):
        self.picked_or_banned = set()
        for match in self.matches:
            self.picked_or_banned.update(match["radiant_picks"])
            self.picked_or_banned.update(match["dire_picks"])
            self.picked_or_banned.update(match["bans"])

    def create_dataframe(self):
        dotaframe = {}
        for i, match in enumerate(self.matches):
            dotaframe[i] = {}
            for hero in self.picked_or_banned:
                if hero in match["radiant_picks"]:
                    if match["winner"] == "radiant":
                        dotaframe[i][hero] = "W"
                    else:
                        dotaframe[i][hero] = "L"
                elif hero in match["dire_picks"]:
                    if match["winner"] == "radiant":
                        dotaframe[i][hero] = "L"
                    else:
                        dotaframe[i][hero] = "W"
                elif hero in match["bans"]:
                    dotaframe[i][hero] = "B"
                else:
                    dotaframe[i][hero] = None
        self.df = pd.DataFrame(dotaframe)
        self.df = self.df.transpose()

    def push_to_db(self, df: pd.DataFrame, db_name: str):
        df.to_sql(db_name, self.engine, if_exists='replace')

    def analyse_rates(self):
        heroes_df = {}
        for hero in self.df:
            hero_df = {}
            hero_df["pickrate"] = (len(self.df[hero][self.df[hero] == 'W'])+len(self.df[hero][self.df[hero] == 'L']))/len(self.df[hero])
            hero_df["banrate"] = len(self.df[hero][self.df[hero] == 'B'])/len(self.df[hero])
            hero_df["winrate"] = len(self.df[hero][self.df[hero] == 'W'])/(len(self.df[hero][self.df[hero] == 'W'])+len(self.df[hero][self.df[hero] == 'L']))
            heroes_df[hero] = hero_df
        heroes_df = pd.DataFrame(heroes_df)
        heroes_df = heroes_df.transpose()
        self.push_to_db(heroes_df, "hero_rates")

    def __str__(self) -> str:
        return str(self.df)

    def __repr__(self) -> str:
        return self.df




if __name__ == "__main__":
    db = Databaser()
    print(db.df)
    db.push_to_db(db.df, "dota_dataset")  
    db.analyse_rates()  