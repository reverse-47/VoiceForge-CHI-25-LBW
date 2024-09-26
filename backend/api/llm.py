from backend.function.util.parse_json import _parse_list
import backend.config as cfg
import numpy as np

system_prompt_getTextReplyFromLLM = """
Please generate response according to user's input.
"""

system_prompt_getImpressionFromLLM = """
Generate an 8-dimensional list based on a description of a virtual character's voice. The list should represent:
[gender, age, pitch, warmth, clarity, power, thickness, smoothness]
Use these value ranges:
Gender: 1 (Female) to 3 (Male)
All others: 1 (Very low/young/cold/hoarse/weak/thin/rough) to 5 (Very high/old/warm/clear/strong/thick/smooth)
Guidelines:
Infer values from the given description.
Use neutral values (2 for gender, 3 for others) if not mentioned.
Return a Python list of 8 integers.
Example:
Input: "A young female with a clear, warm voice that's somewhat high-pitched and smooth."
Output: [1, 2, 4, 4, 4, 3, 3, 4]
"""

system_prompt_getGreetingTextFromLLM = """
Based on the user's description of a character's personality, generate an appropriate greeting phrase. 
"""

def getTextReplyFromLLM(llm, prompt):
    try:
        completion = llm.chat.completions.create(
            model = cfg.LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt_getTextReplyFromLLM}, # <-- This is the system message that provides context to the model
                {"role": "user", "content": prompt}  # <-- This is the user message for which the model will generate a response
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"
    
def getImpressionFromLLM(llm, prompt):
    try:
        completion = llm.chat.completions.create(
            model = cfg.LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt_getImpressionFromLLM}, # <-- This is the system message that provides context to the model
                {"role": "user", "content": prompt}  # <-- This is the user message for which the model will generate a response
            ]
        )
        res = np.array(_parse_list(completion.choices[0].message.content.strip()))
        print(res)
        return res
    except Exception as e:
        return f"An error occurred: {str(e)}"
    
def getGreetingTextFromLLM(llm, prompt):
    try:
        completion = llm.chat.completions.create(
            model = cfg.LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt_getGreetingTextFromLLM}, # <-- This is the system message that provides context to the model
                {"role": "user", "content": prompt}  # <-- This is the user message for which the model will generate a response
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"