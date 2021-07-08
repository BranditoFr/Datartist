package API.endpoints

object AlbumEndpoints extends SpotifyEndpoints {
  private val lAlbumEndpoint = lBaseAPIUrl + "/v1/albums/"

  def getAlbum(albumId: String): String = {
    callRequest(iEndpoint = lAlbumEndpoint + albumId)
  }

  def getAlbums(albumIds: List[String]): String = {
    callRequest(iEndpoint = lAlbumEndpoint, iParams = List(("ids", albumIds.mkString(","))))
  }

  def getAlbumTracks(albumId: String): String = {
    callRequest(iEndpoint = lAlbumEndpoint + albumId + "/tracks")
  }
}
