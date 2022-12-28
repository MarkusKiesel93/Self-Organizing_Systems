import org.nlogo.app.App;

import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.nio.file.Paths;
import java.util.*;


// Netlogo User Manual: http://ccl.northwestern.edu/netlogo/docs/index2.html
// Netlogo Controlling API: https://github.com/NetLogo/NetLogo/wiki/Controlling-API
public class Main {

    private static final int ITERATIONS_BY_EXPERIMENT = 1;
    private static final int MAX_ITERATIONS_BY_RUN = 500;
    private static final String MODEL_FILE_NAME = "PSO_NL_Template.nlogo";
    public static final String OUTPUT_FILE_NAME = "results.csv";


    public static void main(String[] argv) {
        // init NetLogo
        App.main(argv);
        try {
            loadNetLogoModel();
            runAllExperiments();
        }
        catch(Exception e) {
            e.printStackTrace();
        }
    }

    // load the Model from the MODEL_FILE_NAME value
    private static void loadNetLogoModel() throws InvocationTargetException, InterruptedException {
        String modelFilePath = Paths.get(MODEL_FILE_NAME).toAbsolutePath().toString();

        java.awt.EventQueue.invokeAndWait(() -> {
            try {
                App.app().open(modelFilePath, true);
            }
            catch(java.io.IOException ex) {
                ex.printStackTrace();
            }});
    }

    // loop for all experiments
    private static void runAllExperiments() throws IOException {
        // setup experiments and output writer
        ExperimentSetup.setup();
        ExperimentSetup.saveAsCSV();
        ExperimentSetup.validate();
        List<Experiment> allExperiments = ExperimentSetup.getExperiments();
        String outputFilePath = Paths.get(OUTPUT_FILE_NAME).toAbsolutePath().toString();
        OutputWriter outputWriter = new OutputWriter(outputFilePath, true);
        // multiple iterations by experiment
        for (int i = 0; i < ITERATIONS_BY_EXPERIMENT; i++) {
            for (Experiment experiment : allExperiments) {
                System.out.println("Start Experiment " + experiment.getNumber() + " iteration " + i);
                runExperiment(experiment);
                System.out.println("Stop Experiment " + experiment.getNumber() + " iteration " + i);
                outputWriter.writeExperimentWithResult(experiment, i);
            }
        }
        outputWriter.close();
    }

    // steps performed for one experiment
    private static void runExperiment(Experiment experiment) {
        setParams(experiment.getParameters());
        setup();
        run();
        report(experiment);
        // todo: maybe use save command from NetLogo to store the experiment
    }

    private static void setup() {
        App.app().command("setup");
    }

    private static void run() {
        App.app().command("repeat " + MAX_ITERATIONS_BY_RUN + " [ iterate ]");
    }

    // NetLogo run command
    private static void runStepByStep(Experiment experiment) {
        final double optimum = (double) App.app().report("[val] of true-best-patch");
        double currentBestVal = -1;
        int iterationOfCurrentBestVal = -1;
        for (int i = 1; i <= MAX_ITERATIONS_BY_RUN; i++) {
            App.app().command("iterate");
            double bestVal = (double) App.app().report("global-best-val");
            if (bestVal > currentBestVal) {
                currentBestVal = bestVal;
                iterationOfCurrentBestVal = i;
            }
            if (currentBestVal == optimum) {
                System.out.printf("Optimum reached after %d iterations!%n", i);
                experiment.setOptimumReached(true);
                break;
            }

        }
        experiment.setNumberOfIterations(iterationOfCurrentBestVal);
        if (experiment.isOptimumReached()) {
            System.out.printf("Optimum of '%f' was reached after %d iterations", currentBestVal, iterationOfCurrentBestVal);

        }else {
            System.out.printf("Optimum of '%f' was NOT reached, best value was '%f' after %d iterations", optimum, currentBestVal, iterationOfCurrentBestVal);
        }
    }

    // NetLogo extract variables of interest
    private static void report(Experiment experiment) {
        experiment.setFitness((double) App.app().report("global-best-val"));
        experiment.setOptimum((double) App.app().report("[val] of true-best-patch"));
        experiment.setNumberOfIterations((int) (double) App.app().report("iterations-to-opt"));
        if (experiment.getFitness() == experiment.getOptimum()) {
            experiment.setOptimumReached(true);
        }
    }

    // NetLogo repeat commands
    private static void repeat() {
        App.app().command("clear-all");
        App.app().command("import-world \"backup.txt\"");
        App.app().command("update-highlight");
        App.app().command("reset-ticks");
    }

    // NetLogo set parameters of Experiment
    private static void setParams(Map<String, Object> params) {
        params.forEach((paramName, param) ->
            App.app().command(setCommand(paramName, param)));
    }

    // NetLogo set global variable command
    private static String setCommand(String name, Object value) {
        if (value instanceof String) {
            return "set " + name + " \"" + value + "\"";
        } else if (value instanceof Boolean) {
            if ((boolean) value) {
                return "set " + name + " TRUE";
            } else {
                return "set " + name + " FALSE";
            }
        } else {
            return "set " + name + " " + value;
        }
    }

}
