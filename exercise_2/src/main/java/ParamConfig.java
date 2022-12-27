import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class ParamConfig {

    public static final String FITNESS_FUNCTION_SUBERT = "Shubert function";
    public static final String FITNESS_FUNCTION_BOOTH = "Booth's function";
    public static final String FITNESS_FUNCTION_SCHWEFEL = "Schwefel function";

    public static final String CONSTRAINT_HANDLING_REJECTION = "Rejection Method";
    public static final String CONSTRAINT_HANDLING_PENALTY = "Penalty Method";

    public static final String CONSTRAINT_3 = "Constraint 3";
    public static final String CONSTRAINT_5 = "Constraint 5";
    public static final String CONSTRAINT_10 = "Constraint 10";

    public static final int POPULATION_SIZE_MIN = 1;
    public static final int POPULATION_SIZE_DEFAULT = 14;
    public static final int POPULATION_SIZE_MAX = 100;

    public static final int PARTICLE_SPEED_LIMIT_MIN = 1;
    public static final int PARTICLE_SPEED_LIMIT_DEFAULT = 10;
    public static final int PARTICLE_SPEED_LIMIT_MAX = 20;

    public static final double PARTICLE_INERTIA_MIN = 0.0;
    public static final double PARTICLE_INERTIA_DEFAULT = 0.3;
    public static final double PARTICLE_INERTIA_MAX = 1.0;

    public static final double PERSONAL_CONFIDENCE_MIN = 0.0;
    public static final double PERSONAL_CONFIDENCE_DEFAULT = 0.8;
    public static final double PERSONAL_CONFIDENCE_MAX = 2.0;

    public static final double SWARM_CONFIDENCE_MIN = 0.0;
    public static final double SWARM_CONFIDENCE_DEFAULT = 1.3;
    public static final double SWARM_CONFIDENCE_MAX = 2.0;

    public static final double CONSTRAINT_R_MIN = -1.0;
    public static final double CONSTRAINT_R_DEFAULT = -0.65;
    public static final double CONSTRAINT_R_MAX = 0.0;

    public static final List<String> FITNESS_FUNCTIONS = List.of(
            FITNESS_FUNCTION_SUBERT, FITNESS_FUNCTION_BOOTH, FITNESS_FUNCTION_SCHWEFEL);

    public static final List<String> CONSTRAINTS = List.of(
            CONSTRAINT_3, CONSTRAINT_5, CONSTRAINT_10);

    public static final List<String> CONSTRAINT_HANDLING_OPTIONS = List.of(
            CONSTRAINT_HANDLING_PENALTY, CONSTRAINT_HANDLING_REJECTION
    );

    public static final Map<String, Object> DEFAULTS = Map.of(
            "fitnessFunction", FITNESS_FUNCTION_SUBERT,
            "useConstraint", false,
            "constraintHandlingMethod", CONSTRAINT_HANDLING_REJECTION,
            "constraint", CONSTRAINT_3,
            "particleSpeedLimit", PARTICLE_SPEED_LIMIT_DEFAULT,
            "populationSize", POPULATION_SIZE_DEFAULT,
            "personalConfidence", PERSONAL_CONFIDENCE_DEFAULT,
            "swarmConfidence", SWARM_CONFIDENCE_DEFAULT,
            "particleInertia", PARTICLE_INERTIA_DEFAULT,
            "constraintR", CONSTRAINT_R_DEFAULT
    );

    public static final Map<String, Object> MIN = Map.of(
            "particleSpeedLimit", PARTICLE_SPEED_LIMIT_MIN,
            "populationSize", POPULATION_SIZE_MIN,
            "personalConfidence", PERSONAL_CONFIDENCE_MIN,
            "swarmConfidence", SWARM_CONFIDENCE_MIN,
            "particleInertia", PARTICLE_INERTIA_MIN,
            "constraintR", CONSTRAINT_R_MIN
    );

    public static final Map<String, Object> MAX = Map.of(
            "particleSpeedLimit", PARTICLE_SPEED_LIMIT_MAX,
            "populationSize", POPULATION_SIZE_MAX,
            "personalConfidence", PERSONAL_CONFIDENCE_MAX,
            "swarmConfidence", SWARM_CONFIDENCE_MAX,
            "particleInertia", PARTICLE_INERTIA_MAX,
            "constraintR", CONSTRAINT_R_MAX
    );

    public static final Map<String, String> NETLOGO_MAPPING = Map.of(
            "fitnessFunction", "fitness_function",
            "useConstraint", "constraints",
            "constraintHandlingMethod", "constraint_handling_method",
            "constraint", "Constraint",
            "particleSpeedLimit", "particle-speed-limit",
            "populationSize", "population-size",
            "personalConfidence", "personal-confidence",
            "swarmConfidence", "swarm-confidence",
            "particleInertia", "particle-inertia",
            "constraintR", "constraint_r"
    );

    public static final LinkedHashMap<String, String> OUTPUT_MAPPING_SORTED = new LinkedHashMap<>();
    static {
        OUTPUT_MAPPING_SORTED.put("fitness_function", "fitness_function");
        OUTPUT_MAPPING_SORTED.put("constraints", "use_constraint");
        OUTPUT_MAPPING_SORTED.put("constraint_handling_method", "constraint_handling_method");
        OUTPUT_MAPPING_SORTED.put("Constraint", "constraint");
        OUTPUT_MAPPING_SORTED.put("particle-speed-limit", "particle_speed_limit");
        OUTPUT_MAPPING_SORTED.put("population-size", "population_size");
        OUTPUT_MAPPING_SORTED.put("personal-confidence", "personal_confidence");
        OUTPUT_MAPPING_SORTED.put("swarm-confidence", "swarm_confidence");
        OUTPUT_MAPPING_SORTED.put("particle-inertia", "particle_inertia");
        OUTPUT_MAPPING_SORTED.put("constraint_r", "constraint_r");
    }

    public static void checkConstraint(String paramName, Object value) {
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
