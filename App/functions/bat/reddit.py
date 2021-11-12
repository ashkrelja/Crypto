from praw import Reddit, exceptions
import psycopg2
import re


# Program runs continuously in windows task-scheduler within AWS EC2 instance


class RedditStream(Reddit):

    def __init__(self):
        self._reddit_connection = Reddit(client_id = "5b_xx1hbLDofqw", client_secret = "90fZ1BTCg24nnH7XZfwbwXvtZstv6w",
                                         password = "Economics3$", user_agent = "text_analysis",username = "ashkrelja")

        self._reddit_list = ['SHIBArmy', 'CryptoCurrency', 'wallstreetbets', 'Wallstretbetsnew'] 

        self._db_connection = psycopg2.connect(database = 'postgres',user = 'postgres', password = 'Economics3$',
                                    host = 'aws-crypto-db.c49synhfql06.us-east-2.rds.amazonaws.com', port = '5432')
        
        self._db_cur = self._db_connection.cursor()


    def stream_comments(self):

        subreddit = self._reddit_connection.subreddit("+".join(self._reddit_list))

        try:

            for comment in subreddit.stream.comments():

                if re.findall("SHIB", str(comment.body)):

                    self._db_cur.execute("INSERT INTO public.reddit_stream (author, id, subreddit, body, created_utc) VALUES (%s, %s, %s, %s, %s)",
                    (str(comment.author), str(comment.id), str(comment.subreddit), str(comment.body), str(comment.created_utc)))

                    self._db_connection.commit()


        except exceptions.PRAWException as e:
            pass

if __name__ == '__main__':

    strm_test = RedditStream()  

    strm_test.stream_comments()




