import psycopg2
import psycopg2.pool
import configparser
from typing import List, Dict


class PostgreSQL:
    def __init__(self, config_file: str):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.pool = psycopg2.pool.SimpleConnectionPool(
            1,
            10,
            host=self.config['postgresql']['host'],
            database=self.config['postgresql']['database'],
            user=self.config['postgresql']['user'],
            password=self.config['postgresql']['password']
        )
        self.table_name = self.config['table']['name']

    def execute_query(self, query: str, values: tuple = None):
        conn = self.pool.getconn()
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        self.pool.putconn(conn)

    def insert_data(self, data: Dict[str, str]):
        query = f"INSERT INTO {self.table_name} (article, link) VALUES (%s, %s)"
        self.execute_query(query, (data['text'], data['link']))

    def insert_multiple_data(self, data_list: List[Dict[str, str]]):
        query = f"INSERT INTO {self.table_name} (article, link) VALUES (%s, %s)"
        values = [(data['text'], data['link']) for data in data_list]
        conn = self.pool.getconn()
        cursor = conn.cursor()
        cursor.executemany(query, values)
        conn.commit()
        cursor.close()
        self.pool.putconn(conn)
