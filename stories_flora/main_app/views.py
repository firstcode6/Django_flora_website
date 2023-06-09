from django.http import HttpResponse
from django.core.management import call_command
import os
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Stories, Stories_i18n, Pages, Languages, Categories, Categories_i18n, Geolocations
from .forms import StoriesForm, Stories_i18nForm, PagesForm, RegisterUserForm, LoginUserForm
from django.views.generic import DetailView, UpdateView, View, ListView, CreateView
from datetime import date
from django.db.models import Prefetch
from django.db.models import Max

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView


# region Login
############################################## Login #############################################################
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'main_app/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class RegisterUser(CreateView):
    form_class = RegisterUserForm  # UserCreationForm
    template_name = 'main_app/register.html'
    success_url = reverse_lazy('login')

    # success registration
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


@login_required(login_url='login')
def download_database(request):
    # Generate the JSON file using the dumpdata command
    call_command('dumpdata', stdout=open('main_app/fixtures/data.json', 'w', encoding='utf-8'), indent=1,
                 exclude=['contenttypes', 'auth'])

    # Check if the JSON file exists before opening it
    if os.path.exists('main_app/fixtures/data.json'):
        with open('main_app/fixtures/data.json', 'r', encoding='utf-8') as f:
            data = f.read()

        # Create the HTTP response with the JSON file contents and appropriate headers
        response = HttpResponse(data, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=data.json'
        return response
    else:
        return HttpResponse('Error: Could not find data.json file.')
        # return redirect('home')


# endregion

# region View
############################################## View #############################################################

class StoriesView(LoginRequiredMixin, ListView):
    model = Stories
    template_name = 'main_app/stories.html'
    context_object_name = 'stories_key'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['checkbox_checked'] = True  # Set this based on your condition
        context['categ_news_val'] = self.request.GET.get("categ_news_val") == 'True'
        return context

    def get_queryset(self):
        # Define a Prefetch object to prefetch the related Stories_i18n objects
        stories_i18n_prefetch = Prefetch('storiesi18n_stories', queryset=Stories_i18n.objects.filter(language="de"))

        # Use prefetch_related to retrieve the Stories objects and their related Stories_i18n objects
        queryset = super().get_queryset().prefetch_related(stories_i18n_prefetch)
        return queryset


class AboutView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        return render(request, 'main_app/about.html')


class StoryDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'key_story'
    model = Stories
    queryset = Stories.objects.prefetch_related('storiesi18n_stories').all()
    template_name = 'main_app/story_details.html'
    login_url = 'login'  # if the user is not authorized redirect to authorization page

    # login_url = reverse_lazy('home') # redirect to home page
    # raise_exception = True  # redirect to page 403 Forbidden

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print("self.kwargs['pk']=", self.kwargs['pk'])
        context['stories_i18n'] = self.object.storiesi18n_stories.all()
        return context


class Story_i18nDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'page_story'
    model = Stories_i18n
    queryset = Stories_i18n.objects.prefetch_related('pages_storiesi18n').all()
    template_name = 'main_app/story_i18n_details.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pages'] = self.object.pages_storiesi18n.all()
        return context


class LanguagesView(LoginRequiredMixin, ListView):
    model = Languages
    template_name = 'main_app/languages.html'
    context_object_name = 'languages'
    login_url = 'login'


class CategoriesView(LoginRequiredMixin, ListView):
    model = Categories
    template_name = 'main_app/categories.html'
    context_object_name = 'categories'
    login_url = 'login'


class CategoryDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'key_category'
    model = Categories
    queryset = Categories.objects.prefetch_related('categoriesi18n_categories').all()
    template_name = 'main_app/category_details.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_i18n'] = self.object.categoriesi18n_categories.all()
        return context


# endregion

