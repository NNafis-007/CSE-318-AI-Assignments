import java.util.ArrayList;
import java.util.HashMap;

public class DecisionTree {
    private Dataset dataset;
    private String targetColName;
    private Node root;
    private int maxDepth;
    private String criteriaType; // "IG", "IGR", or "NWIG"
    
    // Constructor
    public DecisionTree(Dataset dataset, String targetColName) {
        this.dataset = dataset;
        this.targetColName = targetColName;
        this.maxDepth = 10; // Default max depth
        this.criteriaType = "IG"; // Default criteria
    }
    
    // Constructor with parameters
    public DecisionTree(Dataset dataset, String targetColName, int maxDepth, String criteriaType) {
        this.dataset = dataset;
        this.targetColName = targetColName;
        this.maxDepth = maxDepth;
        this.criteriaType = criteriaType;
    }
    
    // Get the target column name
    public String getTargetColName() {
        return targetColName;
    }
    
    // Get the root node
    public Node getRoot() {
        return root;
    }
    
    // Member function to calculate score based on criteria type
    private double calculateCriteria(String attributeColName, HashMap<String, ArrayList<ArrayList<String>>> groupedRows, Node node) {
        ArrayList<String> targetCol = getTargetColumnFromNodeData(node);
        
        switch (criteriaType.toUpperCase()) {
            case "IGR":
                return calcIGRForNode(attributeColName, groupedRows, targetCol, node);
            case "NWIG":
                return calcNWIGForNode(attributeColName, groupedRows, targetCol, node);
            case "IG":
            default:
                return calcIGForNode(attributeColName, groupedRows, targetCol, node);
        }
    }
    
    // Calculate entropy for the target column
    public double calcEntropy() {
        return Criteria.calcEntropy(dataset, targetColName);
    }
    
    
    // Build the decision tree
    public void buildTree() {
        System.out.println("Building decision tree with target column: " + targetColName);
        System.out.println("Max depth: " + maxDepth + ", Criteria: " + criteriaType);
        
        // Get all available attributes (excluding target column)
        ArrayList<String> availableAttributes = new ArrayList<>();
        ArrayList<String> headers = dataset.getHeaders();
        for (String header : headers) {
            if (!header.equals(targetColName) && !header.equals("Id")) {
                availableAttributes.add(header);
            }
        }
        
        // Get all data rows
        ArrayList<ArrayList<String>> allData = dataset.getData();
        
        // Create root node and start building tree
        root = new Node();
        root.setNodeData(allData);
        root.setDepth(0);
        
        // Start recursive tree building
        buildTreeRecursive(root, availableAttributes, 0);
        
        System.out.println("Decision tree built successfully!");
    }
    
