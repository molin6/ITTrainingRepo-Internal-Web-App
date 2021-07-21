from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating, UserRating
class BaseModel(models.Model):
    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=120)


class Type(BaseModel):
    name = models.CharField(max_length=120)


class PriceRange(BaseModel):
    name = models.CharField(max_length=120)


class Level(BaseModel):
    name = models.CharField(max_length=120)


class Opportunity(BaseModel):
    name = models.CharField(max_length=120)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    type = models.ForeignKey(Type, on_delete=models.PROTECT, null=True)
    price_range = models.ForeignKey(PriceRange, on_delete=models.PROTECT, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    level = models.ForeignKey(Level, on_delete=models.PROTECT, null=True)
    ratings = GenericRelation(Rating)
    link = models.CharField(max_length=512, null=True)

    ## these accessors (get_average_rating and get_total_rating_count) 
    ## are needed to catch a DoesNotExist error thrown by the ratings
    ## model when an object has not yet been rated
    def get_average_rating(self):
        average = None
        try:
            average = self.ratings.get().average
        except:
            pass

        return average

    def get_rating_count(self):
        count = None
        try:
            count = self.ratings.get().count
        except:
            pass

        return count

    def verbose_name_overrides():
        return {
            "ratings__average": "Average Rating",
            "ratings__count": "# of Ratings",
        }

class UserRatingComment(BaseModel):
    created_on = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True, null=True)
    user_rating = models.OneToOneField(
        UserRating,
        on_delete=models.PROTECT,
        related_name='comment'
    )
    
    @property
    def name(self):
        
        return "Comment on %s" % self.user_rating

    @property
    def created_by(self):
        return self.text
    
    @property
    def comment(self):
        return self.text
