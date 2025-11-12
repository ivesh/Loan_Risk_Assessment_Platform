from mlProject.config.configuration import ConfigurationManager
from mlProject.components.eda_and_data_transformation import EDA_and_DataTransformation
from mlProject import logger


STAGE_NAME = "Data Validation stage"

class DataTansformationPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_trans_config = config.get_data_transformation_config()
        transformer = EDA_and_DataTransformation(config=data_trans_config)
        transformer.run_eda_and_transformation()
        print("EDA, charts, feature engineered data, train/test files saved under appropriate artifact paths.")





if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataTansformationPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e

