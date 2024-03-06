Philip Wallis
PTW190000
CS4371.001 HW2

Question D:
The program returns the average of AvgTemperature for all Capital cities

Requirements:
Hadoop 3.3.6
Java 1.8

To run the jar file:

1. Turn on hadoop
2. run `hadoop jar <Path/>CapitalAvgTemp.jar <input_temperature> <input_capital> <output_path>`
   For example, `hadoop jar CapitalAvgTemp.jar /user/philip/input/city_temperature.csv /user/philip/input/country-list.csv /user/philip/output/capitalavgtemp`
3. Then to retrieve the results, run `hdfs dfs -get <output_path_from_above> <new_output_path>`
   For example: `hdfs dfs -get /user/philip/output/capitalavgtemp /Users/philip/Desktop/School/CS4371`
4. Open the WordCount folder to see `_SUCCESS` file and `part-r-00000` file
