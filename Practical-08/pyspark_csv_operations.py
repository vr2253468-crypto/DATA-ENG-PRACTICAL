"""Run common PySpark DataFrame operations on sales and product CSV files."""

import argparse

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import avg, col, count, sum as spark_sum


def read_csv(spark: SparkSession, path: str) -> DataFrame:
    """Read a headered CSV file and infer its column types."""
    return (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .option("mode", "FAILFAST")
        .csv(path)
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sales_csv", help="Path to the sales CSV file")
    parser.add_argument("products_csv", help="Path to the products CSV file")
    args = parser.parse_args()

    spark = (
        SparkSession.builder.appName("CsvDataFrameOperations")
        .master("local[*]")
        .getOrCreate()
    )

    try:
        sales = read_csv(spark, args.sales_csv)
        products = read_csv(spark, args.products_csv)

        print("=== Sales schema ===")
        sales.printSchema()

        print("=== Filter: completed orders with positive quantity ===")
        filtered_sales = sales.filter(
            (col("status") == "completed") & (col("quantity") > 0)
        )
        filtered_sales.show(truncate=False)

        print("=== Group and aggregate: units and sales by product ===")
        product_totals = (
            filtered_sales.withColumn(
                "sales_amount", col("quantity") * col("unit_price")
            )
            .groupBy("product_id")
            .agg(
                spark_sum("quantity").alias("total_units"),
                spark_sum("sales_amount").alias("total_sales"),
                count("order_id").alias("order_count"),
            )
            .orderBy("product_id")
        )
        product_totals.show(truncate=False)

        print("=== Remove duplicate records ===")
        sales_without_duplicates = sales.dropDuplicates()
        print(f"Rows before deduplication: {sales.count()}")
        print(f"Rows after deduplication: {sales_without_duplicates.count()}")

        print("=== Join sales with product details ===")
        joined_sales = filtered_sales.join(products, on="product_id", how="inner")
        joined_sales.show(truncate=False)

        print("=== Average sales by product category ===")
        average_sales_by_category = (
            joined_sales.withColumn(
                "sales_amount", col("quantity") * col("unit_price")
            )
            .groupBy("category")
            .agg(avg("sales_amount").alias("average_sales"))
            .orderBy("category")
        )
        average_sales_by_category.show(truncate=False)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
