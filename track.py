################################################################################
#NAME: track
#PURPOSE: 
#AUTHOR: Jeremy Ferguson
#DATE CREATED: 5/22/18
#DATE LAST EDITED: 5/22/18
################################################################################

from bs4 import BeautifulSoup
import requests,inspect
import quikstats
#Hardcoded parameters specific to the track results page
EVENTS_OPTION_ID = 'ctl00_ContentPlaceHolder1_ui_TrackEvent_DropDownList'
EVENTS_OPTION_NAME = 'ctl00$ContentPlaceHolder1$ui_TrackEvent_DropDownList'
SITE_OPTION_ID = 'ctl00_ContentPlaceHolder1_ui_GroupSets_Repeater_ctl02_ui_Group_DropDownList'
SITE_OPTION_NAME = 'ctl00$ContentPlaceHolder1$ui_GroupSets_Repeater$ctl02$ui_Group_DropDownList'
__VIEWSTATEGENERATOR = '2F95BAE9'

#Generates the default parameters.  These will need to have the __EVENTVALIDATION and __VIEWSTATE parameters added by the main quikstats module
def getParams():
    params = {
        '__VIEWSTATEGENERATOR':__VIEWSTATEGENERATOR,
        'ctl00$ContentPlaceHolder1$ui_Team_DropDownList':'',#Team Select
        'ctl00$ContentPlaceHolder1$ui_TrackEvent_DropDownList':'',#Event Select
        'ctl00$ContentPlaceHolder1$ui_GroupSets_Repeater$ctl00$ui_Group_DropDownList':'',#Class Select
        'ctl00$ContentPlaceHolder1$ui_GroupSets_Repeater$ctl01$ui_Group_DropDownList':'',#Conference Select
        'ctl00$ContentPlaceHolder1$ui_GroupSets_Repeater$ctl02$ui_Group_DropDownList':'',#State Qualifying Site Select
        'ctl00$ContentPlaceHolder1$ui_LoadList_Button':'Load List'
    }
    return(params)

#Changes the team selection in the parameters    
def changeTeam(scraper,selection):
    scraper.changeParam('ctl00$ContentPlaceHolder1$ui_Team_DropDownList',selection)
    #Resets the conference, state qualifying site, and division parameters
    scraper.params['ctl00$ContentPlaceHolder1$ui_GroupSets_Repeater$ctl01$ui_Group_DropDownList'] = ''
    scraper.params['ctl00$ContentPlaceHolder1$ui_GroupSets_Repeater$ctl02$ui_Group_DropDownList'] = ''
    scraper.params['ctl00$ContentPlaceHolder1$ui_GroupSets_Repeater$ctl00$ui_Group_DropDownList'] = ''

#Changes the event selection in the parameters
def changeEvent(scraper,selection):
    scraper.changeParam('ctl00$ContentPlaceHolder1$ui_TrackEvent_DropDownList',selection)
    scraper.event=selection
    
#Changes the division selection in the parameters
def changeDiv(scraper,selection):
    scraper.changeParam('ctl00$ContentPlaceHolder1$ui_GroupSets_Repeater$ctl00$ui_Group_DropDownList',selection)
    #Resets the team, conference, and state qualifying site parameters
    scraper.params['ctl00$ContentPlaceHolder1$ui_Team_DropDownList'] = ''
    scraper.params['ctl00$ContentPlaceHolder1$ui_GroupSets_Repeater$ctl01$ui_Group_DropDownList'] = ''
    scraper.params['ctl00$ContentPlaceHolder1$ui_GroupSets_Repeater$ctl02$ui_Group_DropDownList'] = ''
    scraper.div=selection
    
