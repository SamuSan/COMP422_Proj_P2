package main;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.HashMap;



public class FeatureExtractor
{

    HashMap<String, Integer [][]> images = new HashMap<String, Integer [][]>();
    private static String[] files = {};
    private static String currDir = "";

    public FeatureExtractor( String[] dirs )
    {
        files = dirs;
    }


}
