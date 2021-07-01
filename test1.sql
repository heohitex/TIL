select distinct city
from station
where lower(SUBSTR(city,-1,1)) not in ('a','e','i','o','u');
