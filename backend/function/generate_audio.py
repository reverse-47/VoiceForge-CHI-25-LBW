import torchaudio
import torch
import io
import base64
from pydub import AudioSegment

def getAudioFromTone(ttsm, tone_ebd, text):
    if tone_ebd.ndim == 1:
        tone_ebd = tone_ebd.reshape(1, -1)

    tensor = torch.from_numpy(tone_ebd)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    tensor_cuda = tensor.to(device).float()   
    
    for i, j in enumerate(ttsm.inference_ebd(text, tensor_cuda, stream=False)):
         # 保存为OGG格式
        ogg_buffer = io.BytesIO()
        torchaudio.save(ogg_buffer, j['tts_speech'], 22050, format="ogg")
        ogg_buffer.seek(0)
        
        # 将OGG字节流编码为base64字符串
        audio_base64 = base64.b64encode(ogg_buffer.getvalue()).decode('utf-8')
        return audio_base64