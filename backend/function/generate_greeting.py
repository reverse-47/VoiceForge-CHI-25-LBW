from backend.map.infer import generate_embedding,get_most_similar_embedding
from backend.api.llm import getImpressionFromLLM, getGreetingTextFromLLM
from backend.function.generate_audio import getAudioFromTone
import base64
import numpy as np
import io
from scipy.io import wavfile
import torch
import torchaudio

GREETING = "Good morning, It's a pleasure to see you!"

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

def getGreetingFromMixedTimbre(ttsm, timbreList):
    greeting_data = {} 
    tone_ebd = getMixedTimbre(ttsm, timbreList)
    greeting_data['tone'] = tone_ebd.tolist()
    greeting_data['text'] = GREETING
    greeting_data['audio'] = getAudioFromTone(ttsm, tone_ebd, GREETING)
    return greeting_data

def getMixedTimbre(ttsm, timbreList):
    """
    混合多个音色的嵌入向量
    
    Parameters:
    ttsm: TTS 模型实例
    timbreList: 包含音频和权重的列表，格式如 [{"speech": "base64_audio", "weight": 0.5}, ...]
    
    Returns:
    mixed_embedding: 混合后的说话人嵌入向量
    """
    embeddings = []
    weights = []
    target_sr = 16000  # 目标采样率
    
    for item in timbreList:
        try:
            # 解码 base64 音频
            audio_bytes = base64.b64decode(item["speech"])
            
            # 将音频字节转换为文件对象
            audio_buffer = io.BytesIO(audio_bytes)
            
            # 使用 torchaudio 加载音频
            speech, sample_rate = torchaudio.load(audio_buffer)
            
            # 如果是立体声，转换为单声道
            speech = speech.mean(dim=0, keepdim=True)
            
            # 重采样到目标采样率（如果需要）
            if sample_rate != target_sr:
                assert sample_rate > target_sr, f'wav sample rate {sample_rate} must be greater than {target_sr}'
                speech = torchaudio.transforms.Resample(
                    orig_freq=sample_rate, 
                    new_freq=target_sr
                )(speech)
            
            # 获取说话人嵌入
            embedding = ttsm.get_spk_embedding(speech)
            embeddings.append(np.array(embedding))
            weights.append(item["weight"])
            
        except Exception as e:
            print(f"Error processing audio: {str(e)}")
            continue
    
    if not embeddings:
        raise ValueError("No valid embeddings generated")
    
    # 确保权重和为 1
    weights = np.array(weights)
    weights = weights / np.sum(weights)
    
    # 将嵌入向量转换为 numpy 数组并堆叠
    embeddings = np.stack(embeddings)
    
    # 根据权重混合嵌入向量
    mixed_embedding = np.sum(embeddings * weights[:, np.newaxis], axis=0)
    
    # 标准化混合后的嵌入向量
    mixed_embedding = mixed_embedding / np.linalg.norm(mixed_embedding)
    
    return mixed_embedding