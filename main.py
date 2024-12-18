from typing import Optional

from fastapi import FastAPI

app = FastAPI()


from typing import Union
import requests
from bs4 import BeautifulSoup


from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
def read_root():
    return {"message":  "Welcome to home notes backend API"}


@app.post('/api')
def scrap_images(url= 'https://www.drench.co.uk/p/harbour-acclaim-rimless-wm-pan-soft-close-seat'):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
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
        
        # Return the list of image URLs as a JSON response
        return JSONResponse(content={"image_urls": image_urls})
        
    except requests.exceptions.RequestException as e:
        # Handle any request exceptions
        return {"error": str(e)}

