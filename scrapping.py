import requests
from bs4 import BeautifulSoup
import time
import logging
import pandas as pd
from setting import TARGET_URL, REQUEST_TIMEOUT, USER_AGENT

logging.basicConfig(level=logging.INFO)
logger=logging.getlogger(__name__)

class WebScrapper:
    def __init__(self):
        self.session=requests.Session()
        self.session.header.update({'User-Agent':USER_AGENT})
        
    def scrap_hacker_news(self):
             
            logger.info(f"scraping data from {TARGET_URL}")
            response=self.session.get(TARGET_URL,timeout=REQUEST_TIMEOUT)

            response.raise_for_status()
            

            soup=BeautifulSoup(response.content,'html.parser')
            news_items=[]

            rows=soup.find_all('tr',class_='athing')

            for row in rows:
                try:
                    title_link=row.find('a',class_='title_link')
                    if title_link:
                        title_name=title_link.text
                        url=title_link.get('href','')

                        next_row=row.find_next_sibling('tr')
                        if next_row:
                            score_span=next_row.find('span',class_='score')
                            score=int(score_span.text.split()[0]) if score_span else 0


                            user_link=next_row.find('a',class_='hnuser')
                            link=user_link.text if user_link else 'Anonymus'

                            age_span=next_row.find('span',class_='age')
                            age=age_span.text if age_span else ''

                            news_items.append({ 
                                'title_name':title_name,
                                'url':url,
                                'score':score,
                                'link':link,
                                'age':age
                                'scrapedat':pd.TimeStamp.now()

                                         })
                except Exception as e:
                    logger.warning(f"Error parsing now {e}")

                continue
                logger.info(f"Successfully sacraped {len(news_items)} items from Hacker News")
                return pd.DataFrame(news_items)
            
             except request.RequestException as e:
            logger.error(f"Reqest fail : {e}")
            return pd.Dataframe()
         except exception as e:
    logger.error(f"Scraping error:{e}")
    return pd.DataFrame()