import requests
import pandas as pd
from io import StringIO

url = "https://www.ndbc.noaa.gov/view_text_file.php?filename=tplm2h2024.txt.gz&dir=data/historical/stdmet/"

response = requests.get(url)
response.raise_for_status()

text_data = response.text

# Correct 19-column stdmet header
columns = [
    "YY","MM","DD","hh","mm",
    "WDIR","WSPD","GST","WVHT","DPD","APD","MWD",
    "PRES","ATMP","WTMP","DEWP","VIS","PTDY","TIDE"
]

df = pd.read_csv(
    StringIO(text_data),
    sep=r"\s+",
    names=columns,
    comment="#",
    engine="python",   # <-- important for whitespace parsing
    na_values=["MM"]
)

print("Columns:", df.columns.tolist())
print(df.head())

# Build timestamp as string instead of datetime
df["observation_time"] = (
    df["YY"].astype(int).astype(str).str.zfill(4) + "-" +
    df["MM"].astype(int).astype(str).str.zfill(2) + "-" +
    df["DD"].astype(int).astype(str).str.zfill(2) + " " +
    df["hh"].astype(int).astype(str).str.zfill(2) + ":" +
    df["mm"].astype(int).astype(str).str.zfill(2) + ":00"
)


df.to_csv("tplm2h2024.csv", index=False)

print("Saved as tplm2h2024.csv")

