# import sys
# # 将路径添加到 sys.path
# sys.path.append("./backend/third_party/CosyVoice")
# sys.path.append("./backend/third_party/CosyVoice/third_party/Matcha-TTS")

from backend.map.infer import generate_embedding,get_most_similar_embedding
from backend.api.llm import getImpressionFromLLM, getGreetingTextFromLLM
from backend.function.generate_audio import getAudioFromTone, getWavFromTone
import sys
sys.path.append("./backend/third_party/CosyVoice")
sys.path.append("./backend/third_party/CosyVoice/third_party/Matcha-TTS")
from backend.third_party.CosyVoice.cosyvoice.cli.cosyvoice import CosyVoice
import backend.config as cfg
import numpy as np

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

def generate_wav_with_impressions(ttsm, text, base_impression, varying_index, varying_values):
    """
    Generate multiple wav files by varying a specific impression value.
    
    Args:
        ttsm: CosyVoice model instance
        text: Text to be converted to speech
        base_impression: Base impression array (length 9)
        varying_index: Index of the impression to vary
        varying_values: List of values to try for the varying impression
    """
    base = base_impression.copy()
    for value in varying_values:
        # Update the specific impression value
        base[varying_index] = value
        # Generate embedding
        tone_ebd = generate_embedding(base, k=3)
        # Generate filename based on the pattern
        filename = f"{int(base[0])}{int(base[1])}{'5' if varying_index != 2 else str(int(value))}.wav"
        # Generate wav file
        getWavFromTone(ttsm, tone_ebd, text, filename)

def generate_all_combinations(text, model_path):
    """
    Generate all combinations of voice impressions.
    
    Args:
        text: Text to be converted to speech
        model_path: Path to the TTS model
    """
    # Initialize the TTS model
    ttsm = CosyVoice(model_path)
    
    # Define the values to try
    varying_values = [1, 4, 7, 10]
    
    # Base impressions for first varying digit = 3
    base_impression_3 = np.array([3, 5, 5, 5, 5, 5, 5, 5, 6])
    
    # Generate combinations with first digit = 3
    # Vary second digit
    generate_wav_with_impressions(ttsm, text, base_impression_3, 1, varying_values)
    # Vary third digit
    generate_wav_with_impressions(ttsm, text, base_impression_3, 2, varying_values)
    
    # Base impressions for first varying digit = 1
    base_impression_1 = np.array([1, 5, 5, 5, 5, 5, 5, 5, 6])
    
    # Generate combinations with first digit = 1
    # Vary second digit
    generate_wav_with_impressions(ttsm, text, base_impression_1, 1, varying_values)
    # Vary third digit
    generate_wav_with_impressions(ttsm, text, base_impression_1, 2, varying_values)

if __name__ == "__main__":
    text = "hi, it's a pleasure to see you tody"
    generate_all_combinations(text, cfg.TTS_MODEL_PATH)
    # ttsm = CosyVoice(cfg.TTS_MODEL_PATH)
    # impression = np.array([3, 1, 5, 5, 5, 5, 5, 5, 6])
    # tone_ebd = generate_embedding(impression, k=3)
    # getWavFromTone(ttsm, tone_ebd, text, '315.wav')
    # impression = np.array([3, 4, 5, 5, 5, 5, 5, 5, 6])
    # tone_ebd = generate_embedding(impression, k=3)
    # getWavFromTone(ttsm, tone_ebd, text, '345.wav')
    # impression = np.array([3, 7, 5, 5, 5, 5, 5, 5, 6])
    # tone_ebd = generate_embedding(impression, k=3)
    # getWavFromTone(ttsm, tone_ebd, text, '375.wav')
    # impression = np.array([3, 10, 5, 5, 5, 5, 5, 5, 6])
    # tone_ebd = generate_embedding(impression, k=3)
    # getWavFromTone(ttsm, tone_ebd, text, '3105.wav')
    # impression = np.array([3, 5, 1, 5, 5, 5, 5, 5, 6])
    # tone_ebd = generate_embedding(impression, k=3)
    # getWavFromTone(ttsm, tone_ebd, text, '351.wav')
    # impression = np.array([3, 5, 4, 5, 5, 5, 5, 5, 6])
    # tone_ebd = generate_embedding(impression, k=3)
    # getWavFromTone(ttsm, tone_ebd, text, '354.wav')
    # impression = np.array([3, 5, 7, 5, 5, 5, 5, 5, 6])
    # tone_ebd = generate_embedding(impression, k=3)
    # getWavFromTone(ttsm, tone_ebd, text, '357.wav')
    # impression = np.array([3, 5, 10, 5, 5, 5, 5, 5, 6])
    # tone_ebd = generate_embedding(impression, k=3)
    # getWavFromTone(ttsm, tone_ebd, text, '3510.wav')
    # impression = np.array([1, 1, 5, 5, 5, 5, 5, 5, 6])
    # tone_ebd = generate_embedding(impression, k=3)
    # getWavFromTone(ttsm, tone_ebd, text, '115.wav')
    # impression = np.array([1, 4, 5, 5, 5, 5, 5, 5, 6])
    # tone_ebd = generate_embedding(impression, k=3)
    # getWavFromTone(ttsm, tone_ebd, text, '145.wav')
    # impression = np.array([1, 7, 5, 5, 5, 5, 5, 5, 6])
    # tone_ebd = generate_embedding(impression, k=3)
    # getWavFromTone(ttsm, tone_ebd, text, '175.wav')
    # impression = np.array([1, 10, 5, 5, 5, 5, 5, 5, 6])
    # tone_ebd = generate_embedding(impression, k=3)
    # getWavFromTone(ttsm, tone_ebd, text, '1105.wav')
    # impression = np.array([1, 5, 1, 5, 5, 5, 5, 5, 6])
    # tone_ebd = generate_embedding(impression, k=3)
    # getWavFromTone(ttsm, tone_ebd, text, '151.wav')
    # impression = np.array([1, 5, 4, 5, 5, 5, 5, 5, 6])
    # tone_ebd = generate_embedding(impression, k=3)
    # getWavFromTone(ttsm, tone_ebd, text, '154.wav')
    # impression = np.array([1, 5, 7, 5, 5, 5, 5, 5, 6])
    # tone_ebd = generate_embedding(impression, k=3)
    # getWavFromTone(ttsm, tone_ebd, text, '157.wav')
    # impression = np.array([1, 5, 10, 5, 5, 5, 5, 5, 6])
    # tone_ebd = generate_embedding(impression, k=3)
    # getWavFromTone(ttsm, tone_ebd, text, '1510.wav')