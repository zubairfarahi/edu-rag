import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel
from typing import List



class LocalEmbeddingModel:
    def __init__(self, model_name: str = "nvidia/NV-Embed-v2"):
        self.model_name = model_name
        # self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(model_name, trust_remote_code=True)
        # self.model.eval()

    def get_embeddings(self, texts: List[str], instruction: str = "", max_length: int = 32768) -> List[List[float]]:
        embedding = self.model.encode(
            texts, instruction=instruction, max_length=max_length
        )
        embedding = F.normalize(embedding, p=2, dim=1)

        return embedding.tolist()


    
    def get_embedding(self, text: str, instruction: str = "", max_length: int = 32768) -> List[float]:
        embedding =  self.model.encode(
            text, instruction=instruction, max_length=max_length
        )
        embedding = F.normalize(embedding, p=2, dim=1)
        print(embedding)
        return embedding.tolist()
    

if __name__ == "__main__":
    # model_name = os.getenv("LOCAL_EMBEDDING_MODEL_NAME", "nvidia/NV-Embed-v2")
    local_embedding_model = LocalEmbeddingModel(model_name="nvidia/NV-Embed-v2")
    
    # print(local_embedding_model.async_get_embedding("Hello, world!", "This is a test instruction."))
    
    print(local_embedding_model.get_embedding(["Hello, world!", "Goodbye, world!"]))


