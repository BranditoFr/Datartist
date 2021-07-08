package com.spotify

import API.endpoints.{AlbumEndpoints, ArtistEndpoints, SearchEndpoints, TrackEndpoints}
import API.token.Token._
import com.spotify.ParserUtilities._
import com.typesafe.config.{Config, ConfigFactory}
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types.StructType
import org.apache.spark.sql.{DataFrame, Row, SparkSession}
import utils.Schema._
import utils.StaticStrings._

import java.io.File
import java.text.SimpleDateFormat
import java.util.Calendar


object Parser {
  println("Start Spotify Parser")
  val mToken: String = getToken

  val mSpark: SparkSession =
    SparkSession
      .builder()
      .appName("Spotify-Parser")
      .master("local[*]")
      .getOrCreate()

  mSpark.sparkContext.setLogLevel("ERROR")

  import mSpark.implicits._

  def main(iArgs: Array[String]): Unit = {
    val lRunMode = iArgs(0)

    /** CONF * */

//    if (lRunMode == "cluster"){
//      val lArtistsCommonListPath: String = "/work/conf/listArtist.csv"
//      val lArtistsListPath: String = "/work/conf/listArtistSpotify/"
//      val lOutput: String = "/work/output/spotify/"
//      val lOutputCsv: String = "/work/conf/"
//      val lAlbumsMaxRequest: Int = 20
//      val lTracksMaxRequest: Int = 50
//      val lArtistsMaxRequest: Int = 50

//    }else{
      val lConfig: Config = ConfigFactory.parseResources("spotify.conf").getConfig(lRunMode)
      val lAppConf: Config = lConfig.getConfig("spotify")
      val lAppParams: Config = getExternalConf(lRunMode, lAppConf, "spotify.conf")
//          val lAppParams: Config = ConfigFactory.load("spotify")
          val lArtistsCommonListPath: String = lAppParams.getString("common.artists.list")
          val lArtistsListPath: String = lAppParams.getString("spotify.artists.list")
          val lOutput: String = lAppParams.getString("output.parquet")
          val lOutputCsv: String = lAppParams.getString("output.csv")
          val lAlbumsMaxRequest: Int = lAppParams.getInt("request.albums.max")
          val lTracksMaxRequest: Int = lAppParams.getInt("request.tracks.max")
          val lArtistsMaxRequest: Int = lAppParams.getInt("request.artists.max")
//    }

    val format = new SimpleDateFormat("dd/MM/yyyy")
    val formatFolder = new SimpleDateFormat("yyyyMMdd")
    val lToday: String = format.format(Calendar.getInstance().getTime)
    val lTodayFolder: String = formatFolder.format(Calendar.getInstance().getTime)

    /** SEARCH ARTISTS ID */

    val lArtistsListOldDf: DataFrame = readFromCsv(lArtistsListPath, lRunMode)
    val lArtistsCommonListDf: DataFrame = readFromCsv(lArtistsCommonListPath, lRunMode)
    lArtistsListOldDf.show(false)

    val lArtistToSearch: DataFrame =
      lArtistsCommonListDf
        .select(regexp_replace(lower(col(sArtists)), " ", "") as sArtists)
        .except(
          lArtistsListOldDf
            .select(regexp_replace(lower(col(sName)), " ", "") as sName)
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
                .withColumn(sNameCommon, lit(lArtist))
                .select(
                  sName,
                  sNameCommon,
                  sId
                )
            )
          })
        lArtistSearchResultDf.persist()
        println(lArtistSearchResultDf.count())
        saveToCsv(lArtistSearchResultDf, lArtistsListPath)
        lArtistSearchResultDf.unpersist()

        lArtistSearchResultDf
      } else {
        lArtistsListOldDf
      }
    lArtistsListDf.show(false)

    /** ARTISTS DATA * */
    val lArtistsList: List[String] = dataFrameToList(lArtistsListDf, sId)
    println(lArtistsList)

    //    val lArtistLength: Int = lArtistsList.length
    //    val lArtistGroup: Int = calculGroupMax(lArtistsMaxRequest, lArtistLength)
    //    (0 until lArtistGroup).foldLeft("")((lAcc, lInt) => {
    //      val lMin: Int = lInt * lArtistsMaxRequest
    //      val lMax: Int = if (lInt != lArtistGroup) (lInt + 1) * lArtistsMaxRequest - 1 else lArtistLength
    //      lAcc ++
    //      ujson.read(ArtistEndpoints.getArtists(lArtistsList.slice(lMin, lMax)))(sArtists).toString()
    //    })

    val lArtistJson = ujson.read(ArtistEndpoints.getArtists(lArtistsList))(sArtists)

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
        .join(
          lArtistsListDf
            .select(col(sName), col(sNameCommon)),
          col(sArtistName) === col(sName)
        )
        .withColumn(sArtistName, col(sNameCommon))
        .drop(sName, sNameCommon)

    lArtistsDf.show(false)

    /** TOP TRACKS DATA * */

    val lSchema: StructType = getSchema

    val lTopTracksDf: DataFrame =
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

    /** ALBUMS DATA */
    val lSchemaId: StructType = getSchemaId

    val lAlbumsDf: DataFrame =
      lArtistsList.foldLeft(mSpark.createDataFrame(mSpark.sparkContext.emptyRDD[Row], lSchemaId))((lAccDf, lArtist) => {
        val lAlbumsJson = ujson.read(ArtistEndpoints.getArtistAlbums(lArtist))(sItems)
        lAccDf.union(
          mSpark
            .read
            .json(Seq(lAlbumsJson.toString()).toDS)
            .filter(col(sAlbumType) === sAlbum)
            .dropDuplicates(sName)
            .select(sId)
        )
      })

    val lAlbumList: List[String] = dataFrameToList(lAlbumsDf, sId)

    val lAlbumListLength: Int = lAlbumList.length

    val lAlbumGroup: Int = calculGroupMax(lAlbumsMaxRequest, lAlbumListLength)


    val lAlbumsDataDf: DataFrame =
      (0 until lAlbumGroup).foldLeft(mSpark.createDataFrame(mSpark.sparkContext.emptyRDD[Row], lSchema))((lAccDf, lInt) => {
        val lMin: Int = lInt * lAlbumsMaxRequest
        val lMax: Int = if (lInt != lAlbumGroup) (lInt + 1) * lAlbumsMaxRequest - 1 else lAlbumListLength

        val lAlbumsJson = ujson.read(AlbumEndpoints.getAlbums(lAlbumList.slice(lMin, lMax + 1)))(sAlbums)

        lAccDf.union(
          mSpark
            .read
            .json(Seq(lAlbumsJson.toString()).toDS)
            .select(
              col(sArtists + "." + sId).getItem(0) as sArtistId,
              col(sTracks + "." + sItems + "." + sId) as sTrackId,
              col(sTracks + "." + sItems + "." + sName) as sTrackName,
              col(sPopularity) as sTrackPopularity,
              col(sTotalTracks) as sTrackNumber,
              col(sId) as sAlbumId,
              col(sName) as sAlbumName,
              col(sReleaseDate) as sAlbumDate,
              col(sAlbumType),
              col(sType)
            )
            .withColumn(sTrackId, concat_ws(",", col(sTrackId)))
            .withColumn(sTrackName, concat_ws(",", col(sTrackName)))
        )

      })
    lAlbumsDataDf.show(false)

    /** TRACKS FROM ALBUMS/SINGLES */

    val lTracksList: List[String] =
      dataFrameToList(lAlbumsDataDf, sTrackId)
        .mkString(",")
        .split(",")
        .toList

    val lTracksLength: Int = lTracksList.length

    val lTracksGroup: Int = calculGroupMax(lTracksMaxRequest, lTracksLength)

    val lTracksDataDf: DataFrame =
      (0 until lTracksGroup).foldLeft(mSpark.createDataFrame(mSpark.sparkContext.emptyRDD[Row], lSchema))((lAccDf, lInt) => {
        val lMin = lInt * lTracksMaxRequest
        val lMax = if (lInt != lTracksGroup) (lInt + 1) * lTracksMaxRequest - 1 else lTracksLength

        val lTracksJson = ujson.read(TrackEndpoints.getTracks(lTracksList.slice(lMin, lMax + 1)))(sTracks)
        lAccDf.union(
          mSpark
            .read
            .json(Seq(lTracksJson.toString()).toDS)
            .select(
              col(sArtists + "." + sId).getItem(0) as sArtistId,
              col(sId) as sTrackId,
              col(sName) as sTrackName,
              col(sPopularity) as sTrackPopularity,
              col(sTrackNumber) as sTrackNumber,
              col(sAlbum + "." + sId) as sAlbumId,
              col(sAlbum + "." + sName) as sAlbumName,
              col(sAlbum + "." + sReleaseDate) as sAlbumDate,
              col(sAlbum + "." + sAlbumType),
              col(sType)
            )
        )
      })

    lTracksDataDf.show(false)

    /** ALL DATA JOIN */

    val lArtistWithDataDf =
      lArtistsDf
        .join(
          lTopTracksDf
            .union(
              lAlbumsDataDf
                .filter(col(sAlbumType) === sAlbum)
            )
            .union(lTracksDataDf),
          col(sId) === col(sArtistId)
        )
        .withColumn(sDate, lit(lToday))
        .drop(sId)
        .distinct()

    lArtistWithDataDf.show(false)
    /** SAVE * */
    saveToParquet(lArtistWithDataDf, lOutput, lTodayFolder, lRunMode)

//  parquetToCsv(lOutput, lOutputCsv)
  }
}


