# Kantamal Streamflow Forecasting using Deep Learning

## Project Overview

This project focuses on **daily streamflow forecasting for the Kantamal catchment in the Mahanadi River Basin, Odisha, India**, using deep learning and hydrological data analysis.

The primary objective is to study and compare:

- Long Short-Term Memory (LSTM)
- Bidirectional LSTM (BiLSTM)
- Transformer-based models

for streamflow forecasting.

The project also involves GIS-based catchment delineation and preparation of hydrometeorological variables such as rainfall, temperature, water level, and streamflow.

---

## Study Area

**Gauge / Station:** Kantamal  
**River:** Tel River  
**River Basin:** Mahanadi River Basin  
**State:** Odisha, India

QGIS is being used to locate the gauging station and delineate the upstream catchment.

---

## Project Workflow

```text
Hydrological & Meteorological Data
                |
                v
        Data Preprocessing
                |
                v
        Time-Series Sequences
                |
        -------------------
        |        |        |
       LSTM    BiLSTM  Transformer
        |        |        |
        -------------------
                |
                v
        Model Evaluation
                |
                v
       Streamflow Forecast
