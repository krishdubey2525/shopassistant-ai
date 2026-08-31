\# 🛍️ ShopAssist AI



An AI-powered product recommendation assistant that understands natural-language shopping requests and recommends suitable products based on the available product data.



ShopAssist AI combines a \*\*React frontend\*\*, \*\*FastAPI backend\*\*, \*\*SQLite database\*\*, and \*\*Ollama with Llama 3.2\*\* to provide conversational product recommendations.



\---



\## ✨ Features



\- 🤖 AI-powered product recommendations

\- 💬 Natural-language shopping queries

\- 💰 Budget-aware recommendations

\- 🏷️ Product category detection

\- ⭐ Rating-based product filtering

\- 🗄️ Product data stored in SQLite

\- ⚡ FastAPI REST API

\- 🎨 Modern React chat interface

\- 🧠 Local LLM using Ollama + Llama 3.2

\- 🔒 Runs locally without requiring a paid cloud AI API



\---



\## 🏗️ System Architecture



```text

&#x20;                   User

&#x20;                     │

&#x20;                     ▼

&#x20;            ┌─────────────────┐

&#x20;            │  React Frontend │

&#x20;            │    Vite + CSS   │

&#x20;            └────────┬────────┘

&#x20;                     │

&#x20;                HTTP Request

&#x20;                     │

&#x20;                     ▼

&#x20;            ┌─────────────────┐

&#x20;            │ FastAPI Backend │

&#x20;            │                 │

&#x20;            │ /recommend      │

&#x20;            │ /health         │

&#x20;            └───────┬─────────┘

&#x20;                    │

&#x20;         ┌──────────┴──────────┐

&#x20;         ▼                     ▼

&#x20;┌─────────────────┐   ┌─────────────────┐

&#x20;│ Product Database│   │ Ollama / Llama  │

&#x20;│     SQLite      │   │      3.2        │

&#x20;└─────────────────┘   └─────────────────┘

🛠️ Tech Stack

Frontend

React

Vite

Axios

JavaScript

CSS

Backend

Python

FastAPI

Uvicorn

Pydantic

AI

Ollama

Llama 3.2 3B

Database

SQLite

Development Tools

Git

GitHub

VS Code / IntelliJ

Swagger UI

📁 Project Structure

shopassistant-ai/

│

├── app/

│   ├── \_\_init\_\_.py

│   ├── ai\_service.py

│   ├── database.py

│   ├── main.py

│   ├── models.py

│   └── products.py

│

├── frontend/

│   ├── public/

│   ├── src/

│   │   ├── assets/

│   │   ├── App.css

│   │   ├── App.jsx

│   │   ├── index.css

│   │   └── main.jsx

│   ├── package.json

│   ├── package-lock.json

│   └── vite.config.js

│

├── .gitignore

├── requirements.txt

└── README.md

🤖 AI Model



ShopAssist AI uses a locally running Llama 3.2 3B model through Ollama.



The model is used to understand the user's shopping request and generate a natural-language recommendation.



Example:



User:

I need a laptop under ₹70,000 for programming.



ShopAssist AI:

I recommend the CodeMaster X15...

🔌 API

Health Check

GET /health



Used to verify that the backend is running.



Product Recommendation

POST /recommend



Example request:



{

&#x20; "message": "I need a laptop under ₹70,000 for programming"

}



Example response:



{

&#x20; "response": "I recommend the CodeMaster X15 laptop..."

}

⚙️ Backend Setup

1\. Clone the repository

git clone https://github.com/krishdubey2525/shopassistant-ai.git

cd shopassistant-ai

2\. Create a virtual environment

python -m venv venv

3\. Activate the environment



Windows:



venv\\Scripts\\activate

4\. Install dependencies

pip install -r requirements.txt

5\. Start Ollama



Make sure Ollama is installed and running.



Check the installation:



ollama --version



Pull the model:



ollama pull llama3.2:3b



Test the model:



ollama run llama3.2:3b

6\. Start the FastAPI server

uvicorn app.main:app --reload



The backend will be available at:



http://127.0.0.1:8000



Swagger API documentation:



http://127.0.0.1:8000/docs

🎨 Frontend Setup



Open another terminal:



cd frontend



Install dependencies:



npm install



Start the development server:



npm run dev



The frontend will normally be available at:



http://localhost:5173

💡 Example Queries



ShopAssist AI can handle requests such as:



Laptop under ₹70,000 for programming

Smartphone under ₹50,000

Headphones under ₹5,000

Watch under ₹10,000

Laptop with rating above 4.5





🚀 How It Works

The user enters a shopping requirement in the React interface.

The frontend sends the request to the FastAPI /recommend endpoint.

The backend processes the natural-language request.

Product requirements such as category, budget and rating are extracted.

Available products are evaluated against the requirements.

Ollama/Llama 3.2 generates the recommendation.

The recommendation is returned to the React frontend.

The result is displayed in the conversational chat interface.

🎯 Project Objective



The objective of ShopAssist AI is to demonstrate how a locally running Large Language Model can be integrated with a web application to create an intelligent product recommendation system.



The project combines:



REST API development

Natural-language processing

Local LLM integration

Database-driven product filtering

React frontend development

AI-assisted decision making

👨‍💻 Author



Krish Dubey



Computer Science Engineering Student



GitHub:

https://github.com/krishdubey2525



📌 Future Improvements

Product images

More product categories

Conversation memory

Better product ranking

Product comparison

Authentication

Deployment to a cloud platform

More advanced recommendation logic

