import torch
import torchaudio
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

class AudioAnalyzer:
    def __init__(self, model_name="facebook/wav2vec2-base-960h", device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = Wav2Vec2Processor.from_pretrained(model_name)
        self.model = Wav2Vec2ForCTC.from_pretrained(model_name).to(self.device)

    def analyze_audio(self, audio_path):
        waveform, sample_rate = torchaudio.load(audio_path)
        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
            waveform = resampler(waveform)

        input_values = self.processor(waveform.squeeze().numpy(), return_tensors="pt", sampling_rate=16000).input_values.to(self.device)
        with torch.no_grad():
            logits = self.model(input_values).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)[0]
        return transcription