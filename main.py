import numpy as np
import laspy
import pdal
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.colors as colors
import pandas as pd

pth = "C:/Users/hejtm/Downloads/2021-04-28_17-48-15_100pct_time.laz"
pth = "C:/Users/hejtm/Downloads/plochaBK_sample49m.las"

las = laspy.read(pth)

## Checking the dimensions
list(las.point_format.dimension_names)

las[['X', 'Y', 'Z']]

## PDAL
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
df.describe()

##
df_plt = df.sample(n=10000)
fig = plt.figure(figsize=[20, 5])
ax = plt.axes(projection='3d')
sc = ax.scatter(df_plt['X'], df_plt['Y'], df_plt['Z'],
                c=df_plt['Intensity'], s=0.1, marker='o', cmap="Spectral")
plt.colorbar(sc)
plt.show()


## Groud seearch

pipeline_search_ground="""{
"pipeline": [
    {
        "type": "readers.las",
        "filename": "C:/Users/hejtm/Downloads/2021-04-28_17-48-15_100pct_time.laz",
        "count":1000000
    },
    {
        "type":"filters.assign",
        "assignment":"Classification[:]=0"
    },
    {
        "type":"filters.elm"
    },
    {
      "type":"filters.outlier"
    },
    {
      "type":"filters.smrf",
      "ignore":"Classification[7:7]",
      "slope":0.2,
      "window":16,
      "threshold":0.45,
      "scalar":1.2
    },
    {
      "type":"filters.range",
      "limits":"Classification[2:2]"
    },
    {
        "type":"writers.las",
        "filename":"output-ground.las"
    }
]
}"""

pipe_ground = pdal.Pipeline(pipeline_search_ground)
pipe_ground.validate()
pipe_ground.execute()

df_ground = pd.DataFrame(pipe_ground.arrays[0])
df_plt = df_ground.sample(50000)
fig = plt.figure(figsize=[20, 5])
ax = plt.axes(projection='3d')
sc = ax.scatter(df_plt['X'], df_plt['Y'], df_plt['Z'],
                c=df_plt['Intensity'], s=0.1, marker='o', cmap="Spectral")
plt.colorbar(sc)
plt.show()

## 
cmap = ListedColormap(["white", "tan", "springgreen", "darkgreen"])

# Define a normalization from values -> colors
norm = colors.BoundaryNorm([0, 2, 10, 20, 30], 5)

fig, ax = plt.subplots(figsize=(10, 5))
hm_plot = ax.imshow(
                     cmap=cmap,
                     norm=norm)

ax.set_title("Lidar Canopy Height Model (CHM)")

# Add a legend for labels
legend_labels = {"tan": "short", "springgreen": "medium", "darkgreen": "tall"}

patches = [Patch(color=color, label=label)
           for color, label in legend_labels.items()]

ax.legend(handles=patches,
          bbox_to_anchor=(1.35, 1),
          facecolor="white")

ax.set_axis_off()
plt.show()