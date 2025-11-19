<!-- 80d5e2d8-2a38-4546-b11a-6369e6f234c4 312b9710-f032-4ca9-ab54-acfd4a362fed -->
# Real-Time Emotion-Aware Customer Service Assistant - Implementation Plan

## Architecture Overview

- **Frontend**: React web app (browser-based)
- **Backend**: Python (FastAPI) with WebSocket support
- **Audio Processing**: Hume AI API (WebSocket streaming)
- **LLM**: OpenAI GPT-4/GPT-3.5
- **RAG**: Vector database (ChromaDB/Pinecone) with embeddings
- **Real-time Communication**: WebSocket connections

## Step-by-Step Implementation Plan

### Step 1: Project Setup and Basic Structure

**Goal**: Create project structure and verify basic setup works

**Backend Setup**:

- Create Python virtual environment
- Initialize `backend/` directory with FastAPI project
- Create `requirements.txt` with initial dependencies (fastapi, uvicorn, websockets, python-dotenv)
- Create basic FastAPI server with health check endpoint
- Add `.env` file template for API keys

**Frontend Setup**:

- Initialize React app in `frontend/` directory
- Install basic dependencies (react, react-dom, axios)
- Create basic App component with "Hello World"
- Set up development scripts

**Verification**:

- Backend server starts on `http://localhost:8000` and health check returns 200
- Frontend runs on `http://localhost:3000` and displays basic UI
- No console errors in browser or terminal

**Files to create**:

- `backend/main.py` (basic FastAPI app)
- `backend/requirements.txt`
- `backend/.env.example`
- `frontend/package.json`
- `frontend/src/App.jsx`
- `README.md` (setup instructions)

---

### Step 2: Backend WebSocket Server

**Goal**: Establish WebSocket connection between frontend and backend

**Implementation**:

- Add WebSocket endpoint to FastAPI (`/ws`)
- Create WebSocket connection handler
- Implement basic message echo (send back what client sends)
- Add CORS middleware for React frontend

**Frontend**:

- Create WebSocket client utility
- Connect to backend WebSocket on component mount
- Send test message and receive echo
- Display connection status in UI

**Verification**:

- Frontend successfully connects to backend WebSocket
- Test message sent from frontend is echoed back
- Connection status indicator shows "Connected"
- Console logs show WebSocket messages

**Files to modify/create**:

- `backend/main.py` (add WebSocket endpoint)
- `frontend/src/utils/websocket.js` (WebSocket client)
- `frontend/src/components/ConnectionStatus.jsx`

---

### Step 3: Audio Capture Setup

**Goal**: Capture microphone audio from browser

**Implementation**:

- Use browser MediaDevices API to request microphone access
- Create audio context and media stream
- Display microphone permission status
- Show visual indicator when audio is being captured
- Handle permission denial gracefully

**Verification**:

- Browser prompts for microphone permission
- Permission granted shows "Microphone Active" indicator
- Permission denied shows error message
- No console errors related to audio access

**Files to create**:

- `frontend/src/hooks/useAudioCapture.js` (custom hook)
- `frontend/src/components/AudioCapture.jsx`
- Update `frontend/src/App.jsx` to include audio capture

---

### Step 4: Audio Streaming to Backend

**Goal**: Stream audio data from frontend to backend via WebSocket

**Implementation**:

- Convert MediaStream to audio chunks (using AudioWorklet or ScriptProcessorNode)
- Send audio chunks as binary data over WebSocket
- Backend receives and logs audio chunks
- Add audio format configuration (sample rate, channels)

**Verification**:

- Audio chunks are sent from frontend to backend
- Backend receives and logs audio data
- No WebSocket connection errors
- Audio streaming indicator shows active state

**Files to modify/create**:

- `frontend/src/hooks/useAudioCapture.js` (add streaming)
- `backend/main.py` (handle binary WebSocket messages)
- `backend/audio_processor.py` (audio handling utilities)

---

### Step 5: Hume AI Integration - Basic Connection

**Goal**: Connect backend to Hume AI API

**Implementation**:

- Install Hume AI Python SDK
- Add Hume API key to `.env`
- Create Hume client initialization
- Establish WebSocket connection to Hume API
- Test connection with dummy audio data
- Handle connection errors

**Verification**:

- Backend successfully connects to Hume API
- Connection status logged in backend console
- Error handling works for invalid API keys
- No connection timeouts

**Files to create/modify**:

