SELECT subreddit, COUNT(*) FROM public.reddit_stream
WHERE subreddit IN ('wallstreetbets','SHIBArmy','CryptoCurrency')
GROUP BY subreddit