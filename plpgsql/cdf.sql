DROP FUNCTION IF EXISTS trip_window();
CREATE OR REPLACE FUNCTION trip_window(window_ date[]) RETURNS TABLE (t_distance float4)
AS
$$
BEGIN
	FOR t_distance in SELECT trip_distance from taxi WHERE lpep_pickup_datetime BETWEEN window_[1] AND window_[2]
	LOOP
		return next; 
	END LOOP;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS calc_cdf();
CREATE OR REPLACE FUNCTION calc_cdf(scope_ date [] DEFAULT null) RETURNS TABLE( x_value float4, cdf_value float4 ) 
AS
$$
DECLARE
	step float4 := 0;
	x_step float4;
	counter int;
	min_ smallint; 
	max_ smallint;
	taxi_ float4[];
BEGIN 
	IF scope_ IS NOT NULL THEN 
		RAISE NOTICE 'Calculating CDF withing window [% - %]', scope_[1], scope_[2];
		SELECT COUNT(trip_distance), MAX(trip_distance), MIN(trip_distance) from taxi 
			WHERE lpep_pickup_datetime BETWEEN scope_[1] AND scope_[2]
			INTO counter, max_, min_;
		x_step := (max_ - min_)::float4/99;
		FOR x_value, cdf_value in SELECT g.n, COUNT(t_distance)
				FROM generate_series(0, 99) g(n) LEFT JOIN
				trip_window(scope_)
				ON width_bucket(t_distance, min_, max_, 99) = g.n
				GROUP BY g.n
				ORDER BY g.n
		LOOP
			cdf_value := cdf_value/counter + step;
			step := cdf_value;
			x_value := min_+ x_value*x_step;
			RETURN NEXT;
		END LOOP;
	ELSE
		RAISE NOTICE 'Calculating CDF for all records';
		SELECT COUNT(trip_distance), MAX(trip_distance), MIN(trip_distance) from taxi 
			INTO counter, max_, min_;
		x_step := (max_ - min_)::float4/99;
		FOR x_value, cdf_value in SELECT g.n, COUNT(trip_distance)
				FROM generate_series(0, 99) g(n) LEFT JOIN
				taxi
				ON width_bucket(trip_distance, min_, max_, 99) = g.n
				GROUP BY g.n
				ORDER BY g.n 
		LOOP
			cdf_value := cdf_value/counter + step;
			step := cdf_value;
			x_value := min_+ x_value*x_step;
			RETURN NEXT;
		END LOOP;
	END IF;
END;
$$ LANGUAGE plpgsql;