    // Recursive method to build the tree
    private void buildTreeRecursive(Node currentNode, ArrayList<String> availableAttributes, int currentDepth) {
        // Check stopping conditions
        
        // 1. Check if max depth reached
        if (currentDepth >= maxDepth) {
            String mostFrequentClass = currentNode.getMostFrequentClass(dataset, targetColName);
            currentNode.setLeaf(true);
            currentNode.setTargetClass(mostFrequentClass);
            // System.out.println("Leaf node created at max depth " + currentDepth + " with class: " + mostFrequentClass);
            return;
        }
        
        // 2. Check if in a node, all data/instances have same target class)
        if (currentNode.isPure(dataset, targetColName)) {
            String pureClass = currentNode.getMostFrequentClass(dataset, targetColName);
            currentNode.setLeaf(true);
            currentNode.setTargetClass(pureClass);
            // System.out.println("Pure leaf node created at depth " + currentDepth + " with class: " + pureClass);
            return;
        }
        
        // 3. Check if no more attributes available
        if (availableAttributes.isEmpty()) {
            String mostFrequentClass = currentNode.getMostFrequentClass(dataset, targetColName);
            currentNode.setLeaf(true);
            currentNode.setTargetClass(mostFrequentClass);
            // System.out.println("Leaf node created (no more attributes) at depth " + currentDepth + " with class: " + mostFrequentClass);
            return;
        }
        
        // 4. Check if node has no data
        if (currentNode.getNodeData().isEmpty()) {
            String mostFrequentClass = "Unknown"; // or get from parent
            currentNode.setLeaf(true);
            currentNode.setTargetClass(mostFrequentClass);
            System.out.println("(ERROR) Empty leaf node created at depth " + currentDepth);
            return;
        }
        
        // 5. Check if node has very few instances (less than 2)
        if (currentNode.getNodeData().size() < 2) {
            String mostFrequentClass = currentNode.getMostFrequentClass(dataset, targetColName);
            currentNode.setLeaf(true);
            currentNode.setTargetClass(mostFrequentClass);
            // System.out.println("Leaf node created (insufficient data: " + currentNode.getNodeData().size() + ") at depth " + currentDepth + " with class: " + mostFrequentClass);
            return;
        }
        
        // Find the best attribute to split on
        String bestAttribute = findBestAttribute(availableAttributes, currentNode);
        
        if (bestAttribute == null) {
            String mostFrequentClass = currentNode.getMostFrequentClass(dataset, targetColName);
            currentNode.setLeaf(true);
            currentNode.setTargetClass(mostFrequentClass);
            // System.out.println("Leaf node created (no best attribute) at depth " + currentDepth + " with class: " + mostFrequentClass);
            return;
        }
        
        // Set the current node's attribute
        currentNode.setAttributeName(bestAttribute);
        
        // Check if attribute is continuous based on node data, not entire dataset
        boolean isContinuous = isContinuousInNodeData(currentNode, bestAttribute);
        currentNode.setContinuous(isContinuous);
        
        // Group the current node's data by the best attribute
        HashMap<String, ArrayList<ArrayList<String>>> groupedData;
        
        if (isContinuous) {
            // Handle continuous attributes with ranges
            double minVal = getMinValueFromNodeData(currentNode, bestAttribute);
            double maxVal = getMaxValueFromNodeData(currentNode, bestAttribute);
            
            // Check if min and max are the same (no variation)
            if (Math.abs(maxVal - minVal) < 1e-10) {
                String mostFrequentClass = currentNode.getMostFrequentClass(dataset, targetColName);
                currentNode.setLeaf(true);
                currentNode.setTargetClass(mostFrequentClass);
                // System.out.println("Leaf node created (continuous attribute same) at depth " + currentDepth + " with class: " + mostFrequentClass);
                return;
            }
            
            //int intervals = Math.max(2, Math.min(5, (int) Math.round((maxVal - minVal) * 3))); // Limit intervals

            int intervals = (int) Math.round((maxVal - minVal) * 3); // Limit intervals

            
            currentNode.setMinRange(minVal);
            currentNode.setMaxRange(maxVal);
            currentNode.setIntervals(intervals);
            
            groupedData = groupNodeDataByAttributeWithRanges(currentNode, bestAttribute, minVal, maxVal, intervals);
            // System.out.println("Splitting on continuous attribute '" + bestAttribute + "' with " + intervals + " intervals at depth " + currentDepth);
        } else {
            // Handle categorical attributes
            groupedData = groupNodeDataByAttribute(currentNode, bestAttribute);
            // System.out.println("Splitting on categorical attribute '" + bestAttribute + "' at depth " + currentDepth);
        }
        
        if (groupedData == null || groupedData.isEmpty()) {
            String mostFrequentClass = currentNode.getMostFrequentClass(dataset, targetColName);
            currentNode.setLeaf(true);
            currentNode.setTargetClass(mostFrequentClass);
            // System.out.println("Leaf node created (empty grouped data) at depth " + currentDepth + " with class: " + mostFrequentClass);
            return;
        }
        
        // Check if splitting actually creates meaningful groups
        boolean hasValidSplit = false;
        for (ArrayList<ArrayList<String>> group : groupedData.values()) {
            if (group != null && group.size() > 0 && group.size() < currentNode.getNodeData().size()) {
                hasValidSplit = true;
                break;
            }
        }
        
        if (!hasValidSplit) {
            String mostFrequentClass = currentNode.getMostFrequentClass(dataset, targetColName);
            currentNode.setLeaf(true);
            currentNode.setTargetClass(mostFrequentClass);
            // System.out.println("Leaf node created (no meaningful split) at depth " + currentDepth + " with class: " + mostFrequentClass);
            return;
        }
        
        // Create child nodes for each attribute value
        ArrayList<String> remainingAttributes = new ArrayList<>(availableAttributes);
        remainingAttributes.remove(bestAttribute); 
        
        // Create child nodes for each unique attribute value (or range for continous data) in grouped data
        for (String attributeValue : groupedData.keySet()) {
            ArrayList<ArrayList<String>> childData = groupedData.get(attributeValue);
            
            if (childData != null && !childData.isEmpty()) {
                Node childNode = new Node();
                childNode.setNodeData(childData);
                childNode.setDepth(currentDepth + 1);
                
                currentNode.addChild(attributeValue, childNode);
                
                // Recursively build subtree
                buildTreeRecursive(childNode, remainingAttributes, currentDepth + 1);
            }
        }
    }
    
