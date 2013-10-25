# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from museyapp import forms
from museyapp.models import Event,User,Artist, Sale
from django.forms.util import ErrorList

def index(request):
    
    #login=req.session['login']='Log In'
    
    #login=request.session['login']
    return render(request, 'museyapp/index.html',{'login':login,} )

def signup(request):
   
    if request.method =='POST':
        user_form=forms.UserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return HttpResponse('form saved')
    else:
        user_form=forms.UserForm()
    return render(request, 'museyapp/signup.html', {'form': user_form,})
    
def login(request):
    
    
    if request.method =='POST':
        
        login_form=forms.LoginForm(request.POST)
        
        if login_form.is_valid():
            print login_form.cleaned_data['password']
            if not User.objects.filter(email_address=login_form.cleaned_data['email_address'],password=login_form.cleaned_data['password']):
                errors = login_form._errors.setdefault("email_address", ErrorList())
                errors.append(u"Invalid Email Id or Password")
            else:
                 request.session['login']='Logoff'
                 return HttpResponseRedirect('/')
            
    else:
        login_form=forms.LoginForm()
    return render(request,'museyapp/login.html',{'form':login_form,})    
    
def events(request, event_id=None):
    events=Event.objects.all()
    if len(events)>0:
        if not event_id:
            event=events[0]
            
        else:
            event=Event.objects.get(id=event_id)
            
        prv_event=event.getprv()
        nxt_event=event.getnext()
        event_img=event.event_images_set.get(default=True)
    else:
        event=None
    return render(request, 'museyapp/events.html', {'event': event,'prv_event':prv_event,'nxt_event':nxt_event,'event_img':event_img})

def projects(request, prjct_id):
    event=Event.objects.get(id=prjct_id)
    event_img=event.event_images_set.get(default=True)
    return render(request, 'museyapp/projects.html', {'event': event,'event_img':event_img})


def artist(request, artist_id):
    artist=Artist.objects.get(id=artist_id)
    return render(request,'museyapp/artists.html',{'artist':artist})

def charge(request):
    if request.method == "POST":
        form = forms.SalePaymentForm(request.POST)
 
        if form.is_valid(): # charges the card
            return HttpResponse("Success! We've charged your card!")
    else:
        form = forms.SalePaymentForm()
 
    return render_to_response("museyapp/charge.html",
                        RequestContext( request, {'form': form} ) )



#------------------------------PayPal-------------------------------#
#-------------------------------------------------------------------#

from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.core.urlresolvers import reverse
def paypal(request):
# What you want the button to do.
    paypal_dict = {
    "business": settings.PAYPAL_RECEIVER_EMAIL,
    "amount": "1.00",
    "item_name": "name of the item",
    "invoice": "unique-invoice-id",
    "notify_url": "%s%s" % (settings.SITE_NAME, reverse('paypal-ipn')),
    "return_url": "http://www.example.com/your-return-location/",
    "cancel_return": "http://www.example.com/your-cancel-location/",}
# Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form.sandbox()}
    return render_to_response("paypal.html", context)


