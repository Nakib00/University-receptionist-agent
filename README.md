# University Assistant (BIlli)

A university assistant AI inspired by Iron Man's JARVIS, designed to act as a classy, sarcastic butler and university receptionist. BIlli can answer questions, perform web searches, get weather updates, and send emails. It can also speak Bangla.

## Features

- Persona-based AI assistant (Billi)
- Weather updates
- Web search (DuckDuckGo)
- Sarcastic, butler-style responses
- Bangla language support
- Web-based interface for managing university data and unanswered questions.

## Data Manager Web Interface

The project includes a Flask-based web interface to manage the university's knowledge base and review questions that the AI could not answer.

- **Questions Inbox**: View and manage questions that users have asked but the AI could not answer from its knowledge base.
- **Data Editor**: Add, view, and update the JSON data that the AI uses to answer university-related questions directly from the browser.

![Data Manager Webpage](https://github.com/Nakib00/University-receptionist-agent/blob/main/static/image/University_Receptionist_Agent_Data_Manager_page.png?raw=true)

## AI Model Training

The `Train_model` directory contains the scripts and data for training the intent classification model. This model does not learn the answers to questions directly, but rather learns to categorize a user's query into a specific 'tag' or 'intent' (e.g., `greeting`, `departmentheadofcse`, `library_bn`).

### How it Works

* **Intent Files**: The training data is defined in two main files:
    * `intents.json`: Contains the primary intents, patterns, and responses in English.
    * `intents_bengali.json`: Contains intents, patterns, and responses in the local language (Bangla).
* **Training Script**: The `train.py` script reads both `intents.json` and `intents_bengali.json`, combining them to create a multilingual training dataset. It then trains a `PyTorch`-based neural network to classify sentences into the defined tags. The trained model is saved as `data.pth`.
* **University Data**: The extensive information in `university_data.py` is **not** used for training the neural network. Instead, it acts as a real-time knowledge base that the `get_university_info` tool searches when a user asks a question about the university. This approach allows the knowledge base to be updated without needing to retrain the entire model.

### How to Re-train the Model

If you modify the `intents.json` or `intents_bengali.json` files, you will need to re-train the model.

1.  Navigate to the training directory:
    ```powershell
    cd Train_model
    ```
2.  Install the required Python packages for training:
    ```powershell
    pip install -r requirements.txt
    ```
3.  Run the NLTK downloader script:
    ```powershell
    python download_nltk_data.py
    ```
4.  Run the training script:
    ```powershell
    python train.py
    ```
    This will create an updated `data.pth` file in the `Train_model` directory. You will need to move this file to the project's root directory for the agent to use it.


## Setup Instructions

### 1. Clone the Repository

```powershell
git clone <your-repo-url>
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

Create a `.env` file in the project root and add any required environment variables as needed by your plugins and tools.

### 5. Running the Project

#### Run in Console Mode

```powershell
python .\agent.py console
```

#### Run in Server/Dev Mode

```powershell
python .\agent.py dev
```

#### Running the Data Manager Web App
To run the Flask web server for the data manager interface:

```powershell
python .\app.py
```
You can then access the interface at http://127.0.0.1:5000 in your web browser.

---


