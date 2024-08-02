from gradio_client import Client

def Chat(prompt:str="",system_prompt:str=""):
    client = Client("Qwen/Qwen1.5-110B-Chat-demo")
    result = client.predict(
    		api_name="/clear_session"
    )
    result = client.predict(
    		query=prompt,
    		history=[],
    		system=system_prompt,
    		api_name="/model_chat"
    )
    return result[1][0][-1]
