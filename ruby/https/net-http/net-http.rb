#!/usr/bin/env ruby

require 'net/http'
require 'uri'

# Use localhost and port 8080 for qgpass
quotaguard = URI.parse("http://localhost:8080")

proxy_uri = URI.parse("http://#{quotaguard.host}:#{quotaguard.port}")

target_uri = URI.parse('https://ip.quotaguard.com')

Net::HTTP.start(target_uri.host, target_uri.port, proxy_uri.host, proxy_uri.port, :use_ssl => target_uri.scheme == 'https') do |http|
  request = Net::HTTP::Get.new(target_uri)

  response = http.request(request)

  puts response.body
end