from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
import psycopg2
import torch
import torch.nn.functional as F
from torch.nn.utils.rnn import pad_sequence


class Sentiment:

    def __init__(self):

        self._tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

        self._model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

        self._db_connection = psycopg2.connect(database = 'postgres',user = 'postgres', password = 'Economics3$',
                                    host = 'aws-crypto-db.c49synhfql06.us-east-2.rds.amazonaws.com', port = '5432')
        
        self._db_cur = self._db_connection.cursor()

        self._ensure_sentiment_column() # Automatically check & create sentiment column


    def _ensure_sentiment_column(self):
        create_column_sql = """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name='reddit_stream'
                AND column_name='sentiment'
            ) THEN
                ALTER TABLE public.reddit_stream ADD COLUMN sentiment INT;
            END IF;
        END;
        $$;
        """
        self._db_cur.execute(create_column_sql)
        self._db_connection.commit()


    # def pre_process(self, df):

    #     self.df = df

    #     self.df['tokens'] = self.df['body'].apply(lambda x: self._tokenizer.encode(x ,return_tensors = 'pt', max_length = 512, truncation = True))

    #     return self.df

    def pre_process(self, df):

        self.df = df

        self.df['tokens'] = self.df['body'].apply(
            lambda x: torch.tensor(self._tokenizer.encode(
                x , max_length = 512, truncation = True
            ))
        )
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

    # def sentiment_score(self, df):

    #     self.sent_df = df

    #     #self.sent_df['sentiment'] = self.sent_df['tokens'].apply(lambda x: self._sentiment_model(x[:512]))

    #     self.sent_df['sentiment'] = self.sent_df['tokens'].apply(lambda x: self._sentiment_model(x))

    #     return self.sent_df

    def sentiment_score(self, df, batch_size=32):

        tokens_list = df['tokens'].tolist()
        all_sentiments = []

        total = len(tokens_list)
        for i in range(0, len(tokens_list), batch_size):

            batch_tokens = tokens_list[i:i + batch_size]
            
            batch_padded = pad_sequence(batch_tokens, batch_first = True, padding_value = self._tokenizer.pad_token_id)

            attention_mask = (batch_padded != self._tokenizer.pad_token_id).long()

            with torch.no_grad():
                outputs = self._model(batch_padded, attention_mask=attention_mask)
                preds = torch.argmax(outputs.logits, dim=1) +1
                all_sentiments.extend(preds.tolist())

            print(f"Processed {min(i+batch_size, total)} / {total}")

        df['sentiment'] = all_sentiments
        return df

    def sentiment_updater(self,df):

        self.df = df

        rows = zip(self.df.id, self.df.sentiment)

        self._db_cur.execute('DROP TABLE IF EXISTS reddit_feed')

        self._db_cur.execute('CREATE TEMP TABLE reddit_feed(id TEXT, sentiment INT) ON COMMIT DROP')

        self._db_cur.executemany('INSERT INTO reddit_feed (id, sentiment) VALUES(%s, %s)', rows) 

        self._db_cur.execute("""UPDATE public.reddit_stream 
                                    SET sentiment = reddit_feed.sentiment
                                    FROM reddit_feed
                                    WHERE reddit_feed.id = reddit_stream.id  
                            """)

        self._db_connection.commit()

def main():

    main = Sentiment()

    #main_df = main.sentiment_query('SELECT id, body, sentiment FROM public.reddit_stream WHERE sentiment IS NULL LIMIT 1000')

    main_df = main.sentiment_query('SELECT id, body FROM public.reddit_stream')

    main_df_tokens = main.pre_process(main_df)

    main_df_scores = main.sentiment_score(main_df_tokens, batch_size = 32)

    main.sentiment_updater(main_df_scores)

if __name__ == '__main__':

    main()
    
# test = Sentiment()

# df = test.sentiment_query('SELECT id, text, sentiment FROM public.twitter_stream WHERE sentiment IS NULL LIMIT 1000')

# pp_tokens_df = test.pre_process(df)

# sent_scores_df = test.sentiment_score(pp_tokens_df)

# test.sentiment_updater(sent_scores_df)