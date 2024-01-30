import trade_scrape as ts

if __name__ == '__main__':
    max_page = int(ts.get_max_page())
    for page_num in range(1, max_page + 1):
        print(f"Current Page: {page_num}")
        # Allow for parsing within the website
        soup = ts.get_page(page_num)
        # Getting each trade as a row
        rows = ts.get_trade_rows(soup)
        for row in rows:
            ts.get_info_on_row(row)