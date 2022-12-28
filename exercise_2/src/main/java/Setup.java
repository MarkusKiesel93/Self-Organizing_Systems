import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Setup {

    private Integer number;
    private String fitnessFunction;
    private Boolean useConstraint;
    private String constraintHandlingMethod;
    private String constraint;
    private Integer populationSize;
    private Double constraintR;

}
