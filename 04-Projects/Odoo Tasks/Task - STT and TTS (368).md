---
id: odoo-task-368
type: Project Task
project: "AI ML review"
stage: "Prototype Development"
assignees: "Shreya Bhavani"
last_updated: 2026-06-18 15:35:49
sync_date: 2026-08-05 20:04:32
tags:
  - odoo/task
  - project/ai-ml-review
  - status/prototype-development
---
# Task: STT and TTS

- **Project:** [[AI ML review]]
- **Odoo Stage:** Prototype Development
- **Assignees:** Shreya Bhavani
- **Last Sync:** 2026-08-05 20:04:32

## Description
Triage Engine (Backend)STT + TTS (multilingual)Shreya -> 02-06-2026 : Environment setup completed.

Audio recording module completed.

Faster-Whisper installed and configured.

Speech-to-Text working successfully on recorded audio.

Currently optimizing transcription and preparing real-time STT implementation. TTS development will start after STT stabilization.GitHub Repository of Faster-Whisper: https://github.com/SYSTRAN/faster-whisper?utm_source=chatgpt.Speech-to-Text Technology Selection.pdfshreya -> 08-06-2026 :Progress of SST Task AI MEDICAL TRIAGE PLATFORM.pdfWhy
Speech-to-Text Is Required4.
Technology SelectionSelected
FrameworkFaster-WhisperGitHub Repository:
https://github.com/SYSTRAN/faster-whisperOriginal Whisper:
https://github.com/openai/whisperSelected
ModelWhisper BaseReason:
 Good accuracy
 Faster than
     Small model
 Works
     efficiently on CPU
 Suitable for
     16GB RAM systems
 Supports
     multilingual transcription5. Why
Faster-Whisper Was Selected
 
  
  Requirement
  
  
  Needed
  
  
  Supported
  
 
 
  
  Offline Operation
  
  
  Yes
  
  
  Yes
  
 
 
  
  Open Source
  
  
  Yes
  
  
  Yes
  
 
 
  
  CPU Compatible
  
  
  Yes
  
  
  Yes
  
 
 
  
  Low Cost
  
  
  Yes
  
  
  Yes
  
 
 
  
  Multilingual
  
  
  Yes
  
  
  Yes
  
 
 
  
  Indian Languages
  
  
  Yes
  
  
  Yes
  
 
 
  
  Medical Privacy
  
  
  Yes
  
  
  Yes
  
 
 
  
  Real-Time Capability
  
  
  Yes
  
  
  Yes6.
Comparison With Other STT Solutions
 
  
  Feature
  
  
  Faster-Whisper
  
  
  Google STT
  
  
  Deepgram
  
  
  Vosk
  
 
 
  
  Offline Support
  
  
  Yes
  
  
  No
  
  
  No
  
  
  Yes
  
 
 
  
  Open Source
  
  
  Yes
  
  
  No
  
  
  No
  
  
  Yes
  
 
 
  
  Multilingual
  
  
  Excellent
  
  
  Good
  
  
  Good
  
  
  Moderate
  
 
 
  
  Indian Languages
  
  
  Excellent
  
  
  Good
  
  
  Moderate
  
  
  Weak
  
 
 
  
  Privacy
  
  
  High
  
  
  Medium
  
  
  Medium
  
  
  High
  
 
 
  
  Cost
  
  
  Free
  
  
  Paid
  
  
  Paid
  
  
  Free
  
 
 
  
  CPU Performance
  
  
  High
  
  
  Cloud Only
  
  
  Cloud Only
  
  
  Good
  
 
 7.
Development JourneyPhase 1 –
Basic Speech RecognitionObjective: Convert
recorded audio into text.Achievements:
 Audio recording
     implemented
 Whisper model
     integrated
 Basic
     transcription completed
Status: Completed Phase 2 –
Automated STT PipelineObjective: Automate
recording and transcription workflow.Achievements:
 Automatic
     transcription
 Transcript
     persistence
 Modular
     architecture
 Error handling
Status: Completed Phase 3 –
Real-Time Streaming STTObjective: Provide live
speech recognition.Achievements:
 Real-time
     transcription
 Chunk buffering
 Queue
     architecture
 Silence
     detection
 Transcript
     aggregation
 Language
     locking
Status: Completed Phase 4 –
STT Service LayerObjective: Create
reusable STT services.Achievements:
 Service-oriented
     architecture
 Structured
     responses
 Metadata
     generation
 Session
     management
 Logging
Status: CompletedPhase 5 –
FastAPI IntegrationObjective: Expose STT
functionality through APIs.Achievements:
 Swagger UI
 REST APIs
 Metadata access
 Health
     monitoring
 Team
     integration ready
Status: Completed 8. Current
System Architecture9. Key
Features ImplementedAudio Features
 Microphone
     recording
 Streaming
     capture
 Audio
     normalization
 Mono conversion
 Chunk buffering
 RMS filtering
 Silence
     detection
STT Features
 Whisper Base
     integration
 Language
     detection
 Language
     locking
 Real-time
     transcription
 File
     transcription
 Duplicate
     removal
 Transcript
     aggregation
Persistence Features
 Transcript
     storage
 Metadata
     storage
 Session
     tracking
 Timestamped
     outputs
 Log generation
API Features
 FastAPI
     integration
 Swagger
     documentation
 Health endpoint
 Transcription
     endpoint
 Structured JSON
     responses11.
Technologies UsedProgramming Language : Python 3.11Libraries:
 Faster-Whisper
 CTranslate2
 FastAPI
 Uvicorn
 NumPy
 SciPy
 SoundDevice
 Queue
 Threading
 JSON
 Logging
