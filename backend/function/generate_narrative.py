import json
import backend.config as cfg
from backend.api.llm import getMarkedTextFromLLM
from backend.function.generate_audio import getAudioFromTone
import base64
import io
import numpy as np
import torch
import torchaudio

def getNarrativeAudioFromText(llm, ttsm, input_text, toneList):
   with open(cfg.DEFAULT_NARRATOR_PATH, 'r', encoding='utf-8') as file:
       data = json.load(file)
   
   defaultNarrator = data["naweilaite"]
   narratorTone = next((v for k, v in toneList.items() if k.lower() == "narrator" or k.lower() == "旁白"), defaultNarrator)
   
   markedList = getMarkedTextFromLLM(llm, input_text, toneList)
   
   all_audio_tensors = []
   sample_rate = 22050
   
   # 创建1秒静音
   silence_duration = sample_rate
   silence = torch.zeros(1, silence_duration)
   
   # 获取并处理每段音频
   for item in markedList:
       if item["speaker"] == "narrator":
           audio_base64 = getAudioFromTone(ttsm, narratorTone, item["text"])
       else:
           audio_base64 = getAudioFromTone(ttsm, toneList[item["speaker"]], item["text"])
       
       audio_bytes = base64.b64decode(audio_base64)
       audio_buffer = io.BytesIO(audio_bytes)
       waveform, sr = torchaudio.load(audio_buffer)
       all_audio_tensors.append(waveform)
   
   # 添加静音并拼接
   final_audio = []
   for i, tensor in enumerate(all_audio_tensors):
       final_audio.append(tensor)
       if i < len(all_audio_tensors) - 1:
           final_audio.append(silence)
           
   concatenated_audio = torch.cat(final_audio, dim=1)
   
   # 保存为WAV格式
   wav_buffer = io.BytesIO()
   torchaudio.save(wav_buffer, concatenated_audio, sample_rate, format="wav")
   wav_buffer.seek(0)
   
   # 转换为base64
   final_audio_base64 = base64.b64encode(wav_buffer.getvalue()).decode('utf-8')
   
   return final_audio_base64

def convertConversationToPrompt(conversation_list):
    prompt = ""
    for entry in conversation_list:
        if "user" in entry and entry["user"]:
            prompt += f"User: {entry['user']}\n"
        if "assistant" in entry and entry["assistant"]:
            prompt += f"Assistant: {entry['assistant']}\n"
    return prompt.strip()