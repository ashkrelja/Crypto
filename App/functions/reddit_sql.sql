-- select * from public.reddit_stream;

-- SELECT created_utc, COUNT(*) FROM public.reddit_stream
-- GROUP BY created_utc

-- SELECT ((created_utc AT TIME ZONE 'UTC') AT TIME ZONE 'EST') AS local_time FROM public.reddit_stream

-- SELECT to_date(CAST(created_utc as TEXT), 'YYYY-MM-DD') FROM public.reddit_stream

-- SELECT ROUND(created_utc::decimal) FROM public.reddit_stream;

CREATE FUNCTION round_minutes(TIMESTAMP WITHOUT TIME ZONE, integer) 
RETURNS TIMESTAMP WITHOUT TIME ZONE AS $$ 
  SELECT 
     date_trunc('hour', $1) 
     +  cast(($2::varchar||' min') as interval) 
     * round( 
     (date_part('minute',$1)::float + date_part('second',$1)/ 60.)::float 
     / $2::float
      )
$$ LANGUAGE SQL IMMUTABLE;

CREATE FUNCTION round_minutes(TIMESTAMP WITHOUT TIME ZONE, integer,text) 
RETURNS text AS $$ 
  SELECT to_char(round_minutes($1,$2),$3)
$$ LANGUAGE SQL IMMUTABLE;

SELECT COUNT(*), round_minutes(date, 30) AS HALFHOUR FROM
(SELECT created_utc,
to_timestamp(ROUND(created_utc::decimal)::bigint) AT TIME ZONE 'EST' AS date
FROM public.reddit_stream) AS SQ1
GROUP BY HALFHOUR
ORDER BY HALFHOUR

-- SELECT * FROM public.reddit_stream

SELECT subreddit, COUNT(*) FROM public.reddit_stream
WHERE subreddit IN ('wallstreetbets','SHIBArmy','CryptoCurrency')
GROUP BY subreddit

SELECT COUNT(*), round_minutes((date_created::timestamp without time zone at time zone 'utc' at time zone 'est'), 30) AS HALFHOUR
FROM public.twitter_stream
GROUP BY 2
ORDER BY 2

SELECT * FROM public.twitter_stream 
ORDER BY date_created DESC

SELECT COUNT(*) FROM public.twitter_stream

SELECT * FROM public.twitter_stream 
LIMIT 100

-- UPDATE public.twitter_stream set id = author||'_'||date_created
-- WHERE id IS NULL

SELECT COUNT(*) FROM public.twitter_stream WHERE sentiment IS NOT NULL

SELECT sentiment, COUNT(sentiment) AS count FROM public.twitter_stream
WHERE sentiment IS NOT NULL
GROUP BY sentiment

SELECT id, text, sentiment FROM public.twitter_stream WHERE sentiment IS NULL ORDER BY date_created DESC LIMIT 1000

SELECT pg_size_pretty(pg_database_size('postgres'))

SELECT PERCENTILE_DISC(0.5) WITHIN GROUP(ORDER BY sentiment) FROM public.twitter_stream

SELECT * FROM public.reddit_stream LIMIT 100