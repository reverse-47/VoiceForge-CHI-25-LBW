# OPENAI_API_KEY="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"
OPENAI_API_KEY=""
SERPAPI_API_KEY=""
ANTHROPIC_API_KEY=""

LLM = "gpt-3.5-turbo"
TALK_LLM = "claude-2"
IS_LOCAL_MODEL = True
SCORE_MODEL = "albert-base-v2"
SCORE_MODEL_PATH = "seed_1234_trRatio_06albert-base-v2_clsDim_768_baseLr_5e-05_clsLr_0.0001_trEp_12_trBs_64_teBs_256best_model.pth"
NLP = "en_core_web_trf"
EBD_MODEL = 'all-MiniLM-L6-v2'

OBJECT_JSON_PATH = './backend/DataStore/json/Objects_config.json'
ME_JSON_PATH = './backend/DataStore/json/Me_config.json'
SKILL_JSON_PATH = './backend/DataStore/json/Skills_config.json'
NPC_SCHEDULE_JSON_PATH = './backend/DataStore/json/NPCRoutine_config.json'
TASK_JSON_PATH = './backend/DataStore/json/Tasks_config.json'

OBJECT_EBD_PATH = './backend/DataStore/embedding/Objects_ebd.pt'
ME_EBD_PATH = './backend/DataStore/embedding/ME_ebd.pt'
SKILL_EBD_PATH = './backend/DataStore/embedding/Skills_ebd.pt'

THRESHOLD = 0.7

MODEL_PATH = './backend/Model/ChatTTS-Model'