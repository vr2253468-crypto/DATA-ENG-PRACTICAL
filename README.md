📊 Data Engineering Practicals 01–10
Python SQL Power BI PySpark Apache Airflow MongoDB GitHub

📌 About This Repository
This repository contains my Data Engineering Practical work from Practical 01 to Practical 10, organized as a structured academic portfolio.

The practicals cover data parsing, data-quality checks, file processing, database operations, business intelligence, API-based extraction, workflow orchestration, ETL pipelines, PySpark processing, incremental loading, testing, and end-to-end data-warehouse concepts.

Each practical has its own folder and README so that the work can be understood, reproduced, and reviewed independently.

🎯 Objectives
The main objectives of this practical work are to:

Understand fundamental Data Engineering concepts.
Process data from different file formats.
Perform data extraction and transformation.
Identify data-quality issues and anomalies.
Work with binary and serialized files.
Perform database CRUD operations.
Work with MongoDB document operations.
Create and analyze Business Intelligence dashboards.
Extract and clean data using Python.
Understand workflow orchestration with Apache Airflow.
Implement ETL and incremental-loading concepts.
Process CSV data using PySpark.
Build structured and reproducible data pipelines.
Apply basic pipeline testing and validation.
Organize and document technical work using GitHub.
📚 Practical Overview
Practical	Main Work	Key Technologies
Practical 01	File parsing, anomaly checks, binary/pickle files, regex and SQLite CRUD	Python, SQLite
Practical 02	Retail Business Intelligence dashboard	Power BI, Excel
Practical 03	MongoDB document operations	MongoDB, mongosh
Practical 04	Noise elimination, feature selection and EDA	Python, Jupyter
Practical 05	REST API and CSV data extraction	Python, Pandas, Requests
Practical 06	ETL workflow orchestration	Apache Airflow, Python
Practical 07	CSV/JSON ETL with incremental SQLite loading	Python, Pandas, SQLite
Practical 08	CSV processing using Spark DataFrames	PySpark, Apache Spark
Practical 09	Incremental e-commerce ETL	Python, Pandas, SQLite
Practical 10	End-to-end star-schema ETL	Python, Pandas, SQLite, unittest
🔹 Practical 01 — File Processing, Data Extraction & Database Operations
📁 Folder: Practical-01

Practical 01 introduces fundamental Data Engineering operations using Python.

Main Files
ex1_parsing_and_anomalies.py
ex2_binary_files.py
ex3_regex_operations.py
ex4_database_crud.py
setup_data.py
Sample CSV, HTML, XML, JSON and TXT files
Binary and pickle files
SQLite database
Topics Covered
1. Parsing and Anomaly Detection

Processes multiple file formats and demonstrates basic data-quality checking.

2. Binary and Pickle File Processing

Demonstrates reading and writing binary/serialized data using Python.

3. Regular Expressions

Covers pattern matching, searching, splitting, replacing and string processing.

4. SQLite CRUD

Demonstrates:

Create
Read
Update
Delete
Open Practical 01
Go to Practical 01 →

🔹 Practical 02 — Business Intelligence & Power BI
📁 Folder: Practical-02

Practical 02 focuses on building a retail-sales Business Intelligence dashboard using Power BI and Excel.

Main Files
business intelligence practical.pbix
Meridian_Retail_Sales_Dataset.xlsx
Dashboard screenshots
Dashboard Areas
Sales Overview
Sales Channel Performance
Product Analysis
Forecast Summary
Technologies
Microsoft Power BI
Microsoft Excel
Data Visualization
Business Intelligence
Open Practical 02
Go to Practical 02 →

🔹 Practical 03 — MongoDB Document Operations
📁 Folder: Practical-03

Practical 03 demonstrates basic document operations using MongoDB and mongosh.

Aim
To perform single-document insertion, retrieval, multiple-document insertion and formatted query output.

Technology
MongoDB
mongosh
JavaScript commands
Database
practical3
Operations Covered
Step 1 — Insert One Document

db.items.insertOne({
  name: "laptop",
  price: 999
});
Step 2 — Find Documents

db.items.find();
Step 3 — Insert Multiple Documents

db.products.insertMany([
  { name: "phone", price: 500, stock: 10 },
  { name: "tablet", price: 300, stock: 5 },
  { name: "watch", price: 150, stock: 0 }
]);
Step 4 — Formatted Query

db.products.find().pretty();
Open Practical 03
Go to Practical 03 →

🔹 Practical 04 — Noise Elimination, Feature Selection & EDA
📁 Folder: Practical-04

Practical 04 focuses on data analysis and exploratory visualization.

