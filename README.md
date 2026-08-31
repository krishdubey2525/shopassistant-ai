# 🛍️ ShopAssist AI

AI-powered product recommendation assistant that understands natural-language shopping requests and recommends products based on **budget, category, and rating**.

## ✨ Features

- 🤖 Local AI recommendations
- 💬 Natural-language queries
- 💰 Budget filtering
- ⭐ Rating filtering
- 🏷️ Category detection
- 🗄️ SQLite database
- ⚡ FastAPI backend
- 🎨 React frontend

## 🛠️ Tech Stack

**Frontend:** React, Vite, JavaScript, CSS  
**Backend:** Python, FastAPI, Uvicorn  
**AI:** Ollama, Llama 3.2 3B  
**Database:** SQLite  
**Tools:** Git, GitHub, Swagger UI

## 🏗️ Architecture

```text
User
 ↓
React Frontend
 ↓
FastAPI Backend
 ↓
Llama 3.2 + Ollama
 ↓
Product Filtering
 ↓
SQLite Database
 ↓
Recommendation
