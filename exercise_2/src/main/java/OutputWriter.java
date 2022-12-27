import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Map;

public class OutputWriter {

    private File file;
    private FileWriter fileWriter;


    public OutputWriter (String filePath) throws IOException {
        file = new File(filePath);
        fileWriter = new FileWriter(file);
        writeHeading();
    }

    public void close() throws IOException {
        fileWriter.close();
    }

    public void writeExperiment(Experiment experiment, int iteration) throws IOException {
        StringBuilder line = new StringBuilder();
        Map<String, Object> experimentParameters = experiment.getParameters();
        line.append(experiment.getNumber());
        line.append(",");
        line.append(iteration);
        line.append(",");
        ParamConfig.OUTPUT_MAPPING_SORTED.forEach((paramName, outputName) -> {
            line.append(experimentParameters.get(paramName));
            line.append(",");
        });
        line.append(experiment.getFitness());
        line.append(",");
        line.append(experiment.getNumberOfIterations());
        line.append("\n");
        fileWriter.write(line.toString());
    }

    private void writeHeading() throws IOException {
        StringBuilder line = new StringBuilder();
        line.append("number,iteration,");
        ParamConfig.OUTPUT_MAPPING_SORTED.forEach((paramName, outputName) -> {
            line.append(outputName);
            line.append(",");
        });
        line.append("fitness,iterations_to_opt");
        line.append("\n");
        fileWriter.write(line.toString());
    }

}
