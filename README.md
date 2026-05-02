#  Personalized Music Recommendation System

It is a machine learning project that generates personalized music recommendations using user listening behavior from the Last.fm dataset. The system supports both existing users and new users using collaborative filtering techniques.

---

##  Features

- Recommend artists for **existing users** based on listening history
- Handle **cold-start problem** by allowing new users to select favorite artists
- Uses **collaborative filtering** with cosine similarity
- Normalized recommendation scores (0 to 1)
- Interactive web application built with Streamlit

---

---

## Dataset

This project uses the **HetRec 2011 Last.fm 2K Dataset that can be  downloaded here:  
https://grouplens.org/datasets/hetrec-2011/

## How to Run

### Install dependencies
pip install -r requirements.txt
### Run Streamlit app
streamlit run app.py

## Screenshots

<p align="center">
  <img src="output1.png" width="700">
</p>

<p align="center">
  <img src="output2.png" width="700">
</p>




