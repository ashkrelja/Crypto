SELECT PERCENTILE_DISC(0.5) WITHIN GROUP(ORDER BY sentiment) FROM public.twitter_stream
