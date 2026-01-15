import pandas as pd
import sqlite3
from pathlib import Path

class DataManager:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')

    def load_data(self):
        try:
            print("Initializing Data Manager...")
            
            # Smart Path Search
            current_path = Path(__file__).resolve()
            search_paths = [
                current_path.parent,             # Same dir
                current_path.parent / "data",    # ./data
                current_path.parent.parent / "data", # ../data
                Path.cwd() / "data"              # CWD/data
            ]
            
            data_dir = None
            for p in search_paths:
                if (p / "support_cases_anonymized.json").exists():
                    data_dir = p
                    break
            
            if not data_dir:
                print("CRITICAL: Data files not found.")
                print(f"Searched in: {[str(p) for p in search_paths]}")
                return False

            cases_path = data_dir / "support_cases_anonymized.json"
            accounts_path = data_dir / "accounts_anonymized.json"

            cases = pd.read_json(cases_path)
            accounts = pd.read_json(accounts_path, convert_dates=["account_created_date"])
            
            cases['case_created_date'] = pd.to_datetime(cases['case_created_date'])
            cases['case_closed_date'] = pd.to_datetime(cases['case_closed_date'])

            cases.to_sql('cases', self.conn, index=False, if_exists='replace')
            accounts.to_sql('accounts', self.conn, index=False, if_exists='replace')
            
            print(f"Database Loaded: {len(cases)} cases, {len(accounts)} accounts.")
            return True
            
        except Exception as e:
            print(f"Data Load Error: {e}")
            return False

    def get_query(self, sql_query):
        return pd.read_sql(sql_query, self.conn)