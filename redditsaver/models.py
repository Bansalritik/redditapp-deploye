from django.db import models


class Reddit_Data(models.Model):
    Reddit_Id = models.CharField(max_length=10)
    Reddit_Title = models.TextField(default='')
    Reddit_Comments = models.BigIntegerField()
    Reddit_Username = models.CharField(max_length=50)
    Reddit_Score = models.BigIntegerField()
    Reddit_Domain = models.TextField(default='')
    Reddit_Link = models.BooleanField(default=False)
    Reddit_Body = models.TextField(default='')
    Reddit_Subred = models.CharField(max_length=50, default='')
    Reddit_User = models.CharField(max_length=50,default='')
    # reddit_image = models.ImageField(upload_to='static/images', default='')


