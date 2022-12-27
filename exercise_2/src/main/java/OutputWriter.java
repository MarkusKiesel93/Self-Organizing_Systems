import lombok.AllArgsConstructor;

import java.io.File;

public class OutputWriter {

    private File file;

    public OutputWriter (String filePath) {
        file = new File(filePath);
        // todo: write csv heading
    }

    public void writeExperiment(Experiment experiment, int iteration) {
        // todo write to csv file
    }

}
