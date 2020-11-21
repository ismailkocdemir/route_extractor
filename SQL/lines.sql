INSERT INTO public.lines (name, freq, line)
	SELECT cast(itins.itin_id as character varying), itins.freq, ST_MakeLine( points.point)
	FROM public.itins, public.points
	WHERE points.name = itins.name
	GROUP BY itins.itin_id, itins.freq;
