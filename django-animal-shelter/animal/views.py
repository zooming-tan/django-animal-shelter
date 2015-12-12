from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Animal
from .forms import SearchAndFilterForm


# FormMixin (supplemental) provides form handling methods 
# to be used in get() method of ListView (main).
# Most of the time, we need to override the main get()/post() to include
# mixin functionalities.
class AnimalList(FormMixin, ListView):
    model = Animal
    form_class = SearchAndFilterForm  # search form
    paginate_by = 12

    # FormMixin
    def get_form_kwargs(self):
        """Override to pull data from GET request instead of
        the default POST request. """
        kwargs = super().get_form_kwargs()
        kwargs['data'] = self.request.GET or None  # idiom?
        return kwargs

    # ListView (main)
    # copied from http://ccbv.co.uk/projects/Django/1.8/django.views.generic.list/ListView/
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        # >>> insert
        # instantiate a form using get_form_kwargs() above
        form = self.get_form(self.get_form_class())

        if form.is_valid():  # check that query parameters have valid values and types
            # variant:
            # sql_query = {
            #     'name__icontains': form.cleaned_data['query'],
            # }
            sql_query = form.cleaned_data  # a dictionary of named parameters and their values

            # custom logic: If the parameter contains 'Any', drop it from the filter
            sql_query = {k:v for (k,v) in sql_query.items() if v is not None}

            self.object_list = self.object_list.filter(**sql_query)
        # >>> end insert

        allow_empty = self.get_allow_empty()
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if (self.get_paginate_by(self.object_list) is not None
                    and hasattr(self.object_list, 'exists')):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.")
                        % {'class_name': self.__class__.__name__})
        context = self.get_context_data()  # paginated here. Filter first then paginate.

        # >>> insert
        context['form'] = form  # include to be rendered in the template
        # >>> end insert

        return self.render_to_response(context)



class AnimalDetail(DetailView):
    model = Animal