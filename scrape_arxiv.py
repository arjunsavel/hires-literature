import argparse
import time
from datetime import date, timedelta

import arxivscraper
import numpy as np
import pandas as pd

necessary_keywords = ['exoplanet', 'atmosphere']

keywords = ['high-resolution', 'high resolution', 'hi-res', 'high-dispersion',
            'high dispersion', ' HRS ', ' HDS ']

COLS = ('id', 'title', 'categories', 'abstract', 'doi', 'created',
        'updated', 'authors', 'affiliation', 'url')


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


def scrape_window(date_from, date_until, label):
    """
    Scrapes astro-ph between two dates (inclusive), saves any hires candidates
    to data/potential_hires_papers_{label}.csv, and returns how many it found.
    """
    scraper = arxivscraper.Scraper(
        category='physics:astro-ph',
        date_from=date_from.strftime('%Y-%m-%d'),
        date_until=date_until.strftime('%Y-%m-%d'),
        filters={'abstract': ['exoplanet']})
    output = scraper.scrape()

    # arxivscraper doesn't return a list when nothing matches (e.g. weekends)
    if not isinstance(output, list) or len(output) == 0:
        return 0

    df = pd.DataFrame(output, columns=COLS)
    check_hires(df)
    hires_frame = df[df['hires?'] == True]

    if len(hires_frame) != 0:
        hires_frame.to_csv(f'data/potential_hires_papers_{label}.csv')
    return len(hires_frame)


def backfill(start, end, pause=5):
    """
    Runs the scraper once per day from start to end (inclusive).
    Days with no hires candidates produce no file, same as the daily cron.
    """
    failed = []
    day = start
    while day <= end:
        label = day.strftime('%Y-%m-%d')
        try:
            n = scrape_window(day, day, label)
            print(f'{label}: {n} hires candidates')
        except Exception as e:
            print(f'{label}: FAILED ({e})')
            failed.append(label)
        time.sleep(pause)  # be polite to the arXiv OAI server
        day += timedelta(days=1)

    if failed:
        print('\nThese days failed; rerun them individually:')
        print('\n'.join(failed))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--backfill', nargs=2, metavar=('START', 'END'),
                        help='date range to backfill, YYYY-MM-DD YYYY-MM-DD (inclusive)')
    args = parser.parse_args()

    if args.backfill:
        start, end = (date.fromisoformat(d) for d in args.backfill)
        backfill(start, end)
    else:
        # original daily behaviour
        yesterday = date.today() - timedelta(days=1)
        scrape_window(yesterday, date.today(), yesterday.strftime('%Y-%m-%d'))
