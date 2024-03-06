Philip Wallis
PTW190000
CS4371.001 HW2

Question B:
The program returns the average of AvgTemperature for each Asian country's year.

Requirements:
Hadoop 3.3.6
Java 1.8

To run the jar file:

1. Turn on hadoop
2. run `hadoop jar <Path/>avgyearasia.jar <input_path> <output_path>`
   For example, `hadoop jar avgyearasia.jar /user/philip/input/city_temperature.csv /user/philip/output/AvgYearAsia`
3. Then to retrieve the results, run `hdfs dfs -get <output_path_from_above> <new_output_path>`
   For example: `hdfs dfs -get /user/philip/output/AvgYearAsia /Users/philip/Desktop/School/CS4371`
4. Open the WordCount folder to see `_SUCCESS` file and `part-r-00000` file
