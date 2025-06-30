import java.util.ArrayList;
import java.util.HashMap;

public class Main {

    public static void main(String[] args) {
        try {
            // Create dataset and load data
            Dataset dataset = new Dataset();
            String filePath = "./Datasets/iris.csv";
            dataset.readCSV(filePath);

            // Create decision tree with dataset and target column
            DecisionTree decisionTree = new DecisionTree(dataset, "Species");

            ArrayList<String> speciesFromRows = dataset.getColumn("Species");

            if (speciesFromRows != null) {
                // Test entropy calculation using row-based structure
                double entFromRows = decisionTree.calcEntropy();
                System.out.println("Entropy from rows structure: " + entFromRows);
            }
            
            // get all column names from header
            ArrayList<String> headers = dataset.getHeaders();
            headers.remove("Species");
            headers.remove("Id"); // Remove Id column if present
            
            for (String colName : headers) {
                System.out.println("Column: " + colName);
                System.out.println("\n=== Grouping rows by attribute: " + colName + " ===");
                HashMap<String, ArrayList<ArrayList<String>>> groupedRows = null;

                // Get count of unique values for each Column
                int uniqCnt = dataset.getUniqueValueCount(colName);
                System.out.println("\nNumber of unique values in " + colName + " is : " + uniqCnt);

                if (uniqCnt >= 20) {
                    // Group rows by attribute value in ranges
                    double minVal = dataset.getMinValue(colName);
                    double maxVal = dataset.getMaxValue(colName);
                    int intervals = (int) Math.round((maxVal - minVal) * 3);
                    groupedRows = dataset.groupRowsByAttribute(colName, minVal, maxVal, intervals);
                    System.out.println("Grouped rows by " + colName + " in ranges of " + intervals + " intervals.");
                } else {
                    // Group rows by attribute value
                    groupedRows = dataset.groupRowsByAttribute(colName);
                }

                if (groupedRows != null) {
                    System.out.println(
                            "Successfully grouped " + groupedRows.size() + " unique values for attribute: " + colName);

                    // Calculate information gain using grouped data
                    System.out.println("\n=== Calculating Information Gain ===");
                    double ig = decisionTree.calcIG(colName, groupedRows);
                    System.out.println("Information Gain for " + colName + ": " + ig);

                    System.out.println("\n === Calculating Information Gain Ratio (IGR) ===");
                    double igr = decisionTree.calcIGR(colName, groupedRows);
                    System.out.println("Information Gain Ratio for " + colName + ": " + igr);

                    // Calculate NWIG
                    System.out.println("\n=== Calculating Normalized Weighted Information Gain (NWIG) ===");
                    double nwig = decisionTree.calcNWIG(colName, groupedRows);
                    System.out.println("Normalized Weighted Information Gain for " + colName + ": " + nwig);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
