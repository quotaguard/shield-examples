import okhttp3.*;
import java.net.InetSocketAddress;
import java.net.Proxy;
import java.util.List;

public class HttpsTest {
    public static void main(String[] args) throws Exception {
        // Using localhost:8080 with QGPass
        String proxyHost = "localhost";
        int proxyPort = 8080;

        // Create OkHttp client with proxy configuration
        OkHttpClient client = new OkHttpClient.Builder()
                .proxy(new Proxy(Proxy.Type.HTTP, new InetSocketAddress(proxyHost, proxyPort)))
                .protocols(List.of(Protocol.HTTP_1_1))
                .retryOnConnectionFailure(false)
                .build();

        // Simple request to echo proxy IP address
        Request request = new Request.Builder()
                .url("https://ip.quotaguard.com")
                .build();

        try (Response response = client.newCall(request).execute()) {
            int responseCode = response.code();
            System.out.println("Response code: " + responseCode);

            // Print the response body
            if (response.body() != null) {
                System.out.println(response.body().string());
            }
        }
    }
}
