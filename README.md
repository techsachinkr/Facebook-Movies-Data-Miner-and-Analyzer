# Facebook-Movies-Data-Miner-and-Analyzer

Mines Facebook's Official movies pages data and then analyse it to generate some insights

## **Mining and Exploring Facebook's Official Movies Pages Data**

Recently i seen a video course of Mining Social Web-Facebook by Mikhail Klassen. So after seeing that course i learned about Facebook's Graph API and decided to use that knowledge and implement in some practical problem case and that's how i got inspiration for working on this project.

Then i was thinking of some sort of topic with which many can found common grounds with and understand its analytics in realistic perspective. So i cameup with idea of scraping or mining data from facebook about Movies and use them to generate some relative stats and analytics.

In this project i had mined data from official Movies facebook pages using facebook's graph API and then used that data to generate some interesting insights and stats.

## Generating Facebook Graph API accesstoken

Our first step will be,generating a access token for Facebook's Graph API access by going to website
https://developers.facebook.com/tools/explorer/

 Note: Token generated here i a temporary access token,so once it expires,you have to generate a new one.

Your access token would something like this :

```
QMBGEdEise1czAHrLSYyuYIvFQ....... (Continues ...A very long string :-))
```
Now  create a object for GraphAPI access with the access token generated
 ```
graphAccess.request("search", {'q': 'Movies', 'type': 'page'})
```
So once i established connection to graph api,iwe are good to go for getting all facebook movies pages data.


## Filtering data

Now since we are concerned with getting official Movies page data only,we have to filter the movies pages data we are getting in step above as it contain all sorts of official or unofficial or pages not even belonging to a particular movie but only containing some movie keyword in it,so i did some research on all the fields facebook has for a page or one can say metadata on it.

Then i came up with three filters we can apply to get the official Movies data:

i) is_Verified :
Facebook API returns is_Verified field for pages which are official and has a blue tick associated with it.So using this filter will restrcit our data to offcial pages only.

ii) Category:
Now once we got official pages ,next we have to filter out pages belonging to Movies category only as in the actual data we also have pages belonging to studios,entertainment companies which are not the relevant data for us,so we have to filter out them to get the Movies category pages only.

iii) Genre:
Next ,i observed that i was still getting some pages which are official and belonging to Movies category but is not actually a movie but some studio or cinema group page.So i decided to apply a filter of Genre checking if page has a genre associated with it and if it has then surely that will be a movie.

 ```
 fields = 'is_verified,category,genre'
 totalVal=requests.get('{0}{1}?fields={2}&access_token={3}'.format(base_url,records['id'], fields, ACCESS_TOKEN)) 
  ```
## Selecting a subset of data for analytics

Now in this project since i am focusing on doing analytics on top 10 movies(in terms of movie pages with most likes),so next i worked on sorting pages in the list with most likes and then taking top ten records out of it for further filtering

```
moviesidList.sort(key=lambda temp:temp[2],reverse=True) 
```
Next i also got last 6 posts from top ten movies pages to get number of likes,shares and comments onthose 6 posts respectively in order to determine fans engagement and comparative reactions

```
#get pagefeed of a given page
 pagefeed = graphAccess.get_connections(page_id, 'posts')
 #Getting reactions of fans of movie page in terms of likes,shares and comments
 likesCount = graphAccess.get_object(id=post_id, 
                         fields=['likes.limit(0).summary(true)'])\
                         ['likes']['summary']['total_count']
commentsCount = graphAccess.get_object(id=post_id, 
                         fields=['comments.limit(0).summary(true)'])\
                         ['comments']['summary']['total_count']    
sharesCount = graphAccess.get_object(id=post_id, 
                         fields=['shares.limit(0)'])\
                         ['shares']['count'] 
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
```

## Analytics on Movies data for generating some insights or stats

Now did following analytics tasks on data selected as mentioned above:

i) Generated plots for top ten movies with total likes received,comparative to each other

ii) Plotted comparative reactions to each movie last 6 facebook posts in terms of likes,shares and comments on last 6 posts.

iii) Plotting engagement of each movie facebook fanbase to last 6 posts in terms of relative likes,rellative shares and relative comments to last 6 posts.

iv)Finding average engagement of top 10 movies in terms of average comments,likes and shares per fan.


## The End/Further Analysis

I learned a lot while doing this project ,specifically about Facebook's Graph API and manner facebook organises its data.
Moreover i did also generated some really cool stats and figures by doing analysis of movies pages and posts data.
Further i will to work on it more once time permits, to get some more insights based on movie genre data.
