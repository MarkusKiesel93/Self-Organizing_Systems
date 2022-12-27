import lombok.Getter;

import java.util.ArrayList;
import java.util.List;

public final class ExperimentSetup {

    @Getter
    private static List<Experiment> experiments = new ArrayList<>();
    private static int numberOfExperiments = 0;

    public static void setup() {

        ParamConfig.FITNESS_FUNCTIONS.forEach(fitnessFunction ->
            addExperiment(Experiment.builder()
                    .fitnessFunction(fitnessFunction)
                    .particleSpeedLimit(10)
                    .build()));

        ParamConfig.CONSTRAINTS.forEach(constrain ->
            addExperiment(Experiment.builder()
                    .constraint(constrain)
                    .particleSpeedLimit(10)
                    .build()));

        // todo: setup various Experiments (use addExperiment method)


    }

    // handles setting the experiment number for each experiment
    private static void addExperiment(Experiment experiment) {
        experiment.setNumber(++numberOfExperiments);
        experiments.add(experiment);
    }

}
