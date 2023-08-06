# Trail db

A small demo library to save mlflow run data to a mongodb.
Prerequisite is using mlflow to track experiments.

# Installation

pip install traildb

# Get started

from traildb import DB_import

# Instantiate a DB_import object
db_imp = DB_import(URI, database_name, parent_name)

# Call the MLflow_to_db method after the mlflow run (not within the run)

with mlflow.start_run() as run: <br />
  ...your training code... <br />
db_imp.MLflow_to_db(mlflow.get_run(run_id=run.info.run_id), parent_id:"String", data_meta:{JSON})
