# benfordParse
Repo for Benford Parse web application, built with Flask and Docker

## Preamble

In 1938, Frank Benford published a paper showing the distribution of the leading digit in many disparate sources of data. In all these sets of data, the number 1 was the leading digit about 30% of the time. Benford’s law has been found to apply to population numbers, death rates, lengths of rivers, mathematical distributions given by some power law, and physical constants like atomic weights and specific heats.

`benfordParse` allows users to submit a data file, select a column to analyze, and test their dataset against Benfords Law. The expected output of this program is table containing the distribution of found counts against expected, as well as a plot graphing the distribution. This output is saved within a nested username directory, with the contents of their run contained within a user-specified project-id directory.

## Instructions

This application can be ran in one of two ways, either executed through `flask run` or through running as a Docker container. Details on launching as both below:

### Flask
