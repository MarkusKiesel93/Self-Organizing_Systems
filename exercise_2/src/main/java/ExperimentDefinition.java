import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;


@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ExperimentDefinition {

    private Integer number;
    private Integer particleSpeedLimit;
    private Double personalConfidence;
    private Double swarmConfidence;
    private Double particleInertia;
    private Double constraintR;

}
