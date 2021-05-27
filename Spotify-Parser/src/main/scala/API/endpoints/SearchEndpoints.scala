package API.endpoints

object SearchEndpoints extends SpotifyEndpoints {
  private val lSearchEndpoint = lBaseAPIUrl + "/v1/search"

  def searchArtist(artistName: String): String = {
    callRequest(iEndpoint = lSearchEndpoint + s"""?q=$artistName&type=artist&market=fr""")
  }
}
