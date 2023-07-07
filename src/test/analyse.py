import pandas as pd

data = [
        {
            "ddnm": "168482973997d659e015cc5",
            "cknm": "760100461",
            "qynm": "910201000",
            "spnm": "0030000000963",
            "sl": 163,
            "lg": "枚",
            "dpsj": 2608.0
        },
        {
            "ddnm": "168482973997d659e015cc5",
            "cknm": "710752413",
            "qynm": "910201000",
            "spnm": "0030000000963",
            "sl": 34,
            "lg": "枚",
            "dpsj": 646.0
        },
        {
            "ddnm": "168482973997d659e015cc5",
            "cknm": "760100457",
            "qynm": "910201000",
            "spnm": "0030000000963",
            "sl": 10,
            "lg": "枚",
            "dpsj": 1210.0
        },
        {
            "ddnm": "168482973997d659e015cc5",
            "cknm": "760100465",
            "qynm": "910201000",
            "spnm": "0030000000963",
            "sl": 4,
            "lg": "枚",
            "dpsj": 496.0
        },
        {
            "ddnm": "168482973997d659e015cc6",
            "cknm": "760100461",
            "qynm": "910201001",
            "spnm": "0030000000963",
            "sl": 7,
            "lg": "枚",
            "dpsj": 42.0
        },
        {
            "ddnm": "168482973997d659e015cc6",
            "cknm": "710752413",
            "qynm": "910201001",
            "spnm": "0030000000963",
            "sl": 8,
            "lg": "枚",
            "dpsj": 72.0
        },
        {
            "ddnm": "168482973997d659e015cc6",
            "cknm": "760100457",
            "qynm": "910201001",
            "spnm": "0030000000963",
            "sl": 10,
            "lg": "枚",
            "dpsj": 210.0
        },
        {
            "ddnm": "168482973997d659e015cc7",
            "cknm": "760100461",
            "qynm": "910201001",
            "spnm": "0030000000963",
            "sl": 26,
            "lg": "枚",
            "dpsj": 156.0
        },
        {
            "ddnm": "168482973997d659e015cc7",
            "cknm": "710752413",
            "qynm": "910201001",
            "spnm": "0030000000963",
            "sl": 54,
            "lg": "枚",
            "dpsj": 486.0
        },
        {
            "ddnm": "168482973997d659e015cc7",
            "cknm": "760100457",
            "qynm": "910201001",
            "spnm": "0030000000963",
            "sl": 29,
            "lg": "枚",
            "dpsj": 609.0
        },
        {
            "ddnm": "168482973997d659e015cc7",
            "cknm": "760100465",
            "qynm": "910201001",
            "spnm": "0030000000963",
            "sl": 89,
            "lg": "枚",
            "dpsj": 2136.0
        }
    ]
df = pd.DataFrame(data)

grouped_ddnm = df.groupby('ddnm').agg({'sl': 'sum'}).reset_index()
grouped_cknm = df.groupby('cknm').agg({'sl': 'sum'}).reset_index()

print('Sum over ddnm:')
print(grouped_ddnm)
print('\nSum over cknm:')
print(grouped_cknm)
