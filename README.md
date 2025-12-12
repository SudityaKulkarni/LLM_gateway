# LLM Safety Gateway

A comprehensive safety layer for LLM applications with a React frontend and FastAPI backend.

## Features

- 🛡️ **Safe Generate**: Sanitize prompts and generate safe AI responses
- 📊 **Comprehensive Check**: Run all safety detectors simultaneously
- 🔓 **Jailbreak Detection**: Detect attempts to bypass AI safety measures
- ☠️ **Toxicity Detection**: Identify toxic and offensive language
- 🔒 **PII Detection**: Find personally identifiable information (emails, phone numbers, SSN, Aadhar, etc.)
- 💉 **Prompt Injection Detection**: Detect malicious prompt injection attempts
- 🔤 **Gibberish Detection**: Identify nonsensical or spam text
- 📈 **Entropy Analysis**: Analyze text randomness and patterns
- 📋 **Rule-Based Detection**: Pattern-based safety checks

## Project Structure

```
llm_safety_python/
├── frontend/                 # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Page components for each detector
│   │   ├── api.js           # API client
│   │   ├── App.js           # Main app component
│   │   └── index.js         # Entry point
│   └── package.json
├── detectors/               # Safety detector modules
├── services/                # Business logic services
├── schemas/                 # Pydantic schemas
├── utils/                   # Utility functions
└── main.py                  # FastAPI backend
```

## Setup Instructions

### Backend Setup

1. **Create and activate virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```
   GEMINI_API_KEY=your-gemini-api-key-here
   ```

4. **Run the backend:**
   ```powershell
   uvicorn main:app --reload
   ```
   Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```powershell
   cd frontend
   ```

2. **Install dependencies:**
   ```powershell
   npm install
   ```

3. **Start development server:**
   ```powershell
   npm start
   ```
   Frontend will be available at `http://localhost:3000`

## API Endpoints

### Detection Endpoints
- `POST /detect_jailbreak` - Detect jailbreak attempts
- `POST /detect_toxicity` - Detect toxic content
- `POST /detect_pii` - Detect PII
- `POST /detect_prompt_injection` - Detect prompt injection
- `POST /detect_gibberish` - Detect gibberish text
- `POST /shannon_entropy` - Calculate entropy
- `POST /jailbreak_rules` - Rule-based jailbreak detection

### Utility Endpoints
- `POST /sanitize` - Sanitize prompts with Gemini
- `POST /comprehensive_check` - Run all detectors
- `POST /safe_generate_gemini` - Safe generation with sanitization
- `POST /redact_pii` - Redact PII from text

### Health Check
- `GET /health` - Check API health and loaded models
- `GET /` - API information

## Usage Examples

### Individual Detector (Frontend)
Each detector has its own page where you can:
1. Enter text in the input box
2. Click "Check Safety"
3. View detailed results with confidence scores

### Comprehensive Check
Run all detectors at once:
1. Navigate to "Comprehensive Check"
2. Enter your prompt
3. View all detector results in a single dashboard

### Safe Generate
Generate safe AI responses:
1. Navigate to "Safe Generate"
2. Enter your Gemini API key (only used for this request)
3. Enter your prompt
4. View sanitized prompt and AI response
5. See all safety checks that were performed

## Technologies Used

### Frontend
- React 18
- React Router v6
- Axios
- Tailwind CSS

### Backend
- FastAPI
- Transformers (Hugging Face)
- Google Generative AI (Gemini)
- PyTorch
- Pydantic

## Development

### Running Tests
```powershell
# Backend tests
python -m pytest

# Frontend tests
cd frontend
npm test
```

### Building for Production
```powershell
# Frontend
cd frontend
npm run build
```

## Environment Variables

- `GEMINI_API_KEY` - Your Google Gemini API key for AI generation

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
