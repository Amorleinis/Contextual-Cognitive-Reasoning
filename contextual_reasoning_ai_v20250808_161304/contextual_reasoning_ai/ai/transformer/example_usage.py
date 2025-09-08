from context_encoder import ContextEncoder

encoder = ContextEncoder()
embedding = encoder.encode("Potential vulnerability detected in external network traffic.")
print(embedding.shape)