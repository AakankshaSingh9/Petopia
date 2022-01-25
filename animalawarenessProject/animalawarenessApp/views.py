from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from selenium import webdriver
import webbrowser
import csv
from .forms import Registration
from .models import UserRegister, Userfeedback, Userdonation
from django.contrib.auth import login, authenticate, logout
import razorpay 
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
# from webdriver_manager.chrome import ChromeDriverManager


# Create your views here.
def indexview(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phno = request.POST['phno']
        subject = request.POST['subject']
        msg = request.POST['message']
        reg = Userfeedback(name=name, email=email, phno=phno, subject=subject, msg=msg)
        reg.save()
        give = "Thanks {} for your feedback".format(name)
        return render(request, 'index.html', {"status":give})
    return render(request, 'index.html')



def check_user(request):
    if request.method=="POST":
        un = request.POST["username"]
        check = UserRegister.objects.filter(username=un)
        if len(check)==1:
            return HttpResponse("Exists")
        else:
            return HttpResponse("Not Exists")


def signin(request):
    if request.method=="POST":
        un = request.POST["username"]
        pwd = request.POST["password"]
        # user = authenticate(username = un, password = pwd)
        check = UserRegister.objects.filter(email=un, password=pwd)
        
        if len(check)==1:
            values = UserRegister.objects.filter(email=un)
            return render(request, 'UserDashboard.html', {"status": values[0]})
        # if user:
        #     login(request, user)
        #     if user.is_superuser:
        #         return HttpResponseRedirect("/admin")
        #     if user.is_UserRegister:
        #         return HttpResponseRedirect("UserDashboard.html")
        else:
            return render(request, 'Signin.html', {"error":"Invalid Username or Password"})
        
    return render(request, 'Signin.html')

def registration(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        reg = UserRegister(name=name, email=email, password=password)
        reg.save()
        give = "{} You have been successfully registered".format(name)
        return render(request, 'Signup.html', {"status":give})
    else:
        return render(request, 'Signup.html')

def userdashboard(request):
    # name = UserRegister.objects.filter(request.name)
    data = UserRegister()
    msg = "{}".format(data)
    return render(request, 'UserDashboard.html', {"msg":msg})



def userprogramview(request):
    return render(request, 'UserProgramDashboard.html')

def userorganisationview(request):
    return render(request, 'UserOrganisationDashboard.html')




# authorize razorpay client with API Keys.

razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET)) 

def userdonationview(request):
    if request.method == "POST":
        name = request.POST['name']
        paymode = request.POST['paymode']
        amount = request.POST['amount']
        reg = Userdonation(name=name, paymode=paymode, amount=amount)
        reg.save()
        give = "Thank You {} for supporting us!!! You are Awesome".format(name)
        currency = 'INR' 
        # Create a Razorpay Order 
        razorpay_order = razorpay_client.order.create(dict(amount=10000,currency=currency, payment_capture='0')) 
        # order id of newly created order. 
        razorpay_order_id = razorpay_order['id'] 
        callback_url = 'paymenthandler/' 
        # we need to pass these details to frontend. 
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = 10000
        context['currency'] = currency
        context['callback_url'] = callback_url  
        context['msg']=give
        # we need to csrf_exempt this url as
        # POST request will be made by Razorpay
        # and it won't have the csrf token.
        return render(request, 'UserDonationDashboard.html', context=context)
    return render(request, 'UserDonationDashboard.html')



@csrf_exempt

def paymenthandler(request): 
    # only accept POST request. 
    if request.method == "POST":
        try :
            # get the required parameters from post request. 
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '') 
            signature = request.POST.get('razorpay_signature', '')
            params_dict = { 'razorpay_order_id': razorpay_order_id,
                            'razorpay_payment_id': payment_id,
                            'razorpay_signature': signature 
                          } 
            # verify the payment signature. 
            result = razorpay_client.utility.verify_payment_signature(params_dict) 
            if result is None: 
                amount = 10000
        finally:
            pass



