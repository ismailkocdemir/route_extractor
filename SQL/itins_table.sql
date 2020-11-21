-- Table: public.itins

-- DROP TABLE public.itins;

CREATE TABLE public.itins
(
  itin_id integer NOT NULL,
  "long" double precision,
  lat double precision,
  index integer NOT NULL,
  name character varying,
  freq integer,
  CONSTRAINT id_index PRIMARY KEY (itin_id, index)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.itins
  OWNER TO guest;
