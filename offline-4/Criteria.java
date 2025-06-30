import java.util.ArrayList;
import java.util.HashMap;

public class Criteria {
    
    // Calculate entropy for a target column
    public static double calcEntropy(ArrayList<String> targetCol) {
        if (targetCol == null || targetCol.size() == 0) {
            return 0.0;
        }
        
        // for each unique value in targetCol, count the frequency
        HashMap<String, Integer> freqMap = new HashMap<>();
        for (String target : targetCol) {
            // Count the frequency of each target value
            freqMap.put(target, freqMap.getOrDefault(target, 0) + 1);
        }
        
        double entropy = 0.0;
        int total = targetCol.size();

        for (String key : freqMap.keySet()) {
            double freq = freqMap.get(key);
            double p_c = freq / total;
            entropy += p_c * Math.log(p_c) / Math.log(2);
        }

        entropy = -entropy; // Entropy is negative of the sum
        return entropy;
    }

    // Overloaded method to calculate entropy using column name from dataset
    public static double calcEntropy(Dataset dataset, String columnName) {
        ArrayList<String> targetCol = dataset.getColumnFromRows(columnName);
        return calcEntropy(targetCol);
    }

    // Calculate Information Gain
    public static double calcIG(Dataset dataset, ArrayList<String> targetCol, String attributeColName,
            HashMap<String, ArrayList<ArrayList<String>>> groupedRows) {

        double prevEnt = calcEntropy(targetCol);
        double entAfterSplit = 0.0;

        // Print the grouped attribute columns
        System.out.println("Grouped rows by attribute '" + attributeColName + "':");

        int indexOfSpecies = dataset.getHeadersFromRows().indexOf("Species");
        int totalRows = dataset.getRowCount();
        if (indexOfSpecies < 0) {
            System.out.println("Species column not found in headers!");
            return -1.0;
        }

        for (String attrValue : groupedRows.keySet()) {
            ArrayList<ArrayList<String>> rowsForValue = groupedRows.get(attrValue);
            if (rowsForValue == null || rowsForValue.isEmpty()) {
                continue; // Skip if no rows for this attribute value
            }

            ArrayList<String> speciesCol = new ArrayList<>();
            for (var row : rowsForValue) {
                speciesCol.add(row.get(indexOfSpecies)); // Extract species column for this attribute value
            }

            double entForValue = calcEntropy(speciesCol);
            entAfterSplit += ((double) rowsForValue.size() / totalRows) * entForValue;
        }

        return prevEnt - entAfterSplit;
    }

    // Calculate Information Value (IV)
    private static double calcIV(Dataset dataset, String attributeColName, 
            HashMap<String, ArrayList<ArrayList<String>>> groupedRows) {
        double iv = 0.0;
        int totalRows = dataset.getColumn(attributeColName).size();

        for (String attrValue : groupedRows.keySet()) {
            ArrayList<ArrayList<String>> rowsForValue = groupedRows.get(attrValue);
            if (rowsForValue == null || rowsForValue.isEmpty()) {
                continue;
            }

            double p_c = (double) rowsForValue.size() / totalRows;
            iv += p_c * Math.log(p_c) / Math.log(2);
        }

        return -iv; // IV is negative of the sum
    }

    // Calculate Information Gain Ratio (IGR)
    public static double calcIGR(Dataset dataset, ArrayList<String> targetCol, String attributeColName,
            HashMap<String, ArrayList<ArrayList<String>>> groupedRows) {

        double ig = calcIG(dataset, targetCol, attributeColName, groupedRows);
        double iv = calcIV(dataset, attributeColName, groupedRows);

        if (iv == 0) {
            return 0.0; // Avoid division by zero
        }

        double igr = (ig / iv);
        return igr;
    }

    // Calculate Normalized Weighted Information Gain (NWIG)
    public static double calcNWIG(Dataset dataset, ArrayList<String> targetCol, String attributeColName,
            HashMap<String, ArrayList<ArrayList<String>>> groupedRows) {

        // 1) Raw information gain
        double ig = calcIG(dataset, targetCol, attributeColName, groupedRows);
        if (ig < 0) {
            // propagate error
            System.out.println("Negative ig for column: " + attributeColName);
            return -1.0;
        }

        int k = groupedRows.size();
        int totalRows = dataset.getRowCount(); // |S|
        
        // 4) Normalizer: log2(k + 1)
        double logNormalizer = Math.log(k + 1) / Math.log(2);
        if (logNormalizer == 0) {
            // if k+1 == 1, i.e. k == 0, no split at all → NWIG = 0
            return 0.0;
        }

        // 5) Size penalty = (1 - (k-1 / |S|))
        double sizePenalty = 1.0 - ((double) (k - 1) / totalRows);

        // 6) Compute NWIG
        double nwig = (ig / logNormalizer) * sizePenalty;
        return nwig;
    }
}