- `backend/hume_client.py` (Hume AI client wrapper)
- `backend/.env` (add HUME_API_KEY)
- `backend/requirements.txt` (add hume SDK)
- Update `backend/main.py` to initialize Hume client

---

### Step 6: Hume AI - Audio Streaming and Transcription

**Goal**: Stream audio to Hume and receive transcriptions

**Implementation**:

- Forward audio chunks from frontend to Hume API
- Receive transcription results from Hume
- Parse Hume's `user_message` events for transcript text
- Send transcriptions back to frontend via WebSocket
- Display live transcript in frontend UI

**Verification**:

- Speaking into microphone produces transcriptions
- Transcripts appear in real-time on frontend
- Transcript text matches spoken words (basic accuracy check)
- No delays > 2 seconds between speech and transcript

**Files to modify/create**:

- `backend/hume_client.py` (add audio streaming and event handling)
- `backend/main.py` (forward audio to Hume, relay transcripts)
- `frontend/src/components/Transcript.jsx` (display transcript)
- Update `frontend/src/App.jsx` to show transcript

---

### Step 7: Emotion Detection - Parse and Display Top 3

**Goal**: Extract emotion scores from Hume and display top 3 emotions

**Implementation**:

- Parse emotion scores from Hume's `user_message` events
- Extract all emotion dimensions and their scores
- Sort emotions by score and select top 3
- Send top 3 emotions to frontend
- Create emotion display component with labels and scores
- Add visual indicators (colors, icons) for different emotions

**Verification**:

- Speaking with different emotional tones shows different top emotions
- Top 3 emotions update in real-time
- Emotion scores are displayed (e.g., "Frustration: 0.85")
- UI updates smoothly without flickering

**Files to modify/create**:

- `backend/hume_client.py` (parse emotion scores)
- `backend/main.py` (send emotions to frontend)
- `frontend/src/components/EmotionDisplay.jsx` (display top 3 emotions)
- `frontend/src/utils/emotionColors.js` (emotion color mapping)
- Update `frontend/src/App.jsx` to include emotion display

---

### Step 8: OpenAI Integration - Basic LLM Connection

**Goal**: Connect to OpenAI API and test basic completion

**Implementation**:

- Install OpenAI Python SDK
- Add OpenAI API key to `.env`
- Create OpenAI client wrapper
- Test basic completion with simple prompt
- Handle API errors and rate limits

**Verification**:

- Backend successfully calls OpenAI API
- Receives completion response
- Error handling works for invalid API keys
- API response logged in backend console

**Files to create/modify**:

- `backend/openai_client.py` (OpenAI client wrapper)
- `backend/.env` (add OPENAI_API_KEY)
- `backend/requirements.txt` (add openai SDK)
- Update `backend/main.py` to initialize OpenAI client

---

### Step 9: RAG Setup - Vector Database and Embeddings

**Goal**: Set up vector database and embedding system for knowledge retrieval

**Implementation**:

- Install vector database (ChromaDB or Pinecone)
- Install embedding model (OpenAI embeddings or sentence-transformers)
- Create knowledge base loader utility
- Create vector store initialization
- Add sample/test documents (if user provides later, replace these)
- Implement basic semantic search function

**Verification**:

- Vector database initializes successfully
- Test documents are embedded and stored
- Semantic search returns relevant results for test queries
- Search results are ranked by relevance

**Files to create/modify**:

- `backend/rag/vector_store.py` (vector database setup)
- `backend/rag/embeddings.py` (embedding utilities)
- `backend/rag/knowledge_loader.py` (document loading)
- `backend/requirements.txt` (add vector DB dependencies)
- `backend/knowledge_base/` (directory for documents - user will add files here)

---

### Step 10: RAG - Multi-Source Knowledge Retrieval

**Goal**: Implement retrieval from multiple knowledge sources (policies, FAQs)

**Implementation**:

- Organize knowledge base into categories (policies, FAQs)
- Create separate indexes or metadata filters for each category
- Implement multi-source retrieval function
- Retrieve top N results from each source
- Combine and rank results
- Add retrieval logging for debugging

**Verification**:

- Query retrieves results from both policy and FAQ sources
- Results are relevant to the query
- Retrieval completes in < 500ms
- Logs show which sources contributed results

**Files to modify/create**:

- `backend/rag/retriever.py` (multi-source retrieval)
- `backend/knowledge_base/policies/` (directory)
- `backend/knowledge_base/faqs/` (directory)
- Update `backend/rag/vector_store.py` to support categories

---

### Step 11: LLM Suggestions - Basic Prompt Engineering

