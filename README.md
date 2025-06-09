# jrf-child-poverty

A repo for data collection and visualisation for the JRF Child Poverty project.

## Quick links

(Children in low income families visualisation)[https://justknowledge-uk.github.io/jrf-child-poverty/py/children_in_low_income_families]

## Directory structure

Scripts should use relative paths within the root directory (jrf-child-poverty). 

- **data-raw**: For raw data used in scripts. The data folder is ignored by git so that we don't share data we don't mean to, so all data will need to be added manually on local machine. If there is data we want to share (subject to licencing) this will need to be added to a new folder (perhaps called data-clean). But let's not add any data to Github yet.
- **scripts**: For scripts of any language.
- **outputs**: For saving outputs (e.g., figures and tables) from scripts.

**Note** that before we push any outputs we need to make sure that the licences for the data allow us to do so. Most data we are looking at should be ONS data, which is Open Government Licence so fine to publish outputs with attribution.
