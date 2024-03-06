
import java.io.IOException;
import java.util.Map;
import java.util.TreeMap;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

public class TopWords {

    public static class Map1
            extends Mapper<LongWritable, Text, Text, IntWritable>{

        private final static IntWritable one = new IntWritable(1);
        private Text word = new Text(); // type of output key

        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            String[] mydata = value.toString().split(" ");
            for (String data : mydata) {
                data = data.replaceAll("\\p{Punct}", "");
                data = data.toLowerCase();
                if(data.length() >0){
                    word.set(data); // set word as each input keyword
                    context.write(word, one); // create a pair <keyword, 1>
                }
                
            }
        }
    }

    public static class Reduce
            extends Reducer<Text,IntWritable,Text,IntWritable> {

        private IntWritable result = new IntWritable();

        private TreeMap<Integer, String> topWords = new TreeMap<>();

        @Override
        public void setup(Context context){
            topWords = new TreeMap<Integer, String>();
        }

        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            int sum = 0; // initialize the sum for each keyword
            for (IntWritable val : values) {
                sum += val.get();
            }
            topWords.put(sum, key.toString());
            // Keep only top 10 entries
            if (topWords.size() > 10) {
                topWords.remove(topWords.firstKey());
            }
        }

        @Override
        protected void cleanup(Context context) throws IOException, InterruptedException {
            for (Map.Entry<Integer, String> entry : topWords.descendingMap().entrySet()) {
                result.set(entry.getKey());
                context.write(new Text(entry.getValue()), result);
            }
        }
    }


    // Driver program
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
        // get all args
        if (otherArgs.length != 2) {
            System.err.println("Usage: TopWords <in> <out>");
            System.exit(2);
        }

        // create a job with name "topwords"
        Job job = new Job(conf, "topwords");
        job.setJarByClass(WordCount.class);
        job.setMapperClass(Map1.class);
        job.setReducerClass(Reduce.class);

        // uncomment the following line to add the Combiner job.setCombinerClass(Reduce.class);

        // set output key type
        job.setOutputKeyClass(Text.class);
        // set output value type
        job.setOutputValueClass(IntWritable.class);
        //set the HDFS path of the input data
        FileInputFormat.addInputPath(job, new Path(otherArgs[0]));
        // set the HDFS path for the output
        FileOutputFormat.setOutputPath(job, new Path(otherArgs[1]));
        //Wait till job completion
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}