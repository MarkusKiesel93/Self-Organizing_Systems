import lombok.Getter;

import java.util.*;

public final class ExperimentSetup {

    @Getter
    private static List<Experiment> experiments = new ArrayList<>();
    private static int numberOfExperiments = 0;
    private static Map<Integer, List<String>> experimentViolations = new LinkedHashMap<>();

    public static void setup() {

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
                            .particleSpeedLimit(2)
                            .build()));
            
                    ParamConfig.FITNESS_FUNCTIONS.forEach(fitnessFunction ->
                    addExperiment(Experiment.builder()
                            .fitnessFunction(fitnessFunction)
                            .constraint(constrain)
                            .constraintHandlingMethod(constrainHandling)
                            .useConstraint(_useConstraints)
                            .particleSpeedLimit(10)
                            .build()));
            
                    ParamConfig.FITNESS_FUNCTIONS.forEach(fitnessFunction ->
                    addExperiment(Experiment.builder()
                            .fitnessFunction(fitnessFunction)
                            .constraint(constrain)
                            .constraintHandlingMethod(constrainHandling)
                            .useConstraint(_useConstraints)
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
                            .personalConfidence(0.1)
                            .swarmConfidence(1.0)
                            .build()));
            
                    ParamConfig.FITNESS_FUNCTIONS.forEach(fitnessFunction ->
                    addExperiment(Experiment.builder()
                            .fitnessFunction(fitnessFunction)
                            .constraint(constrain)
                            .constraintHandlingMethod(constrainHandling)
                            .useConstraint(_useConstraints)
                            .personalConfidence(0.8)
                            .swarmConfidence(0.8)
                            .build()));
            
                    ParamConfig.FITNESS_FUNCTIONS.forEach(fitnessFunction ->
                    addExperiment(Experiment.builder()
                            .fitnessFunction(fitnessFunction)
                            .constraint(constrain)
                            .constraintHandlingMethod(constrainHandling)
                            .useConstraint(_useConstraints)
                            .personalConfidence(1.0)
                            .swarmConfidence(1.0)
                            .build()));
            
                    ParamConfig.FITNESS_FUNCTIONS.forEach(fitnessFunction ->
                    addExperiment(Experiment.builder()
                            .fitnessFunction(fitnessFunction)
                            .constraint(constrain)
                            .constraintHandlingMethod(constrainHandling)
                            .useConstraint(_useConstraints)
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
                            .particleInertia(0.1)
                            .build()));
            
                    ParamConfig.FITNESS_FUNCTIONS.forEach(fitnessFunction ->
                    addExperiment(Experiment.builder()
                            .fitnessFunction(fitnessFunction)
                            .constraint(constrain)
                            .constraintHandlingMethod(constrainHandling)
                            .useConstraint(_useConstraints)
                            .particleInertia(1.0)
                            .build()));
                    
                    // only run once if constraints are turned off
                    if (_useConstraints == false) {
                        break constraintLoop;
                    }
                }
            }
        }
        // Boundary conditions
        // Penalty Method
        // A too low coefficient can lead to the optimal value sitting inside the 
        // constrained region.
        // Hypothesis:
        // The penalty method allows for the swarm to tunnel through forbidden areas 
        // and therefore better find optima at the constrain boundaries

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

}