#Changes the conference selection in the parameters
def changeConference(scraper,selection):
    scraper.changeParam('ctl00$ContentPlaceHolder1$ui_GroupSets_Repeater$ctl01$ui_Group_DropDownList',selection)
    #Resets the team, state qualifying site, and division parameters
    scraper.params['ctl00$ContentPlaceHolder1$ui_Team_DropDownList'] = ''
    scraper.params['ctl00$ContentPlaceHolder1$ui_GroupSets_Repeater$ctl02$ui_Group_DropDownList'] = ''
    scraper.params['ctl00$ContentPlaceHolder1$ui_GroupSets_Repeater$ctl00$ui_Group_DropDownList'] = ''
    scraper.conference=selection
    
#Changes the state qualifying site in the parameters
def changeStateSite(scraper,selection):
    scraper.changeParam('ctl00$ContentPlaceHolder1$ui_GroupSets_Repeater$ctl02$ui_Group_DropDownList',selection)
    #Resets the team, conference, and division parameters
    scraper.params['ctl00$ContentPlaceHolder1$ui_Team_DropDownList'] = ''
    scraper.params['ctl00$ContentPlaceHolder1$ui_GroupSets_Repeater$ctl01$ui_Group_DropDownList'] = ''
    scraper.params['ctl00$ContentPlaceHolder1$ui_GroupSets_Repeater$ctl00$ui_Group_DropDownList'] = ''
    scraper.stateSite=selection
    
#Takes in a soup for the results of a query involving a single event and outputs the times
def scrapeEventResults(soup,event):
    formcontentdiv = soup.find_all(class_='formcontent')[0]
    resultsTable = formcontentdiv.find_all('table',recursive=False)[1]
    rows = resultsTable.find_all('tr',recursive=False)
    titlerow = rows[0]
    titlecols = titlerow.find_all('td')
    output = []
    #Relays have a different format, so need to be scraped differently
    if not 'Relay' in event and not event == 'Top 5 All Events':
        athletecol = -1
        teamcol = -1
        markcol = -1
        for i in range(len(titlecols)):
            col = titlecols[i]
            #print(col.text)
            if 'Athlete' in col.text:
                athletecol = i
            if 'Team' in col.text:
                teamcol = i
            if 'Mark' in col.text:
                markcol = i
        for row in rows[1:]:
            cols = row.find_all('td',recursive=False)
            output.append({
                'Athlete':cols[athletecol].text.strip(),
                'Team':cols[teamcol].text.strip(),
                'Mark':cols[markcol].text.strip().replace("H","")
            })
            #print(output[len(output)-1])
        return(output)
    elif 'Relay' in event:
        teamcol = -1
        markcol = -1
        for i in range(len(titlecols)):
            col = titlecols[i]
            if 'Team' in col.text:
                teamcol = i
            if 'Mark' in col.text:
                markcol = i
        newrows = rows[1:]
        for i in range(int(len(newrows)/2)):
            firstrow = newrows[i*2]
            firstcols = firstrow.find_all('td')
            secondrow = newrows[i*2+1]
            secondcols = secondrow.find_all('td')[1].find_all('td')
            output.append({
                'Team':firstcols[teamcol].text.strip(),
                'Mark':firstcols[markcol].text.strip(),
                'Members':[i.text.replace('\n','') for i in secondcols]
            })
            #print(output[len(output)-1])
        return(output)
    else:
        output = {}
        tables = resultsTable.find_all('table')
        containers = []
        headers = []
        #print(len(tables))
        for i in range(len(tables)):
            table = tables[i]
            con = table.parent.parent
            header = con.find_all('div',{'style':'width: 100\x25; background-color: #dddddd;'})[0].text.strip()
            body = {}
            for row in table.find_all('tr'):
                cols = row.find_all('td')
                if not cols[0].text.replace('\n','') == '':
                    body[cols[0].text.strip()] = cols[1].text.strip()
            output[header] = body
        return(output)
    
if __name__ == '__main__':
    scraper = quikstats.Scraper('M','3A','Track & Field')
    changeTeam(scraper,'ACGC')
    changeEvent(scraper,'Top 5 All Events')
    changeDiv(scraper,scraper.div)
    #print(scraper.params)
    scraper.scrapeSite()
    output = scrapeEventResults(scraper.pageSoup,scraper.event)
    #print(scraper.pageSoup)
