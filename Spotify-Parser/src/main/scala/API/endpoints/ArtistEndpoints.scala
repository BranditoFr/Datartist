package API.endpoints

object ArtistEndpoints extends SpotifyEndpoints {
  private val lArtistEndpoint = lBaseAPIUrl + "/v1/artists/"

  def getArtist(artistId: String): String = {
    callRequest(iEndpoint = lArtistEndpoint + artistId)
  }

  def getArtists(artistIds: List[String]): String = {
    callRequest(iEndpoint = lArtistEndpoint, iParams = List(("ids", artistIds.mkString(","))))
  }

  def getArtistAlbums(artistId: String): String = {
    callRequest(iEndpoint = lArtistEndpoint + artistId + "/albums")
  }

  def getArtistTopTracks(artistId: String, country: String = "US"): String = {
    callRequest(iEndpoint = lArtistEndpoint + artistId + "/top-tracks", iParams = List(("country", country)))
  }

  def getRelatedArtists(artistId: String): String = {
    callRequest(iEndpoint = lArtistEndpoint + artistId + "/related-artists")
  }
}
