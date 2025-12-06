# Web-scraping-and-ETL-pipeline-project
A complete data engineering pipeline that automatically extracts, transforms, and loads web data to the cloud. 

1. Data Extraction (scrapping.py)
   <br>
    Scrapes Hacker News homepage for news articles
             <br>
    Extracts: Titles, URLs, Scores, Users, Timestamps
             <br>
     Implements error handling and rate limiting
              <br>
      Returns structured pandas DataFrame
               <br>
               <br>
 2. Data Transformation (transformer.py)
                     <br>
    Text Cleaning: Removes extra whitespace, normalizes text
                   <br>
     URL Processing: Extracts domain names
                           <br>
     Time Parsing: Converts age text to minutes
                         <br>
    Deduplication: Removes duplicate entries
                  <br>
         Feature Engineering: Adds metadata columns (has_url, title_length)
                       <br>
                       <br>
 3. Data Quality (data_quality.py)
                <br>
        Row Count Validation: Ensures minimum data threshold
                <br>
         Null Value Checks: Validates critical columns
                   <br>
        Data Type Verification: Confirms column types match expectations
                   <br>
        Completeness Scoring: Calculates overall data quality score

4. Cloud Storage (loader.py)
        <br>
         AWS S3 Integration: Uploads to cloud storage
           <br>
         Bucket Management: Creates S3 buckets if needed
             <br>
         File Upload: Supports CSV and Parquet formats
             <br>
         Error Handling: Robust upload failure management
