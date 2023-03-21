import Config

config :tesla, adapter: {Tesla.Adapter.Mint, proxy: {:http, "localhost", 8080, []}}
