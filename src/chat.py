from gradio_client import Client
chat_api="vilarin/ollama-Chat"

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
		message=prompt,
		model="qwen2:0.5b",
		temperature=tmp,
		max_new_tokens=tokens,
		top_p=top,
		top_k=20,
		penalty=rep,
		api_name="/chat"
    )
    return result
