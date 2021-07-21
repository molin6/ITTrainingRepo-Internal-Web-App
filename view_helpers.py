from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout
)
from rest_framework import viewsets
from .serializers import *
from .forms import *
from .views import *

import inspect, sys, re
from itertools import chain
def get_caller_info(depth=0):
    ## gets the caller function name
    view_function_name = inspect.stack()[1+depth].function
    view_function_name_parts = view_function_name.split("_")
    object_type = view_function_name_parts.pop()
    view_verb = "_".join(view_function_name_parts)

    ## get the associated serializer for this object, which must
    ## exist anyway in order to do listings via datatables
    serializer = getattr(sys.modules[__name__], object_type.title() + "Serializer")

    ## get the associated form for this object
    form = getattr(sys.modules[__name__], object_type.title() + "Form")

    ## get the associated model for this object
    model = getattr(sys.modules[__name__], object_type.title())

    return {
        "view_function_name": view_function_name,
        "view_verb": view_verb,
        "object_type": object_type,
        "serializer": serializer,
        "form": form,
        "model": model
    }

def get_app_name(request):
    return resolve(request.path).app_name

def get_field_display_name(model, field):
    display_name = None

    if( \
        'verbose_name_overrides' in dir(model) and \
        field in model.verbose_name_overrides() \
    ):
        display_name = model.verbose_name_overrides()[field]
    else:
        field = re.sub(r"__.*$", "", field)
        verbose_name = model._meta.get_field(field).verbose_name
        display_name = verbose_name
        if( field != "id" ):
            display_name = display_name.title()

    return display_name


def get_field_specs(caller_info=None, instance_id=None):
    serializer = caller_info['serializer']
    model = caller_info['model']
    instance = None

    if instance_id:
        instance = model.objects.get(pk=instance_id) 
    else:
        try:
            instance = model.objects.get(pk=1) 
        except:
            pass
    
    field_specs = []
    serializer_data = serializer(instance).data
    for field in serializer_data:
        field_spec = {
            'data': field,
            'name': get_field_display_name(model, field)
        }

        if instance_id:
            field_spec['value'] = serializer_data[field]

        field_specs.append(field_spec)

    return field_specs


def list_base(request):
    caller_info = get_caller_info(1)
    page_title = ("%s listing" % caller_info['object_type']).title()
    app_name = get_app_name(request)
    create_view = "%s:create_%s" % (app_name, caller_info['object_type'])
    display_view = "%s:display_%s" % (app_name, caller_info['object_type'])
    search_field = request.GET.get('search_field')
    search_value = request.GET.get('search_value')
    search = None

    if(search_field and search_value):
        search = {
            "display_field": search_field.replace("__", " "),
            "field": search_field,
            "value": search_value
        }

    return render(
        request,
        "%s/list.html" % app_name,
        {
            "page_title": page_title,
            "object_type": caller_info['object_type'],
            "create_view": create_view,
            "display_view": display_view,
            "field_specs": get_field_specs(caller_info),
            "search": search
        }
    )


def create_edit_display_base(request, instance_id=None):
    caller_info = get_caller_info(1)
    model = caller_info['model']
    instance = model.objects.get(pk=instance_id) if instance_id else None
    form = caller_info['form'](request=request, instance=instance)
    app_name = get_app_name(request)
    field_specs = None

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect("%s:list_%s" % (app_name, caller_info['object_type']))

    if form.view_verb == 'display':
        field_specs = get_field_specs(caller_info, instance_id)
    try:
        ratings_for_object = Opportunity.objects.get(id=instance_id).ratings.all()
        user_rating_comments = UserRatingComment.objects \
        .filter(user_rating__rating__in = ratings_for_object)
    except:
        user_rating_comments = ''

    

    return render(
        request,
        "%s/create_edit_display.html" % app_name,
        {
            "form": form,
            "item": field_specs,
            "instance": instance,
            "user_rating_comments": user_rating_comments
        }
    )


def delete_base(request, instance_id=None):
    caller_info = get_caller_info(1)
    instance = None
    app_name = get_app_name(request)
 
    try:
        instance = caller_info['model'].objects.get(pk=instance_id) if instance_id else None
    except:
        pass

    if instance:
        instance.delete()

    return redirect("%s:list_%s" % (app_name, caller_info['object_type']))

def login(request):
    app_name = get_app_name(request)
    if request.method == "POST":
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            if request.GET.get('next', False):
                return redirect(request.GET['next'])
            return redirect("%s:index" % app_name)
        else:
            messages.add_message(request, messages.WARNING, 'Invalid login')
    return render(request, "%s/login.html" % app_name, {})


def logout(request):
    app_name = get_app_name(request)
    auth_logout(request)
    return redirect("%s:index" % app_name)
