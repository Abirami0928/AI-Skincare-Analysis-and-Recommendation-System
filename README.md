# SkinSense AI – AI-Powered Skincare Analysis & Recommendation System

## Overview
SkinSense AI is an AI-powered skincare platform that analyzes users' skin types and provides personalized skincare product recommendations based on their skin concerns and budget.

The system combines Machine Learning, product recommendation techniques, and Retrieval-Augmented Generation (RAG) to provide personalized and research-supported skincare guidance.

## Key Features

- **Skin Type Detection:** Predicts skin type from an uploaded skin image using a Machine Learning model.
- **Personalized Recommendations:** Recommends skincare products based on predicted skin type, skin concerns, and budget.
- **Ingredient-Based Matching:** Identifies relevant skincare ingredients and matches them with available products.
- **Research-Based Assistant:** Uses RAG to retrieve relevant information from skincare research documents.
- **Budget Filtering:** Displays suitable products within the user's specified budget.

## Technology Stack

| Component | Technologies |
|---|---|
| Frontend | React.js, HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| Machine Learning | Scikit-learn, Logistic Regression |
| Data Processing | Pandas, NumPy |
| Vector Database | ChromaDB |
| Embeddings | Sentence Transformers |
| AI Integration | Gemini API |
| Database | MongoDB |

## Project Architecture

React.js Frontend → FastAPI Backend → Machine Learning Model → Product Recommendation Engine → RAG-Based Skincare Assistant

## Dataset

- Skin image dataset for skin type classification.
- Skincare product dataset containing 1,138 products.
- Skincare research documents for knowledge retrieval.

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/Abirami0928/AI-Skincare-Analysis-and-Recommendation-System.git
cd AI-Skincare-Analysis-and-Recommendation-System
```

### 2. Backend setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Start the FastAPI backend using your configured application command.

### 3. Frontend setup

```bash
cd frontend
npm install
npm run dev
```

## Project Objective

To develop an intelligent skincare assistance platform that combines machine learning, product recommendations, and research-based information retrieval to help users make informed skincare decisions.

## Author

**Abirami R**

AI/ML and Data Science Enthusiast