import streamlit as st
from core.context_engine import ContextEngine
from simulation.threat_simulator import ThreatSimulator
from multimodal.audio_analyzer import AudioAnalyzer

st.set_page_config(page_title="Contextual Reasoner Dashboard", layout="centered")
st.title("🧠 Contextual Reasoning Dashboard")

engine = ContextEngine()

# Text Analysis
st.subheader("Text Analysis")
text_input = st.text_area("Enter text for analysis:")
if st.button("Analyze Text"):
    result = engine.analyze_text(text_input)
    st.json(result)

# Image Analysis
st.subheader("Image Analysis")
image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if image_file and st.button("Analyze Image"):
    image_path = f"/tmp/{image_file.name}"
    with open(image_path, "wb") as f:
        f.write(image_file.read())
    result = engine.analyze_image(image_path)
    st.json(result)

# Audio Analysis
st.subheader("Audio Analysis")
audio_file = st.file_uploader("Upload an audio file", type=["wav"])
if audio_file and st.button("Analyze Audio"):
    audio_path = f"/tmp/{audio_file.name}"
    with open(audio_path, "wb") as f:
        f.write(audio_file.read())
    analyzer = AudioAnalyzer()
    result = analyzer.analyze_audio(audio_path)
    st.text("Transcription:")
    st.write(result)

# Threat Simulation
st.subheader("Threat Simulation")
if st.button("Run Simulation"):
    simulator = ThreatSimulator()
    simulator.simulate()
    st.success("Simulation complete. See CLI for output.")