# region Filter
class FilterStoriesView(LoginRequiredMixin, ListView):
    template_name = 'main_app/stories.html'
    context_object_name = 'stories_key'
    login_url = 'login'

    def get_queryset(self):
        # queryset = Stories.objects.filter(category__in=self.request.GET.getlist("categ_val"))
        # queryset = Stories.objects.filter(hide_in_stories=self.request.GET.get("hidden_val"))

        categ_tip = self.request.GET.get("categ_tip_val")
        categ_news = self.request.GET.get("categ_news_val")
        hidden = self.request.GET.get("hidden_val")
        delet = self.request.GET.get("deleted_val")
        actual = self.request.GET.get("date_val")
        print("categ_tip====", categ_tip)
        print("categ_news====", categ_news)
        print("hidden====", hidden)
        print("delet====", delet)
        print("actual====", actual)

        conditions = {}
        # if categories_list and categories_list[0] is not None:
        #     conditions['q1'] = Q(category__in=categories_list)
        if categ_news is not None:
            conditions['q1'] = Q(category='1')
        if categ_tip is not None:
            conditions['q1'] = Q(category='2')
        if categ_tip is not None and categ_news is not None:
            conditions['q1'] = (Q(category='1') | Q(category='2'))

        if hidden is not None:
            conditions['q2'] = Q(hide_in_stories=hidden)
        if delet is not None:
            conditions['q3'] = Q(deleted=delet)
        if actual is not None:
            conditions['q4'] = (Q(fresh_after__lt=date.today()) & \
                                Q(fresh_before__gte=date.today()) | \
                                Q(fresh_after__isnull=True) | \
                                Q(fresh_before__isnull=True))

        combined_query = Q()
        for q in conditions.values():
            if q:
                combined_query &= q

        print("combined_query123===", combined_query)
        # combined_query123 == = (AND: ('category__in', ['2']), ('hide_in_stories', 'True'),
        #                        ('deleted', 'True'),
        #                        (OR: (AND: ('fresh_after__lt', datetime.date(2023, 4, 16)),
        #                                   ('fresh_before__gte', datetime.date(2023, 4, 16))),
        #                                   ('fresh_after__isnull', True),
        #                                   ('fresh_before__isnull', True)))

        if combined_query:
            queryset = Stories.objects.filter(combined_query)
        else:
            queryset = Stories.objects.all()
        return queryset


# endregion

# region Add
############################################## Add #############################################################
@login_required(login_url='login')  # decorator
def add_story(request):
    # static information from table Geolocations
    geo_values = Geolocations.objects.all()

    if request.method == 'POST':
        form_story = StoriesForm(request.POST)  # getting all data which was filled

        if form_story.is_valid():  # validation
            story = form_story.save()
            # redirection on successful save
            return redirect(f'/story={story.pk}/')  # flora-stories-editor/
    else:
        form_story = StoriesForm()  # if validation is fail we keep data in forms

    data = {
        'form_story': form_story,
        'geo_values': geo_values
    }
    return render(request, 'main_app/add_story.html', data)

@login_required(login_url='login')
def add_story_i18n(request, pk_st):
    if request.method == 'POST':
        form_story_i18n = Stories_i18nForm(request.POST, request.FILES)
        print(form_story_i18n.is_valid())
        if form_story_i18n.is_valid():
            story_i18n = form_story_i18n.save()
            return redirect(f'/story={story_i18n.story}/story_i18n={story_i18n.pk}/')  # flora-stories-editor/

    else:
        form_story_i18n = Stories_i18nForm(initial={'story': pk_st})

    data = {
        'form_story_i18n': form_story_i18n
    }
    return render(request, 'main_app/add_story_i18n.html', data)


def new_order(pk_i18n):
    # determine the max value of the order column
    all_pages_by_i18n = Pages.objects.filter(story_i18n=pk_i18n)
    if not all_pages_by_i18n:
        max_order = 100
    else:
        max_order = all_pages_by_i18n.aggregate(Max('order'))
        max_order = max_order['order__max'] + 100
    return max_order


@login_required(login_url='login')
def add_page(request, pk_st, pk_i18n):
    max_order = new_order(pk_i18n)
    error_message = ''

    if request.method == 'POST':
        form_page = PagesForm(request.POST, request.FILES)
        if form_page.is_valid():
            page = form_page.save()
            return redirect(f'/story={page.story_i18n.story}/story_i18n={page.story_i18n.pk}/')  # flora-stories-editor/
        else:
            error_message = "A record with this combination of fields already exists."
            print("error_message123", error_message)
    else:
        form_page = PagesForm(initial={'story_i18n': pk_i18n})

    data = {
        'form_page': form_page,
        'max_order': max_order,
        'error_message': error_message
    }
    return render(request, 'main_app/add_page.html', data)


# endregion

# region Copy
############################################## Copy #############################################################
def copy_pages(page, story_i18n_id):
    new_page = page
    new_page.pk = None
    new_page.story_i18n = get_object_or_404(Stories_i18n, pk=story_i18n_id)
    new_page.save()


