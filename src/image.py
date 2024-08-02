import os
from gradio_client import Client

image_api="prodia/sdxl-stable-diffusion-xl"
default_model="sd_xl_base_1.0.safetensors [be9edd61]"
default_sampler="DPM++ 2M Karras"

def Image(prompt:str="",nprompt:str="",model:str=default_model,
          steps:int=20,sampler:str=default_sampler,cfg:int=7,
          width:int=1024,height:int=1024,seed:int=-1):
    client = Client("prodia/sdxl-stable-diffusion-xl")
    result = client.predict(
    		prompt,
    		nprompt,
    		model,
    		steps,
    		sampler,
    		cfg,
    		width,
    		height,
    		seed,
    		api_name="/flip_text"
    )
    return f'https://prodia-sdxl-stable-diffusion-xl.hf.space/file={result}'
