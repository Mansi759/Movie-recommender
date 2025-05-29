![image](https://github.com/user-attachments/assets/e74e239a-03b7-49e4-afb6-4f3f75bfd1d0)# 🎬 Movie Recommender System

A Streamlit-based web app that recommends movies based on user input. It leverages movie metadata and similarity scores to provide personalized movie suggestions along with detailed movie information, posters, and cast.

---

## Features

- Search for a movie and get top 5 recommended similar movies.
- View detailed movie information, including overview, rating, popularity, release year, genre, and cast.
- Browse different movie sections: Trending, Top Rated, Latest Releases, and Blockbusters.
- Fetch movie posters and cast images dynamically using TMDB API.
- User-friendly interface powered by Streamlit.

---

## Demo

You can try the live demo here: https://movie-recommender-mxyhjy6uthqyizzwtch8jn.streamlit.app/



![image](https://github.com/user-attachments/assets/3b91b412-a1d1-449b-b8eb-805fa7965ad0)

![image](https://github.com/user-attachments/assets/112336f5-cc2f-4205-9aa5-88a327e2479f)

![image](https://github.com/user-attachments/assets/27cb7216-d719-4305-9eb2-d3df3971a1cd)

![image](https://github.com/user-attachments/assets/341c50ce-8238-4fa6-acfa-6122f96cad38)

![image](https://github.com/user-attachments/assets/5f140193-df0e-4b12-9a23-8eb4605e5b46)

![image](https://github.com/user-attachments/assets/ea378df5-61d2-4d7e-a13f-f637a2dbde5b)









---

## Getting Started

### Prerequisites

- Python 3.7+
- [Streamlit](https://streamlit.io/)
- Required libraries (see `requirements.txt`)

### Installation

1. Clone the repo:
    ```bash
    git clone https://github.com/yourusername/movie-recommender.git
    cd movie-recommender
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set your TMDB API key as an environment variable:
    ```bash
    export API_KEY="your_tmdb_api_key"
    ```
    Or on Windows (PowerShell):
    ```powershell
    setx API_KEY "your_tmdb_api_key"
    ```

### Running the App

```bash
streamlit run app.py
