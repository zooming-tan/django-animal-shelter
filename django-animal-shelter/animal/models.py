import os
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from django.core.urlresolvers import reverse
from model_utils import Choices
from taggit.managers import TaggableManager
from sorl.thumbnail import ImageField

BREED_CHOICES = Choices(
    'Border Collie',
    'Bull Terrier',
    'Mastiff',
)

AGE_CHOICES = Choices(
    'Puppy',
    'Young',
    'Adult',
    'Senior',
)

SEX_CHOICES = Choices(
    'Male',
    'Female',
)

SIZE_CHOICES = Choices(
    'Small',
    'Medium',
    'Large',
)

IS_NEUTRED_CHOICES = Choices(
    'Yes',
    'No',
)


class Animal(TimeStampedModel):
    # tupled because django-model-utils does not accept list elements with space, e.g. "Any Breed"
    breed = models.CharField(choices=tuple(BREED_CHOICES), max_length=50, null=True, blank=True)
    age = models.CharField(choices=tuple(AGE_CHOICES), max_length=25, null=True, blank=True)
    sex = models.CharField(choices=tuple(SEX_CHOICES), max_length=20, null=True, blank=True)
    size = models.CharField(choices=tuple(SIZE_CHOICES), max_length=20, null=True, blank=True)

    # If BooleanField is chosen, the rendered checkbox widget will always return the default (T/F but not None)
    # even in initial, untouched state. This is not expected. To solve this problem, NullBoolean field which
    # supports null=True, blank=True (BooleanField does not support null=True, it must always be either T/F) 
    # is used. Caveat: a select box is rendered with a third choice 'Unknown' instead of the usual checkbox.
    ##is_neutered = models.BooleanField(default=False)
    ## is_neutered = models.NullBooleanField(null=True, blank=True, verbose_name="Is neutered/spayed?")
    is_neutered = models.CharField(choices=tuple(IS_NEUTRED_CHOICES), max_length=10, null=True, blank=True)

    # Avoid using null on string-based fields such as CharField and TextField 
    # ref: https://docs.djangoproject.com/en/1.8/ref/models/fields/#null
    name = models.CharField(max_length=255, unique=True)
    biography = models.TextField(max_length=1500, blank=True, help_text=_('A short introduction'))

    # 1. Set related_name='+' to stop the error
    # 2. To limit the choices available to the dropdown, do the following in __init__ of ModelForm
    #    self.fields['cover'].queryset = Photo.objects.filter(dog=self.instance.pk)  # ModelChoiceField.queryset
    #    This essentially narrows down the choices to only those belonging to the currently selected parent instance. 
    cover = models.OneToOneField('Photo', null=True, blank=True, related_name='+', on_delete=models.SET_NULL)

    # https://django-taggit.readthedocs.org/en/latest/api.html#TaggableManager
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('animal:detail', kwargs={'pk': self.pk})

    # https://docs.djangoproject.com/en/1.8/ref/contrib/admin/#reversing-admin-urls
    def get_admin_change_url(self):
        return reverse('admin:animal_animal_change', args=(self.pk,))  # use args, not kwargs


class Photo(TimeStampedModel):
    # TODO: user-uploaded photos in MEDIA_ROOT are not deleted when the parent model is deleted?
    #       ref: https://github.com/un1t/django-cleanup
    #       ref: https://github.com/Chive/django-multiupload
    img = ImageField(upload_to='photo/', null=True, blank=True)  # cannot be optional (definitive)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)  # one-to-many relationship

    def __str__(self):
        return os.path.basename(self.img.name)

