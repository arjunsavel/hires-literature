import arxivscraper
import pandas as pd

import numpy as np
from datetime import date
from datetime import timedelta

necessary_keywords = ['exoplanet', 'atmosphere']

keywords = ['high-resolution', 'high resolution', 'hi-res', 'high-dispersion', 
            'high dispersion', ' HRS ', ' HDS ']

def check_hires_row(row):
    """
    checks whether a paper might be a hires paper based on what's in the abstract.
    """
    abstract = row['abstract']
    hires = 0
    necessary_hires = 0
    for keyword in necessary_keywords:
        if keyword in abstract:
            necessary_hires += 1
            
    for keyword in keywords:
        if keyword in abstract:
            hires += 1
    return necessary_hires == len(necessary_keywords) and hires >= 1
    
    
def check_hires(frame):
    hires = []
    for i, row in frame.iterrows():
        hires += [check_hires_row(row)]
    frame['hires?'] = hires
    
if __name__=='__main__':
    today = date.today().strftime("%Y-%m-%d")
    yesterday = (date.today() - timedelta(days = 1)).strftime("%Y-%m-%d")

    scraper = arxivscraper.Scraper(
    category='physics:astro-ph', 
    date_from=yesterday, date_until=today,
    filters={'abstract':['exoplanet']})
    output = scraper.scrape()
    print(output)
    cols = ('id', 'title', 'categories', 'abstract', 'doi', 'created', 'updated', 'authors', 'affiliation', 'url')
    df = pd.DataFrame(output,columns=cols)
    check_hires(df)
    hires_frame = df[df['hires?']==True]
  
    if len(hires_frame) != 0:
        hires_frame.to_csv(f'data/potential_hires_papers_{yesterday}.csv')
    
    
