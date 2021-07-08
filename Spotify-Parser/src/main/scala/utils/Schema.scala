package utils

import org.apache.spark.sql.types.{StringType, StructField, StructType}
import utils.StaticStrings.{sAlbumDate, sAlbumId, sAlbumName, sAlbumType, sArtistId, sId, sTrackId, sTrackName, sTrackNumber, sTrackPopularity, sType}

object Schema {

  def getSchema: StructType = {
    StructType(
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
  }

  def getSchemaId: StructType = {
    StructType(
      StructField(sId, StringType, nullable = false) :: Nil)
  }
}
