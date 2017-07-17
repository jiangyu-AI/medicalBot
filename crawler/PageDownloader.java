
import java.io.File;
import java.io.FileReader;
import java.io.BufferedReader;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.Queue;
import java.util.List;
import java.util.LinkedList;
import java.util.Set;
import java.util.HashSet;
import java.io.FileWriter;
import java.io.BufferedWriter;
import java.util.*;
import java.util.List;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
import java.io.Writer;
import java.io.OutputStreamWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.File;
import java.net.HttpURLConnection;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.FileOutputStream;
import java.net.URL;
import java.net.URLEncoder;
import java.util.Map;
import java.net.URLDecoder;
public class PageDownloader{

    //private static final int MAX_PAGE_NUM = 500;  // max respons page number, there are < 10000 items in any categroy
    private static final int SLEEP_TIME_MS = 3000; // 3000
    private static final String LIMIT_PARAM = "24";
    private static final String TIME_OUT = "3000";
    private static final String CONTENT_LENGTH = "40";


    // saveDir and tagId are passed from terminal input
    // change saveDir to be the folder where the output webpages to be stored
    //private static final String saveDir = "/home/jyu/data/baikeMedical/webpages/testdisease/";
    // change tagId to be the tagId which the source is
    //private static final String tagId = "75953"; // disease "68038"; // food

    private static String urlPost = "http://%s:8080/requests";
    private static final String REQUEST_URL = "http://baike.baidu.com/wikitag/api/getlemmas";
    private static final int BUFFER_SIZE = 4096;
    private static final String DOWNLOAD_ERROR_FILE = "/home/jyu/data/baike/downloadFailed.txt";
    private static final String DOWNLOAD_STATS_FILE = "/home/jyu/data/baike/downloadStats.txt";
    private static final String VISITED_FILE = "/home/jyu/data/baike/visited.txt";
    private static final String URLS_BFS_FILE = "/home/jyu/data/baike/urlsBfs.txt";
                       
    public PageDownloader(){}
    /**
     * Downloads a file from a URL
     * @param fileURL HTTP URL of the file to be downloaded
     * @param saveDir path of the directory to save the file
     * @throws IOException
     */
    private static int downloadFile(String fileURL, String saveDir)
            throws IOException {
	//System.out.println("downloadFile fileURL: " + fileURL);
	//System.out.println("downloadFile saveDir: " + saveDir);
        URL url = new URL(fileURL);
        HttpURLConnection httpConn = (HttpURLConnection) url.openConnection();
        int responseCode = httpConn.getResponseCode();
 
	boolean redirect = false;
	if(responseCode != HttpURLConnection.HTTP_OK){
		if(responseCode == HttpURLConnection.HTTP_MOVED_TEMP
		    || responseCode == HttpURLConnection.HTTP_MOVED_PERM
		        || responseCode == HttpURLConnection.HTTP_SEE_OTHER)
	        redirect = true;
	}
	if(redirect){
		// get redicret url from "location" header field
		String newUrl = httpConn.getHeaderField("Location");
		// open the new connection again
		System.out.println(newUrl);
		httpConn = (HttpURLConnection) new URL(newUrl).openConnection();

		System.out.println("Redirect to URL: " + newUrl);
	}
	responseCode = httpConn.getResponseCode();

	if(responseCode == 302){
		String newUrl = httpConn.getHeaderField("Location");
		httpConn = (HttpURLConnection) new URL(newUrl).openConnection();
		responseCode = httpConn.getResponseCode();
	}

        // always check HTTP response code first
        if (responseCode == HttpURLConnection.HTTP_OK) {
            String fileName = fileURL.substring(fileURL.lastIndexOf("/") + 1,
                        fileURL.length());
// opens input stream from the HTTP connection 
            InputStream inputStream = httpConn.getInputStream();
            String saveFilePath = saveDir + File.separator + fileName;
             
            // opens an output stream to save into file
            FileOutputStream outputStream = new FileOutputStream(saveFilePath);
 
            int bytesRead = -1;
            byte[] buffer = new byte[BUFFER_SIZE];
            while ((bytesRead = inputStream.read(buffer)) != -1) {
                outputStream.write(buffer, 0, bytesRead);
            }
            outputStream.close();
            inputStream.close();
            System.out.println("File downloaded");

	}else{
		String errorMessage = "No file to download. Server replied HTTP code: " + responseCode;
		//appendToFile(fileURL + ' ' + errorMessage + '\n', DOWNLOAD_ERROR_FILE);
		System.out.println(errorMessage);
		return 0;
        }
        httpConn.disconnect();
        return 1;
    }


    public static void main(String[] args){

	    String saveDir = "/home/jyu/data/baike/bfsNew";
	    String URLS_BFS = "/home/jyu/data/baike/urls_bfs_remaining.txt";
	    List<String> urls = new ArrayList<String>();
	    try{
		    File f = new File(URLS_BFS);
	            Scanner s = new Scanner(f);

		    while(s.hasNext()){
			    urls.add(s.next());
		    }
		    s.close();
	    }catch(IOException e){
		    System.out.println("can't find file: " + URLS_BFS);
            }

	   /* 
	    File folder = new File("/home/jyu/data/baike/bfsNew");
	    File[] listOfFiles = folder.listFiles();

	    Set<String> urlsDownloaded = new HashSet<>();
	    for(int i = 0; i < listOfFiles.length; i++){
		    if(listOfFiles[i].isFile()){
			    urlsDownloaded.add(listOfFiles[i].getName());
		    }
	    }
	    // save downloaded urlBfs pages to file
	    String downloadedUrlBfsFile = "/home/jyu/data/baike/bfsDownloaded.txt";
	    try{
		    FileWriter fw = new FileWriter(downloadedUrlBfsFile);
		    BufferedWriter out = new BufferedWriter(fw);
		    Iterator it = urlsDownloaded.iterator();
		    while(it.hasNext()){
			    out.write(it.next()+"\n");
		    }
		    out.close();
		    fw.close();
	    }catch(IOException e){
		    System.out.println("can't open file to write: " + downloadedUrlBfsFile);
	    }
	    */

            File directory = new File(saveDir);
	    if(!directory.exists()){
		    directory.mkdir();
	    }

	    for( String url : urls){

		   String urlFull =  "https://baike.baidu.com/item/" + url;
		   //if(urlsDownloaded.contains(url)) continue;
		    try{
			    downloadFile(urlFull, saveDir);
		    }catch(Exception e){
			    System.out.println("can't downloadFile: " + urlFull);
		    }
	    }
    }
}
