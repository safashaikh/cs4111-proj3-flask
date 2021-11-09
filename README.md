# Project 1 Part 3 README

## Authors
- Bharathi Saravanabhavan: bs3363
- Safa Shaikh: ss2620

## Postgres DB
- Account: bs3363
- URI: postgresql://bs3363:<password>@35.196.73.133/proj1part2

## Deployed URL
- URL = 'http://35.237.138.209:8111'

## Features
All features from the proposal were implemented. This app serves as a dashboard
for users to view the E-Commerce system. Think of it as an admin portal for users to monitor
E-Commerce activity. 

Some of the features implemented:
 - Users can view their personal details and update them as well.
 - Users can view their orders and details such as total paid, taxes, etc.
 - Users can view the items associated with each order
 - Users can view where their orders will be shipped to and by whom
 - Users can view what credit card was used to pay for the order
 - Users can view what products are available and search by vendor
 - We provide some relevant metrics about the E-commerce system as well
    - Vendor most purchased from
    - Most frequently bought product
    - Most liked product (determined by # of cart adds)
    
## Interesting Features
 - Search bars on every page to search items. For example, for products you can search by name and for orders you can
  search by order id. On the backend this is doing LIKE queries to search for various rows.
 - Orders are displayed relative to a customer and displays orders from most recent to oldest. The orders query joins 
 practically every table to produce meaningful results. In addition, it does a couple subqueries to query from 
 ItemOrders to compute a subtotal of all items ordered. This information isn't immediately available to users, 
 so the query is actually an interesting one.
 - You can click on an order to see what items were purchased, in what quantity, and with what card payment was made 
 and the shipment ID and shipper. Again this query does a handful of joins on the table to present meaningful information
 to the user.
 - User details can be modified with an easy to use form and save button.
 - Metrics page. We have a metrics page that shows various information such as the most purchased items, most liked
 items, and most popular vendors. This uses some mroe complicated aggregation queries to determine meaningful
 metrics basically in real time.
