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
    @IgnoreAsParam
    private String fitnessFunction;
    @IgnoreAsParam
    private Boolean useConstraint;
    @IgnoreAsParam
    private String constraintHandlingMethod;
    @IgnoreAsParam
    private String constraint;
    private Integer particleSpeedLimit;
    @IgnoreAsParam
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

    public Map<String, Object> getParameters() {
        return createParams(true);
    }

    public Map<String, Object> getOutputParameters() {
        return createParams(false);
    }

    // creates a sorted Map for all parameters with the mapped parameter values
    // defaults as configured in ParamConfig are used if not set in Experiment
    private Map<String, Object> createParams(boolean ignoreParameters) {
        Map<String, Object> parameters = new HashMap<>();
        Arrays.stream(getClass().getDeclaredFields()).forEach(field -> {
            if (ignoreParameters && field.isAnnotationPresent(IgnoreAsParam.class)) {
                return;
            }
            String fieldName = field.getName();
            if (ParamConfig.NETLOGO_MAPPING.containsKey(fieldName)) {
                try {
                    if (field.get(this) == null) {
                        field.set(this, ParamConfig.DEFAULTS.get(fieldName));
                    }
                    ParamConfig.checkConstraint(fieldName, field.get(this));
                    parameters.put(ParamConfig.NETLOGO_MAPPING.get(field.getName()), field.get(this));
                } catch (IllegalArgumentException | IllegalAccessException ex) {
                    ex.printStackTrace();
                }
            }
        });
        return parameters;
    }

}

