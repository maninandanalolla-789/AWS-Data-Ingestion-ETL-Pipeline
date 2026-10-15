# AWS Data Ingestion and ETL Pipeline

An end-to-end, production-grade cloud data engineering pipeline designed to ingest, validate, transform, and orchestrate multi-client batch data. This architecture utilizes **AWS serverless computing**, **PySpark big data processing**, and **Infrastructure as Code (IaC)** to deliver scalable, event-driven data workflows.

---

## 🏗️ Architecture Overview

The pipeline implements a robust, automated workflow moving raw client assets into analytical layers:
1. **Ingestion Layer:** Multi-client batch source files (CSV, JSON) are securely uploaded to customized **Amazon S3** landing zones.
2. **Event-Driven Processing:** S3 upload triggers an **AWS Lambda** function to run initial structural, file-name, and schema validations.
3. **Queueing & Auditing:** Validated records/metadata pass through **Amazon SQS** and **Amazon SNS** for microservice messaging, auditing, and real-time operational status monitoring.
4. **ETL & Transformation Layer:** An orchestrated **AWS Glue** Spark job pulls data from S3, applies heavy transformations (using **PySpark** / **Pandas**), applies rigorous business rules, and loads data efficiently.
5. **Storage Layer:** Cleaned, analytical datasets are written directly into target **Amazon RDS (PostgreSQL/MySQL)** and **Amazon Aurora** relational databases for down-stream analytics.
6. **CI/CD & Infrastructure:** Managed entirely using **AWS CloudFormation** templates and deployed automatically via **AWS CodePipeline**.

---

## 🛠️ Technical Stack

* **Cloud Infrastructure (AWS):** S3, Lambda, Glue, SQS, SNS, Aurora, RDS (PostgreSQL/MySQL), EventBridge, Secrets Manager
* **Languages & Scripting:** Python, SQL, Shell Scripting (Bash)
* **Libraries & Data Frameworks:** PySpark (Spark SQL & DataFrames), Pandas, Boto3, SQLAlchemy
* **DevOps & CI/CD:** AWS CloudFormation, AWS CodePipeline, Git/GitHub

---

## ⚙️ Key Optimization & Engineering Highlights

* **Cost Optimization:** Implemented dynamic scaling and partition pruning techniques inside **AWS Glue (PySpark)** scripts, resulting in significant runtime reductions and optimized DPUs compute costs.
* **Resilient Data Quality Framework:** Designed custom validation modules checking for required fields, exact file structures, and data type alignment before triggering database inserts.
* **Automated Failure Recovery:** Configured dead-letter queues (DLQ) via **Amazon SQS** alongside comprehensive **Amazon SNS** alerting to immediately notify engineering squads when pipelines fail.
* **Secure Secret Management:** Extracted database credentials, tokens, and endpoints out of codebase files by natively integrating **AWS Secrets Manager**.

---

## 📂 Repository Structure

```text
├── cloudformation/
│   ├── infrastructure.yaml      # AWS CloudFormation IaC templates for S3, SQS, Lambda, Glue
│   └── pipeline-deploy.yaml     # CI/CD definition for AWS CodePipeline
├── src/
│   ├── lambda/
│   │   ├── file_validator.py    # Ingestion validation and processing triggers
│   │   └── alert_notifier.py    # Audit logging and SNS notification handling
│   ├── glue/
│   │   └── pyspark_etl.py       # Main PySpark processing, transformation, and database load script
│   └── utils/
│       ├── database.py          # SQLAlchemy target database connector modules
│       └── helpers.py           # Reusable data cleansing algorithms
├── sql/
│   └── target_schema.sql        # Core DDL scripts for PostgreSQL/MySQL destination databases
├── tests/
│   └── test_etl.py              # Local testing suites for data quality scripts
├── requirements.txt             # Python environment dependencies
└── README.md                    # Project documentation
```

---

## 🚀 Setup & Deployment

### 1. Prerequisites
* [AWS CLI v2](https://aws.amazon.com/cli/) configured with administrative credentials.
* Python 3.10+ and a functional local PySpark setup for testing.

### 2. Infrastructure as Code (IaC) Deployment
Deploy all core serverless cloud infrastructure elements to your active AWS account:
```bash
aws cloudformation deploy \
  --template-file cloudformation/infrastructure.yaml \
  --stack-name aws-data-pipeline-stack \
  --capabilities CAPABILITY_IAM
```

### 3. Local Testing Execution
Run internal Python automation test scripts to verify business rules before committing script revisions:
```bash
pip install -r requirements.txt
python -m unittest discover tests/
```

---

## 📑 License and Disclaimer
This repository is built for professional review and educational demonstrations.
_This is for informational purposes only. For medical advice or diagnosis, consult a professional. AI responses may include mistakes._
