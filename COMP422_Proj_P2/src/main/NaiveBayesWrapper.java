package main;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.Set;

import weka.classifiers.bayes.*;
import weka.core.Instances;

public class NaiveBayesWrapper extends BayesNet
{
    /**
     * 
     */
    private static final long serialVersionUID = -6955000230935131713L;
    NaiveBayes bn;
    private ArrayList<String> falseClassifications = new ArrayList<String>();
    private Instances trainingData;
    private Instances testData;
    private String[] opts = { "-D" };

    public NaiveBayesWrapper( String train, String test )
    {
        bn = new NaiveBayes();
        createTrainingSet( train );
        createTestSet( test );
        build();
        System.out.println( bn.toString() );

    }

    private void build()
    {
        try
        {
            bn.buildClassifier( trainingData );
        }
        catch ( Exception e )
        {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    private void createTestSet( String test )
    {
        try
        {
            testData = new Instances( new BufferedReader(
                    new InputStreamReader( ClassLoader
                            .getSystemResourceAsStream( test ) ) ) );
            testData.setClassIndex( testData.numAttributes() - 1 );
        }
        catch ( Exception e )
        {
            e.printStackTrace();
        }
    }

    private void createTrainingSet( String train )
    {
        try
        {
            trainingData = new Instances( new BufferedReader(
                    new InputStreamReader( ClassLoader
                            .getSystemResourceAsStream( train ) ) ) );
            trainingData.setClassIndex( trainingData.numAttributes() - 1 );
        }
        catch ( Exception e )
        {
            e.printStackTrace();
        }
    }

    public void classifyTest()
    {
        float correct = 0;
        float incorrect = 0;
        try
        {
            for ( int i = 0; i < testData.numInstances(); i++ )
            {
                double pred = bn.classifyInstance( testData.instance( i ) );
//                System.out.print( "ID: " + testData.instance( i ).value( 0 ) );
//                System.out.print( ", actual: " + testData.classAttribute().value( (int) testData.instance( i ).classValue() ) );
//                System.out.println( ", predicted: " + testData.classAttribute().value( (int) pred ) );
                if ( testData.classAttribute().value( (int) testData.instance( i ).classValue() ) == testData.classAttribute().value( (int) pred ) )
                {
                    correct++;
                }
                else
                {
                    falseClassifications.add( testData.classAttribute().value( (int) testData.instance( i ).classValue() ) );
                    incorrect++;
                }
            }
        }
        catch ( Exception e )
        {
            e.printStackTrace();
        }
        Collections.sort( falseClassifications );
        System.out.println( "Correct" + correct + " Incorrect : " + incorrect + " Total : " + ( correct + incorrect ) );
        System.out.println( "Accuracy: " + correct / ( correct + incorrect ) );
        System.out.println( "False classifications: " + incorrect / ( correct + incorrect ) );
        Set<String> uniquest = new HashSet<String>( falseClassifications );
        for ( String s : uniquest )
        {
            System.out.println( s + " : " + Collections.frequency( falseClassifications, s ) );
        }

    }

    public void classifyTrain()

    {
        float correct = 0;
        float incorrect = 0;
        try
        {
            for ( int i = 0; i < trainingData.numInstances(); i++ )
            {
                double pred = bn.classifyInstance( trainingData.instance( i ) );
                //                System.out.print( "ID: " + trainingData.instance( i ).value( 0 ) );
                //                System.out.print( ", actual: " + trainingData.classAttribute().value( (int) trainingData.instance( i ).classValue() ) );
                //                System.out.println( ", predicted: " + trainingData.classAttribute().value( (int) pred ) );
                if ( trainingData.classAttribute().value( (int) trainingData.instance( i ).classValue() ) == trainingData.classAttribute().value(
                        (int) pred ) )
                {
                    correct++;
                }
                else
                {
                    falseClassifications.add( trainingData.classAttribute().value( (int) trainingData.instance( i ).classValue() ) );
                    incorrect++;
                }
            }
        }
        catch ( Exception e )
        {
            e.printStackTrace();
        }
        Collections.sort( falseClassifications );
        System.out.println( "Correct" + correct + " Incorrect : " + incorrect + " Total : " + ( correct + incorrect ) );
        System.out.println( "Accuracy: " + correct / ( correct + incorrect ) );
        System.out.println( "False classifications: " + incorrect / ( correct + incorrect ) );
        Set<String> uniquest = new HashSet<String>( falseClassifications );
        for ( String s : uniquest )
        {
            System.out.println( s + " : " + Collections.frequency( falseClassifications, s ) );
        }

    }
    
    public Instances getTrainData(){
        return new Instances(trainingData);
    }
    
    public Instances getTestData(){
        return new Instances(testData);
    }
}
