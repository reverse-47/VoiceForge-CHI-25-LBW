from backend.function.util.parse_json import _parse_list
import backend.config as cfg
import numpy as np

system_prompt_getTextReplyFromLLM = """
Generate a response based on the given character's personality, conversation history, and the latest message.
Include tone annotations, simulated laughter, and emphasis in the response.
Use the following format for annotations:
1. [laughter] for laughter
2. [breath] for breath pauses
3. <laughter>text</laughter> for speech while laughing
4. <strong>text</strong> for emphasized words

Example:
"Well, that's kind of scary [laughter]. I don't think I over eat, yeah [breath] and um, I do exercise regularly. 
Well, that pretty much <laughter>covers the subject</laughter>. The team's <strong>unity</strong> and <strong>resilience</strong> helped them win."

Please provide only the final annotated response without any additional explanations or prompts.
"""

system_prompt_getImpressionFromLLM = """
Generate a 9-dimensional list based on a description of a virtual character's voice. The list should represent:
[gender, age, pitch, warmth, clarity, power, thickness, smoothness, emotion]

Use these value ranges:
Gender: 1 (Female) to 3 (Male)
Emotion: 1 (Angry), 2 (Happy), 3 (Fearful), 4 (Sad), 5 (Surprised), 6 (Neutral)
All others: 1 (Very low/young/cold/hoarse/weak/thin/rough) to 10 (Very high/old/warm/clear/strong/thick/smooth)

Guidelines:
- Infer values from the given description
- Use neutral values (2 for gender, 5 for others, 6 for emotion) if not mentioned
- Return a Python list of 9 integers

Example:
Input: "A young female with a happy, warm voice that's somewhat high-pitched and smooth."
Output: [1, 2, 8, 8, 8, 6, 6, 8, 2]  # The last 2 represents "happy" emotion
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