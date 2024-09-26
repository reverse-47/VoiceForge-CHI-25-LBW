# import sys
# # 将路径添加到 sys.path
# sys.path.append("./backend/third_party/CosyVoice")
# sys.path.append("./backend/third_party/CosyVoice/third_party/Matcha-TTS")

from backend.som.infer import predict_embedding_weighted
from backend.api.llm import getImpressionFromLLM, getGreetingTextFromLLM
from backend.function.generate_audio import getAudioFromTone

def getGreetingFromText(llm, ttsm, input_text):
    greeting_data = {"text":"", "audio":""} 
    greeting_text = getGreetingTextFromLLM(llm, input_text)
    tone_ebd = getToneFromText(llm, input_text)
    greeting_data['text'] = greeting_text
    greeting_data['audio'] = getAudioFromTone(ttsm, tone_ebd, greeting_text)
    return greeting_data
    

def getToneFromText(llm, input_text):
    impression = getImpressionFromLLM(llm, input_text)
    tone_ebd = predict_embedding_weighted(impression, k=5)
    return tone_ebd