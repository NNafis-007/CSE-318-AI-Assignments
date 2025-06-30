import java.util.ArrayList;
import java.util.HashMap;

public class Main {

    // Function to group rows by attribute value
    public static HashMap<String, ArrayList<ArrayList<String>>> groupRowsByAttribute(DecisionTree decisionTree,
            String attributeColName) {
        return decisionTree.groupRowsByAttribute(attributeColName);
    }

    public static HashMap<String, ArrayList<ArrayList<String>>> groupRowsByAttribute(DecisionTree decisionTree,
            String attributeColName, double minVal, double maxVal, int intevals) {
        return decisionTree.groupRowsByAttribute(attributeColName, minVal, maxVal, intevals);
    }


    public static void main(String[] args) {
        try {
            DecisionTree decisionTree = new DecisionTree();
            String filePath = "./Datasets/iris.csv";
            decisionTree.readCSV(filePath);

            ArrayList<String> speciesFromRows = decisionTree.getColumnFromRows("Species");
            // get all column names from header
            ArrayList<String> headers = decisionTree.getHeadersFromRows();
            headers.remove("Species");
            headers.remove("Id"); // Remove Id column if present
            for (String colName : headers) {
                System.out.println("Column: " + colName);
                System.out.println("\n=== Grouping rows by attribute: " + colName + " ===");
                HashMap<String, ArrayList<ArrayList<String>>> groupedRows = null;
                if(colName.equals("PetalLengthCm")){                    
                    groupedRows = groupRowsByAttribute(decisionTree, colName, 0.5, 7.0, 10);                
                }
                else{
                    groupedRows = groupRowsByAttribute(decisionTree, colName);
                }

                if (groupedRows != null) {
                    System.out.println(
                            "Successfully grouped " + groupedRows.size() + " unique values for attribute: " + colName);

                    // Calculate information gain using grouped data
                    System.out.println("\n=== Calculating Information Gain ===");
                    double ig = decisionTree.calcIG(speciesFromRows, colName, groupedRows);
                    System.out.println("Information Gain for " + colName + ": " + ig);
                }

            }

            if (speciesFromRows != null) {

                // Test entropy calculation using row-based structure
                double entFromRows = decisionTree.calcEntropy("Species");
                System.out.println("Entropy from rows structure: " + entFromRows);
                }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
