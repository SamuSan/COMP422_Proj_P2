package main;

import weka.classifiers.Evaluation;
import weka.classifiers.evaluation.ThresholdCurve;




public class Main
{
    private static String src  = "main/images/";
    private static String testF  = src+"test/face/";
    private static String testNF  = src+"test/non-face/";
    private static String trainF  = src+"train/face/";
    private static String trainNF  = src+"train/non-face/";
    
    private static String  []  files = {testF, testNF, trainF, trainNF};
    public static void main( String[] args ) throws Exception
    {
        NaiveBayesWrapper nb = new  NaiveBayesWrapper( "imageRecogFeaturestrain.arff", "imageRecogFeaturestest.arff" );
        nb.classifyTrain();
        nb.classifyTest();
        ThresholdCurve th = new ThresholdCurve();
        int classIdx = 0;
        Evaluation eval = new Evaluation( nb.getTrainData() );
        
        

    }

    
    
    
    
    
    
    
    
}
