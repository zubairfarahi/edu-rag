import numpy as np

def cosine_similarity(vector_a: np.array, vector_b: np.array) -> float:
    dot_product = np.dot(vector_a, vector_b)
    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)
    return dot_product / (norm_a * norm_b)