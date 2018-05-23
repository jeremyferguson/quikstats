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

#Changes the event selection in the parameters
def changeEvent(scraper,selection):
    scraper.changeParam('ctl00$ContentPlaceHolder1$ui_TrackEvent_DropDownList',selection)

#Changes the division selection in the parameters
def changeDiv(scraper,selection):
    scraper.changeParam('ctl00$ContentPlaceHolder1$ui_GroupSets_Repeater$ctl00$ui_Group_DropDownList',selection)

#Changes the conference selection in the parameters
def changeConference(scraper,selection):
    scraper.changeParam('ctl00$ContentPlaceHolder1$ui_GroupSets_Repeater$ctl01$ui_Group_DropDownList',selection)

#Changes the state qualifying site in the parameters
def changeStateSite(scraper,selection):
    scraper.changeParam('ctl00$ContentPlaceHolder1$ui_GroupSets_Repeater$ctl02$ui_Group_DropDownList',selection)
