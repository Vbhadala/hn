from typing import Union
import requests
from bs4 import BeautifulSoup


from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

# Assuming 'soup' is your BeautifulSoup object
def get_meta_property(soup, property_name):
    tag = soup.find("meta", {"property": property_name})
    return tag["content"] if tag else None

def get_all_images(soup):

    images = soup.find_all('img')
    image_urls = []
    for image in images:
        image_src = (
            image.get("src") or 
            image.get("data-src") or 
            image.get("data-lazy") or 
            image.get("data-original")
        )

        if image_src:
            image_urls.append(image_src)

    return image_urls
    

@app.get("/")
def read_root():
    return {"message":  "Welcome to home notes backend API"}


@app.post('/api')
def scrap_images(url= 'https://www.drench.co.uk/p/harbour-acclaim-rimless-wm-pan-soft-close-seat'):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")


        image_urls = get_all_images(soup)

        # Extract values
        og_title = get_meta_property(soup, "og:title")
        price_amount = get_meta_property(soup, "product:price:amount")
        og_image = get_meta_property(soup, "og:image")
        og_site_name = get_meta_property(soup, "og:site_name")

        # Return the list of image URLs as a JSON response
        return JSONResponse(content={'og title': og_title,
                                    'price amount': price_amount,
                                    'og image': og_image,
                                    'og site name': og_site_name,
                                    "image_urls": image_urls})
        
    except requests.exceptions.RequestException as e:
        # Handle any request exceptions
        return {"error": str(e)}

