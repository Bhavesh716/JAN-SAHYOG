# JAN SAHYOG — System Architecture

## 1. Overview

JAN SAHYOG combines a physical AI Seva Kiosk with a shared backend and AI platform. The kiosk is the primary rural access point; phone/IVR, mobile, and web interfaces can be added as additional channels.

The kiosk captures user input and displays or speaks the response. AI inference and knowledge retrieval are intended to run on a government-controlled server or approved cloud infrastructure, rather than on the ESP32 controller.

## 2. High-Level Flow

```text
User
 |
 v
AI Seva Kiosk / Phone / Mobile / Web
 |
 v
Interface + Input Processing
 |
 v
Secure API
 |
 v
FastAPI Backend
 |
 v
JEv AI Orchestration
 |----------------------|
 v                      v
RAG Knowledge Base      Authorized Service Integrations
 |                      |
 |----------+-----------|
            v
     Local / Private LLM
            |
            v
    Evidence & Safety Checks
            |
            v
     Text / Voice Response
```

## 3. Main Components

### Kiosk hardware
- Touchscreen, microphone, speaker, and optional camera/scanner.
- Kiosk compute unit runs the main UI.
- ESP32-S3 handles suitable embedded control and peripheral tasks.
- Cellular or Wi-Fi connectivity sends requests to the backend.

### API backend
- Receives requests from client interfaces.
- Validates request shape and manages sessions.
- Routes requests to AI services.
- Returns structured responses to the clients.

### JEv AI orchestration
- Classifies intent.
- Selects retrieval, model, or tool paths.
- Requests clarification when input is insufficient.
- Coordinates response validation.

### RAG knowledge system
- Stores searchable chunks from reviewed official documents.
- Retrieves relevant passages for a question.
- Supplies source metadata and context to the language model.

### Local/private LLM
- Generates plain-language answers using the user's question and retrieved context.
- Runs on approved server infrastructure.
- Must not be treated as authoritative when evidence is missing.

### Data and monitoring
- PostgreSQL may store application metadata and operational records.
- A vector database stores embeddings and retrieval metadata.
- Redis is optional for caching or temporary coordination.
- Logs and metrics support debugging and service monitoring.

## 4. Trust Boundaries

- The kiosk is an untrusted client; validate all incoming requests.
- Do not put model keys or database credentials in kiosk firmware or frontend code.
- External service integrations must use approved credentials and permissions.
- Avoid retaining personal information unless needed for a defined purpose.
- Official document sources, version dates, and update history should be recorded.

## 5. Deployment Approach

Start with a development backend and a small, reviewed document set. Add retrieval and language-model integration only after the ingestion pipeline is tested. Pilot the kiosk hardware separately before field deployment.

The final topology, redundancy, network controls, and data-retention policy should be agreed with the deployment authority.
