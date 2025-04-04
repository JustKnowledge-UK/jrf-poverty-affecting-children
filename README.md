# jrf-child-poverty

A repo for data collection and visualisation for the JRF Child Poverty project

## Directory structure

Scripts should use relative paths within the root directory (jrf-child-poverty). 

- data-raw: For raw data used in scripts. The data folder is ignored by git so that we don't share data we don't mean to, so it will need to be added manually on local machine. If there is data we want to share this will need to be added to a new folder (perhaps called data-clean). 
- scripts: For scripts of any language.
- outputs: For saving outputs (e.g., figures and tables) from scripts.