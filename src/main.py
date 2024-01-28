import trade_scrape as ts

if __name__ == '__main__':
    # Allow for parsing within the website
    soup = ts.get_data()
    # Getting each trade as a row
    rows = ts.get_trade_rows(soup)

    # Printing out the number of trades that I can work with
    print(f'Total number of trades is {len(rows)}')
    # Ensuring that all the columns can be scraped properly
    row = rows[0]
    print(f'Name:             {ts.get_name(row)}')
    print(f'Traded Issue:     {ts.get_traded_issuer(row)}')
    print(f'Published:        {ts.get_published(row)}')
    print(f'Traded:           {ts.get_traded(row)}')
    print(f'Gap:              {ts.get_trade_gap(row)}')
    print(f'Owner:            {ts.get_owner(row)}')
    print(f'Type:             {ts.get_type(row)}')
    print(f'Size:             {ts.get_size(row)}')
    print(f'Price:            {ts.get_price(row)}')