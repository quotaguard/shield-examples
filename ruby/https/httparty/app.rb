#!/usr/bin/env ruby
require 'httparty'
require 'uri'

proxy = URI.parse("http://localhost:8080")

options = {
  http_proxyaddr: proxy.host,
  http_proxyport: proxy.port
}

response = HTTParty.get('https://ip.quotaguard.com/', options)

puts response.body, response.code, response.message, response.headers.inspect