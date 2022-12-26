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

    public static final double CONSTRAINT_R_MIN = 0.0;
    public static final double CONSTRAINT_R_DEFAULT = 50.0;
    public static final double CONSTRAINT_R_MAX = 100;

    public static final Map<String, Object> DEFAULTS = Map.of(
            "fitnessFunction", FITNESS_FUNCTION_SUBERT,
            "constraintHandlingMethod", CONSTRAINT_HANDLING_REJECTION,
            "constraint", CONSTRAINT_5,
            "particleSpeedLimit", PARTICLE_SPEED_LIMIT_DEFAULT,
            "populationSize", POPULATION_SIZE_DEFAULT,
            "personalConfidence", PERSONAL_CONFIDENCE_DEFAULT,
            "swarmConfidence", SWARM_CONFIDENCE_DEFAULT,
            "particleInertia", PARTICLE_INERTIA_DEFAULT,
            "constraintRate", CONSTRAINT_R_DEFAULT
    );

    public static final Map<String, Object> MIN = Map.of(
            "particleSpeedLimit", PARTICLE_SPEED_LIMIT_MIN,
            "populationSize", POPULATION_SIZE_MIN,
            "personalConfidence", PERSONAL_CONFIDENCE_MIN,
            "swarmConfidence", SWARM_CONFIDENCE_MIN,
            "particleInertia", PARTICLE_INERTIA_MIN,
            "constraintRate", CONSTRAINT_R_MIN
    );

    public static final Map<String, Object> MAX = Map.of(
            "particleSpeedLimit", PARTICLE_SPEED_LIMIT_MAX,
            "populationSize", POPULATION_SIZE_MAX,
            "personalConfidence", PERSONAL_CONFIDENCE_MAX,
            "swarmConfidence", SWARM_CONFIDENCE_MAX,
            "particleInertia", PARTICLE_INERTIA_MAX,
            "constraintRate", CONSTRAINT_R_MAX
    );

    public static final Map<String, String> MAPPING = Map.of(
            "fitnessFunction", "fitness_function",
            "constraintHandlingMethod", "constraint_handling_method",
            "constraint", "Constraint",
            "particleSpeedLimit", "particle-speed-limit",
            "populationSize", "population-size",
            "personalConfidence", "personal-confidence",
            "swarmConfidence", "swarm-confidence",
            "particleInertia", "particle-inertia",
            "constraintRate", "constraint_r"
    );

}
