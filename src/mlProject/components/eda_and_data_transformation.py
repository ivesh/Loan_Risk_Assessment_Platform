import os
import numpy as np
import pandas as pd
from mlProject import logger
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

class EDA_and_DataTransformation:
    def __init__(self, config):
        self.config = config

    def load_data(self):
        data = pd.read_csv(self.config.read_data_path)
        logger.info(f"Loaded data from {self.config.read_data_path}")
        return data

    # --- EDA Functions ---

    def univariate_analysis(self, df):
        # Numerical
        num_cols = df.select_dtypes(include=np.number).columns
        for col in num_cols:
            plt.figure()
            sns.histplot(df[col], kde=True)
            plt.title(f'Distribution of {col}')
            plt.savefig(os.path.join(self.config.eda_report_path, f'{col}_hist.png'))
            plt.close()
        # Categorical
        cat_cols = df.select_dtypes(include='object').columns
        for col in cat_cols:
            plt.figure()
            df[col].value_counts().plot(kind='bar')
            plt.title(f'Value counts of {col}')
            plt.savefig(os.path.join(self.config.eda_report_path, f'{col}_bar.png'))
            plt.close()
        logger.info("Univariate EDA charts saved.")

    def bivariate_analysis(self, df, target='emi_eligibility'):
        for col in df.select_dtypes(include=np.number).columns:
            plt.figure()
            sns.boxplot(x=df[target], y=df[col])
            plt.title(f'{col} by {target}')
            plt.savefig(os.path.join(self.config.eda_report_path, f'{col}_by_{target}_box.png'))
            plt.close()
        logger.info("Bivariate EDA charts saved.")

    def correlation_analysis(self, df):
        corr = df.select_dtypes(include=np.number).corr()
        plt.figure(figsize=(12,10))
        sns.heatmap(corr, annot=False, cmap='coolwarm')
        plt.title('Correlation Heatmap')
        plt.savefig(os.path.join(self.config.eda_report_path, 'correlation_heatmap.png'))
        plt.close()
        logger.info("Correlation heatmap saved.")

    def outlier_summary(self, df, cols):
        summary = {}
        for col in cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lb = Q1 - 1.5 * IQR
            ub = Q3 + 1.5 * IQR
            outliers = df[(df[col]<lb) | (df[col]>ub)][col].count()
            summary[col] = outliers
        logger.info(f"Outlier summary: {summary}")
        return summary

    # --- Feature Engineering / Data Transformation ---
    def feature_engineering(self, df):
        df['debt_to_income'] = df['current_emi_amount'] / (df['monthly_salary'] + 1)
        expense_cols = [
            'monthly_rent','school_fees','college_fees','travel_expenses',
            'groceries_utilities','other_monthly_expenses'
        ]
        df['expense_to_income'] = df[expense_cols].sum(axis=1) / (df['monthly_salary'] + 1)
        df['affordability_score'] = (df['monthly_salary'] - df[expense_cols].sum(axis=1) - df['current_emi_amount']) / (df['monthly_salary'] + 1)
        
        def credit_risk(score):
            if score >= 750: return 'Excellent'
            elif score >= 700: return 'Good'
            elif score >= 650: return 'Fair'
            else: return 'Poor'
        df['credit_risk_category'] = df['credit_score'].apply(credit_risk)
        df['employment_stability'] = df['years_of_employment'] / (df['age'] + 1)
        df['income_credit_interaction'] = df['monthly_salary'] * df['credit_score']
        df['loan_to_income'] = df['requested_amount'] / ((df['monthly_salary'] + 1) * 12)
        logger.info("Feature engineering calculated.")

        # Outlier capping and scaling
        iqr_cols = ['monthly_salary','years_of_employment','monthly_rent','college_fees',
                    'travel_expenses','groceries_utilities','other_monthly_expenses',
                    'current_emi_amount','credit_score','bank_balance','emergency_fund',
                    'requested_amount','requested_tenure','max_monthly_emi']
        for col in iqr_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            df[col] = np.where(df[col] < lower, lower, np.where(df[col] > upper, upper, df[col]))
        logger.info("IQR capping complete.")

        scale_cols = iqr_cols
        scaler = StandardScaler()
        df[scale_cols] = scaler.fit_transform(df[scale_cols])
        logger.info("Standard scaling complete.")

        # Encoding
        for col in ['gender', 'marital_status', 'existing_loans']:
            df[col+'_enc'] = LabelEncoder().fit_transform(df[col])
        df = pd.get_dummies(df, columns=['education','employment_type','company_type','house_type','emi_scenario','credit_risk_category'], drop_first=True)
        logger.info("Encoding complete.")

        # Save feature engineered data
        df.to_csv(self.config.fe_file_path, index=False)
        logger.info(f"Feature engineered data saved to {self.config.fe_file_path}")
        return df

    # --- Train/Test Splitting ---
    def train_test_spliting(self, df):
        train, test = train_test_split(df, test_size=0.25, random_state=42)
        train.to_csv(self.config.transformed_train_data, index=False)
        test.to_csv(self.config.transformed_test_data, index=False)
        logger.info(f"Train shape: {train.shape}, Test shape: {test.shape}")
        return train, test

    # --- Main runner (for pipeline) ---
    def run_eda_and_transformation(self):
        df = self.load_data()
        os.makedirs(self.config.eda_report_path, exist_ok=True)
        self.univariate_analysis(df)
        self.bivariate_analysis(df)
        self.correlation_analysis(df)
        outlier_summary = self.outlier_summary(df, ['monthly_salary', 'years_of_employment', 'monthly_rent'])
        df_fe = self.feature_engineering(df)
        train, test = self.train_test_spliting(df_fe)
        logger.info("EDA and data transformation pipeline complete.")