import numpy as np
import laspy
import pdal
import matplotlib.pyplot as plt
import pandas as pd

pth = "C:/Users/hejtm/Downloads/2021-04-28_17-48-15_100pct_time.laz"
pth = "C:/Users/hejtm/Downloads/plochaBK_sample49m.las"


las = laspy.read(pth)

## Checking the dimensions
list(las.point_format.dimension_names)

las[['X', 'Y', 'Z']]

pipeline="""{
  "pipeline": [
    {
        "type": "readers.las",
        "filename": "C:/Users/hejtm/Downloads/2021-04-28_17-48-15_100pct_time.laz",
        "count":1000000
    },
    {
        "type": "filters.sort",
        "dimension": "Z"
    }
  ]
}"""

r = pdal.Pipeline(pipeline)
r.validate()
r.execute()
df = pd.DataFrame(r.arrays[0])

## 
df['Red'].describe()

##
df_plt = df.sample(n=10000)
fig = plt.figure(figsize=[20, 5])
ax = plt.axes(projection='3d')
sc = ax.scatter(df_plt['X'], df_plt['Y'], df_plt['Z'], c=df_plt['Intensity'], s=0.1, marker='o', cmap="Spectral")
plt.colorbar(sc)
plt.show()