Main Resource
Jupyter Notebook
Dataset-analysis screenshots
Histogram
Boxplot
Topics Covered
Dataset inspection
Noise elimination
Feature selection
Exploratory Data Analysis
Distribution analysis
Outlier identification
Histogram visualization
Boxplot visualization
Open Practical 04
Go to Practical 04 →

🔹 Practical 05 — API & CSV Data Extraction
📁 Folder: Practical-05

Practical 05 demonstrates how to extract data from a REST API and combine it with local CSV data.

Main Files
data_extraction.py
locations.csv
cleaned_warehouse_profiles.csv
Supporting screenshots
Workflow
API Data
   +
CSV Data
   ↓
Data Extraction
   ↓
Data Cleaning
   ↓
Data Merging
   ↓
Cleaned Output
Technologies
Python
Pandas
Requests
CSV
REST API
Open Practical 05
Go to Practical 05 →

🔹 Practical 06 — Workflow Orchestration with Apache Airflow
📁 Folder: Practical-06

Practical 06 introduces workflow orchestration using Apache Airflow DAGs.

Main Resources
Practical-06/
└── dags/
    ├── data_extraction.py
    └── data_pipeline_dag.py
Main Concepts
Directed Acyclic Graphs (DAGs)
Tasks
Task dependencies
Workflow scheduling
ETL-style orchestration
Automated data workflows
Basic Workflow
Task 1
  ↓
Task 2
  ↓
Task 3
  ↓
Task 4
Open Practical 06
Go to Practical 06 →

🔹 Practical 07 — CSV/JSON ETL & Incremental Loading
📁 Folder: Practical-07

Practical 07 demonstrates an ETL workflow using CSV and JSON customer data with validation and incremental SQLite loading.

Main Resources
Practical-07/
└── data/
    ├── etl_pipeline.py
    ├── customers.csv
    ├── customers_additional.csv
    └── customer_updates.json
ETL Workflow
       EXTRACT
          ↓
       VALIDATE
          ↓
      TRANSFORM
          ↓
    INCREMENTAL LOAD
          ↓
        SQLite
Main Concepts
Data extraction
Data validation
Data cleaning
Invalid-record tracking
Record hashing
Incremental loading
SQLite updates
Open Practical 07
Go to Practical 07 →

🔹 Practical 08 — PySpark CSV Processing
📁 Folder: Practical-08

Practical 08 demonstrates CSV processing using PySpark DataFrames.

Main Files
pyspark_csv_operations.py
products.csv
sales.csv
Processing Workflow
CSV Files
   │
   ├── products.csv
   │
   └── sales.csv
          ↓
     SparkSession
          ↓
     DataFrames
          ↓
   Transformations
          ↓
   Aggregations / Joins
          ↓
       Results
Main Concepts
SparkSession
CSV reading
Spark DataFrames
Filtering
Aggregation
Deduplication
Joins
Data transformation
Technologies
Python
Apache Spark
PySpark
Open Practical 08
Go to Practical 08 →

🔹 Practical 09 — Incremental E-commerce ETL
📁 Folder: Practical-09

Practical 09 implements an e-commerce ETL pipeline with historical and incremental data loading.

Main Resources
etl_pipeline.py
requirements.txt
data/
tests/test_pipeline.py
ETL Workflow
Source CSV Data
      ↓
Data Validation
      ↓
Data Cleaning
      ↓
Transformation
      ↓
SQLite Load / Upsert
      ↓
Data Quality Tracking
      ↓
Reports
Main Concepts
Historical loading
Incremental loading
Validation rules
Upserts
Data-quality issue logging
Idempotent ETL
Unit testing
Open Practical 09
Go to Practical 09 →

🔹 Practical 10 — End-to-End Star-Schema ETL
📁 Folder: Practical-10

Practical 10 demonstrates a complete end-to-end ETL workflow using Python, Pandas and SQLite.

Project Structure
Practical-10/
├── data/
├── scripts/
│   ├── cleaning.py
│   ├── ingestion.py
│   ├── load_database.py
│   ├── pipeline.py
│   └── transformation.py
├── tests/
│   └── test_pipeline.py
├── requirements.txt
└── run_pipeline.py
Pipeline Architecture
             SOURCE DATA
                  │
                  ▼
             ┌───────────┐
             │ INGESTION │
             └─────┬─────┘
                   │
                   ▼
             ┌───────────┐
             │  CLEANING │
             └─────┬─────┘
                   │
                   ▼
             ┌──────────────┐
             │ TRANSFORM    │
             └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │ STAR SCHEMA  │
             │   DATABASE   │
             └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │   REPORTS /  │
             │   DASHBOARD  │
             └──────────────┘
                    ▲
                    │
                 TESTING
