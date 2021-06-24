name := "Spotify-Parser"

version := "0.1"

scalaVersion := "2.12.10"

libraryDependencies += "org.apache.spark" %% "spark-core" % "2.4.0"
libraryDependencies += "org.apache.spark" %% "spark-sql" % "2.4.0"

libraryDependencies += "com.typesafe" % "config" % "1.2.0"
libraryDependencies += "com.lihaoyi" %% "upickle" % "0.9.5"
libraryDependencies += "com.lihaoyi" %% "os-lib" % "0.7.3"
libraryDependencies +=  "org.scalaj" %% "scalaj-http" % "2.4.2"