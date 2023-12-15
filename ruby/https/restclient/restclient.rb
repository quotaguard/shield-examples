#!/usr/bin/env ruby

require 'rest-client'
require 'uri'

# Use localhost and port 8080 for qgpass
quotaguard = URI.parse("http://localhost:8080")

RestClient.proxy = "http://#{quotaguard.host}:#{quotaguard.port}"

result = RestClient.get('https://ip.quotaguard.com')

puts result.body