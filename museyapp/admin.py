from django.contrib import admin
from museyapp.models import User, Artist,Event,Event_Images,Event_Artist,Event_Donations,Event_Sharing
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
#Used to customize admin interface    
class Artist_admin(admin.ModelAdmin):
    #code
    model=Artist
    readonly_fields=['recvd_donation']
    fieldsets = [('Profile Picture',{'fields': ['profile_pic']}),('Personal Details',
    {'fields': ['first_name','last_name','nick_name','gender','bank_acct']}),
    ('Contact Information',{'fields':['email_id','phone','location']}),('Work',{'fields':['statement','self_desc','recvd_donation']}),('Media Links',{'fields':['Facebook','twitter','myspace','youtube',
    'tumblr','soundcloud','personal_link']})]
    
    
class EventImagesInlineFormSet(BaseInlineFormSet):
    #code
    def clean(self):
      super(EventImagesInlineFormSet, self).clean()
      truecount=0
      for form in self.forms:
         if not form.is_valid():
            return #other errors exist, so don't bother
         elif form.cleaned_data and form.cleaned_data['default']==True:
            truecount+=1
      if truecount==0:
        raise ValidationError('Atleast one image should be selected as default')
      elif truecount>1:
        raise ValidationError('Only one image can be set to default')
            
 
class EventImages_Inline(admin.StackedInline):
    model=Event_Images
    formset=EventImagesInlineFormSet
    extra = 1
    verbose_name_plural=verbose_name='Images'
class EventArtists_Inline(admin.StackedInline):
    model=Event_Artist
    verbose_name_plural=verbose_name="Artists"
    extra=1
    
class EventDonations_Inline(admin.StackedInline):
    model=Event_Donations
    readonly_fields=model._meta.get_all_field_names()
    verbose_name_plural=verbose_name='Donation Statistics'
    
    def has_add_permission(self, request):
        # Nobody is allowed to add
        return False
    
class EventSharing_Inline(admin.StackedInline):
    model=Event_Sharing
    readonly_fields=model._meta.get_all_field_names()
    verbose_name_plural=verbose_name='Sharing statistics'
    
    def has_add_permission(self, request):
        # Nobody is allowed to add
        return False
    
class Event_admin(admin.ModelAdmin):
    #code
    model=Event
    inlines=[EventImages_Inline,EventArtists_Inline,EventDonations_Inline,EventSharing_Inline]
   
admin.site.register(Artist,Artist_admin)
admin.site.register(User)
admin.site.register(Event,Event_admin)