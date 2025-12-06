import pandas as pd
import re # regular expression model for text processing and pattern matching
import logging

logger=logging.ggetlogger(__name__)

from datetime import datetime

class DataTransformer:
    def __init__(self):
        self.processed_count=0

    def clean_text(self,text):
            """"Clean and nnormalize text data"""
            if pd.isna(text):
                return ""
            
            text=re.sub(r'\s+','',str(text)).strip()

            return text
        
    def extract_domain(self,url):
            """Extract domain from URL"""
            if pd.isna(url) or not url.startswith('http'):
                return ""
            try:
                from urllib.parse import urlparse
                domain=urlparse(url).netloc 
                return domain.replace('www.','')
            

            except Exception as e:
                return ""
            
    def parse_age(self,age_text):
            """Parse age text to minutes"""
            if pd.isna(age_text):
                return None
            
            try:
                if 'minute' in age_text:
                    return int(re.search(r'\d',age_text).group(1))
                elif 'hour' in age_text:
                    return int(re.search(r'\d',age_text).group(1))*60
                elif 'day' in age_text:
                    return int(re.search(r'\d',age_text).group(1))*60*24
                else:
                    return None

            except Exception as e:   
                return None
    def transform_data(self,df):
            """Apply all transform data in this""" 
            if df.empty:
                logger.warning(f"data is empty")
                return df
            logger.info(f"starting the data transform")
            df_clean=df.copy()

            df_clean['title']=df_clean['title'].fillna('No itle')
            df_clean['url']=df_clean['url'].fillna('')
            df_clean['score']=df_clean['score'].fillna(0)
            df_clean['user']=df_clean['user'].fillna('Anonymous')

            df_clean['title']=df_clean['title'].apply(self.clean_text)
            df_clean['user']=df_clean['user'].apply(self.clean_text)

            df_clean['domain']=df_clean['url'].apply(self.extract_domain)

            df_clean['age_minute']=df_clean['age'].apply(self.parse_age)

            initial_count=len(df_clean)
            df_clean=df_clean.drop_dublicates(subset=['title','url'])
            dublicate_removed=initial_count-len(df_clean)

            df_clean['has_url']=df_clean['url'].str.startswith('http')
            df_clean['title_length']=df_clean['title'].str.len()

            df_clean['score']=df_clean['score'].astype(int)
            df_clean['scraped_at']=pd.to_datetime(df_clean['scraped_at'])

            self.processed-count=len(df_clean)
            logger.info(f"data transformation completed. Processed {self.processed_count} records, removed {dublicate_removed} dublicates")

            return df_clean
