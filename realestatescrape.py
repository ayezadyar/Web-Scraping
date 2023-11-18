import requests
from bs4 import BeautifulSoup

def scrape_zillow_data(url, headers):
    try:
        data = requests.get(url, headers=headers)
        data.raise_for_status()  # Raise an HTTPError for bad requests

        soup = BeautifulSoup(data.text, 'lxml')

        address = soup.find_all('address', {'data-test': 'property-card-addr'})
        price = soup.find_all('span', {'data-test': 'property-card-price'})

        adr = [result.text for result in address]
        pr = [result.text for result in price]

        print("Num of addresses : ",len(adr))
        print("Num of prices : ",len(pr))


        if len(adr) != len(pr):
            raise ValueError("Error: Lists have different lengths.")

        with open("zillow.csv", "w") as f:
            f.write("Address; Price;\n")

        for i in range(len(adr)):
            with open("zillow.csv", "a") as f:
                f.write(str(adr[i]) + "; " + str(pr[i]) + "\n")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Set the URL and headers
url = 'https://www.zillow.com/kalispell-mt/'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
           'referer': 'https://www.zillow.com/'}

# Call the scraping function
scrape_zillow_data(url, headers)
