from django.http import HttpResponse
from django.views import View
from app.forms import UserForm,DonorSignupForm,VolunteerSignupForm,LoginForm,MyPasswordChangeForm,DonateNowForm,DonationAreaForm
from django.shortcuts import get_object_or_404, redirect, render
from app.models import Donor, Payment,Volunteer,Donation,DonationArea,Gallery
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from datetime import date


# payment
import razorpay # type: ignore
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def index(request):
    return render(request, "index.html")


def gallery(request):
    gallery=Gallery.objects.all()
    return render(request, "gallery.html",locals())


class login_admin(View):
    def get(self,request):
        form=LoginForm()
        return render(request,'login-admin.html',locals())
    
    def post(self,request):
        form=LoginForm(request.POST)
        us=request.POST['username']
        pwd=request.POST['password']
        try:
            if us=="" or pwd=="":
                messages.warning(request,"Please enter Username and Password")
                return redirect('/login-admin')
            
            user=authenticate(username=us,password=pwd)            
            if user:
                if user.is_staff:                  
                    login(request,user)
                    return redirect('/index-admin')
                else:
                    messages.warning(request,"Invalid Admin User")
            else:
                messages.warning(request,"Invalid Username and Password")
        except:
            messages.warning(request,'Login Failed..')
        return render(request,'login-admin.html',locals())
    

class login_donor(View):
    def get(self,request):
        form=LoginForm()
        return render(request,'login-donor.html',locals())
    def post(self,request):
        form=LoginForm(request.POST)
        us=request.POST['username']
        pwd=request.POST['password']
        try:
            if us=="" or pwd=="":
                messages.warning(request,"Please enter Username and Password")
                return redirect('/login-donor')
            
            user=authenticate(username=us,password=pwd)
            if user:
                donor_user=Donor.objects.filter(user_id=user.id)
                if donor_user:
                    login(request,user)
                    return redirect('/index-donor')
                else:
                    messages.warning(request,'Invalid Donor User')
            else:
                messages.warning(request,'Invalid Username and Password')
        except:
            messages.warning(request,'Login Failed')
        return render(request,'login-donor.html',locals())
    

class login_volunteer(View):
    def get(self,request):
        form=LoginForm()
        return render(request,'login-volunteer.html',locals())
    def post(self,request):
        form=LoginForm(request.POST)
        us=request.POST['username']
        pwd=request.POST['password']
        try:
            if us=="" or pwd=="":
                messages.warning(request,"Please enter Username and Password")
                return redirect('/login-volunteer')
            
            user=authenticate(username=us,password=pwd)
            if user:
                vol_user=Volunteer.objects.filter(user_id=user.id)
                if vol_user:
                    login(request,user)
                    return redirect('/index-volunteer')
                else:
                    messages.warning(request,'Invalid Volunteer User')
            else:
                messages.warning(request,'Invalid Username and Password')
        except:
            messages.warning(request,'Login Failed')
        return render(request,'login-volunteer.html',locals())


class signup_donor(View):
    def get(self,requset):
        form1=UserForm()
        form2=DonorSignupForm()
        return render(requset,'signup_donor.html',locals())
    def post(self,request):
        form1=UserForm(request.POST)
        form2=DonorSignupForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            fn=request.POST['first_name']
            ln=request.POST['last_name']
            em=request.POST['email']
            us=request.POST['username']
            pwd=request.POST['password1']
            contact=request.POST['contact']
            userpic=request.FILES['userpic']
            address=request.POST['address']

            try:
                user=User.objects.create_user(first_name=fn,last_name=ln,username=us,email=em,password=pwd)
                Donor.objects.create(user=user,contact=contact,userpic=userpic,address=address)
                messages.success(request,'Congratulations!! Donor Profile Created Successfully... ')
                return redirect('/login-donor')
            except:
                messages.warning(request,'Profile Not Created...')
        return render(request,'signup_donor.html',locals())
    

