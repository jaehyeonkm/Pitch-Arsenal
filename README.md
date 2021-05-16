# Pitch-Arsenal
<img src="https://github.com/jaehyeonkm/Pitch-Arsenal/blob/master/Images/Achter%2C%20A.J.png" width="100%"></img>
<img src="https://github.com/jaehyeonkm/Pitch-Arsenal/blob/master/Images/Achter%2C%20A.J_2.png" width="100%"></img>
<img src="https://github.com/jaehyeonkm/Pitch-Arsenal/blob/master/Images/Dropdown.png" width="100%"></img>

## Goal:
Generate web application that displays the pitch-type signatures of MLB players by frequency, speed, and break. Data ranges from 2008 ~ 2021.

## Requirements:
```
python
dash
numpy
pandas
pybaseball
plotly.express
```

Dataframe `statcast_df` must be downloaded locally using:
```
statcast_df = statcast(start_dt = '2008-01-01', end_dt = '2021-05-31')
```

## Running:
For help run:
```
python app.py
```
