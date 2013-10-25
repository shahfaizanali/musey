from django.db import models
from django.contrib import admin
# Create your models here.

#General User Table
class User(models.Model):
    #fields
    email_address=models.EmailField(primary_key=True)
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    password=models.CharField(('password'),max_length=50)
    
    #what to return when object is get
    def __unicode__(self):
        return self.email_address #returning primary key to identify user
   

class Artist(models.Model):
    #fields
    
    #Basics
    profile_pic=models.ImageField(upload_to='images/artist/pics')
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    nick_name=models.CharField(max_length=20,blank=True)
    MALE='M'
    FEMALE='F'
    GENDER=((MALE, 'Male'),(FEMALE,'Female'))
    gender = models.CharField(max_length=1,choices=GENDER,default=MALE)
    location=models.CharField(max_length=100)
    bank_acct=models.CharField(max_length=20)
    
    #Work
    statement=models.CharField(max_length=100)
    self_desc=models.TextField(max_length=500)
    recvd_donation=models.PositiveIntegerField(default=0)
    
    #Contact
    email_id=models.EmailField()
    phone=models.CharField(max_length=50,blank=True)
    
    #Artist_Media Links
    Facebook=models.URLField(blank=True)
    twitter=models.URLField(blank=True)
    myspace=models.URLField(blank=True)
    youtube=models.URLField(blank=True)
    tumblr=models.URLField(blank=True)
    soundcloud=models.URLField(blank=True)
    personal_link=models.URLField(blank=True)
    
    def __unicode__(self):
        return self.first_name +" "+self.last_name



    
    
class Event(models.Model):
    #fields
    main_title=models.CharField(max_length=50)
    Subtitle=models.CharField(max_length=50)
    datefrom=models.DateField()
    dateto=models.DateField()
    timefrom=models.TimeField()
    timeto=models.TimeField()
    Location=models.CharField(max_length=100)
    Remarks=models.TextField(max_length=500)
    Description=models.TextField(max_length=500)
    external_link=models.URLField()
    
    #what to return when object is get
    def __unicode__(self):
        return self.main_title
    
    def getnext(self):
        events=Event.objects.all()
        size=len(events)
        for x in xrange(size):
            if self.id==events[x].id:
                if x+1 != size:
                    return events[x+1]
                else:
                    return events[0]
    
    def getprv(self):
        events=Event.objects.all()
        size=len(events)
        for x in xrange(size):
            if self.id==events[x].id:
                if x-1 >-1:
                    return events[x-1]
                else:
                    return events[size-1]    
    #Advocates (keep void)
  


class Event_Images(models.Model):
    #code
    def upload_to(instance, filename):
        return 'images/events/'+instance.event.main_title+'/'+filename
    event=models.ForeignKey(Event)
    image=models.ImageField(upload_to=upload_to)
    default=models.BooleanField()
    class Meta:
        unique_together = ('image', 'event',)
   
class Event_Artist(models.Model):
    artist=models.ForeignKey(Artist)
    role=models.CharField(max_length=20)
    event=models.ForeignKey(Event)
    class Meta:
        unique_together = ('artist', 'event',)
    def __unicode__(self):
        artist=self.artist
        return artist.first_name+" "+artist.last_name + '('+ self.role + ')'    

class Event_Donations(models.Model):
    #code
    event=models.ForeignKey(Event)
    doner_account=models.ForeignKey(User)
    donation_amount=models.PositiveIntegerField(default=0)
    donation_location=models.CharField(max_length=100)
    donation_time=models.DateTimeField()
    payment_method=models.CharField(max_length=10,choices=(('p','PayPal'),('c','CreditCard')))

class Event_Sharing(models.Model):
    #code
    user_acct=models.ForeignKey(User)
    event=models.ForeignKey(Event)
    time=models.DateTimeField()
    media=models.CharField(max_length=20)

#--------------------models for stripe-------------------------------#
#--------------------------------------------------------------------#


from django.conf import settings
 
class Sale(models.Model):
    def __init__(self, *args, **kwargs):
        super(Sale, self).__init__(*args, **kwargs)
 
        # bring in stripe, and get the api key from settings.py
        import stripe
        stripe.api_key = settings.STRIPE_API_KEY
 
        self.stripe = stripe
 
    # store the stripe charge id for this sale
    charge_id = models.CharField(max_length=32)
 
    # you could also store other information about the sale
    # but I'll leave that to you!
 
    def charge(self, price_in_cents, number, exp_month, exp_year, cvc):
        """
        Takes a the price and credit card details: number, exp_month,
        exp_year, cvc.
 
        Returns a tuple: (Boolean, Class) where the boolean is if
        the charge was successful, and the class is response (or error)
        instance.
        """
 
        if self.charge_id: # don't let this be charged twice!
            return False, Exception(message="Already charged.")
 
        try:
            response = self.stripe.Charge.create(
                amount = price_in_cents,
                currency = "usd",
                card = {
                    "number" : number,
                    "exp_month" : exp_month,
                    "exp_year" : exp_year,
                    "cvc" : cvc,
 
                    #### it is recommended to include the address!
                    #"address_line1" : self.address1,
                    #"address_line2" : self.address2,
                    #"daddress_zip" : self.zip_code,
                    #"address_state" : self.state,
                },
                description='Thank you for your purchase!')
 
            self.charge_id = response.id
 
        except self.stripe.CardError, ce:
            # charge failed
            return False, ce
 
        return True, response
    
#-----------------------End models of stripe----------------------------------#
#-----------------------------------------------------------------------------#

