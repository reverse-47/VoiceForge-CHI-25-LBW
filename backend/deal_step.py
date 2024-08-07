from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

BACKGROUND = "This is a spacious bar with dim lighting. Besides myself, the only other occupants are a bartender behind the counter and a heavily intoxicated customer slumped over a round table. Empty bottles litter the floor near the customer's feet. In the customer area of the bar, there are only two round tables and a few chairs. The bartender stands behind the counter, guarding the bar counter barrier—the sole entrance and exit. My finial task is to find my missing black cat in this bar."
TRUTH = "Truth is that my black cat awakened its lineage and became a cat demon when it turned 20 years old. At the moment of awakening, the cat felt helpless and scared. Not only could it suddenly understand human speech, but its meows also transformed into human language. Frightened, it sought refuge in a dimly lit and dark bar. Once inside the bar, the cat discovered that the small town had experienced many interesting events. It decided to hide on the rafters, eavesdropping on human conversations and learning the logic of human speech. However, it constantly felt drowsy and would unintentionally fall asleep. The cat demon's powers affected the building itself, causing the walls to shed tears when it slept. The bar owner recently discovered liquid dripping from behind a mural at the back of the bar. Unaware of the truth, she mistook it for bloodstains and urgently covered it up to prevent customers from feeling scared. She guarded the bar counter, preventing others from entering, and kept the bar dimly lit to prevent anyone from noticing the unusual mural on the wall." 

def GenerateStep(llm):

    # res_data = True

    text_template = "【The following events occur in a virtual game scenario.】\n"+BACKGROUND+"\n"+TRUTH+"\n\
    Please make 5-15 steps to help me complete the final task.\n\
    Output the response to the prompt above in json list, each json includes one key: step."
    
    prompt = PromptTemplate.from_template(text_template)
    prompt_text = prompt.format()
    msg = HumanMessage(content=prompt_text)
    res = llm.get_res(msg)
    print(res)
            
    return res