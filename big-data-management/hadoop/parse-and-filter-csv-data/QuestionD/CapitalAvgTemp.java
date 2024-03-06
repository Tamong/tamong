
import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.MultipleInputs;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

public class CapitalAvgTemp {

    public static class CapitalMap
        extends Mapper<LongWritable, Text, Text, DoubleWritable>{
        
        Text countrycity = new Text();
        DoubleWritable exists = new DoubleWritable();

        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            String[] line = value.toString().replaceAll("\"","").split(","); // csv file
            if (line.length > 2) {
                String compositeKey = line[0] + " " + line[1];  // Combine city and country
                countrycity.set(compositeKey);
                exists.set(-999);
                context.write(countrycity, exists);  // Emit <country city>, -999>));
            }
        }
    }

    public static class CityMap
        extends Mapper<LongWritable, Text, Text, DoubleWritable>{

        Text countrycity = new Text();
        DoubleWritable temperature = new DoubleWritable();

        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            String[] line = value.toString().split(","); // csv file
            if (line.length > 7) {
                try {
                    double tempValue = Double.parseDouble(line[7]); // AvgTemperature
                    if (tempValue != -99) { // Filter out unknown temperature values
                        String compositeKey = line[1] + " " + line[3];  // Combine city and country
                        countrycity.set(compositeKey);
                        temperature.set(tempValue);
                        context.write(countrycity, temperature);  // Emit <country city>, AvgTemperature>
                    }
                } catch (NumberFormatException e) {
                    // Skip the record if temperature is not a number
                }
            }
        }
    }


    public static class Reduce extends Reducer<Text, DoubleWritable, Text, DoubleWritable> {

        public void reduce(Text key, Iterable<DoubleWritable> values, Context context)
            throws IOException, InterruptedException {
            
            Text countrycity = new Text();
            double sum = 0;
            int count = 0;
            boolean exists = false;
            // Split the composite key to get city and country separately
            
            for (DoubleWritable val : values) {
                countrycity.set(key);

                double tempValue = val.get();
                double existsValue = -999;
                // If -999 from val, then it is from the capital file
                if (tempValue == existsValue) {
                    // Valid country city
                    exists = true;
                } else{
                    sum += val.get();
                    count++;
                }                
            }

            // If the city is a capital and has temperature
            if (exists && count > 0) {
                double avgTemp = sum / count;
                // Here, you can either output just the country, or both city and country
                context.write(countrycity, new DoubleWritable(avgTemp));
            }
        }
    }

    // Driver program
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
        // get all args
        if (otherArgs.length != 3) {  // Changed from 2 to 3 to accommodate input and output directories
            System.err.println("Usage: capitalavgtemp <capital_in> <temp_in> <out>");
            System.exit(2);
        }

        // create a job with name "capitalavgtemp"
        Job job = Job.getInstance(conf, "capitalavgtemp");
        job.setJarByClass(CapitalAvgTemp.class);

        // Add multiple input paths with different Mapper classes
        MultipleInputs.addInputPath(job, new Path(otherArgs[0]), TextInputFormat.class, CityMap.class);
        MultipleInputs.addInputPath(job, new Path(otherArgs[1]), TextInputFormat.class, CapitalMap.class);
        
        job.setReducerClass(Reduce.class);

        // set output key type
        job.setOutputKeyClass(Text.class);
        // set output value type
        job.setOutputValueClass(DoubleWritable.class);

        // set the HDFS path for the output
        FileOutputFormat.setOutputPath(job, new Path(otherArgs[2]));

        // Wait till job completion
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }

}