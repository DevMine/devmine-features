import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.graphx._


object SimpleApp {
  def main(args: Array[String]) {
    val sc = new SparkContext(args(0), "PageRank", System.getenv("SPARK_HOME"),
      SparkContext.jarOfClass(this.getClass).toSeq)

    // Load the edges as a graph
    val graph = GraphLoader.edgeListFile(sc, args(1))
    // Run PageRank
    val ranks = graph.pageRank(0.0001).vertices
    // Join the ranks with the usernames
    val users = sc.textFile(args(2)).map { line =>
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