    // Helper method to find best attribute for a specific node
    private String findBestAttribute(ArrayList<String> attributes, Node node) {
        String bestAttribute = null;
        double bestScore = -1.0;
        
        for (String attribute : attributes) {
            if (attribute.equals(targetColName) || attribute.equals("Id")) continue;
            
            // Create grouped data for this node
            HashMap<String, ArrayList<ArrayList<String>>> groupedData;
            boolean isContinuous = isContinuousInNodeData(node, attribute);
            
            if (isContinuous) {
                // Continuous attribute
                double minVal = getMinValueFromNodeData(node, attribute);
                double maxVal = getMaxValueFromNodeData(node, attribute);
                
                // Skip if no variation in values
                if (Math.abs(maxVal - minVal) < 1e-10) {
                    continue;
                }
                
                int intervals = Math.max(2, Math.min(5, (int) Math.round((maxVal - minVal) * 3)));
                groupedData = groupNodeDataByAttributeWithRanges(node, attribute, minVal, maxVal, intervals);
            } else {
                // Categorical attribute
                groupedData = groupNodeDataByAttribute(node, attribute);
            }
            
            if (groupedData != null && !groupedData.isEmpty()) {
                // Check if this split creates meaningful groups
                boolean hasValidSplit = false;
                for (ArrayList<ArrayList<String>> group : groupedData.values()) {
                    if (group != null && group.size() > 0 && group.size() < node.getNodeData().size()) {
                        hasValidSplit = true;
                        break;
                    }
                }
                
                if (hasValidSplit) {
                    double score = calculateCriteria(attribute, groupedData, node);
                    if (score > bestScore) {
                        bestScore = score;
                        bestAttribute = attribute;
                    }
                }
            }
        }
        
        return bestAttribute;
    }
    
    // Helper methods to calculate scores for node-specific data
    private double calcIGForNode(String attributeColName, HashMap<String, ArrayList<ArrayList<String>>> groupedRows, ArrayList<String> targetCol, Node node) {
        double prevEnt = Criteria.calcEntropy(targetCol);
        double entAfterSplit = 0.0;
        
        int targetIndex = dataset.getHeaders().indexOf(targetColName);
        int totalRows = node.getNodeData().size();
        
        for (String attrValue : groupedRows.keySet()) {
            ArrayList<ArrayList<String>> rowsForValue = groupedRows.get(attrValue);
            if (rowsForValue == null || rowsForValue.isEmpty()) {
                continue;
            }
            
            ArrayList<String> speciesCol = new ArrayList<>();
            for (ArrayList<String> row : rowsForValue) {
                if (targetIndex < row.size()) {
                    speciesCol.add(row.get(targetIndex));
                }
            }
            
            double entForValue = Criteria.calcEntropy(speciesCol);
            entAfterSplit += ((double) rowsForValue.size() / totalRows) * entForValue;
        }
        
        return prevEnt - entAfterSplit;
    }
    
