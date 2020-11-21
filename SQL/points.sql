INSERT INTO public.points(name, point)
	SELECT DISTINCT itins.name, ST_MakePoint(itins.long, itins.lat)
	FROM public.itins;
