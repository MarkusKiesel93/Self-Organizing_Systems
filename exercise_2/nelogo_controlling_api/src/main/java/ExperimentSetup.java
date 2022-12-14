import lombok.Getter;

import java.io.IOException;
import java.nio.file.Paths;
import java.util.*;
import java.util.ArrayList;
import java.util.List;

public final class ExperimentSetup {

    @Getter
    private static List<Experiment> experiments = new ArrayList<>();
    private static int numberOfExperiments = 0;
    private static Map<Integer, List<String>> experimentViolations = new LinkedHashMap<>();

    public static void setup() {

        for (int popSize = 5; popSize < 80; popSize += 20) {
            final int _populationSize = popSize;
            for (boolean useConstraints = true; useConstraints == true; useConstraints = false) {
                //final boolean useConstraints = _useConstraints;
                final boolean _useConstraints = useConstraints;
                constraintLoop:
                for (String constrainHandling : ParamConfig.CONSTRAINT_HANDLING_OPTIONS) {
                    for (String constrain : ParamConfig.CONSTRAINTS) {

                        // Baseline for the tests to compare against
                        ParamConfig.FITNESS_FUNCTIONS.forEach(fitnessFunction ->
                                addExperiment(Experiment.builder()
                                        .fitnessFunction(fitnessFunction)
                                        .constraint(constrain)
                                        .populationSize(_populationSize)
                                        .constraintHandlingMethod(constrainHandling)
                                        .useConstraint(_useConstraints)
                                        .build()));


                        // Hypothesis:
                        // A small speed limit decreases convergence rate but increases
                        // success changes for convergence

                        ParamConfig.FITNESS_FUNCTIONS.forEach(fitnessFunction ->
                                addExperiment(Experiment.builder()
                                        .fitnessFunction(fitnessFunction)
                                        .constraint(constrain)
                                        .constraintHandlingMethod(constrainHandling)
                                        .useConstraint(_useConstraints)
                                        .populationSize(_populationSize)
                                        .particleSpeedLimit(2)
                                        .build()));

                        ParamConfig.FITNESS_FUNCTIONS.forEach(fitnessFunction ->
                                addExperiment(Experiment.builder()
                                        .fitnessFunction(fitnessFunction)
                                        .constraint(constrain)
                                        .constraintHandlingMethod(constrainHandling)
                                        .useConstraint(_useConstraints)
                                        .populationSize(_populationSize)
                                        .particleSpeedLimit(10)
                                        .build()));

                        ParamConfig.FITNESS_FUNCTIONS.forEach(fitnessFunction ->
                                addExperiment(Experiment.builder()
                                        .fitnessFunction(fitnessFunction)
                                        .constraint(constrain)
                                        .constraintHandlingMethod(constrainHandling)
                                        .useConstraint(_useConstraints)
                                        .populationSize(_populationSize)
                                        .particleSpeedLimit(20)
                                        .build()));

                        // Hypothesis:
                        // A weaker swarm coupling decreases convergence speed, because less individuals
                        // are in a good area, but also decreases the likelihood of getting caught in
                        // a local minima

                        ParamConfig.FITNESS_FUNCTIONS.forEach(fitnessFunction ->
                                addExperiment(Experiment.builder()
                                        .fitnessFunction(fitnessFunction)
                                        .constraint(constrain)
                                        .constraintHandlingMethod(constrainHandling)
                                        .useConstraint(_useConstraints)
                                        .populationSize(_populationSize)
                                        .personalConfidence(0.1)
                                        .swarmConfidence(1.0)
                                        .build()));

                        ParamConfig.FITNESS_FUNCTIONS.forEach(fitnessFunction ->
                                addExperiment(Experiment.builder()
                                        .fitnessFunction(fitnessFunction)
                                        .constraint(constrain)
                                        .constraintHandlingMethod(constrainHandling)
                                        .useConstraint(_useConstraints)
                                        .populationSize(_populationSize)
                                        .personalConfidence(0.8)
                                        .swarmConfidence(0.8)
                                        .build()));

                        ParamConfig.FITNESS_FUNCTIONS.forEach(fitnessFunction ->
                                addExperiment(Experiment.builder()
                                        .fitnessFunction(fitnessFunction)
                                        .constraint(constrain)
                                        .constraintHandlingMethod(constrainHandling)
                                        .useConstraint(_useConstraints)
                                        .populationSize(_populationSize)
                                        .personalConfidence(1.0)
                                        .swarmConfidence(1.0)
                                        .build()));

                        ParamConfig.FITNESS_FUNCTIONS.forEach(fitnessFunction ->
                                addExperiment(Experiment.builder()
                                        .fitnessFunction(fitnessFunction)
                                        .constraint(constrain)
                                        .constraintHandlingMethod(constrainHandling)
                                        .useConstraint(_useConstraints)
                                        .populationSize(_populationSize)
                                        .personalConfidence(1.0)
                                        .swarmConfidence(0.1)
                                        .build()));


                        // Hypothesis:
                        // A high paricle inertia allows the swarm to overcome
                        // a local minima by overshooting the target

                        ParamConfig.FITNESS_FUNCTIONS.forEach(fitnessFunction ->
                                addExperiment(Experiment.builder()
                                        .fitnessFunction(fitnessFunction)
                                        .constraint(constrain)
                                        .constraintHandlingMethod(constrainHandling)
                                        .useConstraint(_useConstraints)
                                        .populationSize(_populationSize)
                                        .particleInertia(0.1)
                                        .build()));

                        ParamConfig.FITNESS_FUNCTIONS.forEach(fitnessFunction ->
                                addExperiment(Experiment.builder()
                                        .fitnessFunction(fitnessFunction)
                                        .constraint(constrain)
                                        .constraintHandlingMethod(constrainHandling)
                                        .useConstraint(_useConstraints)
                                        .populationSize(_populationSize)
                                        .particleInertia(1.0)
                                        .build()));

                        // only run once if constraints are turned off
                        if (_useConstraints == false) {
                            break constraintLoop;
                        }
                    }
                }
            }
        }
        // Boundary conditions
        // Penalty Method
        // A too low coefficient can lead to the optimal value sitting inside the 
        // constrained region.
        // Hypothesis:


        /*
        ParamConfig.CONSTRAINTS.forEach(constrain ->
            addExperiment(Experiment.builder()
                    .constraint(constrain)
                    .particleSpeedLimit(10)
                    .build()));
         */
        // todo: setup various Experiments (use addExperiment method)


    }

