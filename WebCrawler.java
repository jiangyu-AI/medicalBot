/******************************************************************************
 *  Compilation:  javac WebCrawler.java In.java
 *  Execution:    java WebCrawler url
 *  Dependencies: In.java
 *  
 *  Downloads the web page and prints out all urls on the web page.
 *  Gives an idea of how Google's spider crawls the web. Instead of
 *  looking for hyperlinks, we just look for patterns of the form:
 *  http:// followed by an alternating sequence of alphanumeric
 *  characters and dots, ending with a sequence of alphanumeric 
 *  characters.
 *
 *  % java WebCrawler http://www.slashdot.org
 *  http://www.slashdot.org
 *  http://www.osdn.com
 *  http://sf.net
 *  http://thinkgeek.com
 *  http://freshmeat.net
 *  http://newsletters.osdn.com
 *  http://slashdot.org
 *  http://osdn.com
 *  http://ads.osdn.com
 *  http://sourceforge.net
 *  http://www.msnbc.msn.com
 *  http://www.rhythmbox.org
 *  http://www.apple.com
 *  ...
 *
 *  % java WebCrawler http://www.cs.princeton.edu
 *  http://www.cs.princeton.edu
 *  http://www.w3.org
 *  http://maps.yahoo.com
 *  http://www.princeton.edu
 *  http://www.Princeton.EDU
 *  http://ncstrl.cs.Princeton.EDU
 *  http://www.genomics.princeton.edu
 *  http://www.math.princeton.edu
 *  http://libweb.Princeton.EDU
 *  http://libweb2.princeton.edu
 *  http://www.acm.org
 *  ...
 *
 *
 *  Instead of setting the system property in the code, you could do it
 *  from the commandline
 *  % java -Dsun.net.client.defaultConnectTimeout=250 WebCrawler http://www.cs.princeton.edu
 *
 ******************************************************************************/

import java.util.regex.Matcher;
import java.util.regex.Pattern;

import java.util.Queue;
import java.util.List;
import java.util.LinkedList;
import java.util.Set;
import java.util.HashSet;

public class WebCrawler { 

    public static void main(String[] args) { 

        // initial web page
        String url_start = args[0];
        url_start = "http://baike.baidu.com/item/%E6%84%9F%E5%86%92";
        List<String> urls = getUrlsBfs(url_start);
        for(String url : urls){
 	    System.out.println(url);
        }
    }

    private static List<String> getUrlsBfs(String url_start){

	List<String> urls = new LinkedList<>();

        // timeout connection after 500 miliseconds
        System.setProperty("sun.net.client.defaultConnectTimeout", "500");
        System.setProperty("sun.net.client.defaultReadTimeout",    "1000");

        // list of web pages to be examined
        Queue<String> queue = new LinkedList<String>();
        queue.add(url_start);

        // set of examined web pages
        Set<String> marked = new HashSet<String>();
        marked.add(url_start);

        // breadth first search crawl of web
        while (!queue.isEmpty()) {
            String v = queue.remove();
            System.out.println(v);

            String input = null;
            try {
                In in = new In(v);
                input = in.readAll();
            }
            catch (IllegalArgumentException e) {
                System.out.println("[could not open " + v + "]");
                continue;
            }

            // if (input == null) continue;


           /*************************************************************
            *  Find links of the form: http://xxx.yyy.zzz
            *  \\w+ for one or more alpha-numeric characters
            *  \\. for dot
            *  could take first two statements out of loop
            *************************************************************/
            //String regexp = "http://(\\w+\\.)+(\\w+)";
	    //String regexp = "/item/(%\\w\\w)+";
            String regexp = "/item/(%\\w\\w)+(\\/\\d+)?";
            Pattern pattern = Pattern.compile(regexp);

            Matcher matcher = pattern.matcher(input);

            // find and print all matches
            while (matcher.find()) {
                String w = matcher.group();
		String newUrl = "http://baike.baidu.com" + w;
                if (!marked.contains(w)) {
                    //queue.add(w);
                    //marked.add(w);
		    urls.add(newUrl);
                }
            }

        }
	return urls;
    }
}
