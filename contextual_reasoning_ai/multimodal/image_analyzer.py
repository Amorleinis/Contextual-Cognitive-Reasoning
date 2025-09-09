import torch
import clip
from PIL import Image

class ImageAnalyzer:
    def __init__(self, device="cuda" if torch.cuda.is_available() else "cpu"):
        self.device = device
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)

    def analyze_image(self, image_path, text_prompts=None):
        image = self.preprocess(Image.open(image_path)).unsqueeze(0).to(self.device)
        if text_prompts is None:
            text_prompts = ["a computer", "a hacker", "a vulnerability", "a firewall", "a network attack"]

        text = clip.tokenize(text_prompts).to(self.device)
        with torch.no_grad():
            image_features = self.model.encode_image(image)
            text_features = self.model.encode_text(text)
            logits_per_image, _ = self.model(image, text)
            probs = logits_per_image.softmax(dim=-1).cpu().numpy()

        results = list(zip(text_prompts, probs[0]))
        return sorted(results, key=lambda x: -x[1])