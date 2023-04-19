# Redis_data_pipelines
The task is to build a pipeline that can efficiently extract, transform, and load data from CSV files into a Postgres database. The data to be extracted is related to customer call logs, which contain information about the duration, cost,and destination of customer calls. 
The extracted data needs to be transformed to ensure it is in the correct format and structure for storage in the database. The pipeline should also cache
data using Redis to speed up the data extraction and transformation.


# Best Practices used
* Used Redis cache to store the extracted data for faster retrieval in subsequent runs of the pipeline. This can significantly reduce the time it takes to extract data from a CSV file and avoid I/O overheads
* Use of parameterized SQL queries when inserting data into the PostgreSQL database. This helps to prevent SQL injection attacks and improves performance by reducing the overhead of parsing and optimizing SQL queries.
* 
