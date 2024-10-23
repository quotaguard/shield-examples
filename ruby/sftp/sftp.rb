#!/usr/bin/env ruby

require 'net/sftp'

Net::SFTP.start('test.rebex.net', 'demo', password: 'password', port: 2222) do |sftp|
  sftp.download!('readme.txt', 'readme.txt')
end

if File.exist?('readme.txt')
  puts "Downloaded 'readme.txt' successfully"
  puts "   CONTENTS"
  puts "--------------"
  puts File.read('readme.txt')
  puts "--------------"
else
  puts "MISSING 'readme.txt'"
  exit 1
end