    // validate all experiments
    public static void validate() {
        if (experimentViolations.size() == 0) {
            return;
        }
        StringBuilder stringBuilder = new StringBuilder();
        stringBuilder.append("There are constraint violations in ");
        stringBuilder.append(experimentViolations.size());
        stringBuilder.append(" Experiments.");
        stringBuilder.append("\n");
        experimentViolations.forEach((experimentNumber, violations) -> {
            stringBuilder.append("\n");
            stringBuilder.append("violations in Experiment ");
            stringBuilder.append(experimentNumber);
            stringBuilder.append(":\n");
            violations.forEach(violation -> {
                stringBuilder.append(violation);
                stringBuilder.append("\n");
            });

        });
        throw new RuntimeException(stringBuilder.toString());
    }

    // handles setting the experiment number for each experiment and validates Experiment
    private static void addExperiment(Experiment experiment) {
        experiment.setNumber(numberOfExperiments++);
        List<String> constraintViolations = experiment.validate();
        if (constraintViolations.size() > 0) {
            experimentViolations.put(experiment.getNumber(), constraintViolations);
        }
        experiments.add(experiment);
    }

    public static void saveAsCSV() throws IOException {
        final String OUTPUT_FILE_NAME = "experiment_setup.csv";
        String outputFilePath = Paths.get(OUTPUT_FILE_NAME).toAbsolutePath().toString();
        OutputWriter outputWriter = new OutputWriter(outputFilePath, false);
        for (Experiment experiment : experiments) {
            outputWriter.writeExperiment(experiment);
        }
        outputWriter.close();
    }

    public static List<Setup> createSetups() {
        int[] populations = new int[]{5, 10, 35, 80};
        List<Setup> setups = new ArrayList<>();


        double[] constraintRs = new double[]{
                -1.0, -1.5, -2.0
        };

        int counter = 0;
        for (int population : populations) {
            for (String fitnessFunction : ParamConfig.FITNESS_FUNCTIONS) {
                setups.add(Setup.builder()
                        .fitnessFunction(fitnessFunction)
                        .populationSize(population)
                        .useConstraint(false)
                        .number(++counter)
                        .build());
                for (String constraintHandlingMethod : ParamConfig.CONSTRAINT_HANDLING_OPTIONS) {
                    for (String constraint : ParamConfig.CONSTRAINTS) {
                        for (double constraintR : constraintRs) {
                            setups.add(Setup.builder()
                                    .fitnessFunction(fitnessFunction)
                                    .populationSize(population)
                                    .useConstraint(true)
                                    .constraintHandlingMethod(constraintHandlingMethod)
                                    .constraint(constraint)
                                    .number(++counter)
                                    .constraintR(constraintR)
                                    .build());
                        }
                    }
                }
            }
        }

        System.out.printf("Created %d setups%n", setups.size());
        return setups;
    }

    public static List<Setup> createSetups2() {
        int[] populations = new int[]{5, 10, 35, 80};
        List<Setup> setups = new ArrayList<>();
        
        int counter = 0;
        for (int population : populations) {
            for (String fitnessFunction : ParamConfig.FITNESS_FUNCTIONS) {
                setups.add(Setup.builder()
                        .fitnessFunction(fitnessFunction)
                        .populationSize(population)
                        .useConstraint(false)
                        .number(++counter)
                        .build());
            }
        }

        System.out.printf("Created %d setups%n", setups.size());
        return setups;
    }
    public static List<ExperimentDefinition> createExperiments2() {
        List<ExperimentDefinition> experiments = new ArrayList<>();

        int[] particleSpeedLimits = new int[]{
                2, 10, 19
        };
        int counter = 0;
        for (int particleSpeedLimit : particleSpeedLimits) {
            experiments.add(ExperimentDefinition.builder()
                    .particleSpeedLimit(particleSpeedLimit)
                    .number(++counter)
                    .build());
        }

        return experiments;
    }

    public static List<ExperimentDefinition> createExperiments() {
        List<ExperimentDefinition> experiments = new ArrayList<>();

        int[] particleSpeedLimits = new int[]{
                2, 10, 19
        };

        double[] particleInertias = new double[]{
                0.1, 0.5, 0.9
        };

        double[] personalConfidences = new double[]{
                //                0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75
                0.5, 1.0, 1.5
        };

        double[] swarmConfidences = new double[]{
                //                0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75
                0.5, 1.0, 1.5
        };

        int counter = 0;
        for (int particleSpeedLimit : particleSpeedLimits) {
            for (double particleInertia : particleInertias) {
                for (double personalConfidence : personalConfidences) {
                    experiments.add(ExperimentDefinition.builder()
                            .particleSpeedLimit(particleSpeedLimit)
                            .particleInertia(particleInertia)
                            .personalConfidence(personalConfidence)
                            .swarmConfidence(2 - personalConfidence)
                            .number(++counter)
                            .build());
                }
            }
        }

        System.out.printf("Created %d experiments%n", experiments.size());


        return experiments;
    }
}
