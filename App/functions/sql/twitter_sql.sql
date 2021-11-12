SELECT COUNT(*), round_minutes((date_created::timestamp without time zone at time zone 'utc' at time zone 'est'), 30) AS HALFHOUR  
FROM public.twitter_stream 
GROUP BY 2
ORDER BY 2