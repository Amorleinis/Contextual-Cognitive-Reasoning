import argparse
from core.context_engine import ContextEngine
from simulation.threat_simulator import ThreatSimulator
from multimodal.audio_analyzer import AudioAnalyzer

def main():
    parser = argparse.ArgumentParser(description="Contextual Reasoner CLI")
    parser.add_argument("--text", type=str, help="Analyze text input")
    parser.add_argument("--image", type=str, help="Analyze image file")
    parser.add_argument("--audio", type=str, help="Analyze audio file")
    parser.add_argument("--simulate", action="store_true", help="Run threat simulation")

    args = parser.parse_args()
    engine = ContextEngine()

    if args.text:
        result = engine.analyze_text(args.text)
        print("Text Analysis Result:")
        print(result)

    if args.image:
        result = engine.analyze_image(args.image)
        print("Image Analysis Result:")
        print(result)

    if args.audio:
        analyzer = AudioAnalyzer()
        transcription = analyzer.analyze_audio(args.audio)
        print("Audio Transcription:")
        print(transcription)

    if args.simulate:
        simulator = ThreatSimulator()
        simulator.simulate()

if __name__ == "__main__":
    main()