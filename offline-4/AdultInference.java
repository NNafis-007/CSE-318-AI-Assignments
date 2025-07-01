import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Random;

public class AdultInference {
    
    public static void main(String[] args) {
        if(args.length < 2) {
            System.out.println("Usage : java AdultInference <Criteria> <MaxDepth>");
            return;
        }
        
        try {
            // Parse command line arguments
            String criteria = args[0].toUpperCase();
            int argDepth = Integer.parseInt(args[1]);
            int maxDepth = argDepth > 0 ? argDepth : Integer.MAX_VALUE; // Use max depth if provided, else no limit
            
            System.out.println("Criteria: " + criteria);
            System.out.println("Max Depth: " + maxDepth);
            
            // Load the Adult dataset
            Dataset fullDataset = new Dataset();
            fullDataset.readCSV("Datasets/adult.data");
            
            System.out.println("Loaded Adult dataset successfully!");
            System.out.println("Total records: " + fullDataset.getRowCount());
            
            // Print dataset headers to understand structure
            ArrayList<String> headers = fullDataset.getHeaders();
            System.out.println("Dataset headers: " + headers);
            
            // Get headers and data
            ArrayList<ArrayList<String>> allData = fullDataset.getData();

            // Create a shuffled list of indices for random splitting
            ArrayList<Integer> indices = new ArrayList<>();
            for (int i = 0; i < allData.size(); i++) {
                indices.add(i);
            }
            
            // Shuffle the indices for randomness
            Random random = new Random(42); // Set seed for reproducibility
            Collections.shuffle(indices, random);
            
            // Calculate split sizes (80% train, 20% test)
            int totalSize = allData.size();
            int trainSize = (int) (totalSize * 0.8);
            int testSize = totalSize - trainSize;
            
            System.out.println("Train size: " + trainSize + " (" + (trainSize * 100.0 / totalSize) + "%)");
            System.out.println("Test size: " + testSize + " (" + (testSize * 100.0 / totalSize) + "%)");
            
            // Split the data
            ArrayList<ArrayList<String>> trainData = new ArrayList<>();
            ArrayList<ArrayList<String>> testData = new ArrayList<>();
            
            for (int i = 0; i < totalSize; i++) {
                int dataIndex = indices.get(i);
                ArrayList<String> row = allData.get(dataIndex);
                
                if (i < trainSize) {
                    trainData.add(new ArrayList<>(row));
                } else {
                    testData.add(new ArrayList<>(row));
                }
            }
            
            // Create train and test datasets
            Dataset trainDataset = new Dataset(headers, trainData);
            Dataset testDataset = new Dataset(headers, testData);
            
            System.out.println("\nDataset split completed!");
            System.out.println("Training dataset size: " + trainDataset.getRowCount());
            System.out.println("Testing dataset size: " + testDataset.getRowCount());
            
            // Print class distribution in training and test sets manually
            String targetColumn = "SalaryRange";
            int targetColumnIndex = headers.indexOf(targetColumn);
            
            System.out.println("\nClass distribution in training set:");
            java.util.HashMap<String, Integer> trainClassCount = new java.util.HashMap<>();
            for (ArrayList<String> row : trainData) {
                if (targetColumnIndex < row.size()) {
                    String className = row.get(targetColumnIndex);
                    trainClassCount.put(className, trainClassCount.getOrDefault(className, 0) + 1);
                }
            }
            for (String className : trainClassCount.keySet()) {
                System.out.println("  " + className + ": " + trainClassCount.get(className));
            }
            System.out.println("Total unique values: " + trainClassCount.size());
            
            System.out.println("\nClass distribution in test set:");
            java.util.HashMap<String, Integer> testClassCount = new java.util.HashMap<>();
            for (ArrayList<String> row : testData) {
                if (targetColumnIndex < row.size()) {
                    String className = row.get(targetColumnIndex);
                    testClassCount.put(className, testClassCount.getOrDefault(className, 0) + 1);
                }
            }
            for (String className : testClassCount.keySet()) {
                System.out.println("  " + className + ": " + testClassCount.get(className));
            }
            System.out.println("Total unique values: " + testClassCount.size());
            
            // Train the decision tree
            System.out.println("\n" + "=".repeat(50));
            System.out.println("TRAINING DECISION TREE");
            System.out.println("=".repeat(50));
            
            // Test different criteria
            String[] criteriaTypes = {criteria}; // Use only the provided criteria
            int[] maxDepths = {maxDepth}; // Use only the provided max depth
            
            for (String criteriaType : criteriaTypes) {
                for(int depth : maxDepths) {
                    System.out.println("\n" + "-".repeat(30));
                    System.out.println("Training with criteria: " + criteriaType + ", Max Depth: " + depth);
                    System.out.println("-".repeat(30));
                    
                    // Use smaller max depth for adult dataset due to larger size
                    DecisionTree tree = new DecisionTree(trainDataset, targetColumn, depth, criteriaType);
                    
                    // Measure training time
                    long startTime = System.currentTimeMillis();
                    tree.buildTree();
                    long endTime = System.currentTimeMillis();
                    
                    System.out.println("Training time: " + (endTime - startTime) + " ms");
                    
                    // Print tree statistics
                    tree.printTreeStats();
                    
                    // Test the tree on the test dataset
                    System.out.println("\n" + "=".repeat(10));
                    System.out.println("TESTING DECISION TREE");
                    System.out.println("=".repeat(10));
                    
                    int correctPredictions = 0;
                    int totalPredictions = 0;
                    
                    ArrayList<ArrayList<String>> testDataRows = testDataset.getData();
                    
                    System.out.println("\nTesting on " + testDataRows.size() + " instances...");
                    
                    // For large dataset, we'll just show accuracy without individual predictions
                    long testStartTime = System.currentTimeMillis();
                    
                    for (ArrayList<String> testInstance : testDataRows) {
                        // Get the actual class (last column is SalaryRange)
                        String actualClass = testInstance.get(testInstance.size() - 1);
                        
                        // Create instance without the target class for prediction
                        ArrayList<String> instanceForPrediction = new ArrayList<>();
                        for (int i = 0; i < testInstance.size() - 1; i++) {
                            instanceForPrediction.add(testInstance.get(i));
                        }
                        
                        // Make prediction
                        String predictedClass = tree.predict(instanceForPrediction);
                        
                        boolean isCorrect = actualClass.equals(predictedClass);
                        if (isCorrect) {
                            correctPredictions++;
                        }
                        totalPredictions++;
                    }
                    
                    long testEndTime = System.currentTimeMillis();
                    System.out.println("Testing time: " + (testEndTime - testStartTime) + " ms");
                    
                    // Calculate and display accuracy
                    double accuracy = (double) correctPredictions / totalPredictions;
                    System.out.println("\n" + "=".repeat(40));
                    System.out.println("ACCURACY RESULTS (" + criteriaType + ")");
                    System.out.println("=".repeat(40));
                    System.out.println("Correct predictions: " + correctPredictions + "/" + totalPredictions);
                    System.out.println("Accuracy: " + String.format("%.2f%%", accuracy * 100));
                    System.out.println("Error rate: " + String.format("%.2f%%", (1 - accuracy) * 100));
                    

                }
                System.out.println("\n" + "=".repeat(50));
            }            
        } catch (IOException e) {
            System.err.println("Error reading the dataset: " + e.getMessage());
            e.printStackTrace();
        } catch (Exception e) {
            System.err.println("An error occurred: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