@login_required(login_url='login')
def copy_story(request, pk):
    sample_story = get_object_or_404(Stories, pk=pk)
    new_story = sample_story
    new_story.pk = None

    if sample_story is not None:
        new_story.save()
        story = new_story

        # make copy stories_i18n if they are
        stories_i18n = Stories_i18n.objects.filter(story=pk)
        for story_i18n in stories_i18n:
            if story_i18n is not None:
                story_i18n_id = story_i18n.pk
                new_story_i18n = story_i18n
                new_story_i18n.pk = None
                new_story_i18n.story = get_object_or_404(Stories, pk=story.pk)
                new_story_i18n.save()

                # make copy pages if they are
                pages = Pages.objects.filter(story_i18n=story_i18n_id)
                for page in pages:
                    if page is not None:
                        copy_pages(page, new_story_i18n.pk)

        form_story = StoriesForm(instance=story)
        return redirect(f'/story={story.pk}/edit')  # flora-stories-editor/
    else:
        error = 'Copy error'
        form_story = StoriesForm()

    data = {
        'form_story': form_story,
        'error_add': error
    }
    return render(request, 'main_app/edit_story.html', data)


@login_required(login_url='login')
def copy_story_i18n(request, pk_st, pk):
    sample_story_i18n = get_object_or_404(Stories_i18n, pk=pk)
    new_story_i18n = sample_story_i18n
    new_story_i18n.pk = None

    if sample_story_i18n is not None:
        new_story_i18n.save()
        story_i18n = new_story_i18n

        # make copy pages if they are
        pages = Pages.objects.filter(story_i18n=pk)
        for page in pages:
            if page is not None:
                copy_pages(page, story_i18n.pk)
                # new_page = page
                # new_page.pk = None
                # new_page.story_i18n = get_object_or_404(Stories_i18n, pk=story_i18n.pk)
                # new_page.save()

        form_story_i18n = Stories_i18nForm(instance=story_i18n)
        return redirect(f'/story={story_i18n.story}/story_i18n={story_i18n.pk}/edit')  # flora-stories-editor/
    else:
        error = 'Copy error'
        form_story_i18n = Stories_i18nForm(initial={'story': pk_st})

    data = {
        'form_story_i18n': form_story_i18n,
        'error_add': error
    }
    return render(request, 'main_app/edit_story_i18n.html', data)


@login_required(login_url='login')
def copy_page(request, pk_st, pk_i18n, pk_page):
    sample_page = get_object_or_404(Pages, pk=pk_page)
    new_page = sample_page
    new_page.pk = None
    max_order = new_order(pk_i18n)
    new_page.order = max_order

    if sample_page is not None:
        new_page.save()
        page = new_page
        form_page = PagesForm(instance=page)
        #return redirect(f'/flora-stories-editor/story={page.story_i18n.story}/story_i18n={page.story_i18n.pk}/page={page.pk}-edit')
        return redirect(f'/story={page.story_i18n.story}/story_i18n={page.story_i18n.pk}/page={page.pk}-edit')
    else:
        error = 'Copy error'
        form_page = PagesForm(initial={'story_i18n': pk_i18n})

    data = {
        'form_page': form_page,
        'error_add': error
    }
    return render(request, 'main_app/edit_story.html', data)


# endregion

# region Edit
############################################## Edit #############################################################

class StoryEditView(LoginRequiredMixin, UpdateView):
    template_name = 'main_app/edit_story.html'
    model = Stories
    form_class = StoriesForm
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        story = get_object_or_404(Stories, pk=self.kwargs['pk'])
        context['form_story'] = StoriesForm(instance=story)
        context['geo_values'] = Geolocations.objects.all()
        return context

    # def get_success_url(self):
    #     story_pk = self.kwargs['pk']
    #     return f'/flora-stories-editor/story={story_pk}/'




class Story_i18nEditView(LoginRequiredMixin, UpdateView):
    template_name = 'main_app/edit_story_i18n.html'
    model = Stories_i18n
    form_class = Stories_i18nForm
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        story_i18n = get_object_or_404(Stories_i18n, pk=self.kwargs['pk'])
        context['form_story_i18n'] = Stories_i18nForm(instance=story_i18n)
        return context
    # def get_success_url(self):
    #     story_i18n = get_object_or_404(Stories_i18n, pk=self.kwargs['pk'])
    #     return f'/flora-stories-editor/story={story_i18n.story}/story_i18n={story_i18n.pk}/'


class PageEditView(LoginRequiredMixin, UpdateView):
    template_name = 'main_app/edit_page.html'
    model = Pages
    form_class = PagesForm
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = get_object_or_404(Pages, pk=self.kwargs['pk'])
        context['form_page'] = PagesForm(instance=page)
        return context
    # def get_success_url(self):
    #     page = get_object_or_404(Pages, pk=self.kwargs['pk'])
    #     return f'/flora-stories-editor/story={page.story_i18n.story}/story_i18n={page.story_i18n.pk}/'
# endregion