Development Tools:
 VS Code
 GitHub Copilot
 Swagger UI
 Postman
 12. API
ExampleEndpoint:POST /transcribeInput: audio.wavResponse:{
"status": "success",
"text": "I have fever for three days",
"language": "en",
"timestamp": "...",
"model": "base",
"processing_time": 3.38,
"session_id": "..."
}13. Risks
and MitigationRisk: Background NoiseMitigation: Silence
Detection + Audio NormalizationRisk: Repeated
Transcript FragmentsMitigation: Transcript
Deduplication LogicRisk: Language DriftMitigation: Language
LockingRisk: Memory UsageMitigation: Bounded
Queue ArchitectureRisk: API FailureMitigation: Structured
Logging and Error HandlingShreya -> 18-06-2026Phase 6 – Offline Text-to-Speech (TTS) DevelopmentObjective : Develop a fully offline Text-to-Speech subsystem that converts AI-generated medical recommendations into natural speech.AchievementsImplemented Piper TTS based speech synthesis.Added support for multilingual voice generation:EnglishHindiGermanTeluguMalayalamGujarati (STT supported; TTS model pending)Generated timestamped WAV audio outputs.Added voice alias support.Implemented local audio playback.Added structured JSON responses.Added logging and error handling.Integrated TTS with existing STT service architecture.piper TTS model : https://github.com/rhasspy/piperComparison TableFeaturePiper TTSgTTSCoqui TTSElevenLabsAzure TTSOpen Source✅❌✅❌❌Offline✅❌✅❌❌Free✅✅✅LimitedPaidCPU Friendly✅N/AModerateN/AN/ARailway Deployment✅DifficultHeavyAPI BasedAPI BasedPrivacyHighMediumHighMediumMediumMultilingualGoodGoodExcellentExcellentExcellentInstallation SimplicityEasyEasyComplexVery EasyVery EasyResource UsageLowLowHighCloudCloudInstall Piper TTSpip install piper-ttsInstall Requirementspip install -r requirements.txtVoice Model Download CommandsList Available Voicespython scripts/download_piper_voice.py --listHindi Voicepython scripts/download_piper_voice.py --voice hiGerman Voicepython scripts/download_piper_voice.py --voice deTelugu Voicepython scripts/download_piper_voice.py --voice teMalayalam Voicepython scripts/download_piper_voice.py --voice mlStatus - CompletedPhase 7 -  STT + RAG + TTS IntegrationObjective : Connect Speech-to-Text with the Medical Triage Engine and automatically generate voice responses.AchievementsConnected STT pipeline with deployed Railway Medical Triage API.Added automatic forwarding of transcribed symptoms to the triage engine.Added configurable external analysis URL support.Implemented end-to-end processing:Audio Input↓STT↓Medical Analysis (RAG)↓TTS↓Audio ResponseAdded session tracking and metadata persistence.Added triage response formatting for TTS playback.Implemented production deployment on Railway.Deployment URLsSTT + TTS Service :https://stt-tts-service-production.up.railway.appMedical Triage Service:https://medical-triage-production.up.railway.app/triageStatus :  CompletedCurrent System ArchitectureKey Features ImplementedSTT FeaturesOffline speech recognitionReal-time streaming transcriptionLanguage detectionLanguage lockingChunk-based processingTranscript aggregationTranscript persistenceSession metadata generationLoggingMedical Analysis FeaturesBM25 knowledge retrievalLangChain integrationNVIDIA Nemotron 3 Nano OmniClinical guideline retrieval4-level urgency classification:Self CareDoctor ConsultationUrgent CareEmergency ReferralSafety escalation mechanismTTS FeaturesOffline speech synthesisPiper voice modelsVoice selectionMultilingual audio generationAudio playbackWAV file generationTTS status trackingAPI FeaturesFastAPI backendSwagger UIOpenAPI schemaSession metadata endpointLogs endpointHealth monitoring endpointRailway deploymentTechnologies UsedProgramming LanguagePython 3.11Speech-to-TextFaster-WhisperWhisper BaseCTranslate2Medical AnalysisFastAPILangChainBM25 RetrieverNVIDIA Nemotron 3 Nano OmniOpenRouterText-to-SpeechPiper TTSONNX Voice ModelsBackend & InfrastructureFastAPIUvicornRailway DeploymentJSONLoggingAudio ProcessingSoundDeviceNumPySciPyDevelopment ToolsVS CodeCursor AIGitLabPostmanSwagger UICurrent API EndpointsGET /healthPOST /transcribePOST /triagePOST /analyzeGET /session/{session_id}GET /logsGET /debug/tts-fileGET /docsGET /openapi.jsonRisks and MitigationRiskMitigationBackground NoiseAudio normalization and silence detectionIncorrect Language DetectionLanguage locking supportTranscript DuplicationTranscript aggregation logicMemory ConsumptionQueue-based chunk processingExternal API FailureTimeout and error handlingMissing Voice ModelsVoice alias validation and fallback logicDeployment IssuesRailway monitoring and health endpointsCurrent Project StatusPhase 1 – Basic STT : ✅ CompletedPhase 2 – Automated STT Pipeline : ✅ CompletedPhase 3 – Real-Time Streaming STT : ✅ CompletedPhase 4 – STT Service Layer : ✅ CompletedPhase 5 – FastAPI Integration : ✅ CompletedPhase 6 – Offline TTS : ✅ CompletedPhase 7 – STT + RAG + TTS Integration : ✅ CompletedOverall Module Completion : 95%Deployment Status : Production Deployed on RailwayModule Readiness : Ready for Final Project Demonstration