**Goal**: Generate coaching suggestions using OpenAI with conversation context

**Implementation**:

- Create system prompt for customer service coach role
- Build prompt template with conversation context
- Include emotion information in prompt
- Call OpenAI API with formatted prompt
- Parse and return suggestion text
- Send suggestions to frontend

**Verification**:

- LLM generates relevant suggestions based on conversation
- Suggestions mention detected emotions
- Suggestions are actionable and concise
- Suggestions appear in frontend UI

**Files to modify/create**:

- `backend/llm/prompt_builder.py` (prompt construction)
- `backend/llm/suggestion_generator.py` (LLM call and parsing)
- Update `backend/main.py` to generate suggestions
- `frontend/src/components/SuggestionBox.jsx` (display suggestions)

---

### Step 12: LLM Suggestions - RAG Integration

**Goal**: Incorporate retrieved knowledge into LLM prompts

**Implementation**:

- Retrieve relevant knowledge based on conversation context
- Format retrieved snippets for prompt inclusion
- Update prompt template to include "Relevant Information" section
- Ensure LLM references retrieved knowledge in suggestions
- Add source attribution (optional)

**Verification**:

- Suggestions reference company policies/FAQs when relevant
- Suggestions are more accurate with knowledge base
- Retrieval happens before LLM call
- Suggestions include actionable steps based on policies

**Files to modify/create**:

- Update `backend/llm/prompt_builder.py` (add RAG context)
- Update `backend/llm/suggestion_generator.py` (integrate retrieval)
- Update `backend/main.py` (orchestrate RAG + LLM)

---

### Step 13: Real-Time Pipeline - End-to-End Flow

**Goal**: Connect all components for real-time suggestion generation

**Implementation**:

- Trigger suggestion generation on each new transcript
- Pass transcript, emotions, and conversation history to LLM
- Perform RAG retrieval in parallel with emotion processing
- Stream suggestions to frontend as they're generated
- Handle rapid successive utterances (queue or debounce)
- Add loading states in frontend

**Verification**:

- Complete flow: Audio → Hume → Emotions + Transcript → RAG → LLM → Suggestion
- Suggestions appear within 2-3 seconds of customer speaking
- No blocking or freezing in UI
- Multiple utterances handled correctly

**Files to modify/create**:

- `backend/main.py` (orchestrate full pipeline)
- `backend/pipeline/orchestrator.py` (pipeline coordination)
- Update frontend components to show loading states
- `frontend/src/components/LoadingIndicator.jsx`

---

### Step 14: UI Polish - Complete Dashboard Layout

**Goal**: Create professional, intuitive dashboard interface

**Implementation**:

- Design two-column layout (transcript/emotions left, suggestions right)
- Style emotion display with icons and color coding
- Style suggestion box with clear typography
- Add call status indicator
- Add connection status indicators
- Make UI responsive and accessible
- Add smooth transitions and animations

**Verification**:

- Dashboard is visually clear and professional
- All information is easily readable at a glance
- UI works on different screen sizes
- No layout issues or overflow

**Files to modify/create**:

- `frontend/src/components/Dashboard.jsx` (main layout)
- `frontend/src/styles/` (CSS/styled-components)
- Update all existing components for styling
- `frontend/src/App.jsx` (use Dashboard component)

---

### Step 15: Dual Audio Capture - Client and CSR

**Goal**: Capture and distinguish between client and CSR audio

**Implementation**:

- Modify audio capture to handle dual streams
- Use speaker output capture for client audio (if available)
- Or use separate microphone inputs
- Tag audio chunks with source (client/CSR)
- Send both streams to Hume (or process separately)
- Display transcripts with speaker labels

**Verification**:

- Both client and CSR audio are captured
- Transcripts show speaker labels (Client/CSR)
- Emotions are detected for client audio
- System distinguishes between speakers

**Files to modify/create**:

- Update `frontend/src/hooks/useAudioCapture.js` (dual capture)
- Update `backend/main.py` (handle dual streams)
- Update `frontend/src/components/Transcript.jsx` (show speaker labels)
- `backend/audio_processor.py` (audio source tagging)

---

### Step 16: Conversation Context Management

**Goal**: Maintain conversation history for better LLM context

**Implementation**:

- Store conversation history (transcripts with timestamps)
- Maintain rolling window of recent exchanges
- Include agent responses in context
- Format conversation history for LLM prompt
- Limit context window to prevent token overflow

**Verification**:

