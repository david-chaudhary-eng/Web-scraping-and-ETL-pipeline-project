import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

logger=logging.getlogger(__name__)

class DataQualityChecker:

    def __init__(self , min_rows=1 , max_null_percentage=10):
          self.min_rows=min_rows
          self.max_null_percentage=max_null_percentage
          self.checks_passed=0
          self.total_checks=0

    def check_row_count(self,df,expected_min=None):
          """Check if the dataframe has at least the minimum number of """

          self.total_checks+=1
          min_rows=expected_min or self.min_rows

          if len(df)>=min_rows:
               logger.info(f"So there is the no. of rows which we can proceed now")

               return True
          else:
               logger.error(f"There is no much rows to proceed the process")
               return False
          
    def check_null_values(self,df,critical_columns=None):
         """Checking the presence of thr null value in the data set"""   

         self.total_checks+=1
         critical_columns=critical_columns or ['url','title']

         null_report={}
         all_passed=True

         for column in critical_columns:
              if column in df.columns:
                   null_count=df[column].isnull().sum()
                   null_percentage=(null_count / len(df))*100
                   null_report[column]=null_percentage

                   if null_percentage>self.max_null_percentage:
                        logger.error(f"Null percentage {null_percentage} exceeded the max null percentage")
                        all_passed=False
                   else:
                        logger.info(f"Null check passed ")

                        if all_passed:
                             self.checks_passed+=1
                             return all_passed , null_report

    def check_data_types(self,df,expected_types):
              """Check if required type is available or not"""
              self.total_checks+=1
              type_issues=[]

              for column,expected_type in expected_types.items():
                   if column in df.columns:
                        actual_type=str(df[column].dtype)
                        if expected_type not in actual_type:

                         type_issues.append(f"{column}:ecpected {expected_type} got {actual_type}")

                         if not type_issues:
                              logger.info(f"Data type check passed")
                              self.checks_passed+=1
                              return True, type_issues
                         else:
                              for issue in type_issues:
                                   logger.error(f"Issue in type {type_issues}")
                                   return False

    def generate_quality_repot(df,self):

              report={
                   'total_rows':len(df),
                   'total_coumns':len(df.columns),
                   'checks_passed':f"{self.checks_passed /self.total_checks}",
                   'completeness_score':(self.checks_passed / self.total_checks) * 100 if self.total_checks > 0 else 0

              }            
              for column in df.columns:
                   report[f'{column}_null_count'] = df[column].isnull().sum()
                   report[f'{column}_null_percentage']=(df[column].isnull().sum() / len(df)) *100 

                   logger.info(f"The null report is{report['checks_passed']} out of {report['total_checks']} checks passed")
                   return report
    def run_all_checks(self,df):  
         """Run all data quality checks"""
         logger.info("Run all data quality checks")

         #Defined expected data type
         expected_types={
              'title'      : 'object',
              'score'      :'string',
              'scraped_at' :'daetime'
         }

         # Run checks
         self.check_row_count(df)
         self.check_null_values(df)
         self.check_data_types(df,expected_types)

         # Generate fina report
         report=self.generate_quality_report(df)

         return report['completeness_score']>=80




                            

                   



