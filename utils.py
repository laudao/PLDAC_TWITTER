import mysql.connector
from preprocessing import *

def connect_to_db():
    twitter_db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password",
        database="twitter_db"
    )
    return twitter_db



