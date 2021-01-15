from urllib2 import urlopen  # for Python 3: from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv


def get_tablerows(URL, series_label = "7"):
    """ Scrapes table from /Series_X URL, works for most series """

    soup = BeautifulSoup(urlopen(URL),features="html.parser")
    all_tables = soup.findAll("table", {"class":"article-table"})
    if len(all_tables) == 0:
        all_tables = soup.findAll("table", id="collapsibleTable0")
    table = all_tables[0]

    output_rows = []
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        output_row = [series_label]
        for column in columns:
            # Append column value with some string cleanup applied...
            #output_row.append(column.text.encode('utf-8').rstrip().replace("/\xc2/\xa",""))
            output_row.append(column.text.replace(u'\xa0', u'').replace(u'\xc2', u'').encode('utf-8').rstrip())
        if len(output_row) == 1:
            continue
        output_rows.append(output_row)

    return output_rows



def get_tablerows_old(table, series_label = "7"):
    """ Scrapes tables from the large compiled page """

    output_rows = []
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        output_row = [series_label]
        for column in columns:
            output_row.append(column.text.replace(u'\xa0', u'').replace(u'\xc2', u'').encode('utf-8').rstrip())
        if len(output_row) == 1:
            continue
        output_rows.append(output_row)

    return output_rows



def main():
    # Parse individual Series pages
    series_list = [2, 3, 5, 6, 9, 10, 12, 13]
    all_rows = [["Series", "Episode", "AirDate", "Chaser", "Contribution", "Result"]]
    for s in series_list:
        all_rows += get_tablerows( "https://the-chase.fandom.com/wiki/Series_{}".format(s), series_label = s)
    with open('data/newformat_chase.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(all_rows)

    # Parse Many Page URL
    all_rows = [["Series", "Episode", "AirDate", "Chaser", "P1", "P2", "P3", "P4", "Result"]]
    URL = "https://the-chase.fandom.com/wiki/The_Chase_(List_of_Issues)#Series_1_-_June_29.2C_2009_-_July_10.2C_2009_-_10_Episodes"
    soup = BeautifulSoup(urlopen(URL),features="html.parser")
    all_rows += get_tablerows_old( soup.findAll("table", id="collapsibleTable1")[1], series_label = "7")
    all_rows += get_tablerows_old( soup.findAll("table", id="collapsibleTable1")[2], series_label = "8")
    all_rows += get_tablerows_old( soup.findAll("table", {"class":"article-table"})[-2], series_label = "11")
    with open('data/oldformat_chase.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(all_rows)
        
        
if __name__ == "__main__":
    main()
