import sys
sys.path.append("./backend/third_party/CosyVoice")
sys.path.append("./backend/third_party/CosyVoice/third_party/Matcha-TTS")
import torchaudio
from backend.third_party.CosyVoice.cosyvoice.cli.cosyvoice import CosyVoice
from backend.third_party.CosyVoice.cosyvoice.utils.file_utils import load_wav
import backend.config as cfg
from aip import AipSpeech
from pydub import AudioSegment
import os
import json

# 替换为您的 API 密钥信息
APP_ID = '115921972'
API_KEY = 'cX8At8LZ6buRFmBLTYRZG4Q8'
SECRET_KEY = 'FdvBiaNkkKaUU3sgc309oInofP7vsnQl'
GREETING = "Good morning, I hope this day finds you well. It's a pleasure to see you today!"

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

def preprocess_audio_for_baidu(input_file, output_file=None, max_duration=60):
    try:
        # 加载音频文件
        audio = AudioSegment.from_file(input_file)
        
        # 如果未指定输出文件名，则自动生成
        if output_file is None:
            base, ext = os.path.splitext(input_file)
            output_file = f"{base}_processed{ext}"
        
        # 转换为单声道
        audio = audio.set_channels(1)
        
        # 设置采样率为16kHz
        audio = audio.set_frame_rate(16000)
        
        # 设置位深度为16位
        audio = audio.set_sample_width(2)
        
        # 如果音频长度超过max_duration秒，则只保留前max_duration秒
        if len(audio) > max_duration * 1000:
            audio = audio[:max_duration * 1000]
        
        # 导出处理后的文件
        audio.export(output_file, format="wav")
        
        print(f"预处理完成。处理后的文件保存为: {output_file}")
        return output_file
    
    except Exception as e:
        print(f"预处理音频文件时发生错误: {str(e)}")
        return None

# 读取音频文件
def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()

# 识别本地文件
def recognize_speech(file_path):
    # 读取文件
    audio_data = get_file_content(file_path)
    
    # 发送识别请求
    result = client.asr(audio_data, 'wav', 16000, {
        'dev_pid': 1737,  # 1737 表示英语
    })
    
    # 解析结果
    if result['err_no'] == 0:
        return result['result'][0]
    else:
        return f"Error: {result['err_no']}, {result['err_msg']}"

def getEbdFromFile(ttsm, file_name):
    prompt_speech_16k = load_wav(cfg.WAV_INPUT_PATH+file_name, 16000)
    # result = recognize_speech(cfg.WAV_INPUT_PATH+file_name)
    # print(result+'\n')
    # for i, j in enumerate(ttsm.inference_zero_shot(GREETING, result, prompt_speech_16k, stream=False)):
    #     torchaudio.save(cfg.WAV_OUTPUT_PATH+file_name.format(i), j['tts_speech'], 22050)
    embedding = ttsm.get_spk_embedding(prompt_speech_16k)
        
    # 准备新数据
    file_id = file_name.replace('.wav', '')
    new_data = {
        "ebd": embedding
    }
    
    with open(cfg.CHARACTER_ORIGIN_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # 添加新数据
    data[file_id] = new_data
    
    # 保存回JSON文件
    with open(cfg.CHARACTER_ORIGIN_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
if __name__ == '__main__':
    cosyvoice = CosyVoice('./backend/third_party/CosyVoice/pretrained_models//CosyVoice-300M')
    for filename in os.listdir(cfg.WAV_INPUT_PATH):
        if filename.endswith('.wav'):
            print(filename+'\n')
            # processed_file = preprocess_audio_for_baidu(cfg.WAV_INPUT_PATH+filename, cfg.WAV_INPUT_PATH+filename)
            getEbdFromFile(cosyvoice, filename)