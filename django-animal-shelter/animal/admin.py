from django import forms
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Animal, Photo

# child models first
class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 3

    # TODO: customize inline form to show thumbnails
    # ref: https://django-imagekit.readthedocs.org/en/latest/#admin ?

    # ref: http://www.joshuakehn.com/2014/10/19/fixing-djangos-admin-inlines.html
    def get_extra (self, request, obj=None, **kwargs):
        """Dynamically sets the number of extra forms. 0 if the related object
        already exists or the extra configuration otherwise."""
        return 0 if obj else self.extra


class AnimalCustomAdminForm(forms.ModelForm):
    model = Animal

    # to filter the choices of cover photo
    # ref: http://stackoverflow.com/a/26138015
    # ref: https://stackoverflow.com/questions/10040442/override-a-form-in-django-admin
    # ref: http://www.djangobook.com/en/2.0/chapter06.html
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  #  populate initially
        self.fields['cover'].queryset = Photo.objects.filter(animal=self.instance.pk)  # ModelChoiceField.queryset


# parent model
class AnimalAdmin(admin.ModelAdmin):
    form = AnimalCustomAdminForm
    inlines = [
        PhotoInline,
    ]

    # ref: http://www.szotten.com/david/custom-redirects-in-the-django-admin.html
    def response_change(self, request, obj):
        """Redirect back to the Detail Page upon the completion of editing in the admin interface"""
        response = super(AnimalAdmin, self).response_change(request, obj)
        if (isinstance(response, HttpResponseRedirect) and
            response['location'] == reverse('admin:animal_animal_changelist') and
            request.GET.get('redirect') == 'obj'):
           response['location'] = obj.get_absolute_url()
        return response

admin.site.register(Animal, AnimalAdmin)