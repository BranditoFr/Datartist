package API.endpoints

import com.spotify.Parser.mToken
import scalaj.http.Http
abstract class SpotifyEndpoints {

  protected val lBaseAPIUrl = "https://api.spotify.com"

  protected def callRequest(iEndpoint: String): String = {
    Http(iEndpoint)
      .header("Authorization", "Bearer " + mToken)
      .asString.body
  }

  protected def callRequest(iEndpoint: String, iParams: List[(String, String)]): String = {
    Http(iEndpoint)
      .params(iParams)
      .header("Authorization", "Bearer " + mToken)
      .asString.body
  }
}

