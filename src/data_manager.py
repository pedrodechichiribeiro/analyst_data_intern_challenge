# This is the SQL handler, initializing the datasets as a in-memory DB, sending and receiving SQL commands.

import pandas as pd
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


class DataManager:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:') # A SQL database (and it's connection) is generated in the RAM memory of the device;

    def load_data(self):
        """Reads JSON files and builds SQL tables."""
        try:
            print("System initializing...")
            
            # First the JSON is read, using panda, turning it into workable dataframes of the cases and accounts

            cases_path = DATA_DIR / "support_cases_anonymized.json"
            accounts_path = DATA_DIR / "accounts_anonymized.json"

            cases = pd.read_json(cases_path)
            accounts = pd.read_json(accounts_path, convert_dates=["account_created_date"])
            
            cases['case_created_date'] = pd.to_datetime(cases['case_created_date'])
            cases['case_closed_date'] = pd.to_datetime(cases['case_closed_date'])

            # The dataframes are initialized in system memory as a SQL table for faster, optmized, access.
            
            cases.to_sql('cases', self.conn, index=False, if_exists='replace')
            accounts.to_sql('accounts', self.conn, index=False, if_exists='replace')
            
            print(f"Database Ready. Loaded {len(cases)} cases and {len(accounts)} accounts.")
            return True
            
        except ValueError as e:
            print(f"Error reading data: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    def get_query(self, sql_query):
        """Helper to run SQL and return a Pandas DataFrame."""
        return pd.read_sql(sql_query, self.conn)