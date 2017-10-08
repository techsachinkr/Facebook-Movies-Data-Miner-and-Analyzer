# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 16:11:12 2017

@author: Sachin Kumar
"""
#I am using a temporary token for Facebook's Graph API Access in this project which expires in some hours
#Go to https://developers.facebook.com/tools/access_token/  and click on
#"Get Token" button and then "Get user Access Token" go generate your ACCESS_TOKEN value and then copy that value to field below
ACCESS_TOKEN = 'EAACEdEose0cBAHrSSYyuYIvFQkp8iL7ZBTJD8nZAR0lRduo14UbBO2YYo4fI49FiK7AB0iBwXLmrJMeemmPu9baPEEnlUny1oBzWa3LlVjtL68L9L9H1jmTOQqCa0QwSYwto3fGZBAmBzd2K2XMURyxrSZAvLtZAoyGGMpPCdsuML55pE9nUeMi7qsNjtzNVFbpnJ4uBM2A8r6bO9kJma2WcqJZBZCIdb9j9v3SosCs8QZDZD'

import requests # pip install requests
import facebook # pip install facebook-sdk

# Making connection to the Graph API with access token generated
graphAccess = facebook.GraphAPI(ACCESS_TOKEN, version='2.7')
base_url = 'https://graph.facebook.com/'

# Search for Movie pages
initSearch=graphAccess.request("search", {'q': 'Movies', 'type': 'page'})

#Count of movies pages retrieved from Facebook
resultsCount=1000

searchResults=[]
searchResults.extend(initSearch['data'])

#Getting movies data from all the pages of results retrieved as
#graphapi gives json results in pagination format with a fixed number
#of results per page
while len(searchResults)< resultsCount:
    try:
        initSearch=requests.get(initSearch['paging']['next']).json()
        searchResults.extend(initSearch['data'])
    except KeyError:    
        print('Reached end of feed.')
        break

fields = 'is_verified,category,genre'

verifiedMoviesList=[]
#Filtering Movies records by checking if page is verified
# and if falls in movie category pages as declared in facebook
#and it has a genre associated with it
#Above mentioned parameters are checked to ensure
#we are filtering out official movie pages
for records in searchResults:
    totalVal=requests.get('{0}{1}?fields={2}&access_token={3}'.format(base_url,records['id'], fields, ACCESS_TOKEN))
    currentJson= totalVal.json()
    if currentJson['is_verified'] == True: 
        if currentJson['category'] == 'Movie':  
            if 'genre' in  currentJson:
               verifiedMoviesList.append((currentJson['id'],currentJson['category'],currentJson['genre']))
               
print("\n Records of verified movies filtered out of all movie pages data retrieved \n")    
print(verifiedMoviesList) 

import pandas as pd  # pip install pandas
import matplotlib.pyplot as plt
#Getting total number of fans or likes on a movie page
def total_fans(page_id):
    return int(graphAccess.get_object(id=page_id,fields=['fan_count'])['fan_count'])

#get pagefeed of a given page
def getPageFeed(page_id,no_of_posts):
    pagefeed = graphAccess.get_connections(page_id, 'posts')
    postsList = []
    postsList.extend(pagefeed['data'])
    while len(postsList) < no_of_posts:
        try:
            pagefeed = requests.get(pagefeed['paging']['next']).json()
            postsList.extend(pagefeed['data'])
        except KeyError:
            # When there are no more posts in the feed, break
            print('Reached end of feed.')
            break
    if len(postsList) > no_of_posts:
        postsList = postsList[:no_of_posts]

    print('{} items retrieved from feed'.format(len(postsList)))
    return postsList

#Getting reactions of fans of movie page in terms of likes,shares and comments
def measure_reaction(post_id,totalFansCnt):

    sharesCount=0
    likesCount = graphAccess.get_object(id=post_id, 
                         fields=['likes.limit(0).summary(true)'])\
                         ['likes']['summary']['total_count']
    commentsCount = graphAccess.get_object(id=post_id, 
                         fields=['comments.limit(0).summary(true)'])\
                         ['comments']['summary']['total_count']    
    if 'shares' in    graphAccess.get_object(id=post_id,fields=['shares.limit(0)'] ):               
        sharesCount = graphAccess.get_object(id=post_id, 
                         fields=['shares.limit(0)'])\
                         ['shares']['count']
                        
    likes_percent = likesCount / totalFansCnt * 100.0
    shares_percent = sharesCount / totalFansCnt * 100.0
    comments_percent = commentsCount / totalFansCnt * 100.0                     
    return likesCount,likes_percent, commentsCount,comments_percent,sharesCount,shares_percent    

moviesidList=[]
cntr=0
#Creating movies list for sorting it by number of fans
for cntr in range(len(verifiedMoviesList)):
    page_id=verifiedMoviesList[cntr][0]
    pageName=graphAccess.get_object(id=page_id)['name']
    numberFans=total_fans(page_id)
    moviesidList.append((page_id,pageName,numberFans))
         
#Sorting movies list by number of fans in descending order    
moviesidList.sort(key=lambda temp:temp[2],reverse=True) 
print("\n Movies list sorted by total number of fans \n")
print(moviesidList)

#No. of top movies for analysis moving forward
# Like here i have specified 10,which means i want top ten movies out of movieslist
comparisonLen=10

likesMap=[]
#Creating likes list for plotting 
for likeCntr in range(comparisonLen):
    likesMap.append((moviesidList[likeCntr][1],moviesidList[likeCntr][2]))
print(likesMap)
fgca = plt.figure()    
plt.ticklabel_format(style = 'plain')
likedf=pd.DataFrame(likesMap,columns=['MovieName','Total_Page_Likes'])
likedf.plot(kind='bar',ax=fgca.gca(),x='MovieName',rot=80,title='Most popular movies(in terms of page likes)')

 
#Pandas dataframe for movie informtion     
columns = ['Name',
           'Total Fans',
           'Post Number',
           'Post Date',
           'Likes',
           'Shares',
           'Comments',
           'Relative Likes',
           'Relative Shares',
           'Relative Comments'] 

movies=pd.DataFrame(columns=columns)
loopCntr=0

#Building dataframe for last 6 posts and fans reaction for each of the movies
for loopCntr in range(comparisonLen):
    page_id=moviesidList[loopCntr][0]
    pageName=moviesidList[loopCntr][1]
    totalFans=moviesidList[loopCntr][2]
    pageFeed=getPageFeed(page_id,6)
    for innerCntr, post in enumerate(pageFeed):
        likesCnt,likespct, sharesCnt,sharespct, commentsCnt,commentspct = measure_reaction(post['id'],totalFans)
        movies = movies.append({'Name': pageName,
                                      'Total Fans': totalFans,
                                      'Post Number': innerCntr+1,
                                      'Post Date': post['created_time'],
                                      'Likes': likesCnt,
                                      'Shares': sharesCnt,
                                      'Comments': commentsCnt,
                                      'Relative Likes': likespct,
                                      'Relative Shares': sharespct,
                                      'Relative Comments': commentspct,
                                     }, ignore_index=True)
# Fixing the dtype of some columns    
for col in ['Post Number', 'Total Fans', 'Likes', 'Shares', 'Comments']:
    movies[col] = movies[col].astype(int)    
#Movies Dataframe
print("Listing of Top 10 Movies Dataframe")
print(movies)


movies = movies.set_index(['Name','Post Number'])

#Pivoting index labels and grouping data columns by movie
movies.unstack(level=0)

#Comparison of different movies with each other in terms of likes,shares and comments received on last 6 posts

#Plotting comparative reactions to each movie last 6 facebook posts
plot = movies.unstack(level=0)['Likes'].plot(kind='bar',title='Movies last 6 posts Engagement in terms of Likes Received', subplots=False, figsize=(10,5), width=0.8)
plot.set_xlabel('6 Latest Posts')
plot.set_ylabel('Number of Likes Received')

plot = movies.unstack(level=0)['Shares'].plot(kind='bar',title='Movies last 6 posts Engagement in terms of Shares done', subplots=False, figsize=(10,5), width=0.8)
plot.set_xlabel('6 Latest Posts')
plot.set_ylabel('Number of Shares Dones')

plot = movies.unstack(level=0)['Comments'].plot(kind='bar',title='Movies last 6 posts Engagement in terms of Comments made', subplots=False, figsize=(10,5), width=0.8)
plot.set_xlabel('6 Latest Posts')
plot.set_ylabel('Number of Comments made')

#Plotting engagement of each movie facebook fanbase to last 6 posts
plot = movies.unstack(level=0)['Relative Likes'].plot(kind='bar',title='Movies last 6 posts Engagement in terms of Relative Likes Received', subplots=False, figsize=(10,5), width=0.8)
plot.set_xlabel('6 Latest Posts')
plot.set_ylabel('Relative Number of Likes Received')

plot = movies.unstack(level=0)['Relative Shares'].plot(kind='bar',title='Movies last 6 posts Engagement in terms of Relative Shares done', subplots=False, figsize=(10,5), width=0.8)
plot.set_xlabel('6 Latest Posts')
plot.set_ylabel('Relative Number of Shares Dones')

plot = movies.unstack(level=0)['Relative Comments'].plot(kind='bar',title='Movies last 6 posts Engagement in terms of Relative Comments made', subplots=False, figsize=(10,5), width=0.8)
plot.set_xlabel('6 Latest Posts')
plot.set_ylabel('Relative Number of Comments made')

             
# Finding average engagement of top 10 movies
print('\n Average number of Fans or Likes per fan for top 10 movies')
print(movies.unstack(level=0)['Relative Likes'].mean())

print('\nAverage number of Shares per fan for top 10 movies')
print(movies.unstack(level=0)['Relative Shares'].mean())

print('\nAverage Comments per fan for top 10 movies')
print(movies.unstack(level=0)['Relative Comments'].mean())

    
