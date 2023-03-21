defmodule Qg do
  use Tesla

  plug Tesla.Middleware.BaseUrl, "https://ip.quotaguard.com"

  @moduledoc """
  Example for connecting through the QuotaGuard proxy
  """

  @doc """
  Requesting IP echo
  """
  def request_ip do
    {:ok, response} = get("/")
    IO.puts(response.body)
  end
end
