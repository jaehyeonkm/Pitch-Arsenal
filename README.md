# Pitch-Arsenal
<img src="https://github.com/jaehyeonkm/Pitch-Arsenal/blob/master/Images/Achter%2C%20A.J.png" width="100%"></img>
<img src="https://github.com/jaehyeonkm/Pitch-Arsenal/blob/master/Images/Achter%2C%20A.J_2.png" width="100%"></img>
<img src="https://github.com/jaehyeonkm/Pitch-Arsenal/blob/master/Images/Dropdown.png" width="100%"></img>

## Goal:
Generate web application that displays the pitch-type signatures of MLB players by frequency, speed, and break. Data ranges from 2008 ~ 2021.

## Dataset
The data used for this project is provided by the `pybaseball` package, which focuses on baseball data analysis. The package retrieves statcast data, pitching, batting, and team statistics, etc.

pybaseball GitHub page: https://github.com/jldbc/pybaseball
The README.md on their GitHub repo provides summary of the main functions provided by this package as well as examples.

To understand the variables used in this project, please see the gloassary in https://baseballsavant.mlb.com/csv-docs.

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
statcast_df.to_csv(r'/Users/.../statcast_df.csv', index = False, header = True)
```

## Running:
For help run:
```
python app.py
```
