First some system packages might be needed:

`sudo apt install python3.9 python3.9-dev python3.9-pip python3.9-venv libgdal-dev libudunits2-dev`

Create python virtual environment

`python3.9 -m venv venv`

`source venv/bin/activate`

`python3.9 -m pip install --upgrade pip`

`pip install -r requirements.txt`

Load spatial data to local disk:

`python load.py`

`R CMD BATCH load.R` (or run the script in RStudio)

Run experiments

`python experiment.py`

`R CMD BATCH experiment.R` (or run the script in RStudio)