import time
import spacy
from flask import Flask, render_template
from flask import request
from sentence_transformers import SentenceTransformer
from backend.configure import LLM, TALK_LLM, NLP, EBD_MODEL, MODEL_PATH
from backend.Model.model import GenerationModel
# from backend.dataloader import load_object, load_skill, load_task
from backend.llm import GetTextReply
import ChatTTS
from IPython.display import Audio
import torch
import torchaudio
# from backend.deal_step import GenerateStep

app = Flask(__name__)

llm = GenerationModel(LLM)
# nlp = spacy.load(NLP)
ebd_model = SentenceTransformer(EBD_MODEL)
chat = ChatTTS.Chat()
chat.load()

# 首页面
@app.route("/")
def index():
	return render_template('index.html')

@app.route('/getTextReply',methods=['POST'])
def getTextReply():
    data = request.json
    inputText = data['inputText']
    personality = data['personality']
    lastConversation = data['lastConversation']
    data = GetTextReply(llm, inputText, personality, lastConversation)
    return data

@app.route('/getAudioReply', methods=['POST'])
def getAudioReply():
	data = request.json
	inputText = data['inputText']
	fileName = data['fileName']
	texts = [inputText,]
	wavs = chat.infer(texts, )
	torchaudio.save(fileName, torch.from_numpy(wavs[0]), 24000)
	return fileName

if __name__ == '__main__':
	# 启动多线程参数，加快资源请求，快速响应用户
	app.run(debug = False, host='0.0.0.0', port=5000, threaded = True)
    # generate_step()