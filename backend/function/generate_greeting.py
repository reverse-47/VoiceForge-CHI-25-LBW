# import sys
# # 将路径添加到 sys.path
# sys.path.append("./backend/third_party/CosyVoice")
# sys.path.append("./backend/third_party/CosyVoice/third_party/Matcha-TTS")

from backend.map.infer import generate_embedding,get_most_similar_embedding
from backend.api.llm import getImpressionFromLLM, getGreetingTextFromLLM
from backend.function.generate_audio import getAudioFromTone

def getGreetingFromText(llm, ttsm, input_text):
    greeting_data = {} 
    greeting_text = getGreetingTextFromLLM(llm, input_text)
    tone_ebd = getToneFromText(llm, input_text)
    greeting_data['tone'] = tone_ebd.tolist()
    greeting_data['text'] = greeting_text
    greeting_data['audio'] = getAudioFromTone(ttsm, tone_ebd, greeting_text)
    return greeting_data
    

def getToneFromText(llm, input_text):
    impression = getImpressionFromLLM(llm, input_text)
    tone_ebd = generate_embedding(impression, k=3)
    # tone_ebd = get_most_similar_embedding(impression)
    return tone_ebd