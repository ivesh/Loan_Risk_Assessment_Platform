# Initial Project Setup (Common):
1. data->raw
2. notebook
3. template.py
4. setup.py

# Workflow Steps for ml project(version 1):
1. Update the config.yaml -> Update the configuration for data ingestion & validation, eda, feature engineering and model training
2. Update the schema.yaml -> During data ingestion not required keep dummy key:value
3. Update the params.yaml -> During data ingestion not required keep dummy key:value
4. Update the entity -> Return type of the function is first defined under research dataingestion.
4. Update the constant ->  Will contain the path of the constant yaml paths
5. Update the configuration manager in src config
6. Update the components
7. Update the pipeline
8. Update the main.py
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