class signup_volunteer(View):
    def get(self,request):
        form1=UserForm()
        form2=VolunteerSignupForm()
        return render(request,'signup_volunteer.html',locals())
    
    def post(self,request):
        form1=UserForm(request.POST)
        form2=VolunteerSignupForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            fn=request.POST['first_name']
            ln=request.POST['last_name']
            em=request.POST['email']
            us=request.POST['username']
            pwd=request.POST['password1']
            contact=request.POST['contact']
            userpic=request.FILES['userpic']
            idpic=request.FILES['idpic']
            address=request.POST['address']
            aboutme=request.POST['aboutme']

            try:
                user=User.objects.create_user(first_name=fn,last_name=ln,username=us,email=em,password=pwd)
                Volunteer.objects.create(user=user,contact=contact,userpic=userpic,idpic=idpic,address=address,aboutme=aboutme,status="pending")
                messages.success(request,'Congratulations!! Volunteer Profile Created Successfully... ')
                return redirect('/login-volunteer')
            except:
                messages.warning(request,'Profile Not Created...')
        return render(request,'signup_volunteer.html',locals())


def index_admin(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    totaldonations=Donation.objects.all().count()
    totaldonors=Donor.objects.all().count()
    totalvolunteers=Volunteer.objects.filter(status='accept').count()
    totalpendingdonations=Donation.objects.filter(status="pending").count()
    totalaccepteddonations=Donation.objects.filter(status="Accept").count()
    totaldelivereddonations=Donation.objects.filter(status="Donation Delivered Successfully").count()
    totaldonationareas=DonationArea.objects.all().count()
    return render(request, "index-admin.html",locals())

# admin dashboard

def pending_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation=Donation.objects.filter(status="pending")
    return render(request, "pending-donation.html",locals())


def accepted_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation=Donation.objects.filter(status="accept")
    return render(request, "accepted-donation.html",locals())


def rejected_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation=Donation.objects.filter(status="reject")
    return render(request, "rejected-donation.html",locals())


def volunteerallocated_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation=Donation.objects.filter(status="Volunteer Allocated")
    return render(request, "volunteerallocated-donation.html",locals())


def donationrec_admin(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation=Donation.objects.filter(status="Donation Received")
    return render(request, "donationrec-admin.html",locals())


def donationnotrec_admin(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation=Donation.objects.filter(status="Donation NotReceived")
    return render(request, "donationnotrec-admin.html",locals())


def donationdelivered_admin(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation=Donation.objects.filter(status="Donation Delivered Successfully")
    return render(request, "donationdelivered-admin.html",locals())


def all_donations(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation=Donation.objects.all()
    return render(request, "all-donations.html",locals())


def delete_donation(request,pid):
    donation=Donation.objects.get(id=pid)
    donation.delete()
    return redirect('/all-donations')


def manage_donor(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donor=Donor.objects.all()
    return render(request, "manage-donor.html",locals())


def new_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    volunteer=Volunteer.objects.filter(status='pending')
    return render(request, "new-volunteer.html",locals())


def accepted_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    volunteer=Volunteer.objects.filter(status='accept')
    return render(request, "accepted-volunteer.html",locals())


def rejected_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    volunteer=Volunteer.objects.filter(status='reject')
    return render(request, "rejected-volunteer.html",locals())


def all_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    volunteer=Volunteer.objects.all()
    return render(request, "all-volunteer.html",locals())


def delete_volunteer(request,pid):
    user=User.objects.get(id=pid)
    user.delete()
    return redirect('/all-volunteer')


class add_area(View):
    def get(self,request):
        form=DonationAreaForm()
        return render(request, "add-area.html",locals())
    
    def post(self,request):
        form=DonationAreaForm(request.POST)
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        areaname=request.POST['areaname']
        des=request.POST['description']

        try:
            DonationArea.objects.create(areaname=areaname,description=des)
            messages.success(request,"Area Added Successfully")
        except:
            messages.warning(request,"Area Not Added")
        return render(request, "add-area.html",locals())


class edit_area(View):
    def get(self,request,pid):
        form=DonationAreaForm()
        area=DonationArea.objects.get(id=pid)
        return render(request, "edit-area.html",locals())

    def post(self,request,pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        form=DonationAreaForm(request.POST)
        area=DonationArea.objects.get(id=pid)
        areaname=request.POST['areaname']
        description=request.POST['description']

        area.areaname=areaname
        area.description=description

        try:
            area.save()
            messages.success(request,"Area Updated Successfully")
            return redirect('manage_area')
        except:
            messages.warning(request,"Area Not Updated")
        return render(request, "edit-area.html",locals())
    

def manage_area(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    area=DonationArea.objects.all()
    return render(request, "manage-area.html",locals())


def delete_area(request,pid):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    area=DonationArea.objects.get(id=pid)
    area.delete()
    return redirect('manage_area')


class changepwd_admin(View):
    def get(self,request):
        form=MyPasswordChangeForm(request.user)
        return render(request,'changepwd-admin.html',locals())
    
    def post(self,request):
        form=MyPasswordChangeForm(request.user,request.POST)
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        old=request.POST['old_password']
        newpass=request.POST['new_password1']
        confirmpass=request.POST['new_password2']
        try:
            if old=="" or newpass=="" or confirmpass=="":
                messages.warning(request,"Please enter Old Password and New Passwords")
                return redirect("/changepwd-admin")
            if newpass==confirmpass:
                user=User.objects.get(id=request.user.id)
                if user.check_password(old):
                    user.set_password(newpass)
                    user.save()
                    messages.success(request,'Password changed successfully....')
                else:
                    messages.warning(request,'Old Password Not Matching...')
            else:
                messages.warning(request,'New Password and Confirm Password Not Matched...')
        except:
            messages.warning(request,'Failed to Change Password..')
        return render(request, "changepwd-admin.html",locals())


def user_logout(request):
    logout(request)
    return redirect("index")


# admin view details

class accepted_donationdetail(View):
    def get(self,request,pid):
        donation=Donation.objects.get(id=pid)
        donationarea=DonationArea.objects.all()
        volunteer=Volunteer.objects.filter(status="accept")
        # volunteer=Volunteer.objects.all()
        return render(request, "accepted-donationdetail.html",locals())
    
    def post(self,request,pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        donation=Donation.objects.get(id=pid)
        donationareaid=request.POST['donationareaid']
        volunteerid=request.POST['volunteerid']
        adminremark=request.POST['adminremark']
        da=DonationArea.objects.get(id=donationareaid)
        v=Volunteer.objects.get(id=volunteerid)

        try:
            donation.donationarea=da
            donation.volunteer=v
            donation.adminremark=adminremark
            donation.status="Volunteer Allocated"
            donation.volunteerremark="Not Updated Yet"
            donation.updationdate=date.today()
            donation.save()
            messages.success(request,"Volunteer Allocated Successfully")
        except:
            messages.warning(request,"Failed To Allocate Volunteer")
        return render(request, "accepted-donationdetail.html",locals())
        
   
class view_volunteerdetail(View):
    def get(self,request,pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        volunteer=Volunteer.objects.get(id=pid)
        return render(request, "view-volunteerdetail.html",locals())
    
    def post(self,request,pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        volunteer=Volunteer.objects.get(id=pid)
        status=request.POST['status']
        adminremark=request.POST['adminremark']
        try:
            volunteer.adminremark=adminremark
            volunteer.status=status
            volunteer.updationdate=date.today()
            volunteer.save()
            messages.success(request,"Volunteer Updated Successfully")
        except:
            messages.warning(request,"Volunteer Not Updated Successfully")
        return render(request, "view-volunteerdetail.html",locals()) 
    

def view_donordetail(request, pid):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donor=Donor.objects.get(id=pid)
    return render(request, "view-donordetail.html",locals())


def delete_donor(request,pid):
    user=User.objects.get(id=pid)
    user.delete()
    return redirect('manage_donor')


class view_donationdetail(View):
    def get(self,request,pid):
        donation=Donation.objects.get(id=pid)
        return render(request, "view-donationdetail.html",locals())
    
    def post(self,request,pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        donation=Donation.objects.get(id=pid)
        status=request.POST['status']
        adminremark=request.POST['adminremark']

        try:
            donation.adminremark=adminremark
            donation.status=status
            donation.updationdate=date.today()
            donation.save()
            messages.success(request,"Status and Remark Updated Successfully..")
        except:
            messages.warning(request,"Failed To Update Status and Remark..")
        return render(request, "view-donationdetail.html",locals())
               

# donor dashboard

def index_donor(request):
    if not request.user.is_authenticated:
        return redirect('/login-donor')
    user=request.user
    donor=Donor.objects.get(user=user)
    donationcount=Donation.objects.filter(donor=donor).count()
    acceptedcount=Donation.objects.filter(donor=donor,status="accept").count()
    rejectedcount=Donation.objects.filter(donor=donor,status="reject").count()
    volunteerallocatedcount=Donation.objects.filter(donor=donor,status="Volunteer Allocated").count()
    pendingcount=Donation.objects.filter(donor=donor,status="pending").count()
    deliveredcount=Donation.objects.filter(donor=donor,status="Donation Delivered Successfully").count()
    return render(request, "index-donor.html",locals())


class donate_now(View):
    
    def get(self,request):
        form=DonateNowForm()
        return render(request, "donate-now.html",locals())
    
    def post(self,request):
        myuser= request.user
        print('this is my user',myuser)
        form=DonateNowForm(request.POST)
        if not request.user.is_authenticated:
            return redirect('/login-donor')
        if form.is_valid():
            user=request.user
            donor=Donor.objects.get(user=user)
            donationname=request.POST['donationname']
            donationpic=request.FILES['donationpic']
            collectionloc=request.POST['collectionloc']
            description=request.POST['description']

            try:
                Donation.objects.create(donor=donor,donationname=donationname,donationpic=donationpic,collectionloc=collectionloc,description=description,status='pending',donationdate=date.today())
                messages.success(request,"Donation Saved Successfully")
            except:
                messages.warning(request,"Failed to Donation")
        return render(request,"donate-now.html",locals())
   

def donation_history(request):
    if not request.user.is_authenticated:
        return redirect('/login-donor')
    user=request.user
    donor=Donor.objects.get(user=user)
    donation=Donation.objects.filter(donor=donor)
    return render(request, "donation-history.html",locals())


def donor_accepted_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login-donor')
    user=request.user
    donor=Donor.objects.get(user=user)
    donation=Donation.objects.filter(donor=donor,status='accept')
    return render(request, "donation-history.html",locals())


def donor_rejected_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login-donor')
    user=request.user
    donor=Donor.objects.get(user=user)
    donation=Donation.objects.filter(donor=donor,status='reject')
    return render(request, "donation-history.html",locals())


def donor_volunteer_allocated_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login-donor')
    user=request.user
    donor=Donor.objects.get(user=user)
    donation=Donation.objects.filter(donor=donor,status='Volunteer Allocated')
    return render(request, "donation-history.html",locals())

def donor_pending_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login-donor')
    user=request.user
    donor=Donor.objects.get(user=user)
    donation=Donation.objects.filter(donor=donor,status='pending')
    return render(request, "donation-history.html",locals())

def donor_delivered_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login-donor')
    user=request.user
    donor=Donor.objects.get(user=user)
    donation=Donation.objects.filter(donor=donor,status='Donation Delivered Successfully')
    return render(request, "donation-history.html",locals())

class profile_donor(View):
    def get(self,request):
        form1=UserForm()
        form2=DonorSignupForm()
        user=request.user
        donor=Donor.objects.get(user=user)
        return render(request, "profile-donor.html",locals())
    
    def post(self,request):
        if not request.user.is_authenticated:
            return redirect('/login-donor')
        
        form1=UserForm(request.POST)
        form2=DonorSignupForm(request.POST)

        user=request.user
        donor=Donor.objects.get(user=user)

        fn=request.POST['firstname']
        ln=request.POST['lastname']
        contact=request.POST['contact']
        address=request.POST['address']

        donor.user.first_name=fn
        donor.user.last_name=ln
        donor.contact=contact
        donor.address=address

        try:
            userpic=request.FILES['userpic']
            donor.userpic=userpic
            donor.save()
            donor.user.save()
            messages.success(request,"Profile Updated Successfully...")
        except Exception as e:
            messages.warning(request,'Profile Update Failed...'+e)
        return render(request,"profile-donor.html",locals())

    
class changepwd_donor(View):
    def get(self,request):
        form=MyPasswordChangeForm(request.user)
        return render(request,'changepwd-donor.html',locals())
    def post(self,request):
        form=MyPasswordChangeForm(request.user,request.POST)
        if not request.user.is_authenticated:
            return redirect('/login-donor')
        old=request.POST['old_password']
        newpass=request.POST['new_password1']
        confirmpass=request.POST['new_password2']
        try:
            if old=="" or newpass=="" or confirmpass=="":
                messages.warning(request,"Enter Old Password and New Passwords")
                return redirect("/changepwd-donor") 
            
            if newpass==confirmpass:
                user=User.objects.get(id=request.user.id)
                if user.check_password(old):
                    user.set_password(newpass)
                    user.save()
                    messages.success(request,'Password changed successfully....')
                else:
                    messages.warning(request,'Old Password Not Matching...')
            else:
                messages.warning(request,'New Password and Confirm Password Not Matched...')
        except:
            messages.warning(request,'Failed to Change Password..')
        return render(request, "changepwd-donor.html",locals())


# volunteer dashboard

def index_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-volunteer')
    user=request.user
    volunteer=Volunteer.objects.get(user=user)
    totalCollectionReq=Donation.objects.filter(volunteer=volunteer,status="Volunteer Allocated").count()
    totalRecDonation=Donation.objects.filter(volunteer=volunteer,status="Donation Received").count()
    totalNotRecDonation=Donation.objects.filter(volunteer=volunteer,status="Donation NotReceived").count()
    totalDonationDelivered=Donation.objects.filter(volunteer=volunteer,status="Donation Delivered Successfully").count()

    return render(request, "index-volunteer.html",locals())


def collection_req(request):
    if not request.user.is_authenticated:
        return redirect('/login-volunteer')
    user=request.user
    volunteer=Volunteer.objects.get(user=user)
    donation=Donation.objects.filter(volunteer=volunteer,status="Volunteer Allocated")
    return render(request, "collection-req.html",locals())


def donationrec_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-volunteer')
    user=request.user
    volunteer=Volunteer.objects.get(user=user)
    donation=Donation.objects.filter(volunteer=volunteer,status="Donation Received")
    return render(request, "donationrec-volunteer.html",locals())


def donationnotrec_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-volunteer')
    user=request.user
    volunteer=Volunteer.objects.get(user=user)
    donation=Donation.objects.filter(volunteer=volunteer,status="Donation NotReceived")
    return render(request, "donationnotrec-volunteer.html",locals())


def donationdelivered_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-volunteer')
    user=request.user
    volunteer=Volunteer.objects.get(user=user)
    donation=Donation.objects.filter(volunteer=volunteer,status="Donation Delivered Successfully")
    return render(request, "donationdelivered-volunteer.html",locals())


class profile_volunteer(View):
    def get(self,request):
        form1=UserForm()
        form2=VolunteerSignupForm()
        user=request.user
        volunteer=Volunteer.objects.get(user=user)
        return render(request, "profile-volunteer.html",locals())
    
    def post(self,request):
        if not request.user.is_authenticated:
            return redirect('/login-volunteer')
        form1=UserForm(request.POST)
        form2=VolunteerSignupForm(request.POST)

        user=request.user
        volunteer=Volunteer.objects.get(user=user)
        
        fn=request.POST['firstname']
        ln=request.POST['lastname']
        contact=request.POST['contact']
        address=request.POST['address']
        aboutme=request.POST['aboutme']

        volunteer.user.first_name=fn
        volunteer.user.last_name=ln
        volunteer.contact=contact
        volunteer.address=address
        volunteer.aboutme=aboutme

        try:
            userpic=request.FILES['userpic']
            volunteer.userpic=userpic
            idpic=request.FILES['idpic']
            volunteer.idpic=idpic
            volunteer.save()
            volunteer.user.save()
            messages.success(request,"Profile Updated Successfully")
        except Exception as e:
            messages.warning(request,"Profile Update Failed"+e)
        return render(request, "profile-volunteer.html",locals())


class changepwd_volunteer(View):
    def get(self,request):
        form=MyPasswordChangeForm(request.user)
        return render(request,'changepwd-volunteer.html',locals())
    
    def post(self,request):
        form=MyPasswordChangeForm(request.user,request.POST)
        if not request.user.is_authenticated:
            return redirect('/login-volunteer')
        old=request.POST['old_password']
        newpass=request.POST['new_password1']
        confirmpass=request.POST['new_password2']
        try:
            if old=="" or newpass=="" or confirmpass=="":
                messages.warning(request,"Please enter Old Password and New Passwords")
                return redirect("/changepwd-volunteer")
            
            if newpass==confirmpass:
                user=User.objects.get(id=request.user.id)
                if user.check_password(old):
                    user.set_password(newpass)
                    user.save()
                    messages.success(request,'Password changed successfully....')
                else:
                    messages.warning(request,'Old Password Not Matching...')
            else:
                messages.warning(request,'New Password and Confirm Password Not Matched...')
        except:
            messages.warning(request,'Failed to Change Password..')
        return render(request, "changepwd-volunteer.html",locals())


# view details

def donationdetail_donor(request, pid):
    if not request.user.is_authenticated:
        return redirect('/login-donor')
    donation=Donation.objects.get(id=pid)
    return render(request, "donationdetail-donor.html",locals())


class donationcollection_detail(View):
    def get(self,request,pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        donation=Donation.objects.get(id=pid)
        return render(request, "donationcollection-detail.html",locals())
     
    def post(self,request,pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        donation=Donation.objects.get(id=pid)
        status=request.POST['status']
        volunteerremark=request.POST['volunteerremark']
        try:
            donation.status=status
            donation.volunteerremark=volunteerremark
            donation.updationdate=date.today()
            donation.save()
            messages.success(request,"Volunteer Status and Remark Updated Successfully...")
        except:
            messages.warning(request,"Failed to update Volunteer Status and Remark")
        return render(request,"donationcollection-detail.html",locals())


# class donationrec_detail(View):
#     def get(self,request,pid):
#         if not request.user.is_authenticated:
#             return redirect('/login-admin')
#         donation=Donation.objects.get(id=pid)
#         return render(request, "donationrec-detail.html",locals())

#     def post(self,request,pid):
#         if not request.user.is_authenticated:
#             return redirect('/login-admin')
#         donation=Donation.objects.get(id=pid)
#         status=request.POST['status']
#         deliverypic=request.FILES['deliverypic']
#         try:
#             donation.status=status
#             print("123")
#             donation.updationdate=date.today()
#             print("456")
#             donation.save()
#             print("789")
#             Gallery.objects.create(donation=donation,deliverypic=deliverypic)
#             messages.success(request,"Donation Delivered Successfully")
#         except:
#             messages.warning(request,"Donation Delivered Failed")
#         return render(request, "donationrec-detail.html",locals())
    
class donationrec_detail(View):
    def get(self, request, pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        donation = Donation.objects.get(id=pid)
        return render(request, "donationrec-detail.html", locals())

    def post(self, request, pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        
        donation = Donation.objects.get(id=pid)
        status = request.POST.get('status')
        deliverypic = request.FILES.get('deliverypic')

        if not deliverypic:
            messages.warning(request, "Please upload a delivery picture.")
            return render(request, "donationrec-detail.html", locals())

        try:
            donation.status = status
            donation.updationdate = date.today()

            # Debugging outputs
            print(f"donationname: {donation.donationname}")
            print(f"donor: {donation.donor}, volunteer: {donation.volunteer}")
            print(f"status: {status}")
            
            donation.save()
            print("Donation saved successfully")

            Gallery.objects.create(donation=donation, deliverypic=deliverypic)
            messages.success(request, "Donation Delivered Successfully")
        except Exception as e:
            print(f"Error during donation save: {e}")
            messages.warning(request, "Donation Delivered Failed")
        
        return render(request, "donationrec-detail.html", locals())


def payment(request):
    # Razorpay client instance with API key and secret
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Payment details
    amount = 50000  # Amount in paisa (500.00 INR)
    currency = 'INR'
    receipt = 'order_rcptid_11'

    try:
        # Create an order using Razorpay API
        order = client.order.create({
            'amount': amount,
            'currency': currency,
            'receipt': receipt,
            'payment_capture': '1'
        })
    except Exception as e:
        # Log or print exception for debugging
        print(f"Exception creating Razorpay order: {e}")
        return render(request, 'payment_failure.html', {'error': 'Failed to create payment order. Please try again.'})

    # Pass order details to the template
    context = {
        'razorpay_order_id': order['id'],
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'amount': amount
    }
    return render(request, 'payment.html', context)

@csrf_exempt
def payment_success(request):
    # Retrieve payment details from request
    razorpay_order_id = request.POST.get('razorpay_order_id')
    razorpay_payment_id = request.POST.get('razorpay_payment_id')
    razorpay_signature = request.POST.get('razorpay_signature')

    if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
        return render(request, 'payment_failure.html', {'error': 'Incomplete payment details received.'})

    try:
        # Save payment instance without associating with a donor
        payment = Payment(
            amount=50000,  # Example amount (in paisa)
            razorpay_order_id=razorpay_order_id,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature,
            status='successful'  # Set based on actual payment status
        )
        payment.save()
    except Exception as e:
        # Log or print exception for debugging
        print(f"Exception saving payment details: {e}")
        return render(request, 'payment_failure.html', {'error': 'Failed to save payment details. Please try again.'})

    return render(request, 'payment_success.html', {'message': 'Payment successful! Thank you for your donation.'})

def payment_failure(request):
    return render(request, 'payment_failure.html', {'error': 'Payment failed. Please try again.'})
