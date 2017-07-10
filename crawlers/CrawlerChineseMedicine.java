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
 * The class is written to download web pages from baike medical categories 
 * http://baike.baidu.com/wikitag/taglist?tagId=75954
 */
public class CrawlerChineseMedicine{
    //private static final Logger LOGGER = Logger.getLogger(CrawlerChineseMedicine.class);

    String urlPost = "http://%s:8080/requests";
    public static final String saveDir = "/home/wechaty/data/webpages/ChineseMedicine";
                       
    public CrawlerChineseMedicine(){}
    public CrawlerChineseMedicine(String url){
        setUrlPost(url);
    }
    private static final int BUFFER_SIZE = 4096;

//    public static void saveId2Name(String fileURL, String saveDir){

 //   }
 
    /**
     * Downloads a file from a URL
     * @param fileURL HTTP URL of the file to be downloaded
     * @param saveDir path of the directory to save the file
     * @throws IOException
     */
    public static int downloadFile(String fileURL, String saveDir)
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
 
            //System.out.println("Content-Type = " + contentType);
            //System.out.println("Content-Disposition = " + disposition);
            //System.out.println("Content-Length = " + contentLength);
            //System.out.println("fileName = " + fileName);
 
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

    public void setUrlPost(String urlPost) {
        this.urlPost = urlPost;
    }

    public void setMsgToSend(String msg) {
        this.msgToSend = msg;
    }
    String msgToSend = "";

//    void initMsg(String fname) {
//        msgToSend = FileUtil.readAllTexts(fname);

//    }
    public String sendPost(String msg) {
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
    public static void main(String[] args) throws Exception {
        CrawlerChineseMedicine sc = new CrawlerChineseMedicine();
        /*
        sc.urlPost = String.format(sc.urlPost, args[0]);
        if (args.length >= 2 && args[1].equalsIgnoreCase("get")) {
            if (args.length >= 3) {
                sc.sendGet(args[2]);
            } else {
                //sc.sendGet(DataKey.default_bizid);
            }
        } else if (args.length == 2 && args[1].equalsIgnoreCase("post")) {
            sc.sendPost();
        } else if (args.length == 3 && args[1].equalsIgnoreCase("post")){
            //LOGGER.info("calling with post " +args[2]);
            String fname = args[2];
            // "C:\\Workspace\\prservice\\wxbot_related\\java_tools\\src\\test\\postdata_questions.json";
            String content = FileUtil.readAllTexts(fname);
            //Map<String, Object> map = MapUtil.convertJsonToMap(content);
            sc.msgToSend =content;
            String res = sc.sendPost();
            //LOGGER.info("res " + res);
        } else {
            //LOGGER.info("Usage: java service.CrawlerChineseMedicine get/post");
        }
       */ 
        sc.setUrlPost("http://baike.baidu.com/wikitag/api/getlemmas");
        try(PrintWriter nameIdMapFile = new PrintWriter(saveDir + "/nameIdMap.txt")){
            // there are 73 pages in total
            for(int pageNum = 1; pageNum < 74; pageNum++){
                String s ="limit=100000000000&timeout=3000000&filterTags=%5B%5D&tagId=75956&fromLemma=false&contentLength=4000000000000000&page="+pageNum;
                String res = sc.sendPost(s);
                for(int i = 0; i < res.length()-4; i++){
                  StringBuilder urlBuilder = new StringBuilder();
                  if(res.substring(i, i+4).equals("http")){
                       int j = i+4;
                       while(res.charAt(j) != '"'){
                           j++;
                       }
                       String url = res.substring(i, j);
                       for(char c : url.toCharArray()){
                           if(c != '\\'){
                               urlBuilder.append(c);
                           }
                       }
                       String urlsClean = urlBuilder.toString();
                       //String resultPage = sendGet(urlClean);
		       String[] urls = urlsClean.split("http");
		       for(String urlClean : urls){
                   if(urlClean == null || urlClean.isEmpty()) continue;
                   final ScheduledExecutorService executorService = Executors.newSingleThreadScheduledExecutor();
                   String urlTemp = "http"+urlClean;
                   Thread.sleep(3000);
                   downloadFile(urlTemp, saveDir);
                   /*
                    * executorService.scheduleAtFixedRate(new Runnable(){
                       @Override
                       public void run(){
                           try {
                                downloadFile(urlTemp, saveDir);
                           }catch(Exception e){
                               System.out.println("downloadFile failed!");
                           }
                       }
                   }, 0, 30, TimeUnit.SECONDS);
                   //executorService.scheduleAtFixedRate(App::downloadFile, 0, 1, TimeUnit.SECONDS);
                   */
                   String[] urlSplit = urlClean.split("/");
                   String name = URLDecoder.decode(urlSplit[4], "UTF-8"); 
                   String id = urlSplit[5]; System.out.println(name+" "+id); 
                   nameIdMapFile.println(name + " " + id);
               }
                  // String toEncode = "";
                 //  String encoded = URLEncoder.encode(toEncode, "UTF-8");
                 //  System.out.println("Encoded: " + encoded);
                  // String encoded = "%E8%89%BE%E6%BB%8B%E7%97%85";
                   //String decoded = URLDecoder.decode(encoded, "UTF-8");
                   }
                }
            }
        }
         //Writer w = new OutputStreamWriter(new FileOutputStream("test.txt"), "UTF-8");
         //w.close();
    }
}
