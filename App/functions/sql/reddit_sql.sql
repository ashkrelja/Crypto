SELECT COUNT(*), round_minutes(date, 30) AS HALFHOUR  FROM
(SELECT created_utc,
to_timestamp(ROUND(created_utc::decimal)::bigint) AT TIME ZONE 'EST' AS date
FROM public.reddit_stream) AS SQ1
GROUP BY HALFHOUR 
ORDER BY HALFHOUR 

