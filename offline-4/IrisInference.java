import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Random;

public class IrisInference {
    
    public static void main(String[] args) {
        try {
            // Load the Iris dataset
            Dataset fullDataset = new Dataset();
            fullDataset.readCSV("Datasets/Iris.csv");
            
            System.out.println("Loaded Iris dataset successfully!");
            System.out.println("Total records: " + fullDataset.getRowCount());
            
            // Get headers and data
            ArrayList<String> headers = fullDataset.getHeaders();
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
            
            // Print class distribution in training set
            System.out.println("\nClass distribution in training set:");
            trainDataset.printUniqueValues("Species");
            
            System.out.println("\nClass distribution in test set:");
            testDataset.printUniqueValues("Species");
            
            // Train the decision tree
            String targetColumn = "Species";
            System.out.println("\n" + "=".repeat(50));
            System.out.println("TRAINING DECISION TREE");
            System.out.println("=".repeat(50));
            
            // Test different criteria
            String[] criteriaTypes = {"IG", "IGR", "NWIG"};
            
            for (String criteriaType : criteriaTypes) {
                System.out.println("\n" + "-".repeat(30));
                System.out.println("Training with criteria: " + criteriaType);
                System.out.println("-".repeat(30));
                
                DecisionTree tree = new DecisionTree(trainDataset, targetColumn, 4, criteriaType);
                tree.buildTree();
                
                // Print tree statistics
                tree.printTreeStats();
                
                // Test the tree on the test dataset
                System.out.println("\n" + "=".repeat(30));
                System.out.println("TESTING DECISION TREE");
                System.out.println("=".repeat(30));
                
                int correctPredictions = 0;
                int totalPredictions = 0;
                
                ArrayList<ArrayList<String>> testDataRows = testDataset.getData();
                
                System.out.println("\nPrediction Results:");
                System.out.println("Actual\t\tPredicted\tCorrect");
                System.out.println("-".repeat(40));
                
                for (ArrayList<String> testInstance : testDataRows) {
                    // Get the actual class (last column is Species)
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
                    
                    System.out.println(actualClass + "\t\t" + predictedClass + "\t\t" + (isCorrect ? "YES" : "NO"));
                }
                
                // Calculate and display accuracy
                double accuracy = (double) correctPredictions / totalPredictions;
                System.out.println("\n" + "=".repeat(40));
                System.out.println("ACCURACY RESULTS (" + criteriaType + ")");
                System.out.println("=".repeat(40));
                System.out.println("Correct predictions: " + correctPredictions + "/" + totalPredictions);
                System.out.println("Accuracy: " + String.format("%.2f%%", accuracy * 100));
                System.out.println("Error rate: " + String.format("%.2f%%", (1 - accuracy) * 100));
                
                
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
