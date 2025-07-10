import psycopg2
from psycopg2.extras import DictCursor
import pandas as pd
from datetime import datetime

class AWS_RDB():

    def __init__(self):
        self._db_connection = psycopg2.connect(database = 'postgres',user = 'postgres', password = 'Economics3$',
                                    host = 'aws-crypto-db.c49synhfql06.us-east-2.rds.amazonaws.com', port = '5432')

        self._db_cur = self._db_connection.cursor(cursor_factory = DictCursor)
        # self._db_cur = self._db_connection.cursor()


    def reddit_query_half_hour(self):

        # self.sql_file = open("reddit_sql.sql") #if running locally

        self.sql_file = open("App/functions/sql/reddit_sql.sql") #if running app on web server

        self.sql_as_string = self.sql_file.read()

        self._db_cur.execute(self.sql_as_string)

        self.data = self._db_cur.fetchall()
        
        self.col_names = [column[0] for column in self._db_cur.description]

        self.df = pd.DataFrame(self.data, columns = self.col_names)

        self.df['halfhour'] = self.df['halfhour'].apply(lambda x: datetime.strftime(x, "%m-%d-%Y, %H:%M"))

        # self.jsond = json.dumps(self.df.tail(20).to_dict('list'))

        self.jsond = self.df.tail(20).to_dict('list')

        self._db_cur.close()

        return self.jsond

    def reddit_query_pie_data(self):

        self.sql_file = open("App/functions/sql/reddit_pie.sql")

        # self.sql_file = open("sql/reddit_pie.sql")

        self.sql_as_string = self.sql_file.read()

        self._db_cur.execute(self.sql_as_string)

        self.data = self._db_cur.fetchall()
        
        self.col_names = [column[0] for column in self._db_cur.description]

        self.df = pd.DataFrame(self.data, columns = self.col_names)

        self.jsond = self.df.to_dict('list')

        self._db_cur.close()

        return self.jsond

    # def twitter_query_half_data(self):

    #     self.sql_file = open("App/functions/sql/twitter_sql.sql")

    #     self.sql_as_string = self.sql_file.read()

    #     self._db_cur.execute(self.sql_as_string)

    #     self.data = self._db_cur.fetchall()

    #     self.col_names = [column[0] for column in self._db_cur.description]

    #     self.df = pd.DataFrame(self.data, columns = self.col_names)

    #     self.jsond = self.df.to_dict('list')

    #     self._db_cur.close()

    #     return self.jsond

    # def twitter_sentiment_query(self):

    #     self.sql_file = open("App/functions/sql/twitter_sentiment.sql")

    #     self.sql_as_string = self.sql_file.read()

    #     self._db_cur.execute(self.sql_as_string)

    #     self.data = self._db_cur.fetchall()

    #     self.col_names = [column[0] for column in self._db_cur.description]

    #     self.df = pd.DataFrame(self.data, columns = self.col_names)

    #     self.jsond = self.df.to_dict('list')

    #     self._db_cur.close()

    #     return self.jsond

    def reddit_sentiment_query(self):

        self.sql_file = open("App/functions/sql/reddit_sentiment.sql")

        self.sql_as_string = self.sql_file.read()

        self._db_cur.execute(self.sql_as_string)

        self.data = self._db_cur.fetchall()

        self.col_names = [column[0] for column in self._db_cur.description]

        self.df = pd.DataFrame(self.data, columns = self.col_names)

        self.jsond = self.df.to_dict('list')

        self._db_cur.close()

        return self.jsond

    def reddit_median_query(self):

        self.sql_file = open("App/functions/sql/reddit_median_sql.sql")

        # self.sql_file = open("sql/twitter_median_sql.sql")

        self.sql_as_string = self.sql_file.read()

        self._db_cur.execute(self.sql_as_string)

        self.data = self._db_cur.fetchone()

        self.dict_obj = {'median': self.data[0]}

        self._db_cur.close()

        return self.dict_obj

    # def twitter_total_query(self):

    #     self.sql_file = open("App/functions/sql/twitter_total_sql.sql")

    #     # self.sql_file = open("sql/twitter_median_sql.sql")

    #     self.sql_as_string = self.sql_file.read()

    #     self._db_cur.execute(self.sql_as_string)

    #     self.data = self._db_cur.fetchone()

    #     self.dict_obj = {'count': self.data[0]}

    #     self._db_cur.close()

    #     return self.dict_obj


