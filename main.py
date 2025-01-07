import sys
sys.path.append("./backend/third_party/CosyVoice")
sys.path.append("./backend/third_party/CosyVoice/third_party/Matcha-TTS")
from flask import Flask, render_template
from flask import request
from backend.third_party.CosyVoice.cosyvoice.cli.cosyvoice import CosyVoice
from backend.third_party.CosyVoice.cosyvoice.utils.file_utils import load_wav
from backend.function.generate_greeting import getGreetingFromText, getGreetingFromMixedTimbre
from backend.function.generate_reply import getReplyFromText
import backend.config as cfg
from openai import OpenAI

app = Flask(__name__)

llm = OpenAI(api_key=cfg.OPENAI_API_KEY)
ttsm = CosyVoice(cfg.TTS_MODEL_PATH)

# 首页面
@app.route("/")
def index():
	return render_template('index.html')

@app.route('/getGreeting',methods=['POST'])
def getGreeting():
    data = request.json
    inputText = data['inputText']
    data = getGreetingFromText(llm, ttsm, inputText)
    return data

@app.route('/getMix',methods=['POST'])
def getMix():
    data = request.json
    timbreList = data['timbreList']
    data = getGreetingFromMixedTimbre(ttsm, timbreList)
    return data


@app.route('/getReply',methods=['POST'])
def getReply():
    data = request.json
    inputText = data['inputText']
    personality = data['personality']
    lastConversation = data['lastConversation']
    toneEbd = data['toneEbd']
    data = getReplyFromText(llm, ttsm, inputText, personality, lastConversation, toneEbd)
    return data

if __name__ == '__main__':
	# 启动多线程参数，加快资源请求，快速响应用户
	app.run(debug = False, host='0.0.0.0', port=5000, threaded = True)
    # generate_step()