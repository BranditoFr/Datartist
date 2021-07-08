package com.spotify

import org.apache.spark.sql.{DataFrame, SaveMode}
import Parser.mSpark
import com.typesafe.config.{Config, ConfigFactory}
import mSpark.implicits._
import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.{FileStatus, FileSystem, Path}
import org.apache.spark.sql.functions.col

import java.io.File
import java.nio.file.{Files, Paths}

object ParserUtilities {

  val mFs: FileSystem = FileSystem.get(mSpark.sparkContext.hadoopConfiguration)

  def getExternalConf(iRunMode: String, iConf: Config, iRessourceBasename: String = "", iFile: String = "conf.path"): Config ={
    iRunMode match {
      case "cluster" =>
        mSpark.sparkContext.addFile(iConf.getString(iFile))
        ConfigFactory.load(iRessourceBasename)
      case _ =>
        ConfigFactory.parseFile(new File(iConf.getString("conf.path")))
    }
  }

  def checkExist(iRunMode: String, iPath: String): Boolean = {
      iRunMode match {
        case "cluster" => mFs.exists(new Path(iPath))
        case _ => Files.exists(Paths.get(iPath))
      }
  }

  def readFromCsv(iPath: String, iRunMode: String): DataFrame = {
    val lExist = checkExist(iRunMode, iPath)

    if (lExist) {
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

  def readFromJson(iPath: String, iRunMode: String): DataFrame = {
    val lExist = checkExist(iRunMode, iPath)

    if (lExist) {
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
      .map(_.getString(0))
      .collect()
      .toList
  }

  def saveToParquet(iDf: DataFrame, iPath: String, iToday: String, iRunMode: String): Unit = {
    val lTodayPath = iPath + "/" + iToday
    val lExist = checkExist(iRunMode, lTodayPath)
    if (lExist) {
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
        .option("delimiter", ";")
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
      .option("header","true")
      .csv(iCsvPath)
  }

  def calculGroupMax(iMax: Int, iListLength: Int): Int ={
    if (iListLength % iMax == 0) {
      iListLength / iMax
    } else {
      (iListLength / iMax) + 1
    }
  }

  def updateColumnsName(iPath: String, iColNameOld: String, iColNameNew: String): Unit = {
    val listFolders = new File(iPath + "/old/").listFiles
      .filter(_.isDirectory)
      .map(iPath + "/old/" + _.getName)
      .toList

    println(listFolders)

    val df = mSpark.read.parquet(listFolders: _*)

    val dateList: List[String] = df.select(iColNameOld).map(_.getString(0)).distinct().collect().toList
    println(dateList)
    val dfRename = df.withColumnRenamed(iColNameOld, iColNameNew)
    dateList.foreach(date =>{
      val dateSplit = date.split("/")
      val datePath = iPath + "/" + dateSplit(2) + dateSplit(1) + dateSplit(0)
      dfRename.where(col(iColNameNew) === date).write.parquet(datePath)
    })
  }
}
