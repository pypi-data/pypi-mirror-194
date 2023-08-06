# -*- coding: utf-8 -*-
"""
Example workflow for integrating plotID with jpg or png images.

With tagplot() an ID can be generated and printed on the plot. To export the
plot along with the corresponding research data and the plot generating
script use the function publish().
"""

# %% Import modules
from plotid.tagplot import tagplot
from plotid.publish import publish

# %% Set optional Project ID, which will be placed in front of the generated ID
PROJECT_ID = "MR05_"

# %% Read example images
IMG1 = "example_image1.png"
IMG2 = "example_image2.png"

# %% TagPlot

# If multiple images should be tagged, they must be provided as list.
IMGS_AS_LIST = [IMG1, IMG2]

# Example for how to use tagplot with image files
FIGS_AND_IDS = tagplot(
    IMGS_AS_LIST,
    "image",
    prefix=PROJECT_ID,
    id_method="time",
    location="west",
    qrcode=True,
)
# Required arguments: tagplot(images as list, desired plot engine)


# %% Publish

# Export your tagged images, copy the research data that generated the images,
# specify the destination folder and give a name for the exported image files.

publish(FIGS_AND_IDS, ["../README.md", "../docs", "../LICENSE"], "./data")
# Required arguments: publish(output of tagplot(), list of files,
# path to destination folder)
