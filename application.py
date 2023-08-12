import requests
import re
import csv
from bs4 import BeautifulSoup

def get_reviews(url):
    
    response = requests.get(url, verify=False)

    soup = BeautifulSoup(response.content, 'html.parser')


    reviews = []
    
    review_elements = soup.find_all('div', class_='aMaAEs')


    for review_element in review_elements:

        # Extract name, rating, title, and review text

        name = review_element.find('span', class_='B_NuCI').text.strip()

        rating = review_element.find('div', class_='_3LWZlK').text.strip()

        num_of_ratings = review_element.find('span', class_='_2_R_DZ').text.strip()
        
        discount = ''.join(re.findall('\d', review_element.find('div', class_='_1V_ZGU').text))
        
        after_discount = review_element.find('div', class_='_30jeq3 _16Jk6d').text.strip().replace('₹', '')
        
        before_discount = review_element.find('div', class_='_3I9_wc _2p6lqe').text.strip().replace('₹', '')
        
        packaging_fee = ''.join(re.findall('\d+', review_element.find('div', class_='wjKmXL').li.text))
 

        comment = review_element.find('div', class_='t-ZTKy')

        reviews.append({

            'Name': name,

            'Rating': rating,

            'Num of Ratings': num_of_ratings,
            
            'discount': discount,
            
            'after discount':  after_discount,
            
            'before discount': before_discount,
            
            'packaging_fee': packaging_fee
        })
        

    return reviews

 
def write_to_csv(reviews, filename):

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:

        fieldnames = ['Name', 'Rating', 'Num of Ratings', 'discount', 'after discount', 'before discount', 'packaging_fee']#, 'Title', 'Comment'

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        

        writer.writeheader()
        

        for review in reviews:

 

            writer.writerow(review)

 

if __name__ == '__main__':

 

    url = "https://www.flipkart.com/apple-iphone-14-midnight-256-gb/p/itmdb32e3c997112?pid=MOBGHWFH4H3MMRAA&lid=LSTMOBGHWFH4H3MMRAAO7KNHD&marketplace=FLIPKART&q=iphone+14&store=tyy%2F4io&srno=s_1_7&otracker=AS_QueryStore_OrganicAutoSuggest_2_2_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_2_2_na_na_na&fm=organic&iid=1517749c-d38c-4400-b134-017a72926e01.MOBGHWFH4H3MMRAA.SEARCH&ppt=hp&ppn=homepage&ssid=i9dn1fty280000001691084028479&qH=860f3715b8db08cd"

 
    reviews = get_reviews(url)

    csv_filename = 'reviews.csv'


    write_to_csv(reviews, csv_filename)


    print(f"Reviews written to {csv_filename}")