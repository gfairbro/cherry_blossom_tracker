# Proposal

## Section 1. Motivation & Purpose

|                    |                                                                       |
|--------------------|-----------------------------------------------------------------------|
| Role               | Data Science Consulting firm contracted by Tourism Board of Vancouver |
| Primary Audience   | Tourists to Vancouver during Cherry Blossom Season                    |
| Secondary Audience | Blossom loving Vancouverites, Botanists/Dendrologists                 |

...

## Section 2. Data Description

We will be visualizing a dataset of approximately 150,000 public trees on boulevards in the City of Vancouver. Each tree has 19 variables that describe the public tree's ID (`TREE_ID`), its location data (`CIVIC_NUMBER`, `STD_STREET`, `ASSIGNED`, and `Geom`, etc.) which reveals different information, its biological characteristics (`GENUS_NAME`, `SPECIES_NAME`, `CULTIVAR_NAME`, `COMMON_NAME`), its physical characteristics (`HEIGHT_RANGE_ID`, `DIAMETER`), whether a root barrier is installed (`ROOT_BARRIER`),  and when it is planted (`DATE_PLANTED`).

**Dataset limitations**

There are some missing values: 70605 of `CULTIVAR_NAME`, 1530 of `PLANT_AREA`, 82253 of `DATE_PLANTED`, and 21826 of `Geom`. We might continually update how we deal with them through the design of the dashboard.

The dataset does not contain trees that grow on private property or in the parks. The trees in this dataset are found on city-managed land such as along the roadways. Some trees are missing from the dataset. The information regarding tree circumference may be outdated or missing.

## Section 3. Research questions and usage scenarios


**Research questions:**

1. Where are the most rewarding places to view the cherry blossoms in Vancouver?
2. What types of trees appear in what neighbourhoods?
3. When are the trees most likely to blossom? blossoms most probably blooming?

**Usage Scenario:**

Tom is an international tourist planning to visit Vancouver for the first time during the yearly cherry blossom season. Tom is a huge cherry blossom enthusiast and wants a tool where he can learn more about cherry blossom trees in Vancouver. He wishes to stay in a hotel that is within walking distance to nearby cherry blossoms viewing spots. Tom is a visual person, hence he wants to view this information on a map. The map will be able to show the position of each tree, as well as the cultivars and tree diameter. Tom also wants to find out which neighbourhood has the most Cherry Blossoms, how many cultivars of cherry blossoms there are, and where the biggest cherry blossom trees (by diameter) are located. The tool should be interactive, such that when he filters by e.g. different cultivars of cherry blossoms, the map will also reflect the change.

