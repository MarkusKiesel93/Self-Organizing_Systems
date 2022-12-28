import org.nlogo.app.App;

import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.nio.file.Paths;
import java.text.SimpleDateFormat;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;


// Netlogo User Manual: http://ccl.northwestern.edu/netlogo/docs/index2.html
// Netlogo Controlling API: https://github.com/NetLogo/NetLogo/wiki/Controlling-API
public class Main {

    private static final int ITERATIONS_BY_EXPERIMENT = 10;
    private static final int ITERATIONS = 10;
    private static final int MAX_ITERATIONS_BY_RUN = 500;
    private static final String MODEL_FILE_NAME = "PSO_NL_Template.nlogo";
    public static final String OUTPUT_FILE_NAME = "results";

    private static final DateTimeFormatter DATE_TIME_FORMATTER = DateTimeFormatter.ofPattern("HH:mm:ss");

    public static void main(String[] argv) {
        // init NetLogo
        App.main(argv);
        try {
            loadNetLogoModel();
            runAllExperiments();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // load the Model from the MODEL_FILE_NAME value
    private static void loadNetLogoModel() throws InvocationTargetException, InterruptedException {
        String modelFilePath = Paths.get(MODEL_FILE_NAME).toAbsolutePath().toString();

        java.awt.EventQueue.invokeAndWait(() -> {
            try {
                App.app().open(modelFilePath, true);
            } catch (java.io.IOException ex) {
                ex.printStackTrace();
            }
        });
    }

    // loop for all experiments
    private static void runAllExperiments() throws IOException {
        // setup experiments and output writer
        //        ExperimentSetup.setup();
        //        ExperimentSetup.saveAsCSV();
        //        ExperimentSetup.validate();

        final List<Setup> setups = ExperimentSetup.createSetups();
        final List<ExperimentDefinition> experiments = ExperimentSetup.createExperiments();
        if (true) return;

        String dateTime = LocalDateTime.now().format(DateTimeFormatter.ofPattern("dd-MM_HH-mm-ss"));
        String outputFilePath = Paths.get(OUTPUT_FILE_NAME + dateTime + ".csv").toAbsolutePath().toString();
        OutputWriter outputWriter = new OutputWriter(outputFilePath, true);

        System.out.printf("Started: %s%n", LocalDateTime.now().format(DATE_TIME_FORMATTER));

        for (int i = 1; i <= ITERATIONS; i++) {
            for (Setup setup : setups) {
                if (setup.getFitnessFunction().equals(ParamConfig.FITNESS_FUNCTION_SCHWEFEL)) {
                    App.app().command("resize-world -512 512 -512 512");
                } else {
                    App.app().command("resize-world -100 100 -100 100");
                }
                App.app().command(
                        setCommand(ParamConfig.NETLOGO_MAPPING.get("fitnessFunction"), setup.getFitnessFunction()));
                App.app().command(
                        setCommand(ParamConfig.NETLOGO_MAPPING.get("useConstraint"), setup.getUseConstraint()));
                if (setup.getUseConstraint()) {
                    App.app().command(setCommand(ParamConfig.NETLOGO_MAPPING.get("constraintHandlingMethod"),
                            setup.getConstraintHandlingMethod()));
                    App.app().command(setCommand(ParamConfig.NETLOGO_MAPPING.get("constraint"), setup.getConstraint()));
                    App.app().command(
                            setCommand(ParamConfig.NETLOGO_MAPPING.get("constraintR"), setup.getConstraintR()));

                }
                App.app().command(
                        setCommand(ParamConfig.NETLOGO_MAPPING.get("populationSize"), setup.getPopulationSize()));

                setup();
                System.out.printf("### Running setup: %s%n", setup);

                for (ExperimentDefinition experimentDefinition : experiments) {
                    final Experiment experiment = Experiment.builder()
                            .fitnessFunction(setup.getFitnessFunction())
                            .useConstraint(setup.getUseConstraint())
                            .constraintHandlingMethod(
                                    setup.getUseConstraint() ? setup.getConstraintHandlingMethod() : "")
                            .constraint(setup.getUseConstraint() ? setup.getConstraint() : "")
                            .constraintR(setup.getConstraintR())
                            .populationSize(setup.getPopulationSize())
                            .particleInertia(experimentDefinition.getParticleInertia())
                            .personalConfidence(experimentDefinition.getPersonalConfidence())
                            .swarmConfidence(experimentDefinition.getSwarmConfidence())
                            .number(experimentDefinition.getNumber() + (setup.getNumber() * 10000))
                            .build();
                    repeat();
                    System.out.printf("%s: Start Experiment %d/%d, setup %d/%d, iteration %d/%d%n",
                            LocalDateTime.now().format(DATE_TIME_FORMATTER), experiment.getNumber(),
                            experiments.size(), setup.getNumber(), setups.size(), i, ITERATIONS);
                    setParams(experiment.getParameters());
                    run();
                    report(experiment);

                    System.out.printf(
                            "%s: Finished Experiment %d/%d, setup %d/%d, iteration %d/%d: Optimum of '%f' was %s " +
                                    "after %d iterations%n",
                            LocalDateTime.now().format(DATE_TIME_FORMATTER), experiment.getNumber(),
                            experiments.size(), setup.getNumber(), setups.size(), i, ITERATIONS,
                            experiment.getOptimum(),
                            experiment.isOptimumReached() ? "reached" :
                                    "NOT reached, best value was '" + experiment.getFitness() + "'",
                            experiment.getNumberOfIterationsUntilFitness());
                    outputWriter.writeExperimentWithResult(experiment, i);
                }
            }

        }

        outputWriter.close();

    }

    private static void setup() {
        App.app().command("setup");
    }

    private static void run() {
        App.app().command("repeat " + MAX_ITERATIONS_BY_RUN + " [ iterate ]");
    }


    // NetLogo extract variables of interest
    private static void report(Experiment experiment) {
        experiment.setFitness((double) App.app().report("global-best-val"));
        experiment.setOptimum((double) App.app().report("[val] of true-best-patch"));
        experiment.setNumberOfIterations((int) (double) App.app().report("iterations"));
        experiment.setNumberOfIterationsUntilFitness((int) (double) App.app().report("iterations-to-opt"));
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
