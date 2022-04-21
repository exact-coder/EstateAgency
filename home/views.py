
from django.contrib.auth import decorators
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage

from home.models import Inquary, Property, Slider

# Create your views here.

def home(request):
    slider = Slider.objects.all()
    property = Property.objects.all()
    context = {
        'slider' : slider,
        'property' : property,
    }
    return render(request, 'home/index.html',context)

def all_property(request):
    property_list = Property.objects.filter(is_publish = True)
    paginator = Paginator(property_list, 6)
    page_number = request.GET.get('page')
    property = paginator.get_page(page_number)

    context = {
        'property' : property,
    }
    return render(request, 'home/all_property.html', context)

def single_property(request, id):
    property = Property.objects.get(id = id)
    context = {
        'property' : property
    }
    return render(request, 'home/single_property.html', context)

@login_required
def post_property(request):
    if request.method == "POST" and request.FILES['image']:
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        location = request.POST.get('location')
        area = request.POST.get('area')
        beds = request.POST.get('beds')
        baths = request.POST.get('baths')
        garage = request.POST.get('garage')
        video = request.POST.get('video')
        image = request.FILES['image']
        user = request.user

        Property.objects.create(name= name,description = description, price = price, location = location , area = area, beds = beds, baths= baths, garage = garage, video = video, image =image, user = user)
        messages.success(request, 'Property added successfully')
    else:
        messages.success(request, 'Something happening wrong!')
    return render(request, 'home/post_property.html')

def inquary(request):
    if request.method == 'POST':
        property_owner_email = request.POST.get('property_owner_email')
        property_id = request.POST.get('property_id')
        property_name = request.POST.get('property_name')


        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        user = request.user
        Inquary.objects.create(user = user, name = name, email = email, phone = phone, message = message)
        email_subject = 'Property Inquary Message From EstateAgency'
        email_body = 'You have an inquary message from ' + name + '\nEmail: '+email+'\nPhone: '+ phone +'\nHe/She send you this message: \n'+ message + '\n\n For Property ID:  '+str(property_id)+'\nProperty Name: ' + property_name+''
        email_address = property_owner_email

        email = EmailMessage(
            email_subject,
            email_body,
            'noreply@estateagency.com',
            [email_address],
        )
        email.send(fail_silently=False)
        messages.success(request,'Your message send Successfully')
        return render(request, 'home/single_property.html')
    else:
        messages.success(request, 'Some Wrong Occuring')
    return render(request, '/')

def search(request):
    get_method = request.GET.copy()
    keywords = get_method.get('keywords') or None
    """ property_types = get_method.get('property_types') or None
    property_citys = get_method.get('property_citys') or None
    property_bedrooms = get_method.get('property_bedrooms') or None
    property_garages = get_method.get('property_garages') or None
    property_baths = get_method.get('property_baths') or None
    property_prices = get_method.get('property_prices') or None """
    property_list = Property.objects.all()

    if keywords is not None:
        keyword = get_method['keywords']
        property_list = property_list.filter(description__icontains = keyword)
    if 'property_types' in get_method:
        property_type = get_method['property_types']
        if property_type == 'None':
            pass
        else:
            property_list = property_list.filter(property_type__iexact = property_type)
    if 'property_citys' in get_method:
        property_city = get_method['property_citys']
        if property_city == 'None':
            pass
        else:
            property_list = property_list.filter(location__iexact = property_city)
    if 'property_bedrooms' in get_method:
        property_bedroom = get_method['property_bedrooms']
        if property_bedroom == 'None':
            pass
        else:
            property_list = property_list.filter(beds__lte = property_bedroom)
    if 'property_garages' in get_method:
        property_garage = get_method['property_garages']
        if property_garage == 'None':
            pass
        else:
            property_list = property_list.filter(garage__lte = property_garage)
    if 'property_baths' in get_method:
        property_bath = get_method['property_baths']
        if property_bath == 'None':
            pass
        else:
            property_list = property_list.filter(baths__lte = property_bath)
    if 'property_prices' in get_method:
        property_price = get_method['property_prices']
        if property_price == 'None':
            pass
        else:
            property_list = property_list.filter(price__lte = property_price)
        
    context = {
        'property_list': property_list,
    }
    return render(request, 'includes/search_result.html',context)

