
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

public class avgyearasia {

    public static class Map
            extends Mapper<LongWritable, Text, Text, DoubleWritable>{
        
        // The mapper will output <Region, AvgTemperature>
        private Text countryYear = new Text();
        private DoubleWritable temperature = new DoubleWritable();

        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            String[] line = value.toString().split(","); // csv file

            if (line.length > 7 && "Asia".equals(line[0])) {
                String country = line[1];
                String year = line[6];
                countryYear.set(country + "_" + year);  // Combine Country and Year
                try {
                    double tempValue = Double.parseDouble(line[7]); // AvgTemperature
                    if (tempValue != -99) { // Filter out unknown temperature values
                        temperature.set(tempValue);
                        context.write(countryYear, temperature);  // Emit <Country-Year, AvgTemperature>
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
            System.err.println("Usage: avgyearasia <in> <out>");
            System.exit(2);
        }

        // create a job with name "avgtempasiayear"
        Job job = Job.getInstance(conf, "avgtempasiayear");
        job.setJarByClass(avgyearasia.class);
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