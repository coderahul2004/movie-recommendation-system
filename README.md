# 🎬 Movie Recommendation System

This is a Machine Learning project that recommends similar movies using TF-IDF and NLP.

It also shows movie posters and ratings using OMDb API.

---

## 🚀 Features

- Search any movie
- Get recommended movies
- Show posters 
- FastAPI backend
- Streamlit frontend

---

## 🛠️ Technologies Used

- Python
- Scikit-learn (TF-IDF)
- FastAPI
- Streamlit
- OMDb API

---

## ▶️ How to Run

### 1. Install requirements
pip install -r requirements.txt

### 2. Add API key
Create a file named `.env` and write:
OMDB_API_KEY=your_api_key_here

### 3. Run backend
uvicorn main:app --reload

### 4. Run frontend
streamlit run app.py

---

## 📁 Files

- main.py → backend
- app.py → frontend
- df.pkl → dataset
- tfidf_matrix.pkl → model

---

## 👨‍💻 Author

Rahul Samanta
