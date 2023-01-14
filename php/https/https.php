<?php

function lookup(){
  $quotaguard_env = getenv("QUOTAGUARDSHIELD_URL");
  $quotaguard = parse_url($quotaguard_env);

  $proxyUrl  = $quotaguard['host'].":".$quotaguard['port'];
  $proxyAuth = $quotaguard['user'].":".$quotaguard['pass'];

  $url = "https://ip.quotaguard.com/";

  $ch = curl_init();
  curl_setopt($ch, CURLOPT_URL, $url);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
  curl_setopt($ch, CURLOPT_PROXY, $proxyUrl);
  curl_setopt($ch, CURLOPT_PROXYAUTH, CURLAUTH_BASIC);
  curl_setopt($ch, CURLOPT_PROXYUSERPWD, $proxyAuth);
  curl_setopt($ch, CURLOPT_PROXYTYPE, CURLPROXY_HTTPS);
  $response = curl_exec($ch);
  return $response;
}

$res = lookup();
print_r($res);

?>
