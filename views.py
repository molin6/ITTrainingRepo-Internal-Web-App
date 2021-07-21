from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.template import loader
from star_ratings import app_settings as star_ratings_app_settings
from django.templatetags.static import static
import uuid
from decimal import Decimal
from rest_framework import viewsets, permissions
from star_ratings.models import UserRating
from .models import (
    Opportunity,
    UserRatingComment
)
from .serializers import OpportunitySerializer
from .view_helpers import *
from django.urls import reverse
## by default, go to the opportunity listing
def index(request):
    app_name = get_app_name(request)
    return redirect("%s:agenda" % app_name)

@login_required
def add_rating_comment(request):
    user_rating_comment_text = request.POST.get("user_rating_comment_text","")
    user_rating_comment_id = request.POST.get("user_rating_comment_id","")
    user_rating_id = request.POST.get("user_rating_id","")
    user = request.user

    if(user_rating_comment_text and user_rating_id):
        user_rating = UserRating.objects.get(id=user_rating_id)

        if(not user_rating_comment_id):
            user_rating_comment = UserRatingComment()
            user_rating_comment.text = user_rating_comment_text
            user_rating_comment.user_rating = user_rating
            user_rating_comment.save()
            user_rating_comment_id = user_rating_comment.id

        user_rating_comment = UserRatingComment.objects.get(id=user_rating_comment_id)
        user_rating_comment.text = user_rating_comment_text
        user_rating_comment.save()
    return redirect(reverse('it_training_repo:list_opportunity'))


@login_required
def list_opportunity(request):
    return list_base(request)

@login_required
def agenda(request):
    return render(request,"it_training_repo/agenda_gcal.html")

@login_required
def upcoming_opportunity(request):
    return render(request,"it_training_repo/upcoming_gcal.html")

@login_required
def create_edit_display_opportunity(request, id=None):
    return create_edit_display_base(request, id)

@login_required
def delete_opportunity(request, id=None):
    return delete_base(request, id)


def static_stars(request, stars=None):
    max_stars = star_ratings_app_settings.STAR_RATINGS_RANGE
    percentage = 100 * (Decimal(stars) / Decimal(max_stars))
    icon_height = icon_width = 15
    sprite_width = icon_width * 3
    
    return render(
        request,
        "it_training_repo/static_stars.html",
        {
            'stars': [i for i in range(1, star_ratings_app_settings.STAR_RATINGS_RANGE + 1)],
            'star_count': max_stars,
            'percentage': percentage,
            'icon_height': icon_height,
            'icon_width': icon_width,
            'sprite_width': sprite_width,
            'sprite_image': static(star_ratings_app_settings.STAR_RATINGS_STAR_SPRITE),
            'id': 'dsr{}'.format(uuid.uuid4().hex),
            'read_only': True,
        }
    )

    
class OpportunityViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer

