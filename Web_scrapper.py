#Used for scrapping the contents from individual html pages from the local computer without any kind of request to the host
import pandas as pd
from bs4 import BeautifulSoup as bs

#Empty list to copy the data 

product_names = []
product_prices = []
product_links = []
product_stars = []
product_ratings = []
index=0
while True:

    cmd=input('Enter Y to continue : ')
    if cmd=='Y':
        index+=1
        ind=str(index)
        #In my scenario I placed everything in D drive and location is of the looks like D:\Amazon_data\A1.htm
        file_location='D:/Amazon_data/A'+ind+'.htm'        
        with open(file_location, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Parse the whole HTML content
        soup = bs(html_content, 'html.parser')

        # Find individual div's that contents the data 
        divs = soup.find_all('div', class_='sg-col-inner')

        # Extract data from each div
        for div in divs:
            # product name
            product_name = div.find('span', class_='a-size-medium a-color-base a-text-normal')
            product_name = product_name.get_text(strip=True) if product_name else " "

            # product price
            product_price = div.find('span', class_='a-price-whole')
            product_price = product_price.get_text(strip=True) if product_price else " "

            product_link = div.find('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
            if product_link:
                product_link = "https://www.amazon.in" + product_link['href']
            else:
                product_link = ' '

            # Extract stars and ratings
            product_stars_value = " "
            product_ratings_value = " "
            
            rating_div = div.find('div', class_='a-row a-size-small')
            if rating_div:
                product_stars_span = rating_div.find('span', attrs={'aria-label': lambda x: x and 'out of 5 stars' in x})
                product_ratings_span = rating_div.find('span', attrs={'aria-label': lambda x: x and 'ratings' in x})
                
                if product_stars_span:
                    product_stars_value = product_stars_span['aria-label']
                
                if product_ratings_span:
                    product_ratings_value = product_ratings_span['aria-label']

            product_names.append(product_name)
            product_prices.append(product_price)
            product_stars.append(product_stars_value)
            product_ratings.append(product_ratings_value)
            product_links.append(product_link)
        print(' page %d data inserted into the list'%index)
    else:
        break

# Create a DataFrame to copy the contents
data = {
    'Product Name': product_names,
    'Product Price': product_prices,
    'Product Stars': product_stars,
    'Product Ratings': product_ratings,
    'Product Link': product_links,
}
df = pd.DataFrame(data)

#converting datafrane to Excel file
#Thier should not be any kind of existing file
df.to_excel('Amazon_Products.xlsx', index=False)
