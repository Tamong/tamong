
import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

public class avgtemp {

    public static class Map
            extends Mapper<LongWritable, Text, Text, DoubleWritable>{
        
        // The mapper will output <Region, AvgTemperature>
        private Text region = new Text();
        private DoubleWritable temperature = new DoubleWritable();

        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            // Split the line by comma
            String[] line = value.toString().split(","); // csv file
            if (line.length > 7) {  // Check to ensure line has enough data
                region.set(line[0]); // Set region as the key
                try {
                    double tempValue = Double.parseDouble(line[7]); // AvgTemperature
                    if (tempValue != -99) { // Filter out unknown temperature values
                        temperature.set(tempValue);
                        context.write(region, temperature);  // Emit <City, AvgTemperature>
                    }
                } catch (NumberFormatException e) {
                    // Skip the record if temperature is not a number
                }
            }
        }
    }

    public static class Reduce
            extends Reducer<Text,DoubleWritable,Text,DoubleWritable> {

        private DoubleWritable avgTemperature = new DoubleWritable();

        public void reduce(Text key, Iterable<DoubleWritable> values, Context context) throws IOException, InterruptedException {
            double sum = 0;
            int count = 0;

            for (DoubleWritable val : values) {
                sum += val.get();
                count++;
            }
            avgTemperature.set(sum / count); // Calculate the average temperature
            context.write(key, avgTemperature); // Emit <Region, AvgTemperature>
        }
    }


    // Driver program
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
        // get all args
        if (otherArgs.length != 2) {
            System.err.println("Usage: avgtemp <in> <out>");
            System.exit(2);
        }

        // create a job with name "averagetemperature"
        Job job = Job.getInstance(conf, "averagetemperature");
        job.setJarByClass(avgtemp.class);
        job.setMapperClass(Map.class);
        job.setReducerClass(Reduce.class);

        // uncomment the following line to add the Combiner job.setCombinerClass(Reduce.class);

        // set output key type
        job.setOutputKeyClass(Text.class);
        // set output value type
        job.setOutputValueClass(DoubleWritable.class);
        //set the HDFS path of the input data
        FileInputFormat.addInputPath(job, new Path(otherArgs[0]));
        // set the HDFS path for the output
        FileOutputFormat.setOutputPath(job, new Path(otherArgs[1]));
        //Wait till job completion
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}