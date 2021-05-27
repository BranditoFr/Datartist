package parser

import API.endpoints.{ArtistEndpoints, SearchEndpoints}
import API.token.Token._
import com.typesafe.config.{Config, ConfigFactory}
import org.apache.spark.sql.functions.{col, concat_ws, lit, lower, regexp_replace}
import org.apache.spark.sql.types.{StringType, StructField, StructType}
import org.apache.spark.sql.{DataFrame, Row, SparkSession}
import parser.ParserUtilities._
import ujson.Value
import utils.StaticStrings._
import java.text.SimpleDateFormat
import java.util.Calendar

object Parser {
  val mToken: String = getToken

  val mSpark: SparkSession =
    SparkSession
      .builder()
      .appName("Spotify-Parser")
      .master("local[*]")
      .getOrCreate()

  mSpark.sparkContext.setLogLevel("ERROR")

  import mSpark.implicits._

  def main(args: Array[String]): Unit = {
    /** CONF * */
    val lConf: Config = ConfigFactory.load("parser.conf")
    val lArtistsCommonListPath: String = lConf.getString("common.artists.list")
    val lArtistsListPath: String = lConf.getString("spotify.artists.list")
    val lOutput: String = lConf.getString("output")

    val format = new SimpleDateFormat("YYYYMMdd")
    val lToday: String = format.format(Calendar.getInstance().getTime)

    /** SEARCH ARTISTS ID */

    val lArtistsListOldDf: DataFrame = readFromCsv(lArtistsListPath)
    val lArtistsCommonListDf: DataFrame = readFromCsv(lArtistsCommonListPath)
    lArtistsListOldDf.show(false)

    val lArtistToSearch: DataFrame =
      lArtistsCommonListDf
        .select(regexp_replace(lower(col(sArtists))," ", "") as sArtists)
      .except(
        lArtistsListOldDf
          .select(regexp_replace(lower(col(sName))," ", "") as sName)
      )
      .select(col(sArtists))
    lArtistToSearch.show(false)

    val lArtistsListDf: DataFrame =
      if (lArtistToSearch.count() > 0) {
        println("Search Other Artists")
        val lArtistsSearchList: List[String] = dataFrameToList(lArtistToSearch, sArtists)

        val lArtistSearchResultDf: DataFrame =
          lArtistsSearchList.foldLeft(lArtistsListOldDf)((lAccDf, lArtist) => {
            val lArtistData = ujson.read(SearchEndpoints.searchArtist(lArtist))(sArtists)(sItems)(0)
            lAccDf.union(
            mSpark
              .read
              .json(Seq(lArtistData.toString()).toDS)
              .select(
                sName,
                sId
              )
            )
          })
        lArtistSearchResultDf.persist()
        println(lArtistSearchResultDf.count())
        saveToCsv(lArtistSearchResultDf, lArtistsListPath)
        lArtistSearchResultDf.unpersist()

        lArtistSearchResultDf
      }else{
        lArtistsListOldDf
      }
    lArtistsListDf.show(false)

    /** ARTISTS DATA * */
    val lArtistsList: List[String] = dataFrameToList(lArtistsListDf, sId)
    println(lArtistsList)

    val lArtistJson: Value = ujson.read(ArtistEndpoints.getArtists(lArtistsList))(sArtists)

    val lArtistsDf: DataFrame =
      mSpark
        .read
        .json(Seq(lArtistJson.toString()).toDS)
        .select(
          col(sId),
          col(sName).as(sArtistName),
          col(sFollowers + "." + sTotal).as(sFollowers),
          col(sPopularity).as(sArtistPopularity)
        )

    lArtistsDf.show(false)
    lArtistsDf.printSchema()

    /** TOP TRACKS DATA * */

    val lSchema = StructType(
      StructField(sArtistId, StringType, nullable = false) ::
        StructField(sTrackId, StringType, nullable = true) ::
        StructField(sTrackName, StringType, nullable = true) ::
        StructField(sTrackPopularity, StringType, nullable = true) ::
        StructField(sTrackNumber, StringType, nullable = true) ::
        StructField(sAlbumId, StringType, nullable = true) ::
        StructField(sAlbumName, StringType, nullable = true) ::
        StructField(sAlbumDate, StringType, nullable = true) ::
        StructField(sAlbumType, StringType, nullable = false) ::
        StructField(sType, StringType, nullable = false) :: Nil)

    //    val lTopTracks = ujson.read(ArtistEndpoints.getArtistTopTracks(lArtistsList(0)))(sTracks)
    //    mSpark
    //          .read
    //          .json(Seq(lTopTracks.toString()).toDS)
    //          .printSchema()
    //          .show(false)

    val lTopTracksDf =
      lArtistsList.foldLeft(mSpark.createDataFrame(mSpark.sparkContext.emptyRDD[Row], lSchema))((lAccDf, lArtist) => {
        val lTopTracksJson = ujson.read(ArtistEndpoints.getArtistTopTracks(lArtist))(sTracks)
        lAccDf.union(
          mSpark
            .read
            .json(Seq(lTopTracksJson.toString()).toDS)
            .select(
              col(sAlbum + "." + sArtists + "." + sId).as(sArtistId),
              col(sId).as(sTrackId),
              col(sName).as(sTrackName),
              col(sPopularity).as(sTrackPopularity),
              col(sTrackNumber),
              col(sAlbum + "." + sId).as(sAlbumId),
              col(sAlbum + "." + sName).as(sAlbumName),
              col(sAlbum + "." + sReleaseDate).as(sReleaseDate),
              col(sAlbum + "." + sAlbumType).as(sAlbumType),
              col(sType)
            )
            .withColumn(sArtistId, concat_ws("", col(sArtistId)))
        )
      })
    lTopTracksDf.show(false)

    val lArtistWithTracksDf =
      lArtistsDf
        .join(lTopTracksDf, col(sId) === col(sArtistId))
        .withColumn(sDate, lit(lToday))
        .drop(sId)

    lArtistWithTracksDf.show(false)

    /** SAVE * */
    saveToParquet(lArtistWithTracksDf, lOutput, lToday)
  }
}

