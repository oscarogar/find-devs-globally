from django.db import models
import uuid
from users.models import Profile
# Create your models here.
class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    demo_link = models.CharField(max_length=2000, blank=True, null=True)
    source_link = models.CharField(max_length=2000, blank=True, null=True)
    featured_image = models.ImageField(null=True, blank=True, default='default.jpg')
    tags = models.ManyToManyField('tag' ,blank=True)
    total_vote = models.IntegerField(default=0, blank=True, null=True)
    vote_ratio = models.IntegerField(default=0, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(editable=False, unique=True, default=uuid.uuid4, primary_key=True)
    

    def __str__(self):
        return self.title
    #order the projects based on latest
    class Meta:
        ordering = ['-vote_ratio', '-total_vote', 'title','-created']
    
    #Prevent Owners from voting, get all the reviewers in a list and scan through
    @property
    def reviewers(self):
        queryset = self.review_set.all().value_list('owner__id', flat=True)
        return queryset
        
    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVote = reviews.filter(value='up').count()
        votes = reviews.count()
        ratio = (upVote / votes) * 100
        #commit the votes and ratios to db
        self.total_vote = votes
        self.vote_ratio = ratio
        self.save()

    @property
    def imageURL(self):
        try:

            url = self.featured_image.url
        except:
            url = 'default.jpg'
        
            return url


class Review(models.Model):
    VOTE_TYPE = (
       ( 'up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(editable=False, unique=True, default=uuid.uuid4, primary_key=True)
    
    #Prevent Double Reviews and  Vote
    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value



class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(editable=False, unique=True, default=uuid.uuid4, primary_key=True)
    
    def __str__(self):
        return self.name