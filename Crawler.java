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

/**
 * The class is written to download web pages from baike medical related categories 
 * June 2017
 * e.g. http://baike.baidu.com/wikitag/taglist?tagId=75954
 * Change saveDir, and tagId etc to download pages from different categories
 * usage:
 * MAX_PAGE_NUM: use 1 for test, use 500 for crawling all pages
 * java Crawler tagId saveDir MAX_PAGE_NUM
 */

public class Crawler{

    //private static final int MAX_PAGE_NUM = 500;  // max respons page number, there are < 10000 items in any categroy
    private static final int SLEEP_TIME_MS = 0; // 3000
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
    private static final String DOWNLOAD_ERROR_FILE = "downloadFailed.txt";
    private static final String DOWNLOAD_STATS_FILE = "downloadStats.txt";
                       
    public Crawler(){}
    public Crawler(String url){
        setUrlPost(url);
    }
 
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
 
	// 
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
/*
            String disposition = httpConn.getHeaderField("Content-Disposition");
            //String contentType = httpConn.getContentType();
            //int contentLength = httpConn.getContentLength();
 
            if (disposition != null) {
                // extracts file name from header field
                int index = disposition.indexOf("filename=");
                if (index > 0) {
                    fileName = disposition.substring(index + 10,
                            disposition.length() - 1);
                }
            } else {
                // extracts file name from URL
                fileName = fileURL.substring(fileURL.lastIndexOf("/") + 1,
                        fileURL.length());
            }
*/

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
		appendToFile(fileURL + ' ' + errorMessage + '\n', DOWNLOAD_ERROR_FILE);
		System.out.println(errorMessage);
		return 0;
        }
        httpConn.disconnect();
        return 1;
    }


    private void setUrlPost(String urlPost) {
        this.urlPost = urlPost;
    }

    private void setMsgToSend(String msg) {
        this.msgToSend = msg;
    }
    String msgToSend = "";

    private String sendPost(String msg) {
        String res = "";
        msgToSend = msg;
        try {
            res = sendPost();
        } catch (Exception e) {
            //LOGGER.error("error post data " + msg + " to " + urlPost, e);
        }
        return res;
    }
    // HTTP POST request
    private String sendPost() throws Exception {
        if (urlPost == null) {
            //LOGGER.info("skip post " + msgToSend);
        }
        //LOGGER.info("sending " + msgToSend + " to " + urlPost);

        URL obj = new URL(urlPost);
        HttpURLConnection con = (HttpURLConnection) obj.openConnection();

        //add reuqest header
        con.setRequestMethod("POST");
        con.setRequestProperty("User-Agent", "");
        //con.setRequestProperty("Accept-Language", "en-US,en;q=0.5");

        // Send post request
        con.setDoOutput(true);
        con.setRequestProperty("encoding", "utf-8");
        DataOutputStream wr = new DataOutputStream(con.getOutputStream());

        //wr.writeBytes(msgToSend);  // luanma
        wr.write(msgToSend.getBytes());
        wr.flush();
        wr.close();

        int responseCode = con.getResponseCode();
        //LOGGER.debug("Sending 'POST' request to URL : " + urlPost);
        String log = msgToSend;
        //if (msgToSend.length() > DataKey.max_log_size) {
        //    log = msgToSend.substring(0, DataKey.max_log_size) + "...";
        //}
        //LOGGER.debug("Post parameters : " + log);
        //LOGGER.debug("Response Code : " + responseCode);

        BufferedReader in = new BufferedReader(
                new InputStreamReader(con.getInputStream()));
        String inputLine;
        StringBuffer response = new StringBuffer();

        while ((inputLine = in.readLine()) != null) {
            response.append(inputLine);
        }
        in.close();

        //print result
        String res = response.toString();
        return res;
    }

    public static String sendGet(String url) throws Exception {
        // HTTP GET request\     String urlGet = "http://%s:8080/requests?bizuin=";
        URL obj = new URL(url);
        HttpURLConnection con = (HttpURLConnection) obj.openConnection();

        // optional default is GET
        con.setRequestMethod("GET");

        //add request header
        con.setRequestProperty("User-Agent", "");

        int responseCode = con.getResponseCode();
        //LOGGER.info("\nSending 'GET' request to URL : " + url);
        //LOGGER.info("Response Code : " + responseCode);

        BufferedReader in = new BufferedReader(
                new InputStreamReader(con.getInputStream()));
        String inputLine;
        StringBuffer response = new StringBuffer();

        while ((inputLine = in.readLine()) != null) {
            response.append(inputLine);
        }
        in.close();

        //print result
        //LOGGER.info(response.toString());
        return response.toString();
    }

    private static void writeToFile(List<String> strs, String filePath){
        try(PrintWriter printWriter = new PrintWriter(filePath)){
            for(String s : strs){
                printWriter.println(s);
            }
        }catch(Exception e){
            System.out.printf("Can't write: %s!/n", filePath);
        }
    }

   private static List<String> getUrls(List<String> responses){
        // process urls and write id name map file
        List<String> urls = new LinkedList<String>();
        for(String res : responses){
            for(int i = 0; i < res.length()-4; i++){
              if(res.substring(i, i+4).equals("http")){
                   int j = i+4;
                   while(res.charAt(j) != '"'){
                       j++;
                   }
                   String urlRaw = res.substring(i, j);
                   StringBuilder urlBuilder = new StringBuilder();
                   for(char c : urlRaw.toCharArray()){
                       if(c != '\\'){
                           urlBuilder.append(c);
                        }
                   }
		   String url = urlBuilder.toString();
                   if(url != null && !url.isEmpty() && url.length() > 12 &&
				   url.substring(0, 12).equals("http://baike")){
			   urls.add(url);
		   }
              }
            }
        }
        return urls;
   }

   private static List<String> getNameIds(List<String> urls){
        List<String> nameIds = new LinkedList<String>();
       for(String url : urls){
           String[] urlSplit = url.split("/");
           if(urlSplit.length < 6){
               //System.out.println("getNameIds: " + url);
           }else{
               String id = urlSplit[5]; 
               try{
                   String name = URLDecoder.decode(urlSplit[4], "UTF-8"); 
                   //System.out.println(name+" "+id); 
                   nameIds.add(name + " " + id);
               }catch(Exception e){
                   //System.out.println("Can't decode url with utf8!");
               }
           }
       }
       return nameIds;
   }

   private static List<String> getPostRequestResponses(Crawler crawler, String tagId, int MAX_PAGE_NUM){
        // get response from post request
        List<String> responses = new LinkedList<String>();
        for(int pageNum = 0; pageNum < MAX_PAGE_NUM; pageNum++){
            String params = "limit=" + LIMIT_PARAM + "&timeout=" + TIME_OUT + "&filterTags=%5B%5D&tagId=" + 
		    tagId +"&fromLemma=false&contentLength="+ CONTENT_LENGTH + "&page="+pageNum;
            String res = crawler.sendPost(params);
            responses.add(res);
	    System.out.println("Getting post response page: " + pageNum);
        }
        return responses;
   }


    public static void appendToFile(String data, String filePath) {
		BufferedWriter bw = null;
		FileWriter fw = null;
		try {
			File file = new File(filePath);
			// if file doesnt exists, then create it
			if (!file.exists()) {
				file.createNewFile();
			}
			// true = append file
			fw = new FileWriter(file.getAbsoluteFile(), true);
			bw = new BufferedWriter(fw);
			bw.write(data);
			System.out.println("Done");
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			try {
				if (bw != null)
					bw.close();
				if (fw != null)
					fw.close();
			} catch (IOException ex) {
				ex.printStackTrace();
			}
		}
	}


    public static void main(String[] args) throws Exception {
        Crawler crawler = new Crawler();
        crawler.setUrlPost(REQUEST_URL);

	String tagId = args[0];
	String saveDir = args[1];
	int MAX_PAGE_NUM = Integer.parseInt(args[2]);
	System.out.println("tagId: " + tagId);
	System.out.println("saveDir: " + saveDir);
	System.out.println("MAX_PAGE_NUM: " + MAX_PAGE_NUM);

        File directory = new File(saveDir);
        if(!directory.exists()){
            directory.mkdir();
        }

        List<String> responses = getPostRequestResponses(crawler, tagId, MAX_PAGE_NUM);
        List<String> urls = getUrls(responses);
        List<String> nameIds = getNameIds(urls);
        
        writeToFile(responses, saveDir+"/responses.txt");
        writeToFile(urls, saveDir+"/urls.txt");
        writeToFile(nameIds, saveDir+"/nameIdMap.txt");

        // download webpages
	int count_attempt = 0;
	int count_downloaded = 0;
        for(String url : urls){
		count_attempt = count_attempt + 1;
		System.out.println("Downloading url: " + url);
		System.out.println("Saving page to saveDir: " + saveDir);
                count_downloaded += downloadFile(url, saveDir);
                Thread.sleep(SLEEP_TIME_MS);
           // }else{
                //System.out.println("main: " + url);
            //}
        }
        String counts = "tagId: " + tagId + " " 
	        + "saveDir: " + saveDir + " "	
		+ "Attempts: " +  count_attempt + " " + "Downloaded:" + count_downloaded + "\n";
        appendToFile(counts, DOWNLOAD_STATS_FILE);
    }
}
