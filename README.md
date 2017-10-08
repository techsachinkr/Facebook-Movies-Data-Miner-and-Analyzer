# Facebook-Movies-Data-Miner-and-Analyzer
Mines Facebook's Official movies pages data and then analyse it to generate some insights

## **Mining and Exploring Facebook's Official Movies Pages Data**
Recently i seen a video course of Mining Social Web-Facebook by Mikhail Klassen. So after seeing that course i learned about Facebook's Graph API and decided to use that knowledge and implement in some practical problem case and that's how i got inspiration for working on this project.

Then i was thinking of some sort of topic with which many can found common grounds with and understand its analytics in realistic perspective. So i cameup with idea of scraping or mining data from facebook about Movies and use them to generate some relative stats and analytics.

In this project i had mined data from official Movies facebook pages using facebook's graph API and then used that data to generate some interesting insights and stats.

# Getting the data

Firstly i generated the temporary token for Facebook's Graph API Access by going to website "https://developers.facebook.com/tools/access_token/".

Then created a object for GraphAPI access with the access token generated

```
graphAccess = facebook.GraphAPI(ACCESS_TOKEN, version='2.10')
```

Now once i had established connection to graph api i worked on getting all the facebook Movies pages data
```
graphAccess.request("search", {'q': 'Movies', 'type': 'page'})
```

# Filtering data

Now since we are concerned with getting official Movies page data only,we have to filter the movies pages data we are getting in step above as it contain all sorts of official or unofficial or pages not even belonging to a particular movie but only containing some movie keyword in it,so i did some research on all the fields facebook has for a page or one can say metadata on it.

Then i came up with three filters we can apply to get the official Movies data:
i) is_Verified :
Facebook API returns is_Verified field for pages which are official and has a blue tick associated with it.So using this filter will restrcit our data to offcial pages only.

ii) Category:
Now once we got official pages ,next we have to filter out pages belonging to Movies category only as in the actual data we also have pages belonging to studios,entertainment companies which are not the relevant data for us,so we have to filter out them to get the Movies category pages only.

iii) Genre:
Next ,i observed that i was still getting some pages which are official and belonging to Movies category but is not actually a movie but some studio or cinema group page.So i decided to apply a filter of Genre checking if page has a genre associated with it and if it has then surely that will be a movie.

# Selecting Data for Analytics

Now in this project since i was focusing on doing analytics on top 10 movies(in terms of movie pages with most likes),so next i worked on sorting pages in the list with most likes and then takingtop ten records out of it for further filtering

```
moviesidList.sort(key=lambda temp:temp[2],reverse=True) 
```
Next i also got last 6 posts from top ten movies pages to get number of likes,shares and comments onthose 6 posts respectively in order to determine fans engagement and comparative reactions

```
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

# Analytics on Movies data for generating some insights or stats

Now did following analytics tasks on data selected as mentioned above:
i) Generated plots for top ten movies with total likes received,comparative to each other

ii) Plotted comparative reactions to each movie last 6 facebook posts in terms of likes,shares and comments on last 6 posts.

iii) Plotting engagement of each movie facebook fanbase to last 6 posts in terms of relative likes,rellative shares and relative comments to last 6 posts.

iv)Finding average engagement of top 10 movies in terms of average comments,likes and shares per fan.


# The End/Further Analysis

I learned a lot while doing this project ,specifically about Facebook's Graph API and manner facebook organises its data.
Moreover i did also generated some really cool stats and figures by doing analysis of movies pages and posts data.
Further i will to work on it more once time permits, to get some more insights based on movie genre data.
