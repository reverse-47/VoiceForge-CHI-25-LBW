from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage

import time
import asyncio
import os
import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoConfig, AutoModel

from backend.configure import OPENAI_API_KEY, ANTHROPIC_API_KEY




os.environ['OPENAI_API_KEY']=OPENAI_API_KEY
os.environ['ANTHROPIC_API_KEY']=ANTHROPIC_API_KEY


class GenerationModel:
    def __init__(self, model_name:str, temperature: float = 0.7, max_tokens: int = 1024) -> None:
        # self.model_type = model_type
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_tokens = 0
        
        if self.model_name == "text-davinci-003":
            self.model = OpenAI(model_namese=self.model_name, temperature=self.temperature)
        elif self.model_name == "gpt-3.5-turbo":
            self.model = ChatOpenAI(model_name=self.model_name, temperature=self.temperature, max_tokens=self.max_tokens)
        elif self.model_name == "gpt-3.5-turbo-16k":
            self.model = ChatOpenAI(model_name=self.model_name, temperature=self.temperature, max_tokens=self.max_tokens)
        elif self.model_name == "claude-2":
            self.model = ChatAnthropic(temperature=self.temperature, max_tokens_to_sample=self.max_tokens)
        else:
            raise ValueError("Other model is not supported at the moment")

        # import pdb;pdb.set_trace()

    def get_res(self, messages):
        if self.model_name == "text-davinci-003":
            messages = [messages]
        else:
            messages = [[messages]]
        res = self.model.generate(messages)
        generation_text = res.generations[0][0].text
        
        print("generation_text:  ", generation_text )
        # import pdb; pdb.set_trace()

        return generation_text

class LongTermMemoryModel:
    def __init__(self, score_model_name: str, is_local_model: bool, score_model_path: str = None, num_levels: int = 5) -> None:
        self.score_model_name = score_model_name
        self.is_local_model = is_local_model
        self.score_model_path = score_model_path
        self.num_levels = num_levels

        if is_local_model:
            self.tokenizer = AutoTokenizer.from_pretrained(self.score_model_name)
            # self.model = torch.load(self.score_model_path)
            self.model = PLM(self.score_model_name)
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")          
            if not torch.cuda.is_available():
                print("Notice, the current device is CPU!")
            self.model.load_state_dict(torch.load(self.score_model_path, map_location=device)) 
                
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(self.score_model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.score_model_name)


    def get_score(self, memory):
        memory_score = -1

        inputs = self.tokenizer.encode_plus(memory, return_tensors='pt')
        
        
        output = self.model(**inputs)[0].squeeze()

        memory_score = output.argmax().item()+1


        return memory_score

class PLM(nn.Module):

    def __init__(self, score_model_name: str):

        super(PLM, self).__init__()

        self.gradient_checkpointing = False
        self.training = False
        self.n_class = 5
        self.dropout_rate = 0.1


        self.config = AutoConfig.from_pretrained(score_model_name)
        self.f_dim = self.config.hidden_size
        self.plm = AutoModel.from_pretrained(score_model_name)
        self.dropout = nn.Dropout(self.dropout_rate)
        self.classifier = nn.Linear(self.f_dim, self.n_class)

    def forward(self, input_ids, attention_mask,token_type_ids=None):
        loss = None

        with torch.no_grad():
            features = self.plm(input_ids=input_ids, attention_mask=attention_mask)

        # import pdb;pdb.set_trace()
        
        # use cls embedding or pooler output
        last_embeddings = features[0][:,0,:]
        logits = self.classifier(self.dropout(last_embeddings))
        return logits

class TalkGenerationModel(GenerationModel):
    def __init__(self, model_name: str = "claude-2", temperature: float = 1.0, max_tokens: int = 512) -> None:
        super().__init__(model_name, temperature, max_tokens)

class SummaryGenerationModel(GenerationModel):
    def __init__(self, model_name: str = "gpt-3.5-turbo-16k", temperature: float = 0.7, max_tokens: int = 6000) -> None:
        super().__init__(model_name, temperature, max_tokens)

if __name__=="__main__":
    m = GenerationModel()