import org.nlogo.app.App;
import org.nlogo.nvm.InstructionJ;

import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


// Netlogo User Manual: http://ccl.northwestern.edu/netlogo/docs/index2.html
// Netlogo Controlling API: https://github.com/NetLogo/NetLogo/wiki/Controlling-API
public class Main {

    private static final int ITERATIONS_BY_EXPERIMENT = 100;
    private static final int MAX_ITERATIONS_BY_RUN = 100;
    private static final String MODEL_FILE_NAME = "PSO_NL_Template.nlogo";


    public static void main(String[] argv) {
        App.main(argv);
        String modelFilePath = Paths.get(MODEL_FILE_NAME).toAbsolutePath().toString();
        try {
            java.awt.EventQueue.invokeAndWait(
                    new Runnable() {
                        public void run() {
                            try {
                                App.app().open(modelFilePath, true);
                            }
                            catch(java.io.IOException ex) {
                                ex.printStackTrace();
                            }}});

            List<Experiment> experiments = definedExperiments();
            for (int i = 0; i < experiments.size(); i++) {
                System.out.println("Start Experiment " + (i + 1));
                runExperiment(experiments.get(i));
                System.out.println("Stop Experiment " + (i + 1));
            }
        }
        catch(Exception e) {
            e.printStackTrace();
        }
    }

    private static void runExperiment(Experiment experiment) {
        setParams(experiment.parameters());
        App.app().command("setup");
        for (int i = 0; i < ITERATIONS_BY_EXPERIMENT; i++) {
            run();
            report();
            repeat();
        }
    }

    // todo: how to correctly run the experiment
    private static void run() {
        App.app().command("repeat " + MAX_ITERATIONS_BY_RUN + " [ iterate ]");
    }

    // todo: capture result of experiment run
    private static void report() {
        System.out.println( App.app().report("global-best-val"));
    }

    private static void repeat() {
        App.app().command("clear-all");
        App.app().command("import-world \"backup.txt\"");
        App.app().command("update-highlight");
        App.app().command("reset-ticks");
    }

    private static void setParams(Map<String, Object> params) {
        params.forEach((paramName, param) -> {
            App.app().command(setCommand(paramName, param));
        });
    }


    private static String setCommand(String name, Object value) {
        if (value instanceof String) {
            return "set " + name + " \"" + value + "\"";
        } else {
            return "set " + name + " " + value;
        }
    }

    private static List<Experiment> definedExperiments() {
        List<Experiment> experiments = new ArrayList<>();

        experiments.add(Experiment.builder()
                .fitnessFunction("Booth's function")
                .particleSpeedLimit(10)
                .build());

        // todo: define multiple experiments

        return experiments;
    }

}
