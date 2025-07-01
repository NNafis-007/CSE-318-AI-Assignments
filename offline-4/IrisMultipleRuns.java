import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Random;

public class IrisMultipleRuns {
    
    public static void main(String[] args) {
        try {
            // Load the Iris dataset
            Dataset fullDataset = new Dataset();
            fullDataset.readCSV("Datasets/Iris.csv");
            
            System.out.println("=".repeat(60));
            System.out.println("IRIS DATASET - MULTIPLE RUNS ANALYSIS");
            System.out.println("=".repeat(60));
            System.out.println("Loaded Iris dataset successfully!");
            System.out.println("Total records: " + fullDataset.getRowCount());
            
            // Setup file output
            FileWriter fw = new FileWriter("iris_multiple_runs_results.txt");
            BufferedWriter bw = new BufferedWriter(fw);
            PrintWriter out = new PrintWriter(bw);
            
            out.println("=".repeat(60));
            out.println("IRIS DATASET - MULTIPLE RUNS ANALYSIS");
            out.println("=".repeat(60));
            out.println("Total records: " + fullDataset.getRowCount());
            out.println("Number of runs: 10");
            out.println("Train/Test split: 80%/20%");
            out.println("Criteria tested: IG, IGR, NWIG");
            out.println("Max depths tested: 2, 3, 4");
            out.println("=".repeat(60));
            
            // Get headers and data
            ArrayList<String> headers = fullDataset.getHeaders();
            ArrayList<ArrayList<String>> allData = fullDataset.getData();
            String targetColumn = "Species";
            
            // Test configurations
            String[] criteriaTypes = {"IG", "IGR", "NWIG"};
            int[] depths = {2,3,4};
            int numRuns = 10;
            
            // Store results for analysis
            ArrayList<RunResult> allResults = new ArrayList<>();
            
            // Perform multiple runs with different random seeds
            for (int run = 1; run <= numRuns; run++) {
                // Create shuffled indices with different seed for each run
                ArrayList<Integer> indices = new ArrayList<>();
                for (int i = 0; i < allData.size(); i++) {
                    indices.add(i);
                }
                
                Random random = new Random(run); // Different seed for each run
                Collections.shuffle(indices, random);
                
                // Split data (80% train, 20% test)
                int totalSize = allData.size();
                int trainSize = (int) (totalSize * 0.8);
                
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
                
                Dataset trainDataset = new Dataset(headers, trainData);
                Dataset testDataset = new Dataset(headers, testData);
                
                
                // Test each configuration
                for (String criteriaType : criteriaTypes) {
                    for (int maxDepth : depths) {                        
                        // Train decision tree
                        long trainStart = System.currentTimeMillis();
                        DecisionTree tree = new DecisionTree(trainDataset, targetColumn, maxDepth, criteriaType);
                        tree.buildTree();
                        long trainEnd = System.currentTimeMillis();
                        
                        // Test the tree
                        int correctPredictions = 0;
                        int totalPredictions = 0;
                        
                        long testStart = System.currentTimeMillis();
                        ArrayList<ArrayList<String>> testDataRows = testDataset.getData();
                        
                        for (ArrayList<String> testInstance : testDataRows) {
                            String actualClass = testInstance.get(testInstance.size() - 1);
                            
                            ArrayList<String> instanceForPrediction = new ArrayList<>();
                            for (int i = 0; i < testInstance.size() - 1; i++) {
                                instanceForPrediction.add(testInstance.get(i));
                            }
                            
                            String predictedClass = tree.predict(instanceForPrediction);
                            
                            if (actualClass.equals(predictedClass)) {
                                correctPredictions++;
                            }
                            totalPredictions++;
                        }
                        long testEnd = System.currentTimeMillis();
                        
                        double accuracy = (double) correctPredictions / totalPredictions;
                        
                        // Store result
                        RunResult result = new RunResult(run, criteriaType, maxDepth, accuracy, 
                                                       trainEnd - trainStart, testEnd - testStart);
                        allResults.add(result);
                        
                    }
                }
            }
            
            // Print summary statistics
            printSummaryStatistics(allResults, out);
            printSummaryStatistics(allResults, null); // Print to console
            
            out.close();
            bw.close();
            fw.close();
            
            System.out.println("\n" + "=".repeat(60));
            System.out.println("All runs completed! Results saved to iris_multiple_runs_results.txt");
            System.out.println("=".repeat(60));
            
        } catch (IOException e) {
            System.err.println("Error reading the dataset: " + e.getMessage());
            e.printStackTrace();
        } catch (Exception e) {
            System.err.println("An error occurred: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    private static void printSummaryStatistics(ArrayList<RunResult> results, PrintWriter out) {
        if (out != null) {
            out.println("\n" + "=".repeat(60));
            out.println("SUMMARY STATISTICS (10 RUNS)");
            out.println("=".repeat(60));
        } else {
            System.out.println("\n" + "=".repeat(60));
            System.out.println("SUMMARY STATISTICS (10 RUNS)");
            System.out.println("=".repeat(60));
        }
        
        String[] criteriaTypes = {"IG", "IGR", "NWIG"};
        int[] depths = {2,3,4};
        
        for (String criteria : criteriaTypes) {
            for (int depth : depths) {
                ArrayList<Double> accuracies = new ArrayList<>();
                ArrayList<Long> trainTimes = new ArrayList<>();
                ArrayList<Long> testTimes = new ArrayList<>();
                
                for (RunResult result : results) {
                    if (result.criteria.equals(criteria) && result.maxDepth == depth) {
                        accuracies.add(result.accuracy);
                        trainTimes.add(result.trainTime);
                        testTimes.add(result.testTime);
                    }
                }
                
                if (!accuracies.isEmpty()) {
                    double avgAccuracy = accuracies.stream().mapToDouble(a -> a).average().orElse(0.0);
                    double minAccuracy = accuracies.stream().mapToDouble(a -> a).min().orElse(0.0);
                    double maxAccuracy = accuracies.stream().mapToDouble(a -> a).max().orElse(0.0);
                    double avgTrainTime = trainTimes.stream().mapToLong(t -> t).average().orElse(0.0);
                    double avgTestTime = testTimes.stream().mapToLong(t -> t).average().orElse(0.0);
                    
                    String summary = String.format("\n%s (Depth=%d):\n" +
                                                 "  Average Accuracy: %.2f%%\n" +
                                                 "  Min Accuracy: %.2f%%\n" +
                                                 "  Max Accuracy: %.2f%%\n" +
                                                 "  Avg Train Time: %.1f ms\n" +
                                                 "  Avg Test Time: %.1f ms",
                                                 criteria, depth, avgAccuracy * 100, 
                                                 minAccuracy * 100, maxAccuracy * 100,
                                                 avgTrainTime, avgTestTime);
                    
                    if (out != null) {
                        out.println(summary);
                    } else {
                        System.out.println(summary);
                    }
                }
            }
        }
    }
    
    static class RunResult {
        int run;
        String criteria;
        int maxDepth;
        double accuracy;
        long trainTime;
        long testTime;
        
        RunResult(int run, String criteria, int maxDepth, double accuracy, long trainTime, long testTime) {
            this.run = run;
            this.criteria = criteria;
            this.maxDepth = maxDepth;
            this.accuracy = accuracy;
            this.trainTime = trainTime;
            this.testTime = testTime;
        }
    }
}
