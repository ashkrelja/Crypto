from tweepy import Stream
import json
import psycopg2

#twitter stream

class TwitterStream(Stream):

    def on_data(self, data):

        self._db_connection = psycopg2.connect(database = 'postgres',
                                        user = 'postgres'  , 
                                        password = 'Economics3$',
                                        host = 'aws-crypto-db.c49synhfql06.us-east-2.rds.amazonaws.com',
                                        port = '5432')

        self._db_cur = self._db_connection.cursor()

        all_data = json.loads(data)
        
        screen_name = all_data['user']['screen_name']
        tweet = all_data['text']
        date_created = all_data['created_at']
        id = str(screen_name + '_' + date_created)

        # print(all_data['text'])

        self._db_cur.execute("INSERT INTO public.twitter_stream (id, author, text, date_created) VALUES (%s, %s, %s, %s)",
                            (id, screen_name, tweet, date_created))

        self._db_connection.commit()

        return(True)

    def on_error(self, status):
        print(status)

    def on_status(self, status):
        print(status.user.screen_name + " tweeted: " + status.text)

if __name__ == '__main__':

    consumer_key = 'faXEz0iFOkYeo0Z4mC9p9ZWvu' 
    consumer_secret = '86mVjeh0TcuH3czfE34m6qfz5qDCb6xbXMmsnrgMRziyqw142j'
    access_token = '485364393-r1QCKzHXkEe6OKtnDu08gW4YlvxGOW9NHPU4snYx'
    access_token_secret = 'Ob3WM9eErzPLvt9ejFAV5xXr2jjgcFOq5pWmZ4PH5zxFg'

    test = TwitterStream(consumer_key, consumer_secret, access_token, access_token_secret)
    test.filter(track=['SHIB'])
