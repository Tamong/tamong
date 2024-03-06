Philip Wallis
PTW190000
CS4371.001 HW1

Question 2A:
The program returns the word count for an input txt file.

Requirements:
Hadoop 3.3.6
Java 1.8

To run the jar file:

1. Turn on hadoop
2. run `hadoop jar <Path/>WordCount.jar <input_path> <output_path>`
   For example, `hadoop jar WordCount.jar /user/philip/input/input_hw1.txt /user/philip/output/WordCount`
3. Then to retrieve the results, run `hdfs dfs -get <output_path_from_above> <new_output_path>`
   For example: `hdfs dfs -get /user/philip/output/WordCount /Users/philip/Desktop/School/CS4371`
4. Open the WordCount folder to see `_SUCCESS` file and `part-r-00000` file