def userfeedbackview(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phno = request.POST['phno']
        subject = request.POST['subject']
        msg = request.POST['message']
        reg = Userfeedback(name=name, email=email, phno=phno, subject=subject, msg=msg)
        reg.save()
        give = "Thanks {} for your feedback".format(name)
        return render(request, 'UserFeedbackDashboard.html', {"status":give})
    return render(request, 'UserFeedbackDashboard.html')



def get_results(search_term):
    url = "https://www.google.com/search?q=" + search_term + "&start"
    # browser = webdriver.Chrome(executable_path=r"D:\Python\chromedriver\chromedriver.exe")
    # browser = webdriver.Chrome(ChromeDriverManager().install())
    browser = webdriver.Chrome(executable_path=r"D:\Python\petopia\chromedriver.exe")
    browser.get(url)
    try:
        links = browser.find_elements_by_xpath("//div[@class='eqAnXb']//div//a")
    except:
        links = browser.find_elements_by_xpath("//div//a")
    results = []
    for link in links:
        href = link.get_attribute("href")
        print(href)
        results.append(href)
    browser.close()
    return results
    

def usersearchview(request): 
    if request.method == "POST":
        if request.POST.get('petsubmit'):
            result = get_results("Petshop near me")
            # content = {}
            with open("C:/PetopiaProject/animalawarenessProject/animalawarenessApp/templates/searchresult_petshop2.html", "w") as php_file:
                for element in result:
                    if element is not None:
                        php_file.write(f"{element} + '\n'")
                print("File created successfully !!!")  
            return render(request, 'UserSearchDashboard.html', {"result":result})
        elif request.POST.get('vetsubmit'):
            result = get_results("Veterinarian near me")
            content = {}
            with open("C:/PetopiaProject/animalawarenessProject/animalawarenessApp/templates/searchresult_veterinarian.html", "w") as php_file:
                for element in result:
                    if element is not None:
                        php_file.write(f"{element} + '\n'")
                print("File created successfully !!!")  
            return render(request, 'UserSearchDashboard.html', {"result":result})
        else:
          return render(request, 'UserSearchDashboard.html')
    return render(request, 'UserSearchDashboard.html')
        
          
    

               
def admindashboard(request):
    user = UserRegister.objects.all()
    feedback = Userfeedback.objects.all()
    donation = Userdonation.objects.all()
    return render(request, 'AdminDashboard.html', {"user":user, "feedback":feedback, "donation":donation})
#  if request.method == "POST":
#         if request.POST == 'petsubmit':
#     result = get_results("Petshop near me")
#     # content = {
#     #     'ids': [['id'] for j in result]
#     # }
#     print("Result Type is -----------",type(result))
#     content = {}
#     # for index, value in enumerate(result):
#     #     content[index] = value
#     # print("Result is ------------------", result)
#     # print("Content is ------------------", content)
#     # content['id'] = result
#     # content['r'] = result
#     with open("C:/PetopiaProject/animalawarenessProject/animalawarenessApp/templates/searchresult_petshop2.html", "w") as php_file:
#         for element in result:
#             if element is not None:
#                 php_file.write(f"{element} + '\n'")
#         print("File created successfully !!!")   
#     # output = "\n".join(result)
#     return render(request, 'UserSearchDashboard.html', {"result":result})
#     # return render(request, 'UserSearchDashboard.html')



#download
def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Email', 'Password'])

    users = UserRegister.objects.all().values_list('id', 'name', 'email', 'password')
    for user in users:
        writer.writerow(user)

    return response

def export_users_csv_feed(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Email', 'Phno', 'Subject', 'Message'])

    feeds = Userfeedback.objects.all().values_list('id', 'name', 'email', 'phno', 'subject', 'msg')
    for feed in feeds:
        writer.writerow(feed)

    return response

def export_users_csv_donate(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Paymode', 'Amount', 'Trn Date'])

    donates = Userdonation.objects.all().values_list('id', 'name', 'paymode', 'amount', 'trn_date')
    for donate in donates:
        writer.writerow(donate)

    return response