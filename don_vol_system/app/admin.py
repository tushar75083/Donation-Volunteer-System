from django.contrib import admin
from app.models import Donor,Volunteer,DonationArea,Donation,Gallery,Payment

# Register your models here.
@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display=['id','user','contact','address','regdate']

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display=['id','user','contact','address','regdate']

@admin.register(DonationArea)
class DonationAreaAdmin(admin.ModelAdmin):
    list_display=['id','areaname','description','creationdate']

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display=['id','donor','volunteer','donationarea','donationname']

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display=['id','donation','deliverypic','creationdate']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display=['id','amount','razorpay_order_id','razorpay_payment_id','status','created_at']