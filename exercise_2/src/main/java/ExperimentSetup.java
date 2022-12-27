import lombok.Getter;

import java.util.ArrayList;
import java.util.List;

public final class ExperimentSetup {

    @Getter
    private static List<Experiment> experiments = new ArrayList<>();
    private static int numberOfExperiments = 0;

    public static void setup() {


        
        for (boolean _useConstraints = true; _useConstraints == true; _useConstraints = false) {
            final boolean useConstraints = _useConstraints;

            constraintLoop:
            for (String constrainHandling : ParamConfig.CONSTRAINT_HANDLING_OPTIONS) {
                for (String constrain : ParamConfig.CONSTRAINTS) {

                    // Baseline for the tests to compare against
                    ParamConfig.FITNESS_FUNCTIONS.forEach(fitnessFunction ->
                    addExperiment(Experiment.builder()
                            .fitnessFunction(fitnessFunction)
                            .constraint(constrain)
                            .constraintHandlingMethod(constrainHandling)
                            .useConstraints(useConstraints)
                            .build()));
            

                    // Hypothesis:
                    // A small speed limit decreases convergence rate but increases
                    // success changes for convergence
                
                    ParamConfig.FITNESS_FUNCTIONS.forEach(fitnessFunction ->
                    addExperiment(Experiment.builder()
                            .fitnessFunction(fitnessFunction)
                            .constraint(constrain)
                            .constraintHandlingMethod(constrainHandling)
                            .useConstraints(useConstraints)
                            .particleSpeedLimit(2)
                            .build()));
            
                    ParamConfig.FITNESS_FUNCTIONS.forEach(fitnessFunction ->
                    addExperiment(Experiment.builder()
                            .fitnessFunction(fitnessFunction)
                            .constraint(constrain)
                            .constraintHandlingMethod(constrainHandling)
                            .useConstraints(useConstraints)
                            .particleSpeedLimit(10)
                            .build()));
            
                    ParamConfig.FITNESS_FUNCTIONS.forEach(fitnessFunction ->
                    addExperiment(Experiment.builder()
                            .fitnessFunction(fitnessFunction)
                            .constraint(constrain)
                            .constraintHandlingMethod(constrainHandling)
                            .useConstraints(useConstraints)
                            .particleSpeedLimit(25)
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
                            .useConstraints(useConstraints)
                            .personalConfidence(0.1)
                            .swarmConfidence(2.0)
                            .build()));
            
                    ParamConfig.FITNESS_FUNCTIONS.forEach(fitnessFunction ->
                    addExperiment(Experiment.builder()
                            .fitnessFunction(fitnessFunction)
                            .constraint(constrain)
                            .constraintHandlingMethod(constrainHandling)
                            .useConstraints(useConstraints)
                            .personalConfidence(0.8)
                            .swarmConfidence(1.3)
                            .build()));
            
                    ParamConfig.FITNESS_FUNCTIONS.forEach(fitnessFunction ->
                    addExperiment(Experiment.builder()
                            .fitnessFunction(fitnessFunction)
                            .constraint(constrain)
                            .constraintHandlingMethod(constrainHandling)
                            .useConstraints(useConstraints)
                            .personalConfidence(1.0)
                            .swarmConfidence(1.0)
                            .build()));
            
                    ParamConfig.FITNESS_FUNCTIONS.forEach(fitnessFunction ->
                    addExperiment(Experiment.builder()
                            .fitnessFunction(fitnessFunction)
                            .constraint(constrain)
                            .constraintHandlingMethod(constrainHandling)
                            .useConstraints(useConstraints)
                            .personalConfidence(2.0)
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
                            .useConstraints(useConstraints)
                            .particleInertia(0.1)
                            .build()));
            
                    ParamConfig.FITNESS_FUNCTIONS.forEach(fitnessFunction ->
                    addExperiment(Experiment.builder()
                            .fitnessFunction(fitnessFunction)
                            .constraint(constrain)
                            .constraintHandlingMethod(constrainHandling)
                            .useConstraints(useConstraints)
                            .particleInertia(2.0)
                            .build()));
                    
                    // only run once if constraints are turned off
                    if (useConstraints == false) {
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

    // handles setting the experiment number for each experiment
    private static void addExperiment(Experiment experiment) {
        experiment.setNumber(numberOfExperiments++);
        experiments.add(experiment);
    }

}
