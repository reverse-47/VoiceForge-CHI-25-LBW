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
        tone_ebd = get_most_similar_embedding(base)
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
    text = "Hello, it's a pleasure to see you today."
    generate_all_combinations(text, cfg.TTS_MODEL_PATH)