import os
import sqlite3
import pandas as pd
import datetime

def get_df():
    with sqlite3.connect(os.environ["TEMPMON_CACHE_DB"]) as con:
        df = pd.read_sql("SELECT * from records",con)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

def filter_last_one_day():
    df = get_df()
    last_day = (datetime.datetime.now() - datetime.timedelta(minutes=24*60))
    df = df.loc[df["timestamp"]>=last_day]
    df = df.loc[df["pressure"]>=800]
    df = df[["timestamp","temperature_h","temperature_p","humidity","pressure"]]
    return df

def filter_last_one_week():
    df = get_df()
    last_day = (datetime.datetime.now() - datetime.timedelta(minutes=24*60*7))
    df = df.loc[df["timestamp"]>=last_day]
    df = df.loc[df["pressure"]>=800]
    df = df[["timestamp","temperature_h","temperature_p","humidity","pressure"]]
    return df

def filter_last_one_month():
    df = get_df()
    last_day = (datetime.datetime.now() - datetime.timedelta(minutes=24*60*30))
    df = df.loc[df["timestamp"]>=last_day]
    df = df.loc[df["pressure"]>=895]
    df = df[["timestamp","temperature_h","temperature_p","humidity","pressure"]]
    return df

def filter_last_six_months():
    df = get_df()
    last_day = (datetime.datetime.now() - datetime.timedelta(minutes=24*60*30*6))
    df = df.loc[df["timestamp"]>=last_day]
    df = df.loc[df["pressure"]>=895]
    df = df[["timestamp","temperature_h","temperature_p","humidity","pressure"]]
    return df


