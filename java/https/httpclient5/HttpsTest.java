import org.apache.hc.client5.http.classic.methods.HttpGet;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.core5.http.HttpHost;
import org.apache.hc.core5.http.io.entity.EntityUtils;

public class HttpsTest {
    public static void main(String[] args) throws Exception {
        // QGPass listens on localhost:8080 and forwards to QuotaGuard Shield,
        // wrapping the proxy hop in TLS and adding Basic auth from
        // QUOTAGUARDSHIELD_URL. HC5 only needs to know about the local proxy.
        HttpHost proxy = new HttpHost("http", "localhost", 8080);

        try (CloseableHttpClient client = HttpClients.custom()
                .setProxy(proxy)
                .build()) {

            HttpGet request = new HttpGet("https://ip.quotaguard.com");

            String body = client.execute(request, response -> {
                System.out.println("Response code: " + response.getCode());
                return EntityUtils.toString(response.getEntity());
            });
            System.out.println(body);
        }
    }
}
