import os
import random
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from src.model_list import models
from src.sampler_list import samples
from src.chat import Chat
from src.image import Image, default_model, default_sampler


app = Flask(__name__,static_url_path="/",static_folder="src/ui")
CORS(app)

def random_number():
    return random.randint(0, 500000000)

@app.route("/api/custom", methods=['POST'])
def Custom():
    data = request.get_json()['prompt']
    res = Chat(data).replace("</s>","")
    return jsonify({"data":res})

@app.route("/api/plot", methods=['POST'])
def Plot():
    data = request.get_json()['prompt']
    seed = random_number()
    format = "(Plot:{plot})"
    plot = Chat(f"I want you to write a short profound,unique,exciting,interesting and logical plot for a story of {data} in a specific format {format}. \"{seed}\" This is the number that represents the uniqueness of the plot,plot structure, and plot topics. DO NOT SHOW THE NUMBER IN THE PLOT OR IN YOUR RESPONSE!!! DO NOT SHOW THE UNIQUE NUMBER!!!.").replace("</s>","")
    return jsonify({"data":plot})

@app.route("/api/story", methods=['POST'])
def Story():
    data = request.get_json()['prompt']
    seed = random_number()
    format = "(Story:{story})"
    story = Chat(f"I want you to write a detail,profound,unique,exciting,interesting and logical story for the following plot: \n{data}\n Write the story in a specific format {format}\n. \"{seed}\" This is the number that represents the uniqueness of the story,story structure,story environment, story characters names and story topics, DO NOT SHOW THE NUMBER IN THE STORY!!!.").replace("</s>","")
    return jsonify({"data":story})

@app.route("/api/continue", methods=['POST'])
def ContinueStory():
    data = request.get_json()['prompt']
    seed = random_number()
    format = "(Story:{story})"
    story = Chat(f"I want you to continue writing or expanding a detail,profound,unique,exciting,interesting and logical story for the following half story: \n{data}\n Write the story in a specific format {format}\n. \"{seed}\" This is the number that represents the uniqueness of the story,story structure,story environment, story characters names and story topics, DO NOT SHOW THE NUMBER IN THE STORY!!!.").replace("</s>","")
    return jsonify({"data":story})

@app.route("/api/character", methods=['POST'])
def CharacterDesign():
    data = request.get_json()['prompt']
    seed = random_number()
    format = "(Character:{character_name,character_age,character_gender,character_personality})"
    character = Chat(f"I want you to design characters of living,non-living,individual or groups by extracting all the characters and give them proper name(only if character name is not mentioned in the story), personality, age(give a proper age to every character even if the character is non-living object, THE AGE CANNOT BE UNKNOWN!!!) and gender from the following story: \n{data}\n Write the Characters in a specific format {format}\n. \"{seed}\" This is the number that represents the uniqueness of the characters name(Come up with a Character name if does not exist!), age, gender and personality, DON'T SHOW THE UNIQUE NUMBER!!!!, DO NOT SHOW THE NUMBER IN THE Characters OR IN YOUR RESPONSE!!! DO NOT SHOW THE UNIQUE NUMBER!!!.").replace("</s>","")
    return jsonify({"data":character})

@app.route("/api/character_detail", methods=['POST'])
def CharacterDetail():
    data = request.get_json()['prompt']
    seed = random_number()
    format = "(CharacterDetail:{character_detail})"
    character = Chat(f"I want you tell every possible detail about a characters of living,non-living,individual or groups by analyzing the character and give them proper height, weight, body shape, skin color, face shape, hair type, hair color, hair length, eyes shape, eyes color, eyes size, mouth shape size and color and much more facial and body detail for the following character: \n{data}\n Write the CharacterDetail in a specific format {format}\n. \"{seed}\" This is the number that represents the uniqueness of the character detail, DO NOT SHOW THE NUMBER IN THE CharacterDetail!!!.").replace("</s>","")
    return jsonify({"data":character})

@app.route("/api/environment", methods=['POST'])
def EnvironmentDesign():
    data = request.get_json()['prompt']
    seed = random_number()
    format = "(Environment:{environment_name,environment_terrain,environment_colors,environment_lights,environment_objects}"
    environments = Chat(f"I want you to design an environment by extracting all the possible environments and give them proper name(only if environment name is not mentioned in the story), environment terrain, environment colors, environment lights and environment objects from the following story: \n{data}\n Write the Environment in a specific format {format}\n. \"{seed}\" This is the number that represents the uniqueness of the Environment name, terrain, colors, lights and objects, DO NOT SHOW THE NUMBER IN THE Environments OR IN YOUR RESPONSE!!! DO NOT SHOW THE UNIQUE NUMBER!!!.").replace("</s>","")
    return jsonify({"data":environments})

@app.route("/api/img", methods=['POST'])
def GenerateImage():
    prompt = request.get_json()['image_prompt']
    nprompt = request.get_json()['image_negative_prompt']
    model = request.get_json()['image_model']
    sampler = request.get_json()['image_sample']
    width = int(request.get_json()['image_width'])
    height = int(request.get_json()['image_height'])
    sample_step = int(request.get_json()['image_sampling_step'])
    cfg = int(request.get_json()['image_cfg'])
    seed = int(request.get_json()['image_seed'])
    img = Image(prompt,nprompt,model,sample_step,sampler,cfg,width,height,seed)
    return jsonify({ "url": img })

@app.route("/api/list")
def Options():
    return jsonify({"models" : models, "sampler" : samples, "default_model":default_model,"default_sampler":default_sampler})

@app.route("/")
def ServeUI():
    return send_file('src/ui/index.html')

@app.errorhandler(404)
def page_not_found(error):
    return send_file('src/ui/404.html')

if __name__ == '__main__':
    app.run(debug=True)

