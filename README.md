# University Assistant (BIlli)

A university assistant AI inspired by Iron Man's JARVIS, designed to act as a classy, sarcastic butler and university receptionist. BIlli can answer questions, perform web searches, get weather updates, and send emails. It can also speak Bangla.

## Features

- Persona-based AI assistant (BIlli)
- Weather updates
- Web search (DuckDuckGo)
- Email sending
- Sarcastic, butler-style responses
- Bangla language support

## Setup Instructions

### 1. Clone the Repository

```powershell
git clone <your-repo-url>
cd friday_jarvis
```

### 2. Create and Activate a Virtual Environment

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root and add any required environment variables (API keys, credentials, etc.) as needed by your plugins and tools.

### 5. Running the Project

#### Run in Console Mode

```powershell
python .\agent.py console
```

#### Run in Server/Dev Mode

```powershell
python .\agent.py dev
```

---

## Project Structure

- `agent.py` - Main entry point for the assistant
- `prompts.py` - Persona and prompt instructions
- `tools.py` - Tools for weather, web search, and email
- `requirements.txt` - Python dependencies

## Authors

- Nakibul Islam
- Hana Sultan
- Umme Aiman

---
