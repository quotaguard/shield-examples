# app.rb
require 'curb'

proxy_url = ENV.fetch("QUOTAGUARDSHIELD_URL") do
  abort "Set QUOTAGUARDSHIELD_URL, e.g. http://user:pass@us-east-shield-02.quotaguard.com:9293"
end

begin
  curl = Curl::Easy.new("https://ip.quotaguard.com")
  
  # Split out the URI parts if needed
  require 'uri'
  parsed = URI.parse(proxy_url)
  
  # If it's an HTTP-based proxy:
  curl.proxy_url      = "#{parsed.scheme}://#{parsed.host}:#{parsed.port}"
  curl.proxy_tunnel   = true  # Tells libcurl to use CONNECT for HTTPS
  curl.proxypwd       = "#{parsed.user}:#{parsed.password}" if parsed.user && parsed.password

  # Optional: If you really need to connect to the proxy over HTTPS itself
  # you can try setting:
  # curl.proxy_ssl_verify_peer = false
  # curl.proxy_ssl_verify_host = 0
  # But that’s not recommended for production.

  curl.perform
  puts "Status: #{curl.response_code}"
  puts "Body:\n#{curl.body_str}"
rescue => e
  warn "Request failed: #{e.message}"
  raise
end
