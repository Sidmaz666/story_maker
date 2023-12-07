from gradio_client import Client
chat_api="hf4all/mistral-7b-fast-chat"

def Chat(prompt:str="",tmp:float=0.7,tokens:int=1024,top:float=0.95,rep:float=1.1):
    if tmp > 1:
        tmp = 1
    if tokens > 1024:
        tokens = 1024
    if top > 1:
        top = 1
    if rep > 2:
        rep = 2
    client = Client(src=chat_api,verbose=False)
    result = client.predict(
        prompt,	
        tmp,	
        tokens,
        top,	
        rep,	
        api_name="/chat"
    )
    return result
