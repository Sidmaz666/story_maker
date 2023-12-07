import requests
import base64

def image2dataurl(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        image_data = base64.b64encode(response.content).decode('utf-8')
        data_url = f"data:image/{response.headers['Content-Type'].split('/')[1]};base64,{image_data}"
        return data_url
    else:
        print(f"Failed to fetch image from URL. Status code: {response.status_code}")
        return None
