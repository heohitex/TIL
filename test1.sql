select distinct city
from station
where lower(SUBSTR(city,-1,1)) not in ('a','e','i','o','u');

#
SQL 구문 연습
https://www.hackerrank.com/challenges/weather-observation-station-10/problem?h_r=next-challenge&h_v=zen&h_r=next-challenge&h_v=zen&h_r=next-challenge&h_v=zen
#
