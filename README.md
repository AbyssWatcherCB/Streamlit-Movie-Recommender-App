# 🎬 Movie Recommender System

## 📌 Project Overview

This is a **Movie Recommender System** built using  **Streamlit** . It suggests similar movies based on user selection using a similarity matrix. The recommendations are powered by **cosine similarity** and fetched dynamically from  **The Movie Database (TMDB) API** .

## 🚀 Features

✅ Select a movie from a dropdown menu

✅ Displays the selected movie’s poster

✅ Generates and shows **5 similar movies**

✅ Displays movie details like **release date, rating, genres, and overview**

✅ Fetches movie posters from **TMDB API** for better visualization

## 📂 Project Structure

```
movie-recommender/
│── app.py                   # Streamlit app script
│── movies_list.pkl           # Pickled movie dataset
│── similarity.pkl            # Pickled similarity matrix
│── requirements.txt          # Required dependencies
│── README.md                 # Project documentation
```

## 🛠 Installation & Setup

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/YOUR_USERNAME/movie-recommender.git
cd movie-recommender
```

### 2️⃣ Create a Virtual Environment (Optional but Recommended)

```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 3️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

### 4️⃣ Run the Application

```sh
streamlit run app.py
```

## 📜 License

This project is  **MIT Licensed** . You’re free to modify and distribute it!
