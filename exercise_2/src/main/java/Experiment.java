import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;


@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Experiment {

    // parameters
    private String fitnessFunction;
    private Boolean useConstraint;
    private String constraintHandlingMethod;
    private String constraint;
    private Integer particleSpeedLimit;
    private Integer populationSize;
    private Double personalConfidence;
    private Double swarmConfidence;
    private Double particleInertia;
    private Double constraintR;

    // results
    private double fitness;
    private double optimum;
    private int numberOfIterations;
    private int numberOfIterationsUntilFitness;
    private boolean optimumReached;

    // other
    private int number; // number of experiment
    private Map<String, Object> parameters;

    public Map<String, Object> getParameters() {
        if (this.parameters == null || this.parameters.size() == 0) {
            createParams();
        }
        return this.parameters;
    }

    // creates a sorted Map for all parameters with the mapped parameter values
    // defaults as configured in ParamConfig are used if not set in Experiment
    private void createParams() {
        this.parameters = new HashMap<>();
        Arrays.stream(getClass().getDeclaredFields()).forEach(field -> {
            String fieldName = field.getName();
            if (ParamConfig.NETLOGO_MAPPING.containsKey(fieldName)) {
                try {
                    if (field.get(this) == null) {
                        field.set(this, ParamConfig.DEFAULTS.get(fieldName));
                    }
                    ParamConfig.checkConstraint(fieldName, field.get(this));
                    this.parameters.put(ParamConfig.NETLOGO_MAPPING.get(field.getName()), field.get(this));
                } catch (IllegalArgumentException | IllegalAccessException ex) {
                    ex.printStackTrace();
                }
            }
        });
    }

}
