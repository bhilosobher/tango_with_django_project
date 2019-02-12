from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
def index(request):
    
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories':category_list,'pages':page_list}
    # render and send back response
    return render(request, 'rango/index.html', context_dict)
    #return HttpResponse("Rango says hey there partner!<br/> <a href='/rango/about/'>About</a>")

def about(request):
    return render(request, 'rango/about.html', {})
    #return HttpResponse("Rango says here is the about page.<br/> <a href='/rango/'>Index</a>")
    
def show_category(request, category_name_slug):
    #create a context dictionary which we can pass to the template rendering engine
    context_dict = {}
    
    try:
        category  = Category.objects.get(slug = category_name_slug)
        
        pages = Page.objects.filter(category = category)
        
        context_dict['pages'] = pages
        context_dict['category'] = category
        
    except Category.DoesNotExist:
        #do nothing if no such category
        context_dict['pages'] = None
        context_dict['category'] = None
        
    return render(request, 'rango/category.html', context_dict)
        
def add_category(request):
    form = CategoryForm()
    
    #a http post? yummmy
    if request.method == 'POST':
        #if i received a post request from the user on the page, then post the contents of the form
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit = True)
            return index(request)
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form } )

def add_page(request,category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit = False) #what is commit = false/true?)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
            else:
                print(form.errors)
                
    context_dict = {'form':form, 'category':category}
    return render(request, 'rango/add_page.html', context_dict)