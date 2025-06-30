import java.util.ArrayList;
import java.util.HashMap;

public class DecisionTree {
    private Dataset dataset;
    private String targetColumn;
    
    // Constructor
    public DecisionTree(Dataset dataset, String targetColumn) {
        this.dataset = dataset;
        this.targetColumn = targetColumn;
    }
    
    // Get the dataset
    public Dataset getDataset() {
        return dataset;
    }
    
    // Get the target column name
    public String getTargetColumn() {
        return targetColumn;
    }
    
    // Set the target column
    public void setTargetColumn(String targetColumn) {
        this.targetColumn = targetColumn;
    }
    
    // Calculate entropy for the target column
    public double calcEntropy() {
        return Criteria.calcEntropy(dataset, targetColumn);
    }
    
    // Calculate Information Gain for an attribute
    public double calcIG(String attributeColName, HashMap<String, ArrayList<ArrayList<String>>> groupedRows) {
        ArrayList<String> targetCol = dataset.getColumn(targetColumn);
        return Criteria.calcIG(dataset, targetCol, attributeColName, groupedRows);
    }
    
    // Calculate Information Gain Ratio for an attribute
    public double calcIGR(String attributeColName, HashMap<String, ArrayList<ArrayList<String>>> groupedRows) {
        ArrayList<String> targetCol = dataset.getColumn(targetColumn);
        return Criteria.calcIGR(dataset, targetCol, attributeColName, groupedRows);
    }
    
    // Calculate Normalized Weighted Information Gain for an attribute
    public double calcNWIG(String attributeColName, HashMap<String, ArrayList<ArrayList<String>>> groupedRows) {
        ArrayList<String> targetCol = dataset.getColumn(targetColumn);
        return Criteria.calcNWIG(dataset, targetCol, attributeColName, groupedRows);
    }
    
    // Find the best attribute to split on using Information Gain
    public String findBestAttributeIG(ArrayList<String> attributes) {
        String bestAttribute = null;
        double bestIG = -1.0;
        
        for (String attribute : attributes) {
            if (attribute.equals(targetColumn)) continue; // Skip target column
            
            HashMap<String, ArrayList<ArrayList<String>>> groupedRows = dataset.groupRowsByAttribute(attribute);
            if (groupedRows != null) {
                double ig = calcIG(attribute, groupedRows);
                if (ig > bestIG) {
                    bestIG = ig;
                    bestAttribute = attribute;
                }
            }
        }
        
        return bestAttribute;
    }
    
    // Find the best attribute to split on using Information Gain Ratio
    public String findBestAttributeIGR(ArrayList<String> attributes) {
        String bestAttribute = null;
        double bestIGR = -1.0;
        
        for (String attribute : attributes) {
            if (attribute.equals(targetColumn)) continue; // Skip target column
            
            HashMap<String, ArrayList<ArrayList<String>>> groupedRows = dataset.groupRowsByAttribute(attribute);
            if (groupedRows != null) {
                double igr = calcIGR(attribute, groupedRows);
                if (igr > bestIGR) {
                    bestIGR = igr;
                    bestAttribute = attribute;
                }
            }
        }
        
        return bestAttribute;
    }
    
    // Find the best attribute to split on using NWIG
    public String findBestAttributeNWIG(ArrayList<String> attributes) {
        String bestAttribute = null;
        double bestNWIG = -1.0;
        
        for (String attribute : attributes) {
            if (attribute.equals(targetColumn)) continue; // Skip target column
            
            HashMap<String, ArrayList<ArrayList<String>>> groupedRows = dataset.groupRowsByAttribute(attribute);
            if (groupedRows != null) {
                double nwig = calcNWIG(attribute, groupedRows);
                if (nwig > bestNWIG) {
                    bestNWIG = nwig;
                    bestAttribute = attribute;
                }
            }
        }
        
        return bestAttribute;
    }
    
    // TODO: Add methods for building the actual decision tree
    // This is a placeholder for future implementation
    public void buildTree() {
        System.out.println("Building decision tree with target column: " + targetColumn);
        // Implementation will be added later
    }
    
    // TODO: Add methods for prediction
    // This is a placeholder for future implementation
    public String predict(ArrayList<String> instance) {
        System.out.println("Prediction functionality will be implemented later");
        return null;
    }
}
