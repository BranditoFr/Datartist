package parser

import org.apache.spark.sql.{DataFrame, SaveMode}
import parser.Parser.mSpark
import mSpark.implicits._
import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.{FileStatus, FileSystem, Path}

import java.nio.file.{Files, Paths}

object ParserUtilities {
  def readFromCsv(iPath: String): DataFrame = {
    if (Files.exists(Paths.get(iPath))) {
      println(s"""Read csv from "$iPath"""")
      mSpark
        .read
        .option("delimiter", ";")
        .option("header", "true")
        .csv(iPath)
    }else{
      println(s"""File in "$iPath doesn't exist"""")
      mSpark.emptyDataFrame
    }
  }

  def readFromJson(iPath: String): DataFrame = {
    if (Files.exists(Paths.get(iPath))) {
      println(s"""Read csv from "$iPath"""")
      mSpark
        .read
        .json(iPath)
    }else{
      println(s"""File in "$iPath" doesn't exist"""")
      mSpark.emptyDataFrame
    }
  }

  def dataFrameToList(iDf: DataFrame, iCol: String): List[String] = {
      iDf
        .select(iCol)
        .map(lData => lData.getString(0))
        .collect()
        .toList
  }

  def saveToParquet(iDf: DataFrame, iPath: String, iToday: String): Unit = {
    val lTodayPath = iPath + "/" + iToday
    if (Files.exists(Paths.get(lTodayPath))) {
      println(s"""Folder "$lTodayPath" already exists"""")
    }else{
      println(s"""Save to parquet in folder: "$lTodayPath"""")
      iDf
        .write
        .parquet(lTodayPath)
    }
  }

  def saveToCsv(iDf: DataFrame, iPath: String): Unit = {
    iDf
      .repartition(1)
      .write
      .format("csv")
      .mode("overwrite")
      .option("header", value = true)
      .option("delimiter",";")
      .save(iPath)
  }

  def parquetToCsv(iParquetPath: String, iCsvPath: String): Unit = {
    val fs = FileSystem.get(new Configuration())
    val status: Array[FileStatus] = fs.listStatus(new Path(iParquetPath))
    val lFolderList: Array[String] = status.map(x => iParquetPath + "/" + x.toString.split("/").last.split(";").head)

    println(s"""Read parquet from "$iParquetPath"""")
    val lDf =
      mSpark
      .read
      .parquet(lFolderList: _*)

    println(s"""Save to CSV in folder: "$iCsvPath"""")
    lDf
      .repartition(1)
      .write
      .mode(SaveMode.Overwrite)
      .csv(iCsvPath)
  }

  def calculGroupMax(iMax: Int, iListLength: Int): Int ={
    if (iListLength % iMax == 0) {
      iListLength / iMax
    } else {
      (iListLength / iMax) + 1
    }
  }
}
