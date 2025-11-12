# Initial Project Setup (Common):
1. data->raw
2. notebook
3. template.py
4. setup.py

# Workflow Steps for ml project(version 1):
1. Update the config.yaml -> Update the configuration for data ingestion & validation, eda, feature engineering and model training
2. Update the schema.yaml -> During data ingestion not required keep dummy key:value, during data validation it is required.
3. Update the params.yaml -> During data ingestion not required keep dummy key:value, during model training this is required.
4. Update the entity -> Return type of the function is first defined under research dataingestion.
4. Update the constant ->  Will contain the path of the constant yaml paths
5. Update the configuration manager in src config -> It will read the path of yaml file config, param and schema and create directory under __init__ constructor and has one more function get data ingestion fuction whose returrn type was earlier defined as an entity using dataclass library.
6. Update the components -> It will contain the data ingestion component that will contain the class of Data ingestion under which __init__ contains the Dataingestion configration (paths), and functions responsible for downloading file, and extracting zip file, request library here is used for downloading the data.
7. Update the pipeline -> Data Ingestion pipeline initializes the config object with configuration manager class, post that data ingestion component class is called within which methods of download_file and extract_zip_file is called. 
8. Update the main.py -> Import logger and pipeline to test data ingestion
9. Update the app.py

# MLOPS:
- It refers to the discipline of combining and streamlining machine learning system development(DEV) and machine learning operations(OPS). It involves collaboration between, data scientists, ML Enginneers and IT professionals to automate and optimize the end to end lifecycle of Machine Learning. 

# MLOPS main Components:
1. Data Management
2. Version Control (Code, Data)
3. Automation (CI/CD pipelines)
4. Experiment Tracking (Model)
5. CI/CD
6. Monitoring
7. Retraining

Data Source:
- API
- Web scraping
- s3 storage
- database

## 