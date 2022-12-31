import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Map;

public class OutputWriter {

    private File file;
    private FileWriter fileWriter;


    public OutputWriter (String filePath, Boolean withResults) throws IOException {
        file = new File(filePath);
        fileWriter = new FileWriter(file);
        if (withResults) {
            writeHeadingWithResult();
        } else {
            writeHeading();
        }
    }

    public void close() throws IOException {
        fileWriter.flush();
        fileWriter.close();
    }

    private void addExperimentParams(StringBuilder stringBuilder, Experiment experiment) {
        Map<String, Object> experimentParameters = experiment.getOutputParameters();
        ParamConfig.OUTPUT_MAPPING_SORTED.forEach((paramName, outputName) -> {
            stringBuilder.append(experimentParameters.get(paramName));
            stringBuilder.append(",");
        });
    }

    public void writeExperiment(Experiment experiment) throws IOException {
        StringBuilder line = new StringBuilder();
        line.append(experiment.getNumber());
        line.append(",");
        addExperimentParams(line, experiment);
        line.append("\n");
        fileWriter.write(line.toString());
    }

    public void writeExperimentWithResult(Experiment experiment, int iteration) throws IOException {
        StringBuilder line = new StringBuilder();
        Map<String, Object> experimentParameters = experiment.getOutputParameters();
        line.append(experiment.getNumber());
        line.append(",");
        line.append(iteration);
        line.append(",");
        addExperimentParams(line, experiment);
        line.append(experiment.getFitness());
        line.append(",");
        line.append(experiment.getOptimum());
        line.append(",");
        line.append(experiment.getNumberOfIterations());
        line.append(",");
        line.append(experiment.isOptimumReached());
        line.append(",");
        line.append(experiment.getNumberOfIterationsUntilFitness());
        line.append("\n");
        fileWriter.write(line.toString());
        fileWriter.flush();
    }

    private void writeHeading() throws IOException {
        StringBuilder line = new StringBuilder();
        line.append("number,");
        ParamConfig.OUTPUT_MAPPING_SORTED.forEach((paramName, outputName) -> {
            line.append(outputName);
            line.append(",");
        });
        line.append("\n");
        fileWriter.write(line.toString());
    }

    private void writeHeadingWithResult() throws IOException {
        StringBuilder line = new StringBuilder();
        line.append("number,iteration,");
        ParamConfig.OUTPUT_MAPPING_SORTED.forEach((paramName, outputName) -> {
            line.append(outputName);
            line.append(",");
        });
        line.append("fitness,optimum,iterations,optimum_reached,iterations_to_opt");
        line.append("\n");
        fileWriter.write(line.toString());
        fileWriter.flush();
    }

}