- LLM suggestions reference previous conversation
- Context window is managed efficiently
- Long conversations don't cause errors
- Suggestions improve with more context

**Files to modify/create**:

- `backend/context/conversation_manager.py` (history management)
- Update `backend/llm/prompt_builder.py` (include history)
- Update `backend/main.py` (manage conversation state)

---

### Step 17: Error Handling and Edge Cases

**Goal**: Robust error handling and graceful degradation

**Implementation**:

- Handle API failures (Hume, OpenAI) gracefully
- Add retry logic for transient failures
- Handle network disconnections
- Handle audio capture failures
- Add user-friendly error messages
- Log errors for debugging

**Verification**:

- System continues working if one component fails
- Error messages are clear and actionable
- Reconnection works after network issues
- No crashes on edge cases

**Files to modify/create**:

- `backend/utils/error_handler.py` (error handling utilities)
- Update all components with error handling
- `frontend/src/components/ErrorBoundary.jsx`
- Update WebSocket client with reconnection logic

---

### Step 18: Performance Optimization and Testing

**Goal**: Optimize latency and test full system

**Implementation**:

- Profile and optimize slow components
- Implement request queuing/debouncing
- Add caching where appropriate
- Test with real conversations
- Measure end-to-end latency
- Optimize LLM prompt length
- Test with multiple concurrent sessions

**Verification**:

- End-to-end latency < 3 seconds
- System handles rapid speech
- No memory leaks during long sessions
- Performance is acceptable under load

**Files to modify/create**:

- `backend/utils/performance.py` (profiling utilities)
- Update components based on profiling results
- `tests/` (test suite)
- `docs/PERFORMANCE.md` (performance notes)

---

## Testing Checklist for Each Step

For each step, verify:

- [ ] Application starts without errors
- [ ] No console errors (browser or terminal)
- [ ] Required functionality works as described
- [ ] UI updates correctly (if applicable)
- [ ] Error handling works (test with invalid inputs)
- [ ] Code is clean and follows best practices

## Dependencies Summary

**Backend**:

- fastapi, uvicorn, websockets
- hume-py (Hume AI SDK)
- openai (OpenAI SDK)
- chromadb or pinecone-client (vector DB)
- sentence-transformers or openai (embeddings)
- python-dotenv

**Frontend**:

- react, react-dom
- axios or fetch API
- WebSocket API (native browser)

## Environment Variables Required

- `HUME_API_KEY` - Hume AI API key
- `OPENAI_API_KEY` - OpenAI API key
- `VECTOR_DB_API_KEY` - If using Pinecone (optional for ChromaDB)

## Knowledge Base Structure

```
backend/knowledge_base/
  ├── policies/
  │   └── (user will add policy documents here)
  └── faqs/
      └── (user will add FAQ documents here)
```

## Notes

- Each step builds on the previous one
- Steps can be tested independently
- If a step fails, previous steps should still work
- User will provide knowledge base documents after RAG setup is complete
- Audio capture assumes same device for client and CSR (may need adjustment based on actual setup)

### To-dos

- [ ] Project setup: Create backend (FastAPI) and frontend (React) structure, verify both run without errors
- [ ] Backend WebSocket: Implement WebSocket server and client connection, test message echo
- [ ] Audio capture: Request microphone permission and capture audio stream in browser
- [ ] Audio streaming: Stream audio chunks from frontend to backend via WebSocket
- [ ] Hume AI connection: Connect backend to Hume AI API and verify connection
- [ ] Hume transcription: Stream audio to Hume and display live transcriptions in frontend
- [ ] Emotion detection: Parse emotion scores from Hume and display top 3 emotions in UI
- [ ] OpenAI integration: Connect to OpenAI API and test basic completion
- [ ] RAG setup: Initialize vector database, embeddings, and basic semantic search
- [ ] Multi-source RAG: Implement retrieval from policies and FAQs knowledge sources
- [ ] LLM suggestions: Generate coaching suggestions using OpenAI with conversation and emotion context
- [ ] RAG integration: Incorporate retrieved knowledge into LLM prompts for accurate suggestions
- [ ] Real-time pipeline: Connect all components for end-to-end real-time suggestion generation
- [ ] UI polish: Create professional dashboard layout with proper styling and components
- [ ] Dual audio capture: Capture and distinguish between client and CSR audio streams
- [ ] Conversation context: Maintain conversation history for better LLM context and suggestions
- [ ] Error handling: Implement robust error handling and graceful degradation for all components
- [ ] Performance optimization: Profile, optimize latency, and test full system under load

