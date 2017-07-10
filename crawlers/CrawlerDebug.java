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
 * e.g. http://baike.baidu.com/wikitag/taglist?tagId=75954
 * Change saveDir, and tagId etc to download pages from different categories
 */
public class CrawlerDebug{

    private static final String saveDir = "/home/jyu/data/baikeMedical/webpages/disease/debug";
    private static String tagId = "75953"; // disease "68038"; // food

    private String urlPost = "http://%s:8080/requests";
    private static int maxPageNum = 200;  // max respons page number, there are 73 pages in total for diseases in baidu baike
                       
    public CrawlerDebug(){}
    public CrawlerDebug(String url){
        setUrlPost(url);
    }
    private static final int BUFFER_SIZE = 4096;

 
    /**
     * Downloads a file from a URL
     * @param fileURL HTTP URL of the file to be downloaded
     * @param saveDir path of the directory to save the file
     * @throws IOException
     */
    private static int downloadFile(String fileURL, String saveDir)
            throws IOException {
        URL url = new URL(fileURL);
        HttpURLConnection httpConn = (HttpURLConnection) url.openConnection();
        int responseCode = httpConn.getResponseCode();
 
        // always check HTTP response code first
        if (responseCode == HttpURLConnection.HTTP_OK) {
            String fileName = "";
            String disposition = httpConn.getHeaderField("Content-Disposition");
            String contentType = httpConn.getContentType();
            int contentLength = httpConn.getContentLength();
 
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
        } else {
            System.out.println("No file to download. Server replied HTTP code: " + responseCode);
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
        //LOGGER.debug(res);
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
                   urls.add(urlBuilder.toString());
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
               System.out.println(url);
           }else{
               String id = urlSplit[5]; 
               try{
                   String name = URLDecoder.decode(urlSplit[4], "UTF-8"); 
                   //System.out.println(name+" "+id); 
                   nameIds.add(name + " " + id);
               }catch(Exception e){
                   System.out.println("Can't decode url with utf8!");
               }
           }
       }
       return nameIds;
   }

   private static List<String> getPostRequestResponses(CrawlerDebug crawler, String tagId){
        // get response from post request
        List<String> responses = new LinkedList<String>();
        for(int pageNum = 1; pageNum < maxPageNum; pageNum++){
            String params = "limit=100000000000&timeout=3000000&filterTags=%5B%5D&tagId=" + tagId +"&fromLemma=false&contentLength=4000000000000000&page="+pageNum;
            String res = crawler.sendPost(params);
            responses.add(res);
        }
        return responses;
   }

    public static void main(String[] args) throws Exception {
        CrawlerDebug crawler = new CrawlerDebug();
        crawler.setUrlPost("http://baike.baidu.com/wikitag/api/getlemmas");
        File directory = new File(saveDir);
        if(!directory.exists()){
            directory.mkdir();
        }

        List<String> responses = getPostRequestResponses(crawler, tagId);
        List<String> urls = getUrls(responses);
        List<String> nameIds = getNameIds(urls);
        
        writeToFile(responses, saveDir+"/responses.txt");
        writeToFile(urls, saveDir+"/urls.txt");
        writeToFile(nameIds, saveDir+"/nameIdMap.txt");

        // download webpages
        for(String url : urls){
            if(url != null && url.isEmpty() && url.substring(0, 8).equals("://baike")){
                continue;
                //downloadFile(url, saveDir);
                //Thread.sleep(3000);
            }else{
                //System.out.println(url);
            }
        }
    }
}
