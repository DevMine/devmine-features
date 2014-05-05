import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.graphx._


object SimpleApp {
  def main(args: Array[String]) {
    val sc = new SparkContext("local", "Simple App", ".",
      List("target/scala-2.10/pagerank_2.10-1.0.jar"))

    // Load the edges as a graph
    val graph = GraphLoader.edgeListFile(sc, args(0))
    // Run PageRank
    val ranks = graph.pageRank(0.0001).vertices
    // Join the ranks with the usernames
    val users = sc.textFile(args(1)).map { line =>
      val fields = line.split(",")
                                                          (fields(0).toLong, fields(1))
                                                        }
    val ranksByUsername = users.join(ranks).map {
      case (id, (username, rank)) => (username, rank)
    }
    // Print the result
    println(ranksByUsername.collect().mkString("\n"))
  }
}
