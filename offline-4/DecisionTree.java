import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

public class DecisionTree {
    private HashMap<Integer, ArrayList<String>> rows;

    public void readCSV(String filePath) throws IOException {
        rows = new HashMap<>();
        ArrayList<String[]> tempData = new ArrayList<>();
        String[] headers = null;
        
        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            String line;
            boolean isFirstLine = true;
            
            while ((line = br.readLine()) != null) {
                String[] values = line.split(",");
                
                // Clean up values (remove quotes and trim whitespace)
                for (int i = 0; i < values.length; i++) {
                    values[i] = values[i].trim().replaceAll("^\"|\"$", "");
                }
                
                if (isFirstLine) {
                    headers = values;
                    isFirstLine = false;
                } else {
                    tempData.add(values);
                }
            }
        }
        
        // Store headers at ID = 0
        if (headers != null) {
            ArrayList<String> headersList = new ArrayList<>();
            for (String header : headers) {
                headersList.add(header);
            }
            rows.put(0, headersList);
        }
        
        // Store each row with ID starting from 1
        for (int i = 0; i < tempData.size(); i++) {
            ArrayList<String> rowData = new ArrayList<>();
            for (String value : tempData.get(i)) {
                rowData.add(value);
            }
            rows.put(i + 1, rowData);
        }
    }

    // Get headers from rows structure
    public ArrayList<String> getHeadersFromRows() {
        if (rows != null && rows.containsKey(0)) {
            return new ArrayList<>(rows.get(0));
        }
        return null;
    }

    // Get a specific row by ID
    public ArrayList<String> getRow(int id) {
        if (rows != null && rows.containsKey(id)) {
            return new ArrayList<>(rows.get(id));
        }
        return null;
    }

    // Get all row IDs (excluding headers at ID 0)
    public ArrayList<Integer> getRowIds() {
        if (rows != null) {
            ArrayList<Integer> ids = new ArrayList<>();
            for (Integer id : rows.keySet()) {
                if (id != 0) { // Exclude headers
                    ids.add(id);
                }
            }
            return ids;
        }
        return null;
    }

    // Get total number of data rows (excluding headers)
    public int getRowCount() {
        if (rows != null) {
            return rows.size() - 1; // Subtract 1 for headers
        }
        return 0;
    }

    // Get column data by column name from rows structure
    public ArrayList<String> getColumnFromRows(String columnName) {
        ArrayList<String> headers = getHeadersFromRows();
        if (headers == null || !headers.contains(columnName)) {
            System.out.println("Column " + columnName + " does not exist in the dataset.");
            return null;
        }
        
        int columnIndex = headers.indexOf(columnName);
        ArrayList<String> columnData = new ArrayList<>();
        
        for (Integer id : getRowIds()) {
            ArrayList<String> row = rows.get(id);
            if (row != null) {
                columnData.add(row.get(columnIndex));
            }
        }
        
        return columnData;
    }

    // Print data in row format
    public void printRowData() {
        if (rows != null && !rows.isEmpty()) {
            // Print headers
            ArrayList<String> headers = getHeadersFromRows();
            if (headers != null) {
                System.out.println("Headers (ID=0): " + String.join(", ", headers));
            }
            
            // Print data rows
            for (Integer id : getRowIds()) {
                ArrayList<String> row = getRow(id);
                if (row != null) {
                    System.out.println("Row " + id + ": " + String.join(", ", row));
                }
            }
        }
    }

    // Send the labels column I want to calc entropy for
    public double calcEntropy(ArrayList<String> targetCol){
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
        

        for(String key : freqMap.keySet()){
            double freq = freqMap.get(key);
            double p_c = freq / total;
            System.out.println("Key: " + key + ", Frequency: " 
                + freq + ", prob : " + p_c);
            entropy += p_c * Math.log(p_c) / Math.log(2);
        }

        entropy = -entropy; // Entropy is negative of the sum
        
        return entropy;
    }

    // Overloaded method to calculate entropy using column name from rows structure
    public double calcEntropy(String columnName) {
        ArrayList<String> targetCol = getColumnFromRows(columnName);
        return calcEntropy(targetCol);
    }    
    
    public double calcIG(ArrayList<String> targetCol, String attributeColName, HashMap<String, ArrayList<ArrayList<String>>> groupedRows) {
        
        double prevEnt = this.calcEntropy(targetCol);
        double entAfterSplit = 0.0;

        // Print the grouped attribute columns
        System.out.println("Grouped rows by attribute '" + attributeColName + "':");

        int indexOfSpecies = getHeadersFromRows().indexOf("Species");
        int totalRows = this.getRowCount();
        if(indexOfSpecies < 0) {
            System.out.println("Species column not found in headers!");
            return -1.0;
        }

        for (String attrValue : groupedRows.keySet()) {
            ArrayList<ArrayList<String>> rowsForValue = groupedRows.get(attrValue);
            if (rowsForValue == null || rowsForValue.isEmpty()) {
                continue; // Skip if no rows for this attribute value
            }

            ArrayList<String> speciesCol = new ArrayList<>();
            for(var row : rowsForValue ){
                speciesCol.add(row.get(indexOfSpecies)); // Extract species column for this attribute value
            }

            double entForValue = calcEntropy(speciesCol);


            // extract species column for this 

            System.out.println("Attribute Value: " + attrValue + " (Count: " + rowsForValue.size() + ") - Entropy: " + entForValue);
            entAfterSplit += ((double)rowsForValue.size() / totalRows)  * entForValue;
            // for (ArrayList<String> row : rowsForValue) {
            //     System.out.println("    Row: " + String.join(", ", row));
            // }
        }
    
        return prevEnt - entAfterSplit;
    }

    // Get data from rows structure
    public ArrayList<ArrayList<String>> getDataFromRows() {
        if (rows == null || rows.isEmpty()) {
            return null;
        }
        
        ArrayList<ArrayList<String>> data = new ArrayList<>();
        
        // Add all rows except headers (ID = 0)
        for (Integer id : getRowIds()) {
            ArrayList<String> row = getRow(id);
            if (row != null) {
                data.add(new ArrayList<>(row));
            }
        }
        
        return data;
    }

    public void printData() {
        if (rows != null && !rows.isEmpty()) {
            ArrayList<String> headers = getHeadersFromRows();
            System.out.println("Headers: " + String.join(", ", headers));
            
            ArrayList<ArrayList<String>> data = getDataFromRows();
            if (data != null) {
                for (ArrayList<String> row : data) {
                    System.out.println(String.join(", ", row));
                }
            }
        }
    }

        public void printColumn(String columnName) {
        ArrayList<String> columnData = getColumnFromRows(columnName);
        if (columnData != null) {
            System.out.println("Column: " + columnName);
            for (String value : columnData) {
                System.out.println(value);
            }
        } else {
            System.out.println("Column " + columnName + " does not exist.");
        }
    }

    // Convenience methods with cleaner names
    public ArrayList<String> getHeaders() {
        return getHeadersFromRows();
    }
    
    public ArrayList<ArrayList<String>> getData() {
        return getDataFromRows();
    }
    
    public ArrayList<String> getColumn(String columnName) {
        return getColumnFromRows(columnName);
    }

    // Method to group rows by attribute value
    public HashMap<String, ArrayList<ArrayList<String>>> groupRowsByAttribute(String attributeColName) {
        HashMap<String, ArrayList<ArrayList<String>>> splitAttrCol = new HashMap<>();

        // Check if the attribute column exists
        ArrayList<String> attributeCol = getColumnFromRows(attributeColName);
        if (attributeCol == null) {
            System.out.println("Column " + attributeColName + " not found!");
            return null;
        }

        // iterate over all rows and group rows by attribute value
        ArrayList<ArrayList<String>> allRows = getDataFromRows();
        ArrayList<String> headers = getHeaders();
        
        for(ArrayList<String> row : allRows) {
            int attrIdx = headers.indexOf(attributeColName);
            if (attrIdx >= 0 && attrIdx < row.size()) {
                String attrVal = row.get(attrIdx);
                splitAttrCol.putIfAbsent(attrVal, new ArrayList<ArrayList<String>>());

                ArrayList<ArrayList<String>> curr_rows = splitAttrCol.get(attrVal);
                curr_rows.add(row);  
                splitAttrCol.put(attrVal, curr_rows);  
            }
        }
        return splitAttrCol;
    }
}
