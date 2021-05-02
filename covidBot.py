#region Imports

import discord
from discord.ext import commands

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

#endregion

token = 'YOUR TOKEN HERE'

#region Init

client = commands.Bot(command_prefix='>', case_insensitive=True)
client.remove_command('help')
driver = None
citySearch = False
ontarioPopulation = 14570000


def main():
    global driver

    PATH = r'C:\Program Files (x86)\chromedriver.exe'

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('disable-gpu')

    driver = webdriver.Chrome(executable_path=PATH, options=options)
    
    client.run(token)

#endregion

#region Discord Commands

@client.event
async def on_ready():
    print('Bot Ready')

@client.command(aliases=['citycases', 'new'])
async def newCases(ctx, * , city=None):
    if city == None:
        message = cmdOntarioCases(1)
    else:
        message = cmdCityCases(city.capitalize(), 0, 'New Cases Today')
 
    await ctx.send(message)

@client.command(aliases=['citydeaths', 'deaths'])
async def totalDeaths(ctx, * , city=None):
    if city == None:
        message = cmdOntarioCases(4)
    else:
        message = cmdCityCases(city.capitalize(), 3, 'Total Deaths')

    await ctx.send(message)

@client.command(aliases=['cityactive', 'active', 'currentcases', 'activecases'])
async def totalActive(ctx, * , city=None):
    if city == None:
        message = cmdOntarioCases(6)
    else:
        message = cmdCityCases(city.capitalize(), 1, 'Total Active Cases')
    
    await ctx.send(message)

@client.command(aliases=['total', 'cases','citytotal'])
async def totalCases(ctx, * , city=None):
    if city == None:
        message = cmdOntarioCases(0)
    else:
        message = cmdCityCases(city.capitalize(), 4, 'Total Cases')

    await ctx.send(message)

@client.command()
async def newDeaths(ctx):
    message = cmdOntarioCases(5)
    await ctx.send(message)

@client.command()
async def dailyVaccines(ctx):
    message = cmdVaccineData(0)
    await ctx.send(message)

@client.command()
async def totalVaccines(ctx):
    message = cmdVaccineData(1)
    await ctx.send(message)

@client.command()
async def fullyImmunized(ctx):
    message = cmdVaccineData(2)
    await ctx.send(message)

@client.command()
async def firstDose(ctx):
    message = cmdVaccineData(3)
    await ctx.send(message)

@client.command()
async def help(ctx):
    embed = discord.Embed(color=discord.Colour.green())
    embed.set_author(name='Help')
    embed.add_field(name='City Specific Commands',value='CityCases\nCityDeaths\nCityActive\nCityTotal',inline=False)
    embed.add_field(name='Future plans', value="- add Ontario testing data\n- add postivity rate data\n- add combined statistics for a certain health region", inline=False)
                    
    await ctx.send(embed=embed)

#endregion

#region Website Commands

def cmdOntarioCases(dataSet):
    messages = ['Total Covid 19 Cases in Ontario as of Today: ', 'New Covid 19 Cases in Ontario Today: ', 'Total Resolved Covid 19 Cases in Ontario as of Today: ', 'New Resolved Covid 19 Cases in Ontario Today: ', 'Total Covid 19 Related Deaths in Ontario as of Today: ', 'New Covid 19 Related Deaths in Ontario Today: ', 'Total Active Covid 19 Cases in Ontario as of Today: ']
    
    try:
        if driver.current_url != 'https://covid-19.ontario.ca/covid-19-data/':
            driver.get('https://covid-19.ontario.ca/covid-19-data/')

        caseCounts = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ontario-covid-viz')))

        cases = caseCounts.find_elements_by_class_name('cviz-label-value--value ')

        if dataSet == 6:
            total = int(cases[0].text.replace(',', ''))
            resolved = int(cases[2].text.replace(',', ''))
            active = str(total - resolved)
            return (messages[dataSet] + active[:2] + ',' + active[2:])
        else:
            return (messages[dataSet] + cases[dataSet].text)
    except Exception as e:
        print(e)
        return 'No Response\nPlease Try Again'

def cmdCityCases(city, dataSet, statistic):
    try:
        global citySearch

        if driver.current_url != 'https://covid-19.ontario.ca/covid-19-data/':
                driver.get('https://covid-19.ontario.ca/covid-19-data/')
        elif citySearch:
            closeLeaflet = driver.find_element_by_class_name('leaflet-popup-close-button')
            closeLeaflet.click()
            clearSearch = driver.find_element_by_xpath('//*[@id="compare-chart-controls"]/div[3]/div/button')
            clearSearch.click()
                
        numberFormat = driver.find_element_by_id('cviz_radio-button-optioncapital1')
        numberFormat.click()
        print('Click')
        search = driver.find_element_by_id('cviz-gen-search')
        search.send_keys(city)
            
        result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-focused')))
        print(result.text)
        result = result.text
        search.send_keys(Keys.RETURN)

        print('Search')

        
        content = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="regionalMap"]/div[1]/div[1]/div[6]/div/div[1]/div/div/p[2]')))
        leafletPopup = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'leaflet-popup-content'))).text.split('\n')
        print(len(leafletPopup))
        count = 0
        #while len(leafletPopup) < 2 :
            #continue
        data = leafletPopup[dataSet].split(' ')

        citySearch = True

        print('text')

        print(data)
        if len(data) <= 1:
            return 'No Result for ' + city

        return (result + ' ----> ' + statistic + ':\t' + data[1])
    except Exception as e:
        print(e)
        return 'No Response\nPlease Try Again'

def cmdVaccineData(dataSet):
    try:
        if driver.current_url != 'https://covid-19.ontario.ca/covid-19-vaccines-ontario':
            driver.get('https://covid-19.ontario.ca/covid-19-vaccines-ontario')

        if dataSet == 0:
            element = driver.find_element_by_id('previous-day-doses-administered')
            return('Doses administered yesterday: ' + element.text)
        elif dataSet == 1:
            element = driver.find_element_by_id('total-doses-administered')
            return('Total Doses Administered: ' + element.text)
        elif dataSet == 2:
            elementText = driver.find_element_by_id('total-vaccinations-completed').text
            elementText2 = int(''.join(c for c in elementText if c.isdigit()))
            percentage = '{:.2%}'.format(elementText2/ontarioPopulation)
            return('Number of People Fully Imunized: ' + str(elementText) + '\nPercentage of Ontario Population Fully Immunized: ' + percentage)
        elif dataSet == 3:
            totalDoses = driver.find_element_by_id('total-doses-administered').text
            totalDoses = int(''.join(c for c in totalDoses if c.isdigit()))
            secondDoses = driver.find_element_by_id('total-vaccinations-completed').text
            secondDoses = int(''.join(c for c in secondDoses if c.isdigit()))
            totalDoses = totalDoses - secondDoses
            percentage = '{:.2%}'.format(totalDoses/ontarioPopulation)
            totalDoses = f'{totalDoses:,d}'
            return('Number of People That Have Received At Least One Dose: ' + totalDoses + '\nPercentage of Ontario Population With At Least One Dose: ' + percentage)
    except Exception as e:
        print(e)
        return 'No Response\nPlease Try Again'

#endregion

if __name__ == '__main__':
    main()