import torch
from backend.dataloader import load_object, load_skill, load_object_alias, load_me
from backend.configure import EBD_MODEL, OBJECT_EBD_PATH, SKILL_EBD_PATH, ME_EBD_PATH
from sentence_transformers import SentenceTransformer

def load_object_embedding():
    object_list = load_object_alias()
    print(object_list)
    ebd_model = SentenceTransformer(EBD_MODEL)
    matrix = []
    for object in object_list:
        object_embedding = torch.tensor(ebd_model.encode(object["Name"].lower()))
        matrix.append(object_embedding)
    torch_matrix = torch.stack(matrix)
    torch.save(torch_matrix, OBJECT_EBD_PATH)

def load_skill_embedding():
    skill_list = load_skill()
    print(skill_list)
    ebd_model = SentenceTransformer(EBD_MODEL)
    matrix = []
    for skill in skill_list:
        skill_embedding = torch.tensor(ebd_model.encode(skill["SkillName"].lower()))
        matrix.append(skill_embedding)
    torch_matrix = torch.stack(matrix)
    torch.save(torch_matrix, SKILL_EBD_PATH)

def load_me_embedding():
    me_list = load_me()
    print(me_list)
    ebd_model = SentenceTransformer(EBD_MODEL)
    matrix = []
    for me in me_list:
        me_embedding = torch.tensor(ebd_model.encode(me.lower()))
        matrix.append(me_embedding)
    torch_matrix = torch.stack(matrix)
    torch.save(torch_matrix, ME_EBD_PATH)


if __name__ == '__main__':
    load_object_embedding()