# Reddit_Persona_Creator
A Reddit scrapper to build a Persona profile for the user, highlighting their personality, goals, motivations, frustrations, etc. Combines LLM integration with Reddit API requests.
This project analyzes a Reddit user's public activity (posts and comments) and uses Google's Gemini API to generate a qualitative **User Persona** with citations from their actual Reddit content.

---

## Features

- Scrapes Reddit posts and comments
- Generates a detailed user persona using **Gemini 1.5 Flash**
- Saves output as a text file in the `output/` directory
- Includes citation links to each post/comment used

---

## Tech Stack

- Python
- [Google Gemini API (Free Tier)](https://ai.google.dev/)
- [Reddit API via `praw`](https://praw.readthedocs.io/)
- `.env` file for secure API key storage

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/reddit-persona-gen.git
cd reddit-persona-gen
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up .env file
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=reddit_persona_script
GEMINI_API_KEY=your_google_gemini_api_key

## Run the script
python reddit_persona_gemini.py.
Enter a reddit url when prompted.