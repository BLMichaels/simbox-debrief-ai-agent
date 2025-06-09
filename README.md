# SimBox Debrief AI Agent

An AI-powered debriefing agent for pediatric emergency simulation cases, based on the PEARLS (Promoting Excellence and Reflective Learning in Simulation) model.

## Features

- Interactive text-based debriefing
- Voice-based interaction (speech-to-text and text-to-speech)
- PEARLS model-based debriefing structure
- Real-time feedback and guidance
- Support for multiple simulation scenarios

## Project Structure

```
.
├── backend/           # FastAPI backend
├── frontend/         # React frontend
├── requirements.txt  # Python dependencies
└── README.md        # This file
```

## Setup Instructions

### Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the backend server:
```bash
cd backend
uvicorn main:app --reload
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run the development server:
```bash
npm run dev
```

## PEARLS Model Integration

The debriefing agent follows the PEARLS model structure:
- P: Preparation and Planning
- E: Engagement
- A: Analysis
- R: Reflection
- L: Learning
- S: Summary

## License

MIT License 