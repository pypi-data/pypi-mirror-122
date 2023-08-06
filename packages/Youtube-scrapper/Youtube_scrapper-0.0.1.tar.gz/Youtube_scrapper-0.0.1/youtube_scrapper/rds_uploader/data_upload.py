import psycopg2
import pandas as pd
from sqlalchemy import create_engine


class Dbload:
    def __init__(self, password, host):
        self.password = password
        self.host = host
        self.tablename = 'YoutubeData'
        self.df = pd.read_csv("./youtube_data.csv")
        self.engine = create_engine(f"postgresql+psycopg2://postgres:{password}@{host}:5432/postgres")
        self.conn = psycopg2.connect(f"dbname=postgres user=postgres password={password} host=3.21.144.229 port=5432")

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS YoutubeData")
        cursor.execute(
            "CREATE TABLE YoutubeData (title VARCHAR(255), description VARCHAR(500), hash_tags VARCHAR(30), "
            "views VARCHAR(30), comments VARCHAR(20000))")
        self.conn.commit()

    def save_to_database(self):
        self.create_table()
        # Do not store into postgres with an index column
        self.df.to_sql(self.tablename, self.engine, if_exists='replace', index=False)
        print(f"Created table: {self.tablename}")

    def read_table(self, tbl):
        self.engine.execute(f'''SELECT * FROM {tbl}
            LIMIT 20''').fetchall()


if __name__ == '__main__':
    sv = Dbload(input('Enter password: '), input('Enter host: '))
    sv.save_to_database()
