# What is this project?
This project is an automatic finance trader that will follow what senators are
trading and buy/sell the corresponding stocks. It's merely an experiment to
see how much money one could make through following the stocks being traded
by those in office.
---
# How is this project getting this data?
After the STOCK act was passed, those in office needed to publish which stocks
were being bought and sold. The website that I am using to scrape this data is
https://www.capitoltrades.com/
---
# How are the trades illustrated within each row?
For each row (each one represents its own trade), there are the following columns:
    - Politician -- The name of the politician performing the trade
    - Traded Issuer -- The name of the stock or bond being purchased
    - Published -- When the trade was actually released to the public
    - Traded -- When the politician performed the trade
    - Filed After -- How many days after trading was it published
    - Owner -- Who actually owns the stock (Self, Spouse, or Undisclosed)
    - Type -- Whether they bought or sold the stock
    - Size -- The size of trade being sold, which ranges from 1K up to 50M
    - Price -- The price of the stock
---
# How is the columns stored within the actual website?
On the website, each row is stored within a tr header with the class 'q-tr.'
The following is how each column is stored within the website:
    - Politician -- h3 with class 'q-fieldset politician-name' with the name
                    in the preceding a header
    - Traded Issuer -- h3 with class 'q-fieldset issuer-name' with the name
                       in the preceding a header. Additionally, the ticker
                       is stored in span header with class
                       'q-field issuer-ticker'
    - Published -- Within td with class 'q-td q-column--pubDate, the year is
                   stored in a div header with class 'q-label' while the date
                   is stored in a div header with class 'q-value'
    - Traded -- Same as published but td has class 'q-td q-clumn--txDate'
    - Filed After -- Within td with class 'q-td q-column--reportingGap' with
                     the period stored in the div header with 'q-label' while a
                     span header with class 'reporting-gap-tier--1' stores the
                     actual amount of the designated time period 
    - Owner -- Within td with class 'q-td q-column--owner' and stored in the
               span header with 'q-label'
    - Type -- Within td with class 'q-td q-column--txType' and stored in the
              span with class 'q-field tx-type tx-type--sell/buy' where the
              buy/sell is based on the type
    - Size -- Within td with class 'q-td q-column--value' and stored in span
              with class 'q-label' and posted as a range, such as 15Kû50K
    - Price -- Within span with class 'q-field trade-price'
---
# DISCLAIMER:
No responsibility for if you use this and lose any money from it. Again, this
is just an experiment to see if one could follow all the stocks being traded
and make a profit.