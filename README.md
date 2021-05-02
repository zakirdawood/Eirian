Eirian will take commands from the user and scrape two different sites. It will deliver information on new cases, active cases, deaths, and total cases for cities based on public health units. Additionally, it will provide provincial-wide statistics. Eirian also provides information on vaccine doses administered and the percentage of the population immunized.

## **Instructions to Use** 
- https://sites.google.com/a/chromium.org/chromedriver/downloads
          -> download correct version according to device
- Requires python and pip, along with selenium and discord.py
- Set up your own application for discord to use Eirian and provide its token into the python file by replacing "ENTER YOUR TOKEN HERE PLEASE" with  "token"


## **Sources used to get information**
- https://covid-19.ontario.ca/covid-19-data/
- https://covid-19.ontario.ca/covid-19-vaccines-ontario

## **Command Set**
- ">newCases" (gives Ontario stats)
- ">newDeaths" (gives Ontario stats)
- ">totalCases" (gives Ontario stats)
- ">totalDeaths" (gives Ontario stats)
- ">totalActive" (gives Ontario stats)

- ">newCases City"
- ">totalDeaths City"
- ">totalCases City"
- ">totalActive City"

- ">dailyVaccines"
- ">totalVaccines"
- ">fullyImmunized"
- ">firstDose"
