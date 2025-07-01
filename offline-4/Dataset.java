import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

public class Dataset {
    private HashMap<Integer, ArrayList<String>> rows;

    // Default constructor
    public Dataset() {
        this.rows = new HashMap<>();
    }

    // Constructor to create dataset from headers and data
    public Dataset(ArrayList<String> headers, ArrayList<ArrayList<String>> data) {
        this.rows = new HashMap<>();

        // Store headers at ID = 0
        if (headers != null) {
            this.rows.put(0, new ArrayList<>(headers));
        }

        // Store data rows starting from ID = 1
        if (data != null) {
            for (int i = 0; i < data.size(); i++) {
                this.rows.put(i + 1, new ArrayList<>(data.get(i)));
            }
        }
    }

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

        for (ArrayList<String> row : allRows) {
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

    public HashMap<String, ArrayList<ArrayList<String>>> groupRowsByAttribute(String attributeColName, double min,
            double max, int intervals) {
        HashMap<String, ArrayList<ArrayList<String>>> splitAttrCol = new HashMap<>();

        // Check if the attribute column exists
        ArrayList<String> attributeCol = getColumnFromRows(attributeColName);
        if (attributeCol == null) {
            System.out.println("Column " + attributeColName + " not found!");
            return null;
        }

        ArrayList<Double> ranges = new ArrayList<>();

        double stepSize = (max - min) / intervals;

        for (double i = min; i <= max; i += stepSize) {
            ranges.add(i);
        }

        for (var range : ranges) {
            splitAttrCol.putIfAbsent(String.valueOf(range), new ArrayList<ArrayList<String>>());
        }

        // iterate over all rows and group rows by attribute value
        ArrayList<ArrayList<String>> allRows = getDataFromRows();
        ArrayList<String> headers = getHeaders();

        for (ArrayList<String> row : allRows) {
            int attrIdx = headers.indexOf(attributeColName);
            if (attrIdx >= 0 && attrIdx < row.size()) {
                String attrVal = row.get(attrIdx);

                double initRange = min;
                for (double range = min + stepSize; range <= max; range += stepSize) {
                    if (Double.parseDouble(attrVal) >= initRange && Double.parseDouble(attrVal) < range) {
                        break;
                    }
                    initRange = range;
                }

                ArrayList<ArrayList<String>> curr_rows = splitAttrCol.get(String.valueOf(initRange));
                curr_rows.add(row);
                splitAttrCol.put(String.valueOf(initRange), curr_rows);
            }
        }
        return splitAttrCol;
    }

    // Function to count unique values from a column name
    public HashMap<String, Integer> countUniqueValues(String columnName) {
        HashMap<String, Integer> uniqueCount = new HashMap<>();

        // Get the column data
        ArrayList<String> columnData = getColumnFromRows(columnName);
        if (columnData == null) {
            System.out.println("Column " + columnName + " not found!");
            return null;
        }

        // Count occurrences of each unique value
        for (String value : columnData) {
            uniqueCount.put(value, uniqueCount.getOrDefault(value, 0) + 1);
        }

        return uniqueCount;
    }

    // Function to get the number of unique values in a column
    public int getUniqueValueCount(String columnName) {
        HashMap<String, Integer> uniqueValues = countUniqueValues(columnName);
        return uniqueValues != null ? uniqueValues.size() : 0;
    }

    // Function to print unique values and their counts for a column
    public void printUniqueValues(String columnName) {
        HashMap<String, Integer> uniqueValues = countUniqueValues(columnName);
        if (uniqueValues != null) {
            System.out.println("Unique values in column '" + columnName + "':");
            for (String value : uniqueValues.keySet()) {
                System.out.println("  " + value + ": " + uniqueValues.get(value));
            }
            System.out.println("Total unique values: " + uniqueValues.size());
        }
    }

    // Function to get the minimum value from a column (for numeric columns)
    public double getMinValue(String columnName) {
        ArrayList<String> columnData = getColumnFromRows(columnName);
        if (columnData == null || columnData.isEmpty()) {
            System.out.println("Column " + columnName + " not found or is empty!");
            return Double.NaN;
        }

        double min = Double.MAX_VALUE;
        boolean hasValidNumber = false;

        for (String value : columnData) {
            try {
                double numValue = Double.parseDouble(value);
                min = Math.min(min, numValue);
                hasValidNumber = true;
            } catch (NumberFormatException e) {
                // Skip non-numeric values
                continue;
            }
        }

        if (!hasValidNumber) {
            System.out.println("Column " + columnName + " contains no valid numeric values!");
            return Double.NaN;
        }

        return min;
    }

    // Function to get the maximum value from a column (for numeric columns)
    public double getMaxValue(String columnName) {
        ArrayList<String> columnData = getColumnFromRows(columnName);
        if (columnData == null || columnData.isEmpty()) {
            System.out.println("Column " + columnName + " not found or is empty!");
            return Double.NaN;
        }

        double max = Double.MIN_VALUE;
        boolean hasValidNumber = false;

        for (String value : columnData) {
            try {
                double numValue = Double.parseDouble(value);
                max = Math.max(max, numValue);
                hasValidNumber = true;
            } catch (NumberFormatException e) {
                // Skip non-numeric values
                continue;
            }
        }

        if (!hasValidNumber) {
            System.out.println("Column " + columnName + " contains no valid numeric values!");
            return Double.NaN;
        }

        return max;
    }

    // Function to get both min and max values from a column
    public double[] getMinMaxValues(String columnName) {
        ArrayList<String> columnData = getColumnFromRows(columnName);
        if (columnData == null || columnData.isEmpty()) {
            System.out.println("Column " + columnName + " not found or is empty!");
            return null;
        }

        double min = Double.MAX_VALUE;
        double max = Double.MIN_VALUE;
        boolean hasValidNumber = false;

        for (String value : columnData) {
            try {
                double numValue = Double.parseDouble(value);
                min = Math.min(min, numValue);
                max = Math.max(max, numValue);
                hasValidNumber = true;
            } catch (NumberFormatException e) {
                // Skip non-numeric values
                continue;
            }
        }

        if (!hasValidNumber) {
            System.out.println("Column " + columnName + " contains no valid numeric values!");
            return null;
        }

        return new double[] { min, max };
    }

    // Function to get the minimum value from a column (for string columns -
    // lexicographically)
    public String getMinStringValue(String columnName) {
        ArrayList<String> columnData = getColumnFromRows(columnName);
        if (columnData == null || columnData.isEmpty()) {
            System.out.println("Column " + columnName + " not found or is empty!");
            return null;
        }

        String min = columnData.get(0);
        for (String value : columnData) {
            if (value.compareTo(min) < 0) {
                min = value;
            }
        }

        return min;
    }

    // Function to get the maximum value from a column (for string columns -
    // lexicographically)
    public String getMaxStringValue(String columnName) {
        ArrayList<String> columnData = getColumnFromRows(columnName);
        if (columnData == null || columnData.isEmpty()) {
            System.out.println("Column " + columnName + " not found or is empty!");
            return null;
        }

        String max = columnData.get(0);
        for (String value : columnData) {
            if (value.compareTo(max) > 0) {
                max = value;
            }
        }

        return max;
    }

    // Function to print summary statistics for a numeric column
    public void printColumnStats(String columnName) {
        System.out.println("Statistics for column '" + columnName + "':");

        // Try numeric statistics first
        double min = getMinValue(columnName);
        double max = getMaxValue(columnName);

        if (!Double.isNaN(min) && !Double.isNaN(max)) {
            System.out.println("  Numeric Range: " + min + " to " + max);
            System.out.println("  Range Size: " + (max - min));
        } else {
            // If not numeric, show string range
            String minStr = getMinStringValue(columnName);
            String maxStr = getMaxStringValue(columnName);
            if (minStr != null && maxStr != null) {
                System.out.println("  String Range: '" + minStr + "' to '" + maxStr + "' (lexicographically)");
            }
        }

        int uniqueCount = getUniqueValueCount(columnName);
        System.out.println("  Unique Values: " + uniqueCount);

        ArrayList<String> columnData = getColumnFromRows(columnName);
        if (columnData != null) {
            System.out.println("  Total Records: " + columnData.size());
        }
    }
}
