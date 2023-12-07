import os
from gradio_client import Client
image_api="zenafey/fast-stable-diffusion"
default_model="absolutereality_v181.safetensors [3d9d4d2b]"
default_sampler="DPM++ 2M"

def Image(prompt:str="",nprompt:str="",model:str=default_model,
          step:int=25,sampler:str=default_sampler,cfg:int=7,
          width:int=512,height:int=512,seed:int=-1,bc:int=1):
    client = Client(src=image_api,serialize=False,verbose=False,output_dir=os.getcwd())
    job = client.submit(
	prompt,#Prompt
  	nprompt, #Negative Prompt
  	model, #Model
  	step, #Sampling Steps
    sampler, #Sampling Method
    cfg, #CFG Scale
    width, #Width
    height, #Height
    seed, #Seed
    bc, #Batch Count
  	fn_index=42
    )

    while not job.done():
        result = job.result()
        return result['value'][0]['name']

