from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm, UserProfileForm
from datetime import datetime

def index(request):
    request.session.set_test_cookie()
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories':category_list,'pages':page_list}
  
    #add cookie information to the respose
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    #get response objects earlier so we can add cookie information
    response = render(request, 'rango/index.html', context_dict)
    # return cookie-updating response
    return response    
  

def about(request):
    if request.session.test_cookie_worked():
        print('TEST COOKIE WORKED!')
        request.session.delete_test_cookie()
        #add cookie information to the respose
    visitor_cookie_handler(request)
    context_dict = {'visits':request.session['visits']}
    response = render(request, 'rango/about.html',context_dict)
    return response
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

#important! this function basically handles both displaying the form and processing data from it..
def register(request):
    registered = False
    #if it's a http post, then we it meaans we're getting form data which we must in turn process!
    if request.method == 'POST':
        #try to grab the raw request data(binary?) 
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)
        #if the data from the two forms is valid..
        if user_form.is_valid() and profile_form.is_valid():
            #save the user FORM DATA to the database (but has it been processed yet?)
            user = user_form.save()
            #hash the password, once hashed we then create an user object !!
            user.set_password(user.password)
            user.save() #i.e. now we STORE it in the database; before in was just in the server's RAM or smtng
            #setting commit = false delays saving the mode until we are rid of integrity problems
            #create a variable which stores all the data frm the userProfile form...
            profile = profile_form.save(commit=False)
            #flesh the 1 to 1 relationship i.e. fix the userprofiles's user associate
            profile.user = user
            
            #if the user provided a pic in the registration form..
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            
            registered = True
            
        else:
            #one of the form (or both) is invalid; print the errors to terminal
            print(user_form.errors, profile_form.errors)
    else: #if it's not a post, actually...then it is a GET! sooo let's display stuff
        user_form = UserForm()
        profile_form = UserProfileForm()
        
    return render(request, 'rango/register.html', 
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
    
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        #check if password+user combination is valid; return a user object if it is
        user = authenticate(username = username, password = password)
        
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html', {})
    
@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})

@login_required

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()) )

    last_visit_time = datetime.strptime(last_visit_cookie[:-7], "%Y-%m-%d %H:%M:%S")
    #last_visit_time = datetime.now()
    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        #update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        # set the last visit cookie 
        request.session['last_visit'] = last_visit_cookie
    # update/set the visits cookie
    request.session['visits'] = visits
    
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val
        