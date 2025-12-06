import boto3
import os
import logging
from setting import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, S3_BUCKET_NAME
from botocore.exceptions import ClientError

logger=logging.getlogger(__name__)

class S3_loader:
    def __init__(self):

        self.s3_clent=self._initiaize_s3_client()
        self.bucket_name=S3_BUCKET_NAME

    def _initialize_s3_client(self):
            """Initialize the s3 client"""

            try:
                session=boto3.session(

                    aws_access_key=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    region_name=AWS_REGION
                        )
                return session.client('s3')

            except Exception as e:
                logger.error(f"Failed to initialize :{e}")

                return None

    def create_bucket_if_not_exists(self):
            """Create a bucket"""
            try:
                self.s3_clent.head_bucket(Bucket=self.bucket_name)
                logger.info(f"Bucket {self.bucket_name} already exists")
                return True

            except ClientError:
                try:
                    if AWS_REGION=="us-east-1"
                       self.s3_client.create_bucket(Bucket=self.bucket_name)
                       
                    else :
                         self.s3_client.create_bucket(
                        Bucket=self.bucket_name,
                       CreateBucketConfiguration={'LocationConstraint':AWS_REGION}
                      )
                    logger.info(f"Just created the bucket named {self.bucket_name}")
                    return True
            
                
                except ClientError as e:
                    logger.error(f"Failed o create  bucket {e}")
                    return False

    def uplaod_file(self,file_path,s3_key):
                """Upload the file which is loaced inside a device"""
                try:
                    if not os.path.exists(file_path):
                        logger.error(f"File does not exists")
                        return False
                    
                    else:
                        self.s3_client.uplaod_file(file_path,self.bucket_name,s3_key)
                        logger.info(f"File {file_path} has be successfully uplaoded to s3 bucket anem{self.bucket_name} through s3_key{s3_key} ")
                        return True

                except ClientError as e:
                    logger.error(f"Failed to upload the file {e}")
                    return False

    def uplaod_df(self,df,s3_key,format='parquet'):
                """Upload the dataframe to s3 bucket"""
                try:
                    if format=='parquet':
                        csv_buffer=df.to_parquet(index=False)
                        content_type='application/parquet'

                    else:
                        csv_buffer=df.to_csv(index=False)
                        content_type='text/csv'

                    self.s3_client.put_object(
                        Bucket=self.bucket_name,
                        Key=s3_key,
                        Body=csv_buffer,
                        ContentType=content_type

                    )      
                    logger.info(f"Data frame has being successfully uploaded to s3")

                    return True
                except Exception as e:
                   logger.error(f"Error just happened as uploading to s3 :{e}")
                   return False
                