Main Concepts
Data ingestion
Data cleaning
Data transformation
Star-schema warehouse
Database loading
Analytical reporting
Dashboard generation
Pipeline testing
Open Practical 10
Go to Practical 10 →

🧰 Technologies Used
Programming & Data Processing
Python
Pandas
Requests
Regular Expressions
CSV
JSON
XML
HTML
Databases
SQLite
MongoDB
CRUD operations
Incremental loading
Upserts
Business Intelligence
Microsoft Power BI
Microsoft Excel
Data visualization
Retail sales analysis
Data Engineering
ETL
Data pipelines
Data extraction
Data transformation
Data quality
Data validation
Data warehousing
Star schema
Big Data
Apache Spark
PySpark
Spark DataFrames
Workflow Orchestration
Apache Airflow
DAGs
Task dependencies
Testing & Development
unittest
Git
GitHub
Dependency management
📁 Repository Structure
Data-Engineering-Practical/
│
├── Practical-01/
│   └── File processing & SQLite
│
├── Practical-02/
│   └── Power BI retail dashboard
│
├── Practical-03/
│   └── MongoDB operations
│
├── Practical-04/
│   └── EDA & visualization
│
├── Practical-05/
│   └── API & CSV extraction
│
├── Practical-06/
│   └── Airflow DAGs
│
├── Practical-07/
│   └── CSV/JSON ETL
│
├── Practical-08/
│   └── PySpark processing
│
├── Practical-09/
│   └── Incremental e-commerce ETL
│
├── Practical-10/
│   └── End-to-end star-schema ETL
│
├── LICENSE
└── README.md
🔄 Overall Data Engineering Journey
The practicals collectively demonstrate a progression from fundamental data operations to structured data-engineering workflows:

File Processing
      ↓
Data Quality & Anomaly Checking
      ↓
Database Operations
      ↓
Business Intelligence
      ↓
API & Data Extraction
      ↓
Data Cleaning & Transformation
      ↓
ETL
      ↓
Workflow Orchestration
      ↓
PySpark
      ↓
Incremental Data Loading
      ↓
Data Warehousing
      ↓
End-to-End Data Pipeline
🎓 Learning Outcomes
Through these practicals, I developed hands-on exposure to:

Python-based data processing
File-format parsing
Data extraction
Data cleaning
Data-quality checking
Binary and serialized file handling
Regular expressions
SQLite CRUD operations
MongoDB document operations
Power BI dashboard development
API integration
ETL workflows
Incremental data loading
Apache Airflow concepts
PySpark processing
Data warehouse concepts
Star-schema design
Pipeline testing
Git and GitHub documentation
▶️ Running the Projects
Clone the repository:

git clone https://github.com/Mukeshkarn-DS/Data-Engineering-Practical.git
cd Data-Engineering-Practical
For Python-based practicals:

python filename.py
For projects with a requirements.txt file:

pip install -r requirements.txt
For Practical 09:

cd Practical-09
python etl_pipeline.py
python -m unittest tests/test_pipeline.py
For Practical 10:

cd Practical-10
python run_pipeline.py
python -m unittest tests/test_pipeline.py
Note: Always read the README inside the selected practical before running it because dependencies, input files and execution commands differ between practicals.

🧹 Repository Organization
The repository has been organized specifically around Practical 01–10.

Standardized folder names from Practical-01 through Practical-10.
Removed redundant duplicate practical folders.
Removed generated Python cache files such as __pycache__/ and *.pyc.
Kept practical-specific source code, datasets, notebooks, dashboards, screenshots, tests and documentation.
Excluded generated databases and reports where they can be recreated by the pipeline.
Added individual README files for all 10 practicals.
👨‍💻 Author
Mukesh Karn

B.Sc. Data Science Student

Areas of Interest
Data Engineering
Data Analytics
Data Science
Python
SQL
Power BI
Big Data
Machine Learning
🔗 Repository
GitHub Repository:
https://github.com/Mukeshkarn-DS/Data-Engineering-Practical

⭐ Conclusion
This repository represents my hands-on learning journey through Data Engineering Practicals 01–10.

It covers the progression from basic file and database operations to API extraction, Business Intelligence, ETL, workflow orchestration, PySpark, incremental processing, data warehousing and end-to-end data pipelines.

The practicals demonstrate how different tools and technologies can be combined to understand and build structured Data Engineering workflows.

⭐ Thank You
Thank you for visiting my Data Engineering Practical Repository.

Learn → Build → Process → Test → Document → Improve 🚀
