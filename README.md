# India AQI Predictor

A machine learning web app that predicts the Air Quality Index (AQI) for Indian cities using pollutant data.

## Live Demo

https://india-aqi-predictor.streamlit.app/

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

Air quality data from 26 Indian cities (2015–2020).

---

This was my first end-to-end machine learning project covering data cleaning, exploratory data analysis, model building, and deployment.
