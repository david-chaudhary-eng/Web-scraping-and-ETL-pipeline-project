import pandas as pd
import logging
import os
from datetime import datetime
from scrapping import WebScrapper
from transformer import DataTransformer
from loader import S3_loader
from data_quality import DataQualityChecker
from setting import OUTPUT_DIR,CSV_FILE_NAME,PARQUET_FILE_NAME

logger=logging.getlogger(__name__)

def ensure_output_directive():
    """Create output directive if it doesnot exists"""
    os.makedirs(OUTPUT_DIR,exists_ok=True)

def run_etl_pipeline():
    """Maintain etl pipeline"""
    logger.info(f"Starting ETL pipeline Now ") 

    scraper=WebScrapper()
    loader=S3_loader()
    transformer=DataTransformer()
    quality_checker=DataQualityChecker()

    try:
        # Step1 Scraping the data
        logger.info("Just started the data to scrab")
        raw_data=scraper.scrap_hacker_news()

        if raw_data.empty:
            logger.error("Data is empty try next time hero")

        # Step 2 data Transform 
        logger.info("Started to clean the data")
        transformed_data=transformer.transform_data(raw_data)

        # Step 3 Data Quality Check
        logger.info("Started to check the entiredata")
        quality_passed=quality_checker.run_all_checks(transformed_data)
        if not quality_passed:
            logger.error("Data quality checks failed. Aborting ETL process.")

        # step 4 Load
        ensure_output_directive()

        # Save file locally
        csv_path=os.path.join(OUTPUT_DIR,CSV_FILE_NAME)
        parquet_path=os.path.join(OUTPUT_DIR,PARQUET_FILE_NAME)

        transformed_data.to_csv(csv_path,index=False)
        transformed_data.to_parquet(parquet_path,index=False)

        logger.info(f"File is saved lically in the dir {csv_path}{parquet_path}")

        # Upload S3
        timestamp=datetime.now().strftime("%Y%M%D%_%H%M%S%")
        s3_csv_key=f"hacker_news_data_/{timestamp}/ {CSV_FILE_NAME}"
        s3_parquet_key=f"hacker_news_data_/{timestamp}/ {PARQUET_FILE_NAME}"

        if loader.create_bucket_if_not_exists():
            csv_uploaded=loader.uplaod_file(csv_path,s3_csv_key)
            parquet_uploaded=loader.uplaod_file(parquet_path,s3_parquet_key)

            if csv_uploaded and parquet_uploaded:
                logger.info("ETL completed successfully")
            else:
                logger.error("ETL failed haha")
        else:
            logger.error("Failed now what to do hehe")
            return False
        
    

    except Exception as e:
        logger.error(f"ETL pipeline failed due to {e}")             
