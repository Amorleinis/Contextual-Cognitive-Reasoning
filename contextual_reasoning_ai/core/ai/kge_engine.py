from pykeen.pipeline import pipeline

class KGEmbeddingEngine:
    def __init__(self, triples_path="data/triples.tsv"):
        self.triples_path = triples_path

    def train_model(self):
        result = pipeline(
            model='TransE',
            dataset=None,
            training=self.triples_path,
            model_kwargs=dict(embedding_dim=50),
            training_kwargs=dict(num_epochs=5),
        )
        self.model = result.model
        return result

    def get_entity_embedding(self, entity_label):
        return self.model.entity_representations[0](entity_label)
