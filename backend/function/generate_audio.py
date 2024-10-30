import torchaudio
import torch
import io
import base64
import numpy as np
from pydub import AudioSegment

def getAudioFromTone(ttsm, toneEbd, text):
    tone_ebd = np.array(toneEbd)
    if tone_ebd.ndim == 1:
        tone_ebd = tone_ebd.reshape(1, -1)

    tensor = torch.from_numpy(tone_ebd)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    tensor_cuda = tensor.to(device).float()   
    
    for i, j in enumerate(ttsm.inference_ebd(text, tensor_cuda, "", stream=False)):
         # 保存为WAV格式
        wav_buffer = io.BytesIO()
        torchaudio.save(wav_buffer, j['tts_speech'], 22050, format="wav")
        wav_buffer.seek(0)
        
        # 将OGG字节流编码为base64字符串
        audio_base64 = base64.b64encode(wav_buffer.getvalue()).decode('utf-8')
        return audio_base64
    
def getWavFromTone(ttsm, toneEbd, text, save_path):
    # 处理音色向量
    tone_ebd = np.array(toneEbd)
    if tone_ebd.ndim == 1:
        tone_ebd = tone_ebd.reshape(1, -1)
    
    # 转换为torch tensor并移到适当设备
    tensor = torch.from_numpy(tone_ebd)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    tensor_cuda = tensor.to(device).float()
    
    # 生成音频
    for i, j in enumerate(ttsm.inference_ebd(text, tensor_cuda, "", stream=False)):
        # 直接保存为WAV文件
        torchaudio.save(
            save_path,
            j['tts_speech'],
            22050,
            format="wav"
        )
        break  # 只保存第一个生成的音频