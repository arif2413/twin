# Real-Time Emotion-Aware Customer Service Assistant

A real-time customer service assistant that uses emotion detection, transcription, and AI-powered suggestions to help customer service representatives provide better support.

## Architecture

- **Frontend**: React web app (browser-based)
- **Backend**: Python (FastAPI) with WebSocket support
- **Audio Processing**: Hume AI API (WebSocket streaming)
- **LLM**: OpenAI GPT-4/GPT-3.5
- **RAG**: Vector database (ChromaDB/Pinecone) with embeddings
- **Real-time Communication**: WebSocket connections

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a Python virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file from the example:
   ```bash
   copy .env.example .env  # Windows
   cp .env.example .env    # macOS/Linux
   ```

6. Edit `.env` and add your API keys (you can leave them empty for now if you don't have them yet)

7. Run the backend server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

   The backend should be running at `http://localhost:8000`
   - Health check: `http://localhost:8000/health`
   - API docs: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

   The frontend should be running at `http://localhost:3000`

## Verification

After setup, verify:

- Backend server starts on `http://localhost:8000` and health check returns 200
- Frontend runs on `http://localhost:3000` and displays "Hello World"
- No console errors in browser or terminal

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment variables template
│   └── .env                 # Environment variables (create from .env.example)
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── main.jsx         # React entry point
│   │   └── index.css        # Global styles
│   ├── index.html           # HTML template
│   ├── package.json         # Node.js dependencies
│   └── vite.config.js       # Vite configuration
└── README.md                # This file
```

## Next Steps

Follow the implementation plan in `claude.md` to continue building the application step by step.

