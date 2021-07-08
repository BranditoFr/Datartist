package API.endpoints

object TrackEndpoints extends SpotifyEndpoints {
  private val lTracksEndpoint = lBaseAPIUrl + "/v1/tracks/"

  def getTrack(trackId: String): String =
    callRequest(lTracksEndpoint + trackId)

  def getTracks(trackIds: List[String]): String =
    callRequest(lTracksEndpoint, iParams = List(("ids", trackIds.mkString(","))))
}
