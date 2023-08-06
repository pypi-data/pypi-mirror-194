# -*- coding: utf-8 -*-
"""
Example workflow for integrating plotID with matplotlib figures.

With tagplot() an ID can be generated and printed on the plot. To export the
plot along with the corresponding research data and the plot generating
script use the function publish().
"""

# %% Import modules
import numpy as np
import matplotlib.pyplot as plt
from plotid.tagplot import tagplot
from plotid.publish import publish

# %% Set Project ID
PROJECT_ID = "MR05_"

# %% Create sample data
x = np.linspace(0, 10, 100)
y = np.random.rand(100) + 2
y_2 = np.sin(x) + 2

# %% Create sample figures

# 1. figure
FIG1 = plt.figure()
plt.plot(x, y, color="black")
plt.plot(x, y_2, color="yellow")

# 2. figure
FIG2 = plt.figure()
plt.plot(x, y, color="blue")
plt.plot(x, y_2, color="red")

# %% tagplot

# If multiple figures should be tagged, figures must be provided as list.
FIGS_AS_LIST = [FIG1, FIG2]

# Example for how to use tagplot with matplotlib figures
FIGS_AND_IDS = tagplot(
    FIGS_AS_LIST,
    "matplotlib",
    location="west",
    id_method="random",
    prefix=PROJECT_ID,
    qrcode=True,
)
# Required arguments: tagplot(images as list, desired plot engine)

# %% Publish

publish(FIGS_AND_IDS, ["../README.md", "../docs", "../LICENSE"], "data")
# Required arguments: publish(output of tagplot(), list of files,
# path to destination folder)
