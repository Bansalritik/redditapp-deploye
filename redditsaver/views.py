from django.http import HttpResponse
from django.shortcuts import render, redirect
from prawcore import ResponseException
from django.db.models import Count
import praw
from .models import Reddit_Data



def Index(request):
    Reddit_Data.objects.all().delete()
    try:
        Code = request.GET['code']  # This is coming back correctly
    except:
        return redirect('/')
    Redditt = praw.Reddit(client_id="VwPMw5sfsqc9Ig",
                          client_secret="tAGWTHloyLIXbTRpCgV3FMSQVg8",
                          redirect_uri="https://pure-reaches-41056.herokuapp.com/index",
                          user_agent="testscript by u/fakebot3")
    try:
        Redditt.auth.authorize(Code)
    except:
        return redirect('/')
    Name = Redditt.user.me()
    Subscribed = list(Redditt.user.subreddits(limit=None))
    for Sub in Subscribed:
        SubRedditt = Redditt.subreddit(str(Sub))
        New_Redd = SubRedditt.new(limit=None)
        i = 1
        for Submission in New_Redd:
            if not Reddit_Data.objects.filter(Reddit_Id=Submission.id, Reddit_Username=str(Name)).exists():
                temp = False
                Author_Name = ''
                if(not Submission.selftext):
                    print(Submission.selftext)
                    temp = True
                if Submission.author is not None:
                    Author_Name = Submission.author.name
                Reddit_Data.objects.create(Reddit_Id=Submission.id, Reddit_Title=Submission.title,
                                           Reddit_Comments=Submission.num_comments, Reddit_Username=str(Name),
                                           Reddit_Score=Submission.score, Reddit_Domain=Submission.domain,
                                           Reddit_User=Author_Name, Reddit_Subred=str(Sub), Reddit_Body=Submission.url,
                                           Reddit_Link=temp)
            if i>20:
                break
            i+=1
    print(Reddit_Data.objects.all().count())
    Data = Reddit_Data.objects.filter(Reddit_Link=True, Reddit_Username = str(Name))
    print(Data.count())
    Users = Reddit_Data.objects.filter(Reddit_Username=str(Name)).values('Reddit_User').annotate(total=Count('Reddit_User')).order_by('-total')[:3]
    Domains = Reddit_Data.objects.filter(Reddit_Username=str(Name)).values('Reddit_Domain').annotate(total=Count('Reddit_Domain')).order_by('-total')[:3]
    Context = {
        'Datas': Data,
        'Users': Users,
        'Domains': Domains,
        'UserName' : str(Name)
    }
    # if Data.count()is 0 and Users.count() is 0 and Domains.count() is 0:
    #     return render(request, 'empty.html',Context)
    return render(request, 'redditpage.html', Context)


def Reddit(request):
    Redditt = praw.Reddit(client_id="VwPMw5sfsqc9Ig",
                          client_secret="tAGWTHloyLIXbTRpCgV3FMSQVg8",
                          redirect_uri="https://pure-reaches-41056.herokuapp.com/index",
                          user_agent="testscript by u/fakebot3")
    return redirect(Redditt.auth.url(['identity, history, '
                                      'modlog, modposts, modwiki, mysubreddits,read,'
                                      ' save, ''subscribe, wikiread'], "...", "temporary"))

