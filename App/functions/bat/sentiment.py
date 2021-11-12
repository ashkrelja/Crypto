from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
import psycopg2
import torch


class Sentiment:

    def __init__(self):

        self._tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

        self._model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

        self._db_connection = psycopg2.connect(database = 'postgres',user = 'postgres', password = 'Economics3$',
                                    host = 'aws-crypto-db.c49synhfql06.us-east-2.rds.amazonaws.com', port = '5432')
        
        self._db_cur = self._db_connection.cursor()

    def pre_process(self, df):

        self.df = df

        self.df['tokens'] = self.df['text'].apply(lambda x: self._tokenizer.encode(x ,return_tensors = 'pt'))

        return self.df


    def _sentiment_model(self, token):

        self.token = token

        self.result = self._model(self.token)

        return int(torch.argmax(self.result.logits)) + 1

    def sentiment_query(self, sql):

        self.sql = sql

        self._db_cur.execute(sql)

        self.data = self._db_cur.fetchall()

        self.col_names = [column[0] for column in self._db_cur.description]

        self.df = pd.DataFrame(self.data, columns = self.col_names)

        return self.df

    def sentiment_score(self, df):

        self.sent_df = df

        self.sent_df['sentiment'] = self.sent_df['tokens'].apply(lambda x: self._sentiment_model(x[:512]))

        return self.sent_df

    def sentiment_updater(self,df):

        self.df = df

        rows = zip(self.df.id, self.df.sentiment)

        self._db_cur.execute('DROP TABLE IF EXISTS twitter_feed')

        self._db_cur.execute('CREATE TEMP TABLE twitter_feed(id TEXT, sentiment INT) ON COMMIT DROP')

        self._db_cur.executemany('INSERT INTO twitter_feed (id, sentiment) VALUES(%s, %s)', rows) 

        self._db_cur.execute("""UPDATE public.twitter_stream 
                                    SET sentiment = twitter_feed.sentiment
                                    FROM twitter_feed
                                    WHERE twitter_feed.id = twitter_stream.id  
                            """)

        self._db_connection.commit()

def main():

    main = Sentiment()

    main_df = main.sentiment_query('SELECT id, text, sentiment FROM public.twitter_stream WHERE sentiment IS NULL LIMIT 1000')

    main_df_tokens = main.pre_process(main_df)

    main_df_scores = main.sentiment_score(main_df_tokens)

    main.sentiment_updater(main_df_scores)

if __name__ == '__main__':

    main()
    
# test = Sentiment()

# df = test.sentiment_query('SELECT id, text, sentiment FROM public.twitter_stream WHERE sentiment IS NULL LIMIT 1000')

# pp_tokens_df = test.pre_process(df)

# sent_scores_df = test.sentiment_score(pp_tokens_df)

# test.sentiment_updater(sent_scores_df)