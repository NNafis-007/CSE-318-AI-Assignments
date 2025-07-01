import java.util.ArrayList;

public class Main {

    public static void main(String[] args) {

        if(args.length < 2) {
            System.out.println("Usage : java Main <Criteria> <MaxDepth>");
            return;
        }
        try {
            // Create dataset and load data
            Dataset dataset = new Dataset();
            String filePath = "./Datasets/iris.csv";
            dataset.readCSV(filePath);

            // Create decision tree with dataset and target column
            int maxDepth = Integer.parseInt(args[1]); // Set max depth for the tree
            String criteria = args[0].toUpperCase();

            DecisionTree decisionTree = new DecisionTree(dataset, "Species", maxDepth, criteria);

            System.out.println("=== Dataset Information ===");
            System.out.println("Total rows: " + dataset.getRowCount());
            System.out.println("Headers: " + dataset.getHeaders());
            
            ArrayList<String> speciesFromRows = dataset.getColumn("Species");
            if (speciesFromRows != null) {
                // Test entropy calculation using row-based structure
                double entFromRows = decisionTree.calcEntropy();
                System.out.println("Overall entropy: " + entFromRows);
            }
            
            System.out.println("\n=== Building Decision Tree ===");
            // Build the decision tree
            decisionTree.buildTree();
            
            System.out.println("\n=== Tree Statistics ===");
            decisionTree.printTreeStats();
                        
            System.out.println("\n=== Testing Predictions ===");
            // Test prediction with some sample instances
            ArrayList<ArrayList<String>> testData = dataset.getData();
            if (testData.size() > 0) {
                // Test with first few instances
                for (int i = 0; i < Math.min(5, testData.size()); i++) {
                    ArrayList<String> instance = testData.get(i);
                    String prediction = decisionTree.predict(instance);
                    String actual = instance.get(dataset.getHeaders().indexOf("Species"));
                    
                    System.out.println("Instance " + (i+1) + ":");
                    System.out.println("  Features: " + instance.subList(0, instance.size()-1));
                    System.out.println("  Predicted: " + prediction);
                    System.out.println("  Actual: " + actual);
                    System.out.println("  Correct: " + prediction.equals(actual));
                    System.out.println();
                }
            }
            
            System.out.println("\n=== Testing Different Criteria ===");
            testAccuracy(decisionTree, dataset, criteria);

            // Test with IGR
            // System.out.println("\n--- Using Information Gain Ratio (IGR) ---");
            // DecisionTree treeIGR = new DecisionTree(dataset, "Species", maxDepth, "IGR");
            // treeIGR.buildTree();
            // treeIGR.printTreeStats();
            
            // Test with NWIG
            // System.out.println("\n--- Using Normalized Weighted Information Gain (NWIG) ---");
            // DecisionTree treeNWIG = new DecisionTree(dataset, "Species", maxDepth, "NWIG");
            // treeNWIG.buildTree();
            // treeNWIG.printTreeStats();
            
            // // Test accuracy comparison
            // System.out.println("\n=== Accuracy Comparison ===");
            // testAccuracy(decisionTree, dataset, "IG");
            // testAccuracy(treeIGR, dataset, "IGR");
            // testAccuracy(treeNWIG, dataset, "NWIG");
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    private static void testAccuracy(DecisionTree tree, Dataset dataset, String criteriaName) {
        ArrayList<ArrayList<String>> testData = dataset.getData();
        int correct = 0;
        int total = testData.size();
        
        for (ArrayList<String> instance : testData) {
            String prediction = tree.predict(instance);
            String actual = instance.get(dataset.getHeaders().indexOf("Species"));
            
            if (prediction != null && prediction.equals(actual)) {
                correct++;
            }
        }
        
        double accuracy = (double) correct / total * 100.0;
        System.out.println(criteriaName + " Accuracy: " + correct + "/" + total + " = " + String.format("%.2f", accuracy) + "%");
    }
}
