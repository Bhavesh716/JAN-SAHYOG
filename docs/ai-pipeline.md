# JAN SAHYOG — AI Pipeline

## 1. Goal

The AI pipeline turns a user's question into clear, useful guidance supported by reviewed information. It should prefer evidence over guessing and clearly state when it cannot verify an answer.

## 2. Pipeline

```text
Voice / Text / Document
          |
          v
Input Normalization
          |
          v
Language & Intent Detection
          |
          v
JEv AI Request Routing
          |
          +-----------------------+
          |                       |
          v                       v
Official-Document RAG       Authorized Tool/API
          |                       |
          +-----------+-----------+
                      v
            Context Preparation
                      |
                      v
             Local / Private LLM
                      |
                      v
        Evidence, Safety & Relevance Checks
                      |
                      v
            Text Response + Sources
                      |
                      v
                Optional TTS
```

## 3. Input Processing

- Accept text from the kiosk, web, or mobile interface.
- Convert speech to text using the configured STT component.
- Use OCR when supported documents or images are submitted.
- Preserve the user's original question where useful for traceability.
- Ask for clarification if the request is ambiguous.

## 4. Intent Detection and JEv AI

JEv AI is the planned orchestration layer. It should classify the request into an appropriate category, such as cooperative governance, PACS services, schemes, PMFBY, financial literacy, or grievance support.

It can then decide whether to:
- Search the knowledge base.
- Call an authorized service integration.
- Ask the user for missing information.
- Use a lightweight response path for simple requests.
- Route a complex request to the configured LLM.

Routing decisions should be logged without unnecessarily recording sensitive user content.

## 5. RAG Retrieval

### Document preparation
1. Collect documents from reviewed, permitted sources.
2. Record source URL, publisher, publication/update date, and version where available.
3. Extract text from PDFs, text files, and supported formats.
4. Clean the text and split it into chunks.
5. Generate embeddings.
6. Index the chunks and their metadata.

### Query-time retrieval
1. Embed or otherwise process the user's question.
2. Search for relevant chunks.
3. Retrieve the strongest matches.
4. Apply metadata filters where appropriate.
5. Pass relevant passages and source metadata to the LLM.

Retrieval relevance must be evaluated. A search result is not automatically proof that an answer is correct or current.

## 6. Answer Generation

The LLM should:
- Use retrieved context for factual government guidance.
- Explain terms in simple language.
- Separate confirmed information from general explanation.
- Avoid inventing deadlines, eligibility conditions, benefits, or official actions.
- Include source references when available.
- Ask a clarifying question if required information is missing.

## 7. Validation and Fallback

Before returning an answer, the application should check:
- Whether relevant evidence was retrieved.
- Whether the response is related to the question.
- Whether cited sources exist in the retrieval results.
- Whether critical details conflict across documents.
- Whether the answer needs a date/version caveat.

If evidence is insufficient, return a safe fallback and point the user to the relevant official channel. Do not present a model confidence score as proof of factual correctness.

## 8. Speech Output

- Send the final text to TTS for supported languages.
- Keep the on-screen text available when possible.
- Allow users to repeat or slow down instructions if the chosen TTS service supports it.
- Evaluate pronunciation and recognition across regional accents.

## 9. Evaluation Metrics

Track retrieval precision, answer grounding, citation validity, language quality, STT word error rate, latency, fallback frequency, and user task completion. Evaluate each supported language separately.
