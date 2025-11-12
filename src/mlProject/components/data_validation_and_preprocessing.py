import os
from mlProject import logger
from mlProject.entity.config_entity import DataValidationConfig
import pandas as pd
import numpy as np

class DataValidation:
    def __init__(self, config:DataValidationConfig):
        self.config = config

    def validate_column_types(self, data):
        schema_types = self.config.all_schema
        mismatches = []
        for col, dtype in schema_types.items():
            if col not in data.columns:
                mismatches.append((col, "missing", dtype))
            elif str(data[col].dtype) != dtype:
                mismatches.append((col, str(data[col].dtype), dtype))
        return mismatches

    def summarize_uniques(self, data):
        summary = {}
        for col in data.columns:
            vals = np.unique(data[col].astype(str))
            nr_values = len(vals)
            if nr_values <= 45:
                summary[col] = f"{nr_values}: {vals.tolist()}"
            else:
                summary[col] = f"{nr_values} unique"
        return summary

    def convert_numerics(self, data):
        for col in ['age', 'monthly_salary', 'bank_balance']:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce')
        logger.info("✓ Data type conversion completed")
        return data

    def check_missing(self, data):
        missing_data = data.isnull().sum()
        missing_percent = (missing_data / len(data)) * 100
        missing_df = pd.DataFrame({'Missing_Count': missing_data, 'Percentage': missing_percent})
        logger.info(f"Missing data summary:\n{missing_df[missing_df['Missing_Count'] > 0]}")
        return missing_df

    def standardize_categories(self, data):
        gender_map = {'F': 'Female', 'FEMALE': 'Female', 'Female': 'Female', 
                      'M': 'Male', 'MALE': 'Male', 'Male': 'Male',
                      'female': 'Female', 'male': 'Male'}
        if 'gender' in data.columns:
            data['gender'] = data['gender'].map(gender_map)
        edu_map = {'Professional': 'Professional', 'Post Graduate': 'Post Graduate',
                   'Graduate': 'Graduate', 'High School': 'High School'}
        if 'education' in data.columns:
            data['education'] = data['education'].map(edu_map).fillna(data['education'].mode()[0])
        for col in ['employment_type', 'company_type', 'house_type', 'marital_status', 'emi_scenario']:
            if col in data.columns:
                data[col] = data[col].astype(str).str.title()
        logger.info("✓ Category standardization completed")
        return data

    def impute_missing(self, data):
        num_cols_with_na = ['age','monthly_salary','monthly_rent', 'credit_score', 'bank_balance', 'emergency_fund']
        cat_cols_with_na = ['education']
        for col in num_cols_with_na:
            if col in data.columns:
                median_val = data[col].median()
                data[col].fillna(median_val, inplace=True)
        for col in cat_cols_with_na:
            if col in data.columns:
                mode_val = data[col].mode()[0]
                data[col].fillna(mode_val, inplace=True)
        logger.info("✓ Missing value imputation completed")
        return data

    def run_full_validation(self):
        try:
            status_report = {}
            data = pd.read_csv(self.config.unzip_data_dir)

            # 1. Column type validation
            col_type_mismatches = self.validate_column_types(data)
            status_report['column_types'] = col_type_mismatches
            status_report['column_types_msg'] = (
                "Column validation passed" if not col_type_mismatches else f"Type mismatches: {col_type_mismatches}"
            )

            # 2. Check unique values for all features
            uniques = self.summarize_uniques(data)
            status_report['uniques'] = uniques

            # 3. Data type conversions
            data = self.convert_numerics(data)

            # 4. Missing summary before imputation
            missing_before = self.check_missing(data)
            status_report['missing_before'] = missing_before

            # 5. Categorical standardization
            data = self.standardize_categories(data)
            status_report['category_standardization_msg'] = "Category standardization complete"

            # 6. Imputation for missing values
            data = self.impute_missing(data)
            missing_after = self.check_missing(data)
            status_report['missing_after'] = missing_after

            status_report["missing_msg"] = (
                "All missing values handled" if missing_after['Missing_Count'].sum() == 0 else "Missing values remain"
            )

            # 7. Info and value check of main categoricals
            status_report['data_info'] = str(data.info())
            for col in data.select_dtypes(include='object').columns:
                status_report[col+'_final_values'] = data[col].unique().tolist()

            # 8. Save cleaned data to correct artifacts location
            data.to_csv(self.config.cleaned_file_path, index=False)
            logger.info("✓ Final cleaned data saved for EDA and pipeline progression")

            # 9. Final status log
            status_report['final_status'] = "SUCCESS" if (
                not col_type_mismatches and missing_after['Missing_Count'].sum() == 0
            ) else "FAIL"
            status_report['final_status_msg'] = (
                "Validation and preprocessing successful!"
                if status_report['final_status'] == "SUCCESS"
                else "Check type/missing value errors above."
            )

            # Save status to validation status file
            with open(self.config.STATUS_FILE, 'w') as f:
                for key, val in status_report.items():
                    f.write(f"{key}: {val}\n")
            return status_report

        
        except Exception as e:
            raise e
