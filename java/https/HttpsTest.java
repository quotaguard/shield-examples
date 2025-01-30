import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.Authenticator;
import java.net.HttpURLConnection;
import java.net.PasswordAuthentication;
import java.net.URI;
import java.net.URL;

public class HttpsTest {
    public static void main(String[] args) throws Exception {
        // Using localhost:8080 with QGPass
        URI uri = URI.create("http://localhost:8080");


        String proxyHost = uri.getHost();
        int proxyPort = uri.getPort();

        // Set Java system properties so all HTTPS calls go through the proxy
        System.setProperty("https.proxyHost", proxyHost);
        System.setProperty("https.proxyPort", String.valueOf(proxyPort));

        // Simple request to echo proxy IP address
        URL testUrl = new URL("https://ip.quotaguard.com");
        HttpURLConnection conn = (HttpURLConnection) testUrl.openConnection();

        int responseCode = conn.getResponseCode();
        System.out.println("Response code: " + responseCode);

        // Print the response body
        BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
        String line;
        while ((line = reader.readLine()) != null) {
            System.out.println(line);
        }
        reader.close();
    }
}
