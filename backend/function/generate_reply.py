from backend.api.llm import getTextReplyFromLLM
from backend.function.generate_audio import getAudioFromTone

def getReplyFromText(llm, ttsm, input_text, personality, last_conversation, tone_ebd):
    data = {}
    conversation = convertConversationToPrompt(last_conversation)
    prompt = f"""
    Character's personality:
    {personality}

    Conversation history:
    {conversation}

    Latest message:
    {input_text}

    Generate an annotated response for this character:
    """
    data["text"] = getTextReplyFromLLM(llm, prompt)
    print(data["text"])
    data["audio"] = getAudioFromTone(ttsm, tone_ebd, data["text"])
    
    return data

def convertConversationToPrompt(conversation_list):
    prompt = ""
    for entry in conversation_list:
        if "user" in entry and entry["user"]:
            prompt += f"User: {entry['user']}\n"
        if "assistant" in entry and entry["assistant"]:
            prompt += f"Assistant: {entry['assistant']}\n"
    return prompt.strip()