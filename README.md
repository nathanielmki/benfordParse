# benfordParse
Repo for Benford Parse web application, built with Flask

## Preamble

In 1938, Frank Benford published a paper showing the distribution of the leading digit in many disparate sources of data. In all these sets of data, the number 1 was the leading digit about 30% of the time. Benford’s law has been found to apply to population numbers, death rates, lengths of rivers, mathematical distributions given by some power law, and physical constants like atomic weights and specific heats.

`benfordParse` allows users to submit a data file, select a column to analyze, and test their dataset against Benfords Law. The expected output of this program is table containing the distribution of found counts against expected, as well as a plot graphing the distribution. This output is saved within `/static/results` directory.

## Installation Instructions
The following instructions assume you have `python3`, `pip`, and `venv` already installed on your system.

First, clone the repository from Github and `cd` into it. Then activate the included python virtual environment with `source benfordParse_env/bin/activate`.

Once activated, install all required packages using `pip install -r requirements.txt`.

Launch the flask application by executing `python3 -m flask run` in the app root directory.

Navigate to `127.0.0.1:5000` in your web browser, or `ctrl/cmd-click` the link in the terminal to begin using the webapp.

## How to Use

From the home page, users are greeted by three input fields:
* `Choose File`: Allows users to browse their filesystem and select a file for testing.
* The second field allows users to specify which column the want to operate on.
* Finally, the third field lets users name their output files

Upon hitting submit, users are redirected to the results page, which displays the `Expected vs. Found Distribution` of digits 1-9 in your dataset.

To view the raw CSV file that was used to generate the graph, select `Choose File` under "View Raw Data", browse to the named CSV file in the `/static/results` directory and click `Submit`.

## Locating Files

You can also view the images and files generated by the app by browsing to `/static/results` in a file browser. Any file uploaded is also saved for future reference, in the `/upload` directory.