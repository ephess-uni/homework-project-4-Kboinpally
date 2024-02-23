# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict

def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    reformated_dates = [datetime.strptime(old_date, "%Y-%m-%d").strftime('%d %b %Y') for old_date in old_dates]
    return reformated_dates

def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str):
        raise TypeError()
    if not isinstance(n, int):
        raise TypeError()
    dates_list = []
    strd = datetime.strptime(start, '%Y-%m-%d')
    for a in range(n):
        dates_list.append(strd + timedelta(days=a))
    return dates_list

def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    return list(zip(date_range(start_date, len(values)), values))

def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    columns = ("book_uid,isbn_13,patron_id,date_checkout,date_due,date_returned".
              split(','))
    fees_dict = defaultdict(float)
    with open(infile, 'r') as file:
        completedata = DictReader(file, fieldnames=columns)
        rows = [row for row in completedata]
    rows.pop(0)
    for row in rows:
        patronID = row['patron_id']
        date_due = datetime.strptime(row['date_due'], "%m/%d/%Y")
        date_returned = datetime.strptime(row['date_returned'], "%m/%d/%Y")
        delay = (date_returned - date_due).days
        fees_dict[patronID]+= 0.25 * delay if delay > 0 else 0.0   
    new_header = [
        {'patron_id': pn, 'late_fees': f'{fs:0.2f}'} for pn, fs in fees_dict.items()
    ]
    with open(outfile, 'w') as fl:
        writer = DictWriter(fl,['patron_id', 'late_fees'])
        writer.writeheader()
        writer.writerows(new_header)

# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