    private double calcIGRForNode(String attributeColName, HashMap<String, ArrayList<ArrayList<String>>> groupedRows, ArrayList<String> targetCol, Node node) {
        double ig = calcIGForNode(attributeColName, groupedRows, targetCol, node);
        
        // Calculate IV
        double iv = 0.0;
        int totalRows = node.getNodeData().size();
        
        for (String attrValue : groupedRows.keySet()) {
            ArrayList<ArrayList<String>> rowsForValue = groupedRows.get(attrValue);
            if (rowsForValue == null || rowsForValue.isEmpty()) {
                continue;
            }
            
            double p_c = (double) rowsForValue.size() / totalRows;
            if (p_c > 0) {
                iv += p_c * Math.log(p_c) / Math.log(2);
            }
        }
        
        iv = -iv;
        
        if (iv == 0) {
            return 0.0;
        }
        
        return ig / iv;
    }
    
    private double calcNWIGForNode(String attributeColName, HashMap<String, ArrayList<ArrayList<String>>> groupedRows, ArrayList<String> targetCol, Node node) {
        double ig = calcIGForNode(attributeColName, groupedRows, targetCol, node);
        if (ig < 0) {
            return -1.0;
        }
        
        int k = groupedRows.size();
        int totalRows = node.getNodeData().size();
        
        double logNormalizer = Math.log(k + 1) / Math.log(2);
        if (logNormalizer == 0) {
            return 0.0;
        }
        
        double sizePenalty = 1.0 - ((double) (k - 1) / totalRows);
        return (ig / logNormalizer) * sizePenalty;
    }
    
    // HELPER METHODS
    
    // Get minimum value from node data for a specific attribute
    private double getMinValueFromNodeData(Node node, String attributeName) {
        ArrayList<String> headers = dataset.getHeaders();
        int attributeIndex = headers.indexOf(attributeName);
        if (attributeIndex < 0) {
            return Double.NaN;
        }
        
        double min = Double.MAX_VALUE;
        boolean hasValidNumber = false;
        
        for (ArrayList<String> row : node.getNodeData()) {
            if (attributeIndex < row.size()) {
                try {
                    double value = Double.parseDouble(row.get(attributeIndex));
                    min = Math.min(min, value);
                    hasValidNumber = true;
                } catch (NumberFormatException e) {
                    // Skip non-numeric values
                    break;
                }
            }
        }
        
        return hasValidNumber ? min : Double.NaN;
    }
    
    // Get maximum value from node data for a specific attribute
    private double getMaxValueFromNodeData(Node node, String attributeName) {
        ArrayList<String> headers = dataset.getHeaders();
        int attributeIndex = headers.indexOf(attributeName);
        if (attributeIndex < 0) {
            return Double.NaN;
        }
        
        double max = Double.MIN_VALUE;
        boolean hasValidNumber = false;
        
        for (ArrayList<String> row : node.getNodeData()) {
            if (attributeIndex < row.size()) {
                try {
                    double value = Double.parseDouble(row.get(attributeIndex));
                    max = Math.max(max, value);
                    hasValidNumber = true;
                } catch (NumberFormatException e) {
                    // Skip non-numeric values
                    break;
                }
            }
        }
        
        return hasValidNumber ? max : Double.NaN;
    }
    
    // Group node data by attribute (categorical)
    private HashMap<String, ArrayList<ArrayList<String>>> groupNodeDataByAttribute(Node node, String attributeName) {
        HashMap<String, ArrayList<ArrayList<String>>> groupedData = new HashMap<>();
        
        ArrayList<String> headers = dataset.getHeaders();
        int attributeIndex = headers.indexOf(attributeName);
        if (attributeIndex < 0) {
            return null;
        }
        
        for (ArrayList<String> row : node.getNodeData()) {
            if (attributeIndex < row.size()) {
                String attributeValue = row.get(attributeIndex);
                groupedData.putIfAbsent(attributeValue, new ArrayList<>());
                groupedData.get(attributeValue).add(row);
            }
        }
        
        return groupedData;
    }
    
