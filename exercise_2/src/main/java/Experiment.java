import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.nlogo.app.App;

import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;


@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Experiment {

    private String fitnessFunction;
    private String constraintHandlingMethod;
    private String constraint;
    private Integer particleSpeedLimit;
    private Integer populationSize;
    private Double personalConfidence;
    private Double swarmConfidence;
    private Double particleInertia;
    private Double constraintRate;

    // creates a Map for all parameters with the mapped parameter values
    // defaults as configured in ParamConfig are used if not set in Experiment
    public Map<String, Object> parameters() {
        Map<String, Object> params = new HashMap<>();
        Field[] fields = getClass().getDeclaredFields(); // get all the fields from your class.
        for (Field field : fields) {
            try {
                String fieldName = field.getName();
                if (field.get(this) == null) {
                    field.set(this, ParamConfig.DEFAULTS.get(fieldName));
                }
                checkConstraint(fieldName, field.get(this));
                params.put(ParamConfig.MAPPING.get(field.getName()), field.get(this));
            } catch (IllegalArgumentException ex) {
                ex.printStackTrace();
            } catch (IllegalAccessException ex) {
                ex.printStackTrace();
            }
        }
        return params;
    }


    private void checkConstraint(String paramName, Object value) {
        if (ParamConfig.MIN.containsKey(paramName)) {
            if (value instanceof Integer) {
                int min = (int) ParamConfig.MIN.get(paramName);
                if ((int) value < min) {
                    throw new RuntimeException(paramName + " value " + value + " not allowed min: " + min);
                }
            }
            if (value instanceof Double) {
                double min = (double) ParamConfig.MIN.get(paramName);
                if ((double) value < min) {
                    throw new RuntimeException(paramName + " value " + value + " not allowed min: " + min);
                }
            }
        }
        if (ParamConfig.MAX.containsKey(paramName)) {
            if (value instanceof Integer) {
                int max = (int) ParamConfig.MAX.get(paramName);
                if ((int) value > max) {
                    throw new RuntimeException(paramName + " value " + value + " not allowed max: " + max);
                }
            }
            if (value instanceof Double) {
                double max = (double) ParamConfig.MAX.get(paramName);
                if ((double) value > max) {
                    throw new RuntimeException(paramName + " value " + value + " not allowed max: " + max);
                }
            }
        }
    }
}
