# India AQI Predictor

A machine learning web app that predicts the Air Quality Index (AQI) for Indian cities using pollutant data.

## Live Demo

https://india-aqi-predictor.streamlit.app/

## Important Note

This application is deployed using Streamlit Community Cloud's free hosting plan. The app may automatically go to sleep after periods of inactivity. If you encounter a "This app has gone to sleep" message, simply click **"Yes, get this app back up!"** and wait a few seconds for it to restart.

## About

I built this project to explore whether AQI can still be estimated when some pollutant readings are missing. In real life, sensors don't always work perfectly, but air quality information is still important.

The model predicts AQI using the available data and can handle missing pollutant values during prediction.

## Features

* Predict AQI for Indian cities
* Works even when some pollutant values are unavailable
* Shows CPCB AQI categories
* Provides simple health recommendations
* Built with Streamlit for an interactive experience

## Tech Stack

* Python
* Pandas & NumPy
* XGBoost
* Scikit-learn
* Category Encoders
* Streamlit

## Dataset


This project uses historical air quality data collected from 26 Indian cities between 2015 and 2020. After cleaning and preprocessing the data, it was used to train the AQI prediction model. The cleaned dataset used in this project is included in this repository as `city_day_training_data.csv`.


---

This was my first end-to-end machine learning project covering data cleaning, exploratory data analysis, model building, and deployment.
