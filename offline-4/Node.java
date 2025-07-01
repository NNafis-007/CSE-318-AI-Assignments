import java.util.ArrayList;
import java.util.HashMap;

public class Node {
    // Node attributes
    private String attributeName;           // The attribute this node splits on
    private String attributeValue;          // The value of the parent's attribute that led to this node
    private String targetClass;             // The predicted class (for leaf nodes)
    private boolean isLeaf;                 // Whether this is a leaf node
    private boolean isContinuous;           // Whether the attribute is continuous (uses ranges)
    private double minRange;                // Minimum value for continuous attribute range
    private double maxRange;                // Maximum value for continuous attribute range
    private int intervals;                  // Number of intervals for continuous attributes
    
    // Tree structure
    private Node parent;                    // Parent node
    private HashMap<String, Node> children; // Child nodes mapped by attribute values
    
    // Data at this node
    private ArrayList<ArrayList<String>> nodeData; // Data rows at this node
    private int depth;                      // Depth of this node in the tree
    
    // Constructors
    public Node() {
        this.children = new HashMap<>();
        this.isLeaf = false;
        this.isContinuous = false;
        this.depth = 0;
        this.nodeData = new ArrayList<>();
    }
    
    // Getters and Setters
    public String getAttributeName() {
        return attributeName;
    }
    
    public void setAttributeName(String attributeName) {
        this.attributeName = attributeName;
    }
    
    public String getAttributeValue() {
        return attributeValue;
    }
    
    public void setAttributeValue(String attributeValue) {
        this.attributeValue = attributeValue;
    }
    
    public String getTargetClass() {
        return targetClass;
    }
    
    public void setTargetClass(String targetClass) {
        this.targetClass = targetClass;
    }
    
    public boolean isLeaf() {
        return isLeaf;
    }
    
    public void setLeaf(boolean isLeaf) {
        this.isLeaf = isLeaf;
    }
    
    public boolean isContinuous() {
        return isContinuous;
    }
    
    public void setContinuous(boolean isContinuous) {
        this.isContinuous = isContinuous;
    }
    
    public double getMinRange() {
        return minRange;
    }
    
    public void setMinRange(double minRange) {
        this.minRange = minRange;
    }
    
    public double getMaxRange() {
        return maxRange;
    }
    
    public void setMaxRange(double maxRange) {
        this.maxRange = maxRange;
    }
    
    public int getIntervals() {
        return intervals;
    }
    
    public void setIntervals(int intervals) {
        this.intervals = intervals;
    }
    
    public Node getParent() {
        return parent;
    }
    
    public void setParent(Node parent) {
        this.parent = parent;
    }
    
    public HashMap<String, Node> getChildren() {
        return children;
    }
    
    public void setChildren(HashMap<String, Node> children) {
        this.children = children;
    }
    
    public void addChild(String attributeValue, Node child) {
        this.children.put(attributeValue, child);
        child.setParent(this);
        child.setAttributeValue(attributeValue);
        child.setDepth(this.depth + 1);
    }
    
    public Node getChild(String attributeValue) {
        return children.get(attributeValue);
    }
    
    public ArrayList<ArrayList<String>> getNodeData() {
        return nodeData;
    }
    
    public void setNodeData(ArrayList<ArrayList<String>> nodeData) {
        this.nodeData = nodeData;
    }
    
    public int getDepth() {
        return depth;
    }
    
    public void setDepth(int depth) {
        this.depth = depth;
    }
    
    // Helper methods
    public boolean hasChildren() {
        return !children.isEmpty();
    }
    
    public int getChildrenCount() {
        return children.size();
    }
    
    // Method to get the most frequent target class in the current node's data
    public String getMostFrequentClass(Dataset dataset, String targetColName) {
        if (nodeData == null || nodeData.isEmpty()) {
            return null;
        }
        
        // Get the target column index
        ArrayList<String> headers = dataset.getHeaders();
        int targetIndex = headers.indexOf(targetColName);
        if (targetIndex < 0) {
            return null;
        }
        
        // Count the frequency of each target class
        HashMap<String, Integer> classCount = new HashMap<>();
        for (ArrayList<String> row : nodeData) {
            if (targetIndex < row.size()) {
                String targetValue = row.get(targetIndex);
                classCount.put(targetValue, classCount.getOrDefault(targetValue, 0) + 1);
            }
        }
        
        // Find the most frequent class
        String mostFrequentClass = null;
        int maxCount = 0;
        for (String className : classCount.keySet()) {
            int count = classCount.get(className);
            if (count > maxCount) {
                maxCount = count;
                mostFrequentClass = className;
            }
        }
        
        return mostFrequentClass;
    }
    
    // Method to check if all data in this node belongs to the same class
    public boolean isPure(Dataset dataset, String targetColName) {
        if (nodeData == null || nodeData.isEmpty()) {
            return true;
        }
        
        ArrayList<String> headers = dataset.getHeaders();
        int targetIndex = headers.indexOf(targetColName);
        if (targetIndex < 0) {
            System.out.println("ERROR IN isPure: Target column not found: " + targetColName);
            return false;
        }
        
        String firstClass = null;
        for (ArrayList<String> row : nodeData) {
            if (targetIndex < row.size()) {
                String targetValue = row.get(targetIndex);
                if (firstClass == null) {
                    firstClass = targetValue;
                } else if (!firstClass.equals(targetValue)) {
                    return false;
                }
            }
        }
        
        return true;
    }
    
    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("Node{");
        sb.append("depth=").append(depth);
        sb.append(", isLeaf=").append(isLeaf);
        if (isLeaf) {
            sb.append(", targetClass='").append(targetClass).append("'");
        } else {
            sb.append(", attributeName='").append(attributeName).append("'");
            sb.append(", isContinuous=").append(isContinuous);
            if (isContinuous) {
                sb.append(", range=[").append(minRange).append(",").append(maxRange).append("]");
                sb.append(", intervals=").append(intervals);
            }
        }
        sb.append(", childrenCount=").append(children.size());
        sb.append(", dataSize=").append(nodeData != null ? nodeData.size() : 0);
        sb.append("}");
        return sb.toString();
    }
}
