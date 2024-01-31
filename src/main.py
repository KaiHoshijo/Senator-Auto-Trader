import trade_scrape as ts
import constants

def write_data_to_file(filename, max_page):
    with open(filename, "a", newline="") as f:
        #writer.writerow(constants.COLUMNS)
        for page_num in range(1, max_page + 1):
            # Allow for parsing within the website
            soup = ts.get_page(page_num)
            # Getting each trade as a row
            rows = ts.get_trade_rows(soup)
            for row in rows:
                print(ts.get_info_on_row(row))

if __name__ == "__main__":
    max_page = int(ts.get_max_page())
    
    #write_data_to_file("data/trades.csv", 3)