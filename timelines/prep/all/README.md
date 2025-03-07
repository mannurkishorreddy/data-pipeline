[Community Data](../../../../community-data/)

# Timeline samples

[SQLite in a browser](../../sqlite/) from the phiresky timeline will be modified to show changes in naics industry levels for zips and counties.

[Our Tabulator + Timeline Sample](../../tabulator)
[Phiresky SQLite Timeline](https://phiresky.github.io/blog/2021/hosting-sqlite-databases-on-github-pages/) - Includes filter for selecting countries
[Line Race](../../line-race.html) - [Apache eChart](https://echarts.apache.org/examples/en/editor.html?c=line-race)
[Community Forecasting](/community-forecasting/?page=zip/#zip=30318)

Python to [import .csv files into SQLite](https://github.com/phiresky/world-development-indicators-sqlite/) - Worldbank Development Indicators by year

## NAICS Timelines - Generate Multiple Years

Each year, at the end of April (or later... was Nov in 2019), get the latest industry file.   

Outputs SQLite script for years.

This generates a sqlite file for each year: zcta_2013.SQL.txt, etc.

	python automate.py zcta.SQL.txt 

Then run to send .csv output to data folder:  

	./run.sh

Or run individually:

	sqlite3 zcta.db < zcta_2013.SQL.txt> zcta.OUT.txt  

This sends files to data/[year]

----

# Random Forest and Regression

Make new edits to zcta.SQL.txt, then update line numbers in automate.py.

Annual zcta_[year].SQL.txt files are overwritten by automate.py.  

Might need:
	
	python3 -m venv env &&
	source env/bin/activate &&
	pip install pandas &&
	pip install scikit-learn

1.) Run Random Forest (uses python/runOneFile.py):

	cd python
	python automateRF.py "../output"

2.) Create a summary file. Run in timelines/summary folder:

	cd ../../summary/
	sqlite3 summary.db < summary.SQL.txt > summary.OUT.txt

3.) Generate zips folders using instructions in zipgraph.py

4.) See readme in [regression](../regression)

5.) Also see [Processing NAICS by Zip Code](/community-data/process/naics/) 