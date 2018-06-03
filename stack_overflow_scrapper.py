#####Start of main######
#Add some exceptions if such imports are made
import stack_overflow_props as stack_props
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests

summary = []
questionHyperLinks = []
tagsList = []
viewsList = []
voteList = []
#######Defining a parser to parse all data########
def parse(questionsList):
    
    for question in questionsList:
        questionSummary = question.find(class_="summary").find('h3').get_text()
        hyperLink = question.find(class_="summary").find('h3').find('a').get('href')
        questionTags = [tag.get_text().strip() for tag in question.find_all(class_="post-tag")]
        questionViews = question.find(class_="views").get_text().strip()
        noOfVotes = question.find('strong').get_text().strip()    
        
        summary.append(questionSummary)
        questionHyperLinks.append(stack_props.base_url+hyperLink)
        tagsList.append(questionTags)
        viewsList.append(questionViews)
        voteList.append(noOfVotes)    
    return summary,questionHyperLinks,tagsList,viewsList,voteList

###### make a request to Stack overflow url
page_range = int(stack_props.page_range)
i=1
while i <=page_range:
    resp = requests.get(stack_props.url + "&page=" + str(i))
    print(resp.status_code)
    if '2' not in str(resp.status_code):
        print("Error response has occurred")
    ######Beautiful Soup############
    soup = BeautifulSoup(resp.content,'html.parser')
    questionTags=[]
    questionsList = soup.find_all(class_="question-summary")
    #Call function##
    summary,questionHyperLinks,tags,views,votes = parse(questionsList)
    time.sleep(20)
    i+=1

print("Fetched information for 2 pages")
########Pandas Setting#################
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

stacks = pd.DataFrame({
    "summary":summary,
    "links":questionHyperLinks,
    "tags":tags,
    "views":views,
    "votes":votes})

stacks