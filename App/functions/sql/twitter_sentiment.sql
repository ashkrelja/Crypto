SELECT COUNT(sentiment) FROM public.twitter_stream
WHERE sentiment IS NOT NULL
GROUP BY sentiment