    // Group node data by attribute with ranges (continuous)
    private HashMap<String, ArrayList<ArrayList<String>>> 
    groupNodeDataByAttributeWithRanges(Node node, String attributeName, double min, double max, int intervals) {
        HashMap<String, ArrayList<ArrayList<String>>> groupedData = new HashMap<>();
        
        ArrayList<String> headers = dataset.getHeaders();
        int attributeIndex = headers.indexOf(attributeName);
        if (attributeIndex < 0) {
            return null;
        }
        
        // Create ranges
        double stepSize = (max - min) / intervals;
        ArrayList<Double> ranges = new ArrayList<>();
        for (double i = min; i <= max; i += stepSize) {
            ranges.add(i);
            groupedData.put(String.valueOf(i), new ArrayList<>());
        }
        
        // Group data into ranges
        for (ArrayList<String> row : node.getNodeData()) {
            if (attributeIndex < row.size()) {
                try {
                    double value = Double.parseDouble(row.get(attributeIndex));
                    
                    double initRange = min;
                    for (double range = min + stepSize; range <= max; range += stepSize) {
                        if (value >= initRange && value < range) {
                            break;
                        }
                        initRange = range;
                    }
                    
                    String rangeKey = String.valueOf(initRange);
                    if (groupedData.containsKey(rangeKey)) {
                        groupedData.get(rangeKey).add(row);
                    }
                } catch (NumberFormatException e) {
                    // Skip non-numeric values
                }
            }
        }
        
        return groupedData;
    }
    
    // Get target column values from node data
    private ArrayList<String> getTargetColumnFromNodeData(Node node) {
        ArrayList<String> targetCol = new ArrayList<>();
        ArrayList<String> headers = dataset.getHeaders();
        int targetIndex = headers.indexOf(targetColName);
        
        if (targetIndex >= 0) {
            for (ArrayList<String> row : node.getNodeData()) {
                if (targetIndex < row.size()) {
                    targetCol.add(row.get(targetIndex));
                }
            }
        }
        
        return targetCol;
    }
    
    // Helper method to check if an attribute is continuous based on node data
    private boolean isContinuousInNodeData(Node node, String attributeName) {
        ArrayList<String> headers = dataset.getHeaders();
        int attributeIndex = headers.indexOf(attributeName);
        if (attributeIndex < 0) {
            return false;
        }
        
        // Count unique values in this node's data
        java.util.HashSet<String> uniqueValues = new java.util.HashSet<>();
        for (ArrayList<String> row : node.getNodeData()) {
            if (attributeIndex < row.size()) {
                uniqueValues.add(row.get(attributeIndex));
            }
        }
        
        // If more than 10 unique values or if all values are numeric, consider it continuous
        if (uniqueValues.size() > 5) {
            return true;
        }
        
        // Check if all values are numeric
        boolean allNumeric = true;
        for (String value : uniqueValues) {
            try {
                Double.parseDouble(value);
            } catch (NumberFormatException e) {
                allNumeric = false;
                break;
            }
        }
        
        return allNumeric;
    }
    
    // Predict the class for a given instance
    public String predict(ArrayList<String> instance) {
        if (root == null) {
            System.out.println("Decision tree has not been built yet. Please call buildTree() first.");
            return null;
        }
        
        return predictRecursive(root, instance);
    }
    
    // Recursive prediction method
    private String predictRecursive(Node currentNode, ArrayList<String> instance) {
        // If it's a leaf node, return the target class
        if (currentNode.isLeaf()) {
            return currentNode.getTargetClass();
        }
        
        // Get the attribute this node splits on
        String attributeName = currentNode.getAttributeName();
        ArrayList<String> headers = dataset.getHeaders();
        int attributeIndex = headers.indexOf(attributeName);
        
        if (attributeIndex < 0 || attributeIndex >= instance.size()) {
            // Attribute not found or instance doesn't have this attribute
            // Return the most frequent class in current node
            return currentNode.getMostFrequentClass(dataset, targetColName);
        }
        
        // Get the value of the decisive attribute for this instance
        String instanceValue = instance.get(attributeIndex); 

        
        // Handle continuous vs categorical attributes
        String childKey = null;
        
        if (currentNode.isContinuous()) {
            // For continuous attributes, find the appropriate range
            try {
                double value = Double.parseDouble(instanceValue);
                double min = currentNode.getMinRange();
                double max = currentNode.getMaxRange();
                int intervals = currentNode.getIntervals();
                double stepSize = (max - min) / intervals;
                
                double initRange = min;
                for (double range = min + stepSize; range <= max; range += stepSize) {
                    if (value >= initRange && value < range) {
                        break;
                    }
                    initRange = range;
                }
                
                childKey = String.valueOf(initRange);
            } catch (NumberFormatException e) {
                // If can't parse as number, return most frequent class
                return currentNode.getMostFrequentClass(dataset, targetColName);
            }
        } else {
            // For categorical attributes, use the value directly
            childKey = instanceValue;
        }
        
        // Get the child node for this attribute value
        Node childNode = currentNode.getChild(childKey);
        
        if (childNode == null) {
            // No child node for this attribute value
            // Return the most frequent class in current node
            return currentNode.getMostFrequentClass(dataset, targetColName);
        }
        
        // Recursively predict using the child node
        return predictRecursive(childNode, instance);
    }
    
    
    // Method to get tree statistics
    public void printTreeStats() {
        if (root == null) {
            System.out.println("Tree is empty.");
            return;
        }
        
        int[] stats = getTreeStatsRecursive(root);
        int totalNodes = stats[0];
        int leafNodes = stats[1];
        int maxDepth = stats[2];
        
        System.out.println("Tree Statistics:");
        System.out.println("  Total nodes: " + totalNodes);
        System.out.println("  Leaf nodes: " + leafNodes);
        System.out.println("  Internal nodes: " + (totalNodes - leafNodes));
        System.out.println("  Maximum depth: " + maxDepth);
        System.out.println("  Target column: " + targetColName);
        System.out.println("  Criteria used: " + criteriaType);
        System.out.println("  Max depth limit: " + maxDepth);
    }
    
    // Helper method to calculate tree statistics
    private int[] getTreeStatsRecursive(Node node) {
        if (node == null) {
            return new int[]{0, 0, 0}; // {totalNodes, leafNodes, maxDepth}
        }
        
        int totalNodes = 1;
        int leafNodes = node.isLeaf() ? 1 : 0;
        int maxDepth = node.getDepth();
        
        if (!node.isLeaf()) {
            for (Node child : node.getChildren().values()) {
                int[] childStats = getTreeStatsRecursive(child);
                totalNodes += childStats[0];
                leafNodes += childStats[1];
                maxDepth = Math.max(maxDepth, childStats[2]);
            }
        }
        
        return new int[]{totalNodes, leafNodes, maxDepth};
    }

    // Method to print the tree structure 
    //public void printTree() {
    //     if (root == null) {
    //         System.out.println("Tree is empty. Please build the tree first.");
    //         return;
    //     }
        
    //     System.out.println("Decision Tree Structure:");
    //     printTreeRecursive(root, "", true);
    // }
    
    // // Recursive method to print tree structure
    // private void printTreeRecursive(Node node, String prefix, boolean isLast) {
    //     if (node == null) return;
        
    //     // Print current node
    //     System.out.print(prefix);
    //     System.out.print(isLast ? "└── " : "├── ");
        
    //     if (node.isLeaf()) {
    //         System.out.println("Leaf: " + node.getTargetClass() + " (depth: " + node.getDepth() + ", data size: " + node.getNodeData().size() + ")");
    //     } else {
    //         String nodeInfo = node.getAttributeName();
    //         if (node.isContinuous()) {
    //             nodeInfo += " [continuous: " + node.getMinRange() + " to " + node.getMaxRange() + ", " + node.getIntervals() + " intervals]";
    //         }
    //         nodeInfo += " (depth: " + node.getDepth() + ", data size: " + node.getNodeData().size() + ")";
    //         System.out.println(nodeInfo);
    //     }
        
    //     // Print children
    //     if (!node.isLeaf() && node.hasChildren()) {
    //         ArrayList<String> childKeys = new ArrayList<>(node.getChildren().keySet());
    //         for (int i = 0; i < childKeys.size(); i++) {
    //             String childKey = childKeys.get(i);
    //             Node childNode = node.getChild(childKey);
    //             boolean isLastChild = (i == childKeys.size() - 1);
                
    //             String childPrefix = prefix + (isLast ? "    " : "│   ");
    //             System.out.print(childPrefix);
    //             System.out.print(isLastChild ? "└── " : "├── ");
    //             System.out.print("(" + childKey + ") --> ");
    //             System.out.println();
                
    //             printTreeRecursive(childNode, childPrefix + (isLastChild ? "    " : "│   "), true);
    //         }
    //     }
    // }
}
