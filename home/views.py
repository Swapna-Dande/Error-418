from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Profile,User
from django.contrib.auth import authenticate,login,logout
from .models import Patient,Doctor,Record
from django.http import HttpResponseRedirect
from django.shortcuts import render
from pdf2image import convert_from_path
import cv2
import pytesseract
from transformers import pipeline
import requests
question_answerer = pipeline("question-answering", model='distilbert-base-cased-distilled-squad')


def register(request):
    if request.method == 'POST':
        uname = request.POST['tel']
        pwd = request.POST['pwd']
        role = request.POST['role']
        print(uname)
        print(pwd)
        print(role)
        # User Creation
        usr = User.objects.create_user(username=uname,password=pwd)
        usr.save()
        pf = Profile(user = usr,phone_number = uname,role = role)
        pf.save()
        print(f"This is pf {pf}")
        return redirect('/login')
        # return HttpResponse("User Registered")
    
    return render(request,'register.html')


def login_user(request):
    if request.method == "POST":
        name = request.POST['uname']
        pwd = request.POST['pwd']
        user = authenticate(request,username=name,password = pwd)
        if user is not None:
            login(request,user)
            return redirect("/home")
        else:
            return redirect('/register')
    return render(request,"login.html")    

def test(request):
    print(request.user)
    usr = request.user
    pf = Profile.objects.get(user = usr)
    print(pf)
    print(pf.role)
    return HttpResponse("request.user")

def home(request):
    if request.user.is_authenticated:
        if Profile.objects.get(user = request.user).role == 1:  #Patient
            print("This is patient")
            return render(request,"patient.html")
        elif Profile.objects.get(user = request.user).role == 2: #Doctor
            print("This is doctor")
            return render(request,"doctor.html")
        else: #Management
            print("This is hospital")
            return render(request,"hospital.html")
    else:
        return render(request,"login.html")

def logout_user(request):
    logout(request)
    return redirect('/')


def record(request):
    # if request.method == "POST":
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         handle_uploaded_file(request.FILES['file'])
    #         return HttpResponseRedirect('/success/url/')
    # else:
    #     form = UploadFileForm()
    # return render(request, 'upload.html', {'form': form})
    # pass
    # usr = request.user
    # Pf = Profile.objects.get(user=usr)
    # Pat = Patient.objects.get(profile=Pf)
    # print(Pat)    
    filename = Record.objects.all()[:1].get()
    # print(f"this is path {filename.path}")
    pdfs = f"media/uploads/pd_1.pdf"

    # Convert into Images
    pages = convert_from_path(pdfs, 350)

    i = 0
    for page in pages:
        image_name = "Page_" + str(i) + ".jpg"  
        page.save(image_name, "JPEG")
        i = i+1 

    i = i-1

    context = ''
    op = []
    for x in range(i+1):
        img_cv = cv2.imread(f'Page_{x}.jpg')
        img_rgb = cv2.cvtColor(img_cv,cv2.COLOR_BGR2RGB)
        context = pytesseract.image_to_string(img_rgb)
        op.append(context)

    cnt = ''
    for i in op:
        cnt+=i
    print(cnt)
    API_URL = "https://api-inference.huggingface.co/models/distilbert-base-cased-distilled-squad"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
        
    name_output = query({
        "inputs": {
            "question": "What's the patient's name?",
            "context": cnt,
        },
    })
    age_output = query({
        "inputs": {
            "question": "What's the patient's date of birth?",
            "context": cnt,
        },
    })
    phone_output = query({
        "inputs": {
            "question": "What's the patient's phone number?",
            "context": cnt,
        },
    })
    medical_output = query({
        "inputs": {
            "question": "What's the patient's medical problem?",
            "context": cnt,
        },
    })
    doa_output = query({
        "inputs": {
            "question": "What's the patient's date of admission?",
            "context": cnt,
        },
    })

    # output = {
    #     'name' : name_output,
    #     'dob' : age_output,
    #     'phone' : phone_output,
    #     'problems' : medical_output,
    #     'doa':doa_output,
    # }

    output = {
        'name' : name_output['answer'],
        'dob' : age_output['answer'],
        'phone' : phone_output['answer'],
        'problems' : medical_output['answer'],
        'doa':doa_output['answer']
    }
    print(output)
    
    pdfq = Record.objects.all()[:1].get()
    print(type(pdfq))
    return HttpResponse("PDF")

    
