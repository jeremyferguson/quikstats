################################################################################
#NAME: quikstats
#PURPOSE: enable primary communication with quikstats site and interact with other specific modules for other sports
#AUTHOR: Jeremy Ferguson
#DATE CREATED: 5/22/18
#DATE LAST EDITED: 5/22/18
################################################################################

from bs4 import BeautifulSoup
import requests,sys
import track

#Hardcoded values for accepted inputs into function, corresponding to the divisions that can be searched, and the sports that can be searched for either boys or girls
acceptedDivs = ['1A','2A','3A','4A']
acceptedBoysSports = ['Football','Basketball','Track & Field','Baseball','Bowling','Swimming','Fall Golf','Spring Golf','Tennis']
acceptedGirlsSports = ['Volleyball','Basketball','Track & Field','Softball','Soccer','Bowling','Swimming','Golf','Tennis']

BASE_URL = 'http://www.quikstatsiowa.com/'

class Scraper:
    def __init__ (self,gender=None,div=None,sport=None):
        if gender is not None:
            self.gender = gender
        else:
            self.gender = getGender()
        if div is not None:
            self.div = div
        else:
            self.div = getDiv()
        if sport is not None:
            self.sport = sport
        else:
            self.sport = getSportName(self.gender)
        self.homeSoup = self.getSoup(BASE_URL)
        self.url = BASE_URL + self.getUrl()
        self.pageSoup = self.getSoup(self.url)
        if self.sport == 'Track & Field':
            self.params = track.getParams()
        self.params['__VIEWSTATE'] = self.getViewState()
        self.params['__EVENTVALIDATION'] = self.getEventValidation()
            
    #Generates a BeautifulSoup object from a given url
    def getSoup(self,url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content,'html.parser')
        return(soup)

    #Gets the path for results, based on the sport and gender provided
    def getUrl(self):
        contentdiv = self.homeSoup.find_all(class_ = 'content')[0]
        table = contentdiv.find_all('table',recursive=False)[0]
        innerRow = table.find_all('tr',recursive=False)[1]
        columns = innerRow.find_all('td',recursive=False)
        if self.gender == 'M':
            colnum = 0
        else:
            colnum = 1
        rows = columns[colnum].find_all('tr')
        for row in rows:
            if self.sport in row.text:
                return(row.find('a')['href'])

    #Gets the __VIEWSTATE parameter from the results page for the chosen sport.  This is a very long string, so it makes more sense to get it directly from the page rather than hardcode it        
    def getViewState(self):
        viewStateInput = self.pageSoup.find_all(id='__VIEWSTATE')[0]
        return(viewStateInput['value'])

    #Gets the __EVENTVALIDATION parameter from the results page for the chosen sport.  This is a very long string, so it makes more sense to get it directly from the page rather than hardcode it
    def getEventValidation(self):
        EvalValInput = self.pageSoup.find_all(id='__EVENTVALIDATION')[0]
        return(EvalValInput['value'])

    #changes a parameter in the payload to be delivered to the site
    def changeParam(self,category,choice):
        selectElement = self.pageSoup.find_all('select',{'name':category})[0]
        options = selectElement.find_all('option')
        found = False
        for option in options:
            if choice in option.text:
                self.params[category] = option['value']
                found = True
        if not found:
            self.params[category] = ''
        #print(selectElement)
                
    def scrapeSite(self):
        r = requests.post(self.url,data=self.params)
        self.pageSoup = BeautifulSoup(r.content,'html.parser')
        
#Gets input from user for which division should be searched
def getDivName():
    print('Please enter which division you would like to search. Accepted divisions are:\n'+"\n".join(acceptedDivs))
    div = input().strip()
    if not div in acceptedDivs:
        print('Sorry, this division is not recognized. Please try again')
        return(getDivName())
    else:
        return(div)
    
#Gets input from user for which gender should be searched
def getGender():
    print('Please enter which gender you would like to search (M or F): ')
    gender = input().strip()
    if not gender == 'M' or gender == 'F':
        print('Sorry, this input appears to be invalid.  Please try again with M or F')
        return(getGender())
    else:
        return(gender)
    
#Gets input from user for which sport should be searched
def getSportName(gender):
    print('Please enter which sport you would like to search. Accepted sports are: ')
    if gender == 'M':
        print("\n".join(acceptedBoysSports))
        sport = input().strip()
        if not sport in acceptedBoysSports:
            print('Sorry, this sport is not recognized. Please try again')
            return(getSportName(gender))
        else:
            return(sport)
    elif gender == 'F':
        print("\n".join(acceptedGirlsSports))
        sport = input().strip()
        if not sport in acceptedGirlsSports:
            print('Sorry, this sport is not recognized. Please try again')
            return(getSportName(gender))
        else:
            return(sport)
    else:
        print('Sorry, invalid gender.')
        return(None)
    
if __name__ == '__main__':
    scraper = Scraper('M','3A','Track & Field')
    track.changeTeam(scraper,'ACGC')
    track.changeEvent(scraper,'Top 5 All Events')
    track.changeDiv(scraper,scraper.div)
    #print(scraper.params)
    scraper.scrapeSite()
    track.scrapeEventResults(scraper.pageSoup,scraper.event)
    #print(scraper.pageSoup)
