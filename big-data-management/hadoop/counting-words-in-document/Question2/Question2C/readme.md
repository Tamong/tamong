Philip Wallis
PTW190000
CS4371.001 HW1

Question 2C:
This program extends on top of 2B, WordOccurance, to get the top 10 words with the most occurances.
It is also case insensitive with punctuations removed.

Requirements:
Hadoop 3.3.6
Java 1.8

To run the jar file:

1. Turn on hadoop
2. run `hadoop jar <Path/>TopWords.jar <input_path> <output_path>`
   For example, `hadoop jar TopWords.jar /user/philip/input/input_hw1.txt /user/philip/output/TopWords`
3. Then to retrieve the results, run `hdfs dfs -get <output_path_from_above> <new_output_path`
   For example: `hdfs dfs -get /user/philip/output/TopWords /Users/philip/Desktop/School/CS4371`
4. Open the TopWords folder to see `_SUCCESS` file and `part-r-00000` file
