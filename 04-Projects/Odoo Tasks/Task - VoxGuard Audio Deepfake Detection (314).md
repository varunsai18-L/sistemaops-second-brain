---
id: odoo-task-314
type: Project Task
project: "AI ML review"
stage: "Brainstorm"
assignees: "Unassigned"
last_updated: 2026-06-06 06:03:34
sync_date: 2026-08-25 21:12:32
tags:
  - odoo/task
  - project/ai-ml-review
  - status/brainstorm
---
# Task: VoxGuard Audio Deepfake Detection

- **Project:** [[AI ML review]]
- **Odoo Stage:** Brainstorm
- **Assignees:** Unassigned
- **Last Sync:** 2026-08-25 21:12:32

## Description
Audio deepfakes are becoming a major security gap for biometric authentication systems. I built VoxGuard to accurately detect synthetically generated voices (like ElevenLabs clones). The core of this project is a hybrid CNN-LSTM neural network trained on the ASVspoof 2019 dataset.Instead of just passing raw audio into a basic classifier, the pipeline extracts MFCCs (Mel-Frequency Cepstral Coefficients). This maps out both the frequency patterns and how the audio sequence changes over time. The CNN handles the spatial feature extraction from the spectrograms, while the LSTM specifically tracks the temporal sequence anomalies that usually give away an AI-generated deepfake.What It Actually Does: Users upload an audio file via the Streamlit interface. The backend immediately processes the file into spectrograms, runs inference through the trained CNN-LSTM model, and classifies it as "Real" or "Fake" in seconds.More importantly, I didn't want the system to just be a black box. I integrated SHAP (SHapley Additive exPlanations) directly into the pipeline. After inference, the UI actually highlights the specific frequency bands and timestamps in the audio that triggered the "Fake" classification. This proves why the model made its decision, making it completely transparent.Future Engineering Scope: The current architecture hit ~91% accuracy on the evaluation set. I recently finalized the methodology and submitted the research as a full paper to the IEEE CONIT 2026 conference.Next technical steps involve optimizing the model weights so it can run inference locally on edge devices without relying on a cloud backend, and setting up real-time streaming detection rather than just processing static .wav uploads.System Architecture:Input Layer: Python ingestion script handling audio file loading and basic .wav/.flac format validation.Feature Extraction: Librosa is used to clean the audio and generate MFCCs. This converts the raw 1D audio signal into a 2D matrix representation the neural net can process.Model Layer: TensorFlow/Keras backend. The CNN layers pick up the static frequency anomalies (like weird artifacts left by voice cloning software), while the LSTM layers catch unnatural temporal shifts in the speech cadence.Explainability Layer: SHAP calculates the exact feature importance for the prediction, allowing us to trace the "Fake" classification back to the exact frequency distortion in the audio file.
