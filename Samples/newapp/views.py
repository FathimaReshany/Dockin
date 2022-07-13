import base64

from django.db.models.functions import Lower, Upper
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.db.models import Q

# from .models import login, company, worker, skills, block_request, complaint,user,feedback,vaccancy,vaccancy_skills,vaccancy_request
# Create your views here.
from .models import *
import time, datetime
from django.http import JsonResponse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


media_path="D:\\sample\\Samples\\media\\"


def adm_home(request):
    worker_obj=worker.objects.all().order_by('-id')[:3]
    worker_list=[]
    for i in worker_obj:
        worker_list.append({'name':i.name, 'phone':i.phone, 'email':i.email,'description':i.description,'image':i.image})
    company_obj=company.objects.all().order_by('-id')[:3]
    company_list=[]
    for j in company_obj:
        company_list.append({'name': j.company_name, 'phone': j.phone, 'email': j.email, 'description': j.description,'image':j.image})

    rating_obj=rating.objects.all().order_by('-id')[:4]
    rating_list = []
    for i in rating_obj:
        rr=i.rate
        rated=[]
        for j in range(int(rr)):
            rated.append(j)
        nn=5-int(rr)
        not_rated=[]
        for j in range(nn):
            not_rated.append(j)
        rating_list.append(
            {'rated':rated, 'not_rated':not_rated, 'image':i.USER.image,'name':i.USER.name})

    return render(request,"Admin/home.html",{'data':worker_list,'data2':company_list,'data3':rating_list})


# def worker_home(request):
#     return render(request,"Workers/worker_home.html")


def worker_reg_load(request):
    return render(request,'Worker_registration.html')
def worker_reg_post(request):
    name=request.POST['textfield']
    gender=request.POST['radiobutton']
    dob=request.POST['textfield2']
    district=request.POST['select']
    city=request.POST['textfield3']
    house_name=request.POST['textfield4']
    pin=request.POST['textfield5']
    phone=request.POST['textfield6']
    email=request.POST['textfield7']
    description=request.POST['textarea']
    password=request.POST['textfield8']
    image=request.FILES['file']
    fs=FileSystemStorage()
    fname=time.strftime("%Y%m%d-%H%M%S")+".jpg"
    filename=fs.save(fname, image)
    path=fs.url(filename)

    log_obj=login()
    log_obj.username=email
    log_obj.password=password
    log_obj.logintype='pending'
    log_obj.save()


    worker_obj=worker()
    worker_obj.name=name
    worker_obj.gender=gender
    worker_obj.dob=dob
    worker_obj.district=district
    worker_obj.city=city
    worker_obj.house_name=house_name
    worker_obj.pin=pin
    worker_obj.phone=phone
    worker_obj.email=email
    worker_obj.description=description
    worker_obj.image=path
    worker_obj.LOGIN=log_obj
    worker_obj.save()


    import smtplib
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login("workerapp035@gmail.com", "@workerapp21")
    msg = MIMEMultipart()  # create a message.........."
    message = "Messege from WORKER APP"
    msg['From'] = "workerapp035@gmail.com"
    msg['To'] = email
    msg['Subject'] = "Registered to WORKER APP"
    body = "Username : "+email +"\nPassword : " + str(password)
    msg.attach(MIMEText(body, 'plain'))
    s.send_message(msg)
    return HttpResponse("Registered Successfully")





def company_registration_load(request):
    return render(request,'Company_registration.html')
def company_registration_post(request):
    name=request.POST['name22']
    year=request.POST['textfield10']
    state=request.POST['select']
    district=request.POST['select2']
    city=request.POST['textfield4']
    pin=request.POST['textfield5']
    phone=request.POST['textfield6']
    email=request.POST['textfield7']
    description=request.POST['textarea']
    password=request.POST['textfield8']

    image=request.FILES['file']
    fs=FileSystemStorage()
    fname=time.strftime("%Y%m%d-%H%M%S")+".jpg"
    filename=fs.save(fname, image)
    path=fs.url(filename)


    log_obj=login()
    log_obj.username=email
    log_obj.password=password
    log_obj.logintype='pending'
    log_obj.save()


    compreg_obj=company()
    compreg_obj.company_name=name
    compreg_obj.year=year
    compreg_obj.state=state
    compreg_obj.district=district
    compreg_obj.city=city
    compreg_obj.pin=pin
    compreg_obj.phone=phone
    compreg_obj.email=email
    compreg_obj.description=description
    compreg_obj.image=path
    compreg_obj.LOGIN=log_obj
    compreg_obj.save()


    import smtplib
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login("workerapp035@gmail.com", "@workerapp21")
    msg = MIMEMultipart()  # create a message.........."
    message = "Messege from WORKER APP"
    msg['From'] = "workerapp035@gmail.com"
    msg['To'] = email
    msg['Subject'] = "Registered to WORKER APP"
    body = "Username : "+email +"\nPassword : " + str(password)
    msg.attach(MIMEText(body, 'plain'))
    s.send_message(msg)
    return HttpResponse("Registered Successfully")




def login_load(request):

    return render(request,'Login.html')
def login_post(request):
    username=request.POST['textfield']
    password=request.POST['textfield2']
    log_obj=login.objects.filter(username=username,password=password)
    if log_obj.exists():
        log_obj=log_obj[0]
        type=log_obj.logintype
        if type=="admin":
            # return adm_home(request)
            request.session["lg"] = "yes"
            return HttpResponse("<script>alert('successfully login');window.location='/newapp/adm_home/'</script>")
        elif type=="company":
            company_obj=company.objects.get(LOGIN=log_obj)
            request.session['company_id']=company_obj.id
            request.session["lg"] = "yes"
            # return comp_home(request)
            return HttpResponse("<script>alert('successfully login');window.location='/newapp/comp_home/'</script>")
        elif type=="worker":
            request.session["lg"] = "yes"
            worker_obj=worker.objects.get(LOGIN=log_obj)
            request.session['worker_id']=worker_obj.id
            # return worker_home(request)
            return HttpResponse("<script>alert('successfully login');window.location='/newapp/worker_home/'</script>")

        elif type=="blocked":
            worker_obj=worker.objects.get(LOGIN=log_obj)
            request.session['worker_id']=worker_obj.id
            return HttpResponse("<script>alert('Sorry you are blocked');window.location='/newapp/login_load/'</script>")


        else:
            return HttpResponse("Invalid user")
    else:
        return HttpResponse("<script>alert('Invalid username or password');window.location='/newapp/login_load/'</script>")


def logout(request):
    request.session["lg"]="no"
    return render(request,'Login.html')


##################ADMIN START

def admin_addskill_load(request):
    if request.session["lg"]== "yes":
        return render(request,'Admin/Add_skill.html')
    else:
        return render(request, 'Login.html')


def admin_addskill_load_post(request):
    skill_name=request.POST['textfield']
    sk=skills()
    sk.skill=skill_name
    sk.save()
    return HttpResponse("OK")



def admin_editskill_load(request,skill_id):
    if request.session["lg"]== "yes":
        skill_obj = skills.objects.get(id=skill_id)
        request.session['skill_id'] = skill_id
        return render(request, 'Admin/Edit_skill.html', {'data': skill_obj})
    else:
        return render(request, 'Login.html')

def admin_editskill_load_post(request):
    skill=request.POST['textfield']
    skill_id=request.session['skill_id']
    skill_obj=skills.objects.get(id=skill_id)
    skill_obj.skill=skill
    skill_obj.save()
    return admin_viewskill_load(request)



def admin_viewskill_load(request):
    if request.session['lg']=="yes":

        view_skill_obj=skills.objects.all()

        return render(request,'Admin/View_skill.html',{'data':view_skill_obj})
    else:
        return render(request, 'Login.html')
def admin_viewskill_load_post(request):
    name=request.POST['textfield']
    view_skill_obj=skills.objects.filter(skill__contains=name)
    return render(request,'Admin/View_skill.html',{'data':view_skill_obj})

def admin_delete_skill(request,skill_id):
    skill_obj=skills.objects.get(id=skill_id)
    skill_obj.delete()
    return admin_viewskill_load(request)



def admin_view_registered_companies_and_approval(request):
    if request.session['lg'] == "yes":
        comp_obj=company.objects.filter(LOGIN__logintype='pending')
        return render(request,'Admin/View_registered_comp&approval.html', {'data':comp_obj})
    else:
        return render(request,'Login.html')
def admin_viewregistered_companies_and_approval_post(request):
    name=request.POST['textfield']
    comp_obj=company.objects.filter(LOGIN__logintype='pending', company_name__contains=name)
    return render(request,'Admin/View_registered_comp&approval.html', {'data':comp_obj})

def admin_approve_company(request,login_id):
    log_obj=login.objects.get(id=login_id)
    log_obj.logintype='company'
    log_obj.save()
    return admin_view_registered_companies_and_approval(request)

def admin_reject_company(request,login_id):
    log_obj=login.objects.get(id=login_id)
    log_obj.logintype='rejected'
    log_obj.save()
    return admin_view_registered_companies_and_approval(request)

def admin_block_company(request,login_id):
    log_obj=login.objects.get(id=login_id)
    log_obj.logintype='blocked'
    log_obj.save()
    return admin_view_approved_companies(request)

def admin_unblock_company(request,login_id):
    log_obj=login.objects.get(id=login_id)
    log_obj.logintype='company'
    log_obj.save()
    return admin_view_approved_companies(request)



def admin_view_approved_companies(request):
    if request.session['lg'] == "yes":
        comp_obj=company.objects.filter(Q(LOGIN__logintype='company')|Q(LOGIN__logintype='blocked'))
        return render(request,'Admin/View_approved_comp.html',{'data':comp_obj})
    else:
        return render(request,'Login.html')
def admin_view_approved_companies_post(request):
    name=request.POST['textfield']
    comp_obj=company.objects.filter(LOGIN__logintype='company',company_name__contains=name)
    return render(request,'Admin/View_approved_comp.html',{'data':comp_obj})
    


def admin_view_rejected_companies(request):
    if request.session['lg'] == "yes":
        comp_obj=company.objects.filter(LOGIN__logintype="rejected")
        return render(request,'Admin/View_rejected_comp.html',{'data':comp_obj})
    else:
        return render(request,'Login.html')
def admin_view_rejected_companies_post(request):
    name=request.POST['textfield']
    comp_obj=company.objects.filter(LOGIN__logintype="rejected",company_name__contains=name)
    return render(request,'Admin/View_rejected_comp.html',{'data':comp_obj})



def admin_view_registered_workers_and_approval(request):
    if request.session['lg'] == "yes":
        worker_obj = worker.objects.filter(LOGIN__logintype='pending')
        return render(request, 'Admin/View_registered_worker&approval.html', {'data': worker_obj})
    else:
        return render(request,'Login.html')
def admin_view_registered_workers_and_approval_post(request):
    name=request.POST['textfield']
    worker_obj = worker.objects.filter(LOGIN__logintype='pending',name__contains=name)
    return render(request, 'Admin/View_registered_worker&approval.html', {'data': worker_obj})


def admin_approve_worker(request,login_id):
    log_obj=login.objects.get(id=login_id)
    log_obj.logintype='worker'
    log_obj.save()
    return admin_view_registered_workers_and_approval(request)

def admin_reject_worker(request,login_id):
    log_obj=login.objects.get(id=login_id)
    log_obj.logintype='rejected'
    log_obj.save()
    return admin_view_registered_workers_and_approval(request)

def admin_block_worker(request,login_id):
    log_obj=login.objects.get(id=login_id)
    log_obj.logintype='blocked'
    log_obj.save()
    return admin_view_approved_worker(request)

def admin_unblock_worker(request,login_id):
    log_obj=login.objects.get(id=login_id)
    log_obj.logintype='worker'
    log_obj.save()
    return admin_view_approved_worker(request)

def admin_view_approved_worker(request):
    if request.session['lg'] == "yes":
        worker_obj=worker.objects.filter(Q(LOGIN__logintype='worker')|Q(LOGIN__logintype='blocked'))
        return render(request,'Admin/View_approved_worker.html',{'data':worker_obj})
    else:
        return render(request,'Login.html')
def admin_view_approved_worker_post(request):
    name=request.POST['textfield']
    worker_obj=worker.objects.filter(LOGIN__logintype='worker',name__contains=name)
    return render(request,'Admin/View_approved_worker.html',{'data':worker_obj})




def admin_view_rejected_worker(request):
    if request.session['lg'] == "yes":
        worker_obj=worker.objects.filter(LOGIN__logintype="rejected")
        return render(request,'Admin/View_rejected_worker.html',{'data':worker_obj})
    else:
        return render(request,'Login.html')
def admin_view_rejected_worker_post(request):
    name=request.POST['textfield']
    worker_obj=worker.objects.filter(LOGIN__logintype="rejected",name__contains=name)
    return render(request,'Admin/View_rejected_worker.html',{'data':worker_obj})





def admin_view_block_request_from_user(request):
    if request.session['lg'] == "yes":
        block_obj=block_request.objects.filter(status="pending")
        return render(request,'Admin/View_block_request.html',{'data':block_obj})
    else:
        return render(request,'Login.html')
def admin_view_block_request_from_user_post(request):
    name=request.POST['textfield']
    block_obj=block_request.objects.filter(WORKER__name__contains=name,status="pending")
    return render(request,'Admin/View_block_request.html',{'data':block_obj})
def admin_block_worker_by_request(request,login_id,request_id):
    log_obj=login.objects.get(id=login_id)
    log_obj.logintype='blocked'
    log_obj.save()
    requst_obj=block_request.objects.get(id=request_id)
    requst_obj.status='blocked'
    requst_obj.save()
    return admin_view_block_request_from_user(request)



def admin_view_complaint_from_user(request):
    if request.session['lg'] == "yes":
        user_log_ids = list(login.objects.filter(logintype='user').values_list('id', flat=True))
        print(user_log_ids)
        res_user_comp = complaint.objects.filter(LOGIN_id__in=user_log_ids)
        res=[]

        for i in res_user_comp:
            lid=i.LOGIN_id
            user_obj=user.objects.get(LOGIN_id=lid)
            d={
                'image':user_obj.image,
                'name':user_obj.name,
                'email':user_obj.email,
                'phone':user_obj.phone,
                'cid':i.id,
                'complaint':i.complaint,
                'date':i.complaint_date,
                'type':i.complaint_type,
                'status':i.status,
                'reply':i.reply,
            }
            res.append(d)


        worker_log_ids = list(login.objects.filter(logintype='worker').values_list('id', flat=True))
        print(worker_log_ids)
        res_worker_comp = complaint.objects.filter(LOGIN_id__in=worker_log_ids)
        for i in res_worker_comp:
            lid=i.LOGIN_id
            worker_obj=worker.objects.get(LOGIN_id=lid)
            d={
                'image':worker_obj.image,
                'name':worker_obj.name,
                'email':worker_obj.email,
                'phone':worker_obj.phone,
                'cid':i.id,
                'complaint':i.complaint,
                'date':i.complaint_date,
                'type':i.complaint_type,
                'status':i.status,
                'reply':i.reply,
            }
            res.append(d)
        print(res)
        return render(request,'Admin/View_complaint.html', {'data':res})
    else:
        return render(request,'Login.html')

def admin_view_complaint_from_user_post(request):
    fromdate=request.POST['textfield']
    todate=request.POST['textfield2']
    user_log_ids = list(login.objects.filter(logintype='user').values_list('id', flat=True))
    print(user_log_ids)
    res_user_comp = complaint.objects.filter(complaint_date__range=(fromdate,todate),LOGIN_id__in=user_log_ids)
    res=[]

    for i in res_user_comp:
        lid=i.LOGIN_id
        user_obj=user.objects.get(LOGIN_id=lid)
        d={
            'image':user_obj.image,
            'name':user_obj.name,
            'email':user_obj.email,
            'phone':user_obj.phone,
            'cid':i.id,
            'complaint':i.complaint,
            'date':i.complaint_date,
            'type':i.complaint_type,
            'status':i.status,
            'reply':i.reply,
        }
        res.append(d)

    worker_log_ids = list(login.objects.filter(logintype='worker').values_list('id', flat=True))
    print(worker_log_ids)
    res_worker_comp = complaint.objects.filter(complaint_date__range=(fromdate,todate),LOGIN_id__in=worker_log_ids)
    for i in res_worker_comp:
        lid=i.LOGIN_id
        worker_obj=worker.objects.get(LOGIN_id=lid)
        d={
            'image':worker_obj.image,
            'name':worker_obj.name,
            'email':worker_obj.email,
            'phone':worker_obj.phone,
            'cid':i.id,
            'complaint':i.complaint,
            'date':i.complaint_date,
            'type':i.complaint_type,
            'status':i.status,
            'reply':i.reply,
        }
        res.append(d)
    print(res)

    return render(request,'Admin/View_complaint.html', {'data':res})




def admin_send_reply(request,complaint_id):
    if request.session['lg'] == "yes":
        reply_obj=complaint.objects.get(id=complaint_id)
        request.session['complaint_id']=complaint_id
        return render(request,'Admin/Send_reply.html',{'data':reply_obj})
    else:
        return render(request,'Login.html')
def admin_send_reply_post(request):
    reply=request.POST['textarea']
    complaint_id=request.session['complaint_id']
    reply_obj=complaint.objects.get(id=complaint_id)
    reply_obj.reply=reply
    reply_obj.status="replied"
    reply_obj.save()
    return admin_view_complaint_from_user(request)




def admin_view_feedback_worker(request):
    if request.session['lg'] == "yes":
        worker_log_ids = list(login.objects.filter(logintype='worker').values_list('id', flat=True))
        print(worker_log_ids)
        res_worker_feed = feedback.objects.filter(TO_ID_id__in=worker_log_ids)
        res=[]

        for i in res_worker_feed:
            logid_from=i.FROM_ID
            user_obj=user.objects.get(LOGIN=logid_from)
            logid_to=i.TO_ID
            worker_obj=worker.objects.get(LOGIN=logid_to)
            d={
            'uname':user_obj.name,
            'uimage':user_obj.image,
            'uphone':user_obj.phone,
            'uemail':user_obj.email,
            'wname':worker_obj.name,
            'wimage':worker_obj.image,
            'wphone':worker_obj.phone,
            'wemail':worker_obj.email,
            'feedback':i.feedback,
            'feedback_date':i.feedback_date,


            }
            res.append(d)
        return render(request,'Admin/View_feedback_worker.html',{'data':res})
    else:
        return render(request,'Login.html')
def admin_view_feedback_worker_post(request):
    fromdate = request.POST['textfield']
    todate = request.POST['textfield2']
    worker_log_ids = list(login.objects.filter(logintype='worker').values_list('id', flat=True))
    print(worker_log_ids)
    res_worker_feed = feedback.objects.filter(feedback_date__range=(fromdate,todate),TO_ID_id__in=worker_log_ids)
    res=[]

    for i in res_worker_feed:
        logid_from=i.FROM_ID
        user_obj=user.objects.get(LOGIN=logid_from)
        logid_to=i.TO_ID
        worker_obj=worker.objects.get(LOGIN=logid_to)
        d={
        'uname':user_obj.name,
        'uimage':user_obj.image,
        'uphone':user_obj.phone,
        'uemail':user_obj.email,
        'wname':worker_obj.name,
        'wimage':worker_obj.image,
        'wphone':worker_obj.phone,
        'wemail':worker_obj.email,
        'feedback':i.feedback,
        'feedback_date':i.feedback_date,


        }
        res.append(d)
    return render(request,'Admin/View_feedback_worker.html',{'data':res})




def admin_view_feedback_company(request):
    if request.session['lg'] == "yes":
        company_log_ids = list(login.objects.filter(logintype='company').values_list('id', flat=True))
        print(company_log_ids)
        res_company_feed = feedback.objects.filter(TO_ID_id__in=company_log_ids)
        res=[]

        for i in res_company_feed:
            logid_from=i.FROM_ID
            worker_obj=worker.objects.get(LOGIN=logid_from)
            logid_to=i.TO_ID
            company_obj=company.objects.get(LOGIN=logid_to)
            d={
            'wname':worker_obj.name,
            'wimage':worker_obj.image,
            'wphone':worker_obj.phone,
            'wemail':worker_obj.email,
            'cname':company_obj.company_name,
            'cimage':company_obj.image,
            'cphone':company_obj.phone,
            'cemail':company_obj.email,
            'feedback':i.feedback,
            'feedback_date':i.feedback_date,


            }
            res.append(d)

        return render(request,'Admin/View_feedback_company.html',{'data':res})
    else:
        return render(request,'Login.html')
def admin_view_feedback_company_post(request):
    fromdate = request.POST['textfield']
    todate = request.POST['textfield2']
    company_log_ids = list(login.objects.filter(logintype='company').values_list('id', flat=True))
    print(company_log_ids)
    res_company_feed = feedback.objects.filter(feedback_date__range=(fromdate,todate),TO_ID_id__in=company_log_ids)
    res=[]

    for i in res_company_feed:
        logid_from=i.FROM_ID
        worker_obj=worker.objects.get(LOGIN=logid_from)
        logid_to=i.TO_ID
        company_obj=company.objects.get(LOGIN=logid_to)
        d={
        'wname':worker_obj.name,
        'wimage':worker_obj.image,
        'wphone':worker_obj.phone,
        'wemail':worker_obj.email,
        'cname':company_obj.company_name,
        'cimage':company_obj.image,
        'cphone':company_obj.phone,
        'cemail':company_obj.email,
        'feedback':i.feedback,
        'feedback_date':i.feedback_date,


        }
        res.append(d)

    return render(request,'Admin/View_feedback_company.html',{'data':res})


##################ADMIN END


########COMPANY START
def comp_home(request):

    c_id = request.session['company_id']
    comp_obj = company.objects.get(id=c_id)
    vaccancy_request_obj = vaccancy_request.objects.filter(VACCANCY__COMPANY_id=c_id).order_by('-id')[:3]
    vaccancy_list = []
    for i in vaccancy_request_obj:
        vaccancy_list.append({'image': i.WORKER.image, 'title': i.VACCANCY.title, 'name': i.WORKER.name, 'phone': i.WORKER.phone,
                              'email': i.WORKER.email, 'date': i.vaccancy_request_date})
    feed_obj = feedback.objects.filter(TO_ID=comp_obj.LOGIN).order_by('-id')[:3]
    print("ddddddddddd ", feed_obj)
    feed_list = []
    for i in feed_obj:
        worker_obj = worker.objects.get(LOGIN=i.FROM_ID)
        feed_list.append(
            {'name': worker_obj.name, 'image': worker_obj.image, 'phone': worker_obj.phone, 'email': worker_obj.email,
             'feedback': i.feedback, 'date': i.feedback_date})

    rating_obj = rating.objects.all().order_by('-id')[:4]
    rating_list = []
    for i in rating_obj:
        rr = i.rate
        rated = []
        for j in range(int(rr)):
            rated.append(j)
        nn = 5 - int(rr)
        not_rated = []
        for j in range(nn):
            not_rated.append(j)
        rating_list.append(
            {'rated': rated, 'not_rated': not_rated, 'image': i.USER.image, 'name': i.USER.name})


    return render(request, "Company/home.html", {'data': vaccancy_list, 'data2': feed_list,'data3':rating_list})


def company_view_profile(request):
    if request.session['lg'] == "yes":
        cid=request.session['company_id']
        res=company.objects.get(id=cid)
        return render(request,'Company/View_profile.html',{'data':res})
    else:
        return render(request,'Login.html')
def company_view_profile_post(request):
    return render(request,'Company/View_profile.html')

def company_edit_profile(request):
    if request.session['lg'] == "yes":
        comp_id=request.session['company_id']
        res=company.objects.get(id=comp_id)
        return render(request,'Company/Edit_profile.html',{'data':res})
    else:
        return render(request,'Login.html')
def company_edit_profile_post(request):
    company_name=request.POST['textfield']
    year=request.POST['textfield8']
    state=request.POST['select']
    district=request.POST['select1']
    city=request.POST['textfield3']
    pin=request.POST['textfield5']
    phone=request.POST['textfield6']
    email=request.POST['textfield7']
    description=request.POST['textarea']

    company_id=request.session['company_id']
    
    if 'file' in request.FILES:

        image=request.FILES['file']
        fs=FileSystemStorage()
        fname=time.strftime("%Y%m%d-%H%M%S")+".jpg"
        filename=fs.save(fname, image)
        path=fs.url(filename)
 
        comp_obj=company.objects.filter(id=company_id).update(company_name=company_name,year=year,state=state,district=district,
            city=city,pin=pin,phone=phone,email=email,description=description,image=path)
    else:
         comp_obj=company.objects.filter(id=company_id).update(company_name=company_name,year=year,state=state,district=district,
            city=city,pin=pin,phone=phone,email=email,description=description)
  

   
    
    
    return company_view_profile(request)

def add_vaccancy(request):
    if request.session['lg'] == "yes":
        return render(request,'Company/Add_vaccancy.html')
    else:
        return render(request,'Login.html')
def add_vaccancy_post(request):
    vaccancy_name=request.POST['textfield']
    description=request.POST['textfield8']
    company_id=request.session["company_id"]
    apply_before=request.POST['textfield2']

    vaccancy_obj=vaccancy()
    vaccancy_obj.title=vaccancy_name
    vaccancy_obj.description=description
    vaccancy_obj.date=apply_before
    vaccancy_obj.COMPANY_id=company_id
    vaccancy_obj.save()
    return add_vaccancy(request)


def view_vaccancy(request):
    if request.session['lg'] == "yes":
        cid=request.session['company_id']
        res=vaccancy.objects.filter(COMPANY=cid)

        return render(request,'Company/View_vaccancy.html',{'data':res})
    else:
        return render(request,'Login.html')
def view_vaccancy_post(request):
    cid=request.session['company_id']
    tit=request.POST['title']
    res=vaccancy.objects.filter(COMPANY=cid,title__contains=tit)
    return render(request,'Company/View_vaccancy.html',{'data':res})

def company_edit_view_vaccancy(request,vaccancy_id):
    if request.session['lg'] == "yes":
        vaccancy_obj=vaccancy.objects.get(id=vaccancy_id)

        return render(request,'Company/Edit_vaccancy.html',{'data':vaccancy_obj,'vaccancy_id':vaccancy_id})
    else:
        return render(request,'Login.html')
def company_edit_view_vaccancy_post(request):

    title=request.POST['textfield']
    description=request.POST['textfield8']
    date=request.POST['textfield2']
    vaccancy_id=request.POST['vid']
    vaccancy_obj=vaccancy.objects.filter(id=vaccancy_id).update(title=title,description=description,date=date)
    return view_vaccancy(request)


def company_delete_vaccancy(request,vaccancy_id):
    vaccancy_obj=vaccancy.objects.get(id=vaccancy_id)
    vaccancy_obj.delete()
    return view_vaccancy(request)



def skill_management(request,vaccancy_id):
    if request.session['lg'] == "yes":
        skill_obj=skills.objects.exclude(id__in=(vaccancy_skills.objects.filter(VACCANCY=vaccancy_id).values_list('SKILLS',flat=True)))
        vacancy_skill_obj=vaccancy_skills.objects.filter(VACCANCY=vaccancy_id)
        return render(request,'Company/skill_management.html',{'data':skill_obj,'vaccancy_skill':vacancy_skill_obj,'vaccancy_id':vaccancy_id})
    else:
        return render(request,'Login.html')
def skill_management_post(request):
    vid=request.POST['vid']
    skill=request.POST['select']

    vaccancy_skill_obj=vaccancy_skills()
    vaccancy_skill_obj.SKILLS_id=skill
    vaccancy_skill_obj.VACCANCY_id=vid
    vaccancy_skill_obj.save()

    return skill_management(request,vid)


def company_delete_skill(request,vaccancy_skill_id,vid):
    skill_obj=vaccancy_skills.objects.get(id=vaccancy_skill_id)
    skill_obj.delete()
    return skill_management(request,vid)



def view_vaccancy_request_from_user(request):
    if request.session['lg'] == "yes":
        cid=request.session['company_id']
        vaccancy_req_obj=vaccancy_request.objects.filter(VACCANCY__COMPANY_id=cid,status='pending')
        vaccancy_obj=vaccancy.objects.filter(COMPANY_id=cid)
        return render(request,'Company/View_vaccancy_request.html',{'data':vaccancy_req_obj,'vaccancy_obj':vaccancy_obj})
    else:
        return render(request,'Login.html')
def view_vaccancy_request_from_user_post(request):
    vaccancyid=request.POST['select']
    cid=request.session['company_id']
    vaccancy_req_obj=vaccancy_request.objects.filter(VACCANCY_id=vaccancyid,status='pending')
    vaccancy_obj=vaccancy.objects.filter(COMPANY_id=cid)
    return render(request,'Company/View_vaccancy_request.html',{'data':vaccancy_req_obj,'vaccancy_obj':vaccancy_obj})

def view_vaccancy_request_from_user2(request,wid,reqid):
    if request.session['lg'] == "yes":
        worker_obj=worker.objects.get(id=wid)
        skill_obj=worker_skill.objects.filter(WORKER_id=wid)
        works_obj=works.objects.filter(WORKER_SKILL__WORKER_id=wid)
        resume_obj=worker_resume.objects.filter(WORKER_id=wid)
        if resume_obj.exists():
            resume_obj=resume_obj[0]
            resume_path=resume_obj.resume_path
        else:
            resume_path=" "
        return render(request,'Company/View_vaccancy_request2.html',{'data':worker_obj,'skill_obj':skill_obj,'works_obj':works_obj,'reqid':reqid, 'resume_path': resume_path})
    else:
        return render(request,'Login.html')
def view_vaccancy_request_from_user2_post(request):
    btn=request.POST['Submit']
    requestid=request.POST['reqid']

    if btn=="Accept":
        vaccancy_req_obj=vaccancy_request.objects.filter(id=requestid).update(status='approved')
    else:
        vaccancy_req_obj=vaccancy_request.objects.filter(id=requestid).update(status='rejected')

    return view_vaccancy_request_from_user(request)

def view_approved_vaccancy(request):
    if request.session['lg'] == "yes":
        cid=request.session['company_id']
        vaccancy_req_obj=vaccancy_request.objects.filter(VACCANCY__COMPANY_id=cid,status='approved')
        vaccancy_obj=vaccancy.objects.filter(COMPANY_id=cid)
        return render(request,'Company/View_approved_vaccancy.html',{'data':vaccancy_req_obj,'vaccancy_obj':vaccancy_obj})
    else:
        return render(request,'Login.html')
    
def view_approved_vaccancy_post(request):
    vaccancyid=request.POST['select']
    cid=request.session['company_id']
    vaccancy_req_obj=vaccancy_request.objects.filter(VACCANCY_id=vaccancyid,status='approved')
    vaccancy_obj=vaccancy.objects.filter(COMPANY_id=cid)
    return render(request,'Company/View_approved_vaccancy.html',{'data':vaccancy_req_obj,'vaccancy_obj':vaccancy_obj})

   

def view_approved_vaccancy2(request,wid,reqid):
    worker_obj=worker.objects.get(id=wid)
    skill_obj=worker_skill.objects.filter(WORKER_id=wid)
    works_obj=works.objects.filter(WORKER_SKILL__WORKER_id=wid)
    return render(request,'Company/View_approved_vaccancy2.html',{'data':worker_obj,'skill_obj':skill_obj,'works_obj':works_obj,'reqid':reqid})

   

def view_feedback_from_worker(request):
    if request.session['lg'] == "yes":
        company_id=request.session['company_id']
        company_obj=company.objects.get(id=company_id)
        res_company_feed = feedback.objects.filter(TO_ID=company_obj.LOGIN, feedback_type='company')
        res=[]

        for i in res_company_feed:
            logid_from=i.FROM_ID
            worker_obj=worker.objects.get(LOGIN=logid_from)

            d={
            'wname':worker_obj.name,
            'wimage':worker_obj.image,
            'wphone':worker_obj.phone,
            'wemail':worker_obj.email,
            'feedback':i.feedback,
            'feedback_date':i.feedback_date,


            }
            res.append(d)
        return render(request,'Company/View_feedback_from_worker.html',{'data':res})
    else:
        return render(request,'Login.html')
def view_feedback_from_worker_post(request):
    fromdate = request.POST['textfield']
    todate = request.POST['textfield2']
    company_id=request.session['company_id']
    company_obj=company.objects.get(id=company_id)
    res_company_feed = feedback.objects.filter(feedback_date__range=(fromdate,todate),TO_ID=company_obj.LOGIN, feedback_type='company')
    res=[]

    for i in res_company_feed:
        logid_from=i.FROM_ID
        worker_obj=worker.objects.get(LOGIN=logid_from)
        
        d={
        'wname':worker_obj.name,
        'wimage':worker_obj.image,
        'wphone':worker_obj.phone,
        'wemail':worker_obj.email,
        'feedback':i.feedback,
        'feedback_date':i.feedback_date,


        }
        res.append(d)
    return render(request,'Company/View_feedback_from_worker.html',{'data':res})
    





    

########COMPANY END

####WORKERS START
def worker_home(request):
    w_id = request.session['worker_id']
    worker_obj = worker.objects.get(id=w_id)
    vaccancy_obj = vaccancy.objects.all().order_by('-id')[:3]
    vaccancy_list = []
    for i in vaccancy_obj:
        vaccancy_list.append(
            {'image': i.COMPANY.image, 'title': i.title, 'name': i.COMPANY.company_name, 'phone': i.COMPANY.phone,
             'email': i.COMPANY.email, 'date': i.date})
    feed_obj = feedback.objects.filter(TO_ID=worker_obj.LOGIN).order_by('-id')[:3]
    print("ddddddddddd ", feed_obj)
    feed_list = []
    for i in feed_obj:
        user_obj = user.objects.get(LOGIN=i.FROM_ID)
        feed_list.append(
            {'name': user_obj.name, 'image': user_obj.image, 'phone': user_obj.phone, 'email': user_obj.email,
             'feedback': i.feedback, 'date': i.feedback_date})

    rating_obj = rating.objects.all().order_by('-id')[:4]
    rating_list = []
    for i in rating_obj:
        rr = i.rate
        rated = []
        for j in range(int(rr)):
            rated.append(j)
        nn = 5 - int(rr)
        not_rated = []
        for j in range(nn):
            not_rated.append(j)
        rating_list.append(
            {'rated': rated, 'not_rated': not_rated, 'image': i.USER.image, 'name': i.USER.name})

    return render(request,'Workers/worker_home.html',{'data':vaccancy_list,'data2':feed_list,'data3':rating_list})

def workers_view_profile(request):
    if request.session['lg'] == "yes":
        worker_id=request.session['worker_id']
        res=worker.objects.get(id=worker_id)
        return render(request,'Workers/View_profile.html',{'data':res})
    else:
        return render(request,'Login.html')
def workers_view_profile_post(request):

    return render(request,'Workers/View_profile.html')

# def workers_add_people(request):
#
#     return render(request,'Workers/Add_people.html')
#
# def workers_add_people_post(request):
#
#     name=request.POST['select']
#     phone=request.POST['select']
#     email=request.POST['select']
#     district=request.POST['select']
#     city=request.POST['select']
#     worker_obj=worker()
#     worker_obj.name=name
#     worker_obj.phone=phone
#     worker_obj.email=email
#     worker_obj.district=district
#     worker_obj.city=city
#     worker_obj.save()
#     return workers_add_skill(request)



def workers_edit_profile(request):
    if request.session['lg'] == "yes":
        worker_id=request.session['worker_id']
        res=worker.objects.get(id=worker_id)

        return render(request,'Workers/Edit_profile.html',{'data':res})
    else:
        return render(request,'Login.html')
def workers_edit_profile_post(request):
    name=request.POST['textfield']
    gender=request.POST['radiobutton']
    dob=request.POST['textfield2']
    district=request.POST['select']
    city=request.POST['textfield3']
    house_name=request.POST['textfield4']
    pin=request.POST['textfield5']
    phone=request.POST['textfield6']
    email=request.POST['textfield7']
    description=request.POST['textarea']
    worker_id=request.session['worker_id']
    
    if 'file' in request.FILES:

        image=request.FILES['file']
        fs=FileSystemStorage()
        fname=time.strftime("%Y%m%d-%H%M%S")+".jpg"
        filename=fs.save(fname, image)
        path=fs.url(filename)
 
        worker_obj=worker.objects.filter(id=worker_id).update(name=name,gender=gender,dob=dob,district=district,
            city=city,house_name=house_name,pin=pin,phone=phone,email=email,description=description,image=path)
    else:
         worker_obj=worker.objects.filter(id=worker_id).update(name=name,gender=gender,dob=dob,district=district,
            city=city,house_name=house_name,pin=pin,phone=phone,email=email,description=description)
    
    return workers_view_profile(request)


def workers_add_skill(request):
    if request.session['lg'] == "yes":
        worker_id=request.session['worker_id']
        skill_obj=skills.objects.exclude(id__in=(worker_skill.objects.filter(WORKER_id=worker_id).values_list('SKILL_id',flat=True)))
        worker_skill_obj=worker_skill.objects.filter(WORKER_id=worker_id)
        return render(request,'Workers/Add_skill.html', {'data':skill_obj,'data2':worker_skill_obj})
    else:
        return render(request,'Login.html')
def workers_add_skill_post(request):
    worker_id=request.session['worker_id']
    skill_id=request.POST['select']
    worker_skill_obj=worker_skill()
    worker_skill_obj.SKILL_id=skill_id
    worker_skill_obj.WORKER_id=worker_id
    worker_skill_obj.save()
    return workers_add_skill(request)

def worker_delete_skill(request,worker_skill_id):
    skill_obj=worker_skill.objects.get(id=worker_skill_id)
    skill_obj.delete()

    return workers_add_skill(request)




def workers_upload_previous_works(request):
    if request.session['lg'] == "yes":
        worker_id=request.session['worker_id']
        worker_skill_obj=worker_skill.objects.filter(WORKER_id=worker_id)
        return render(request,'Workers/Upload_previous_works.html',{'data':worker_skill_obj})
    else:
        return render(request,'Login.html')
def workers_upload_previous_works_post(request):
    work_done_from=request.POST['textfield']
    description=request.POST['textarea']
    skill=request.POST['select']
    amount=request.POST['textfield1']
    image=request.FILES['file']
    fs=FileSystemStorage()
    fname=time.strftime("%Y%m%d-%H%M%S")+".jpg"
    filename=fs.save(fname,image)
    path=fs.url(filename)
    works_obj=works()
    works_obj.WORKER_SKILL_id=skill
    works_obj.title=work_done_from
    works_obj.description=description
    works_obj.works_image=path
    works_obj.amount=amount
    works_obj.save()
    return workers_upload_previous_works(request)




def workers_upload_work_images(request,work_id):
    if request.session['lg'] == "yes":
        request.session['work_id']=work_id
        imgs_obj=work_image.objects.filter(WORKS_id=work_id)
        res=[]
        for i in imgs_obj:
            d={'id':i.id, 'path':i.path}
            res.append(d)
        return render(request,'Workers/Upload_images.html', {'data':res})
    else:
        return render(request,'Login.html')
def workers_upload_work_images_post(request):
    img=request.FILES['file']
    fs = FileSystemStorage()
    fname = time.strftime("%Y%m%d-%H%M%S") + ".jpg"
    filename = fs.save(fname, img)
    path = fs.url(filename)
    wid=request.session['work_id']
    work_image_obj=work_image()
    work_image_obj.WORKS_id=wid
    work_image_obj.path=path
    work_image_obj.save()
    imgs_obj = work_image.objects.filter(WORKS_id=wid)
    res = []
    for i in imgs_obj:
        d = {'id': i.id, 'path': i.path}
        res.append(d)
    return render(request, 'Workers/Upload_images.html', {'data': res})

def workers_remove_work_images_post(request,work_image_id):
    work_image_obj=work_image.objects.filter(id=work_image_id)
    work_image_obj.delete()
    wid = request.session['work_id']
    return workers_upload_work_images(request,wid)


def workers_view_previous_works(request):
    if request.session['lg'] == "yes":
        worker_id=request.session['worker_id']
        works_obj=works.objects.filter(WORKER_SKILL__WORKER_id=worker_id)
        return render(request,'Workers/View_previous_works.html',{'data':works_obj})
    else:
        return render(request,'Login.html')

def workers_delete_previous_works(request,work_id):
    works_obj=works.objects.get(id=work_id)
    works_obj.delete()
    return workers_view_previous_works(request)

def workers_upload_resume(request):
    if request.session['lg'] == "yes":
        return render(request,'Workers/Upload_resume.html')
    else:
        return render(request,'Login.html')

def workers_upload_resume_post(request):
    worker_id=request.session['worker_id']
    doc=request.FILES['file']
    doc_extn=str(doc.name).split('.')[-1]
    fs=FileSystemStorage()
    fname=time.strftime("%Y%m%d-%H%M%S")+"."+doc_extn
    filename=fs.save(fname,doc)
    path=fs.url(filename)
    curdate=datetime.datetime.now().date()
    resume_obj=worker_resume.objects.filter(WORKER_id=worker_id)
    if resume_obj.exists():
        resume_obj=resume_obj[0]
        resume_obj.date=curdate
        resume_obj.resume_path=path
        resume_obj.save()
    else:
        resume_obj=worker_resume()
        resume_obj.date=curdate
        resume_obj.resume_path=path
        resume_obj.WORKER_id=worker_id
        resume_obj.save()
    return render(request,'Workers/Upload_resume.html')

def workers_send_complaint(request):
    if request.session['lg'] == "yes":
        return render(request, 'Workers/Send_complaints.html')
    else:
        return render(request,'Login.html')
def workers_send_complaint_post(request):
    comp=request.POST['textarea']
    worker_id=request.session['worker_id']
    worker_obj=worker.objects.get(id=worker_id)
    complaint_obj=complaint()
    curdate=datetime.datetime.now().date()
    complaint_obj.complaint_date=curdate
    complaint_obj.reply='pending'
    complaint_obj.status='pending'
    complaint_obj.complaint=comp
    complaint_obj.complaint_type='worker'
    complaint_obj.LOGIN=worker_obj.LOGIN
    complaint_obj.save()
    return workers_send_complaint(request)


def workers_view_complaint_reply(request):
    if request.session['lg'] == "yes":
        worker_id=request.session['worker_id']
        worker_obj=worker.objects.get(id=worker_id)
        reply_obj=complaint.objects.filter(LOGIN=worker_obj.LOGIN)
        return render(request, 'Workers/View_complaint_reply.html',{'data':reply_obj})
    else:
        return render(request,'Login.html')
def workers_view_complaint_reply_post(request):
    fromdate = request.POST['textfield']
    todate = request.POST['textfield2']
    res=[]
    worker_id=request.session['worker_id']
    worker_obj=worker.objects.get(id=worker_id)
    reply_obj=complaint.objects.filter(LOGIN=worker_obj.LOGIN, complaint_date__range=(fromdate,todate))
    return render(request, 'Workers/View_complaint_reply.html',{'data':reply_obj})



def worker_delete_complaint(request,complaint_id):
    complaint_obj=complaint.objects.get(id=complaint_id)
    complaint_obj.delete()
    return workers_view_complaint_reply(request)



def workers_view_vaccancy_and_send_request(request):
    if request.session['lg'] == "yes":
        curdate=datetime.datetime.now().date()
        worker_id=request.session['worker_id']
        requested_vaccancies=[]         # vaccancies already requested by worker
        req_list=vaccancy_request.objects.filter(WORKER_id=worker_id).values_list('VACCANCY_id',flat=True)
        for i in req_list:
            requested_vaccancies.append(i)
        print(requested_vaccancies)
        worker_skill_obj=worker_skill.objects.filter(WORKER_id=worker_id)
        worker_skill_ids=[]
        for i in worker_skill_obj:
            worker_skill_ids.append(i.SKILL_id)


        vaccancy_obj=vaccancy.objects.filter(date__gte=curdate) # vaccancies whose last date not over
        res=[]
        for i in vaccancy_obj:
            d={}
            if i.id not in requested_vaccancies:
                d['id']=i.id
                d['date']=i.date
                d['company_name']=i.COMPANY.company_name
                d['title']=i.title
                d['description']=i.description
                skill_obj=vaccancy_skills.objects.filter(VACCANCY_id=i.id)
                req_skill=[]        # required skills
                is_eligible=False
                for j in skill_obj:
                    if j.SKILLS_id in worker_skill_ids:  # checking if eligible
                        is_eligible=True
                    req_skill.append(j.SKILLS.skill)
                print("Eligible : ", is_eligible)
                d['skill_name']=", ".join(req_skill)
                if is_eligible:
                    res.append(d)
                else:
                    continue
        print(res)

        return render(request, 'Workers/View_vaccancy&send_req.html',{'data':res})
    else:
        return render(request,'Login.html')
def workers_view_vaccancy_and_send_request_post(request):
    curdate=datetime.datetime.now().date()
    worker_id=request.session['worker_id']
    title=request.POST['textfield']
    requested_vaccancies=[]         # vaccancies already requested by worker
    req_list=vaccancy_request.objects.filter(WORKER_id=worker_id).values_list('VACCANCY_id',flat=True)
    for i in req_list:
        requested_vaccancies.append(i)
    print(requested_vaccancies)
    worker_skill_obj=worker_skill.objects.filter(WORKER_id=worker_id)
    worker_skill_ids=[]
    for i in worker_skill_obj:
        worker_skill_ids.append(i.SKILL_id)


    vaccancy_obj=vaccancy.objects.filter(date__gte=curdate,title__contains=title) # vaccancies whose last date not over
    res=[]
    for i in vaccancy_obj:
        d={}
        if i.id not in requested_vaccancies:
            d['id']=i.id
            d['date']=i.date
            d['company_name']=i.COMPANY.company_name
            d['title']=i.title
            d['description']=i.description
            skill_obj=vaccancy_skills.objects.filter(VACCANCY_id=i.id)
            req_skill=[]        # required skills
            is_eligible=False
            for j in skill_obj:
                if j.SKILLS_id in worker_skill_ids:  # checking if eligible
                    is_eligible=True
                req_skill.append(j.SKILLS.skill)
            print("Eligible : ", is_eligible)
            d['skill_name']=", ".join(req_skill)
            if is_eligible:
                res.append(d)
            else:
                continue
    print(res)

    return render(request, 'Workers/View_vaccancy&send_req.html',{'data':res})




def worker_sent_vaccancy_request(request,vaccancy_id):
    worker_id=request.session['worker_id']
    curdate=datetime.datetime.now().date()

    request_obj=vaccancy_request()
    request_obj.vaccancy_request_date=curdate
    request_obj.status='pending'
    request_obj.VACCANCY_id=vaccancy_id
    request_obj.WORKER_id=worker_id
    request_obj.save()
    return workers_view_vaccancy_and_send_request(request)





def workers_view_sent_vaccancy_request(request):
    if request.session['lg'] == "yes":
        worker_id=request.session['worker_id']
        request_obj=vaccancy_request.objects.filter(WORKER_id=worker_id)
        res=[]
        for i in request_obj:
            d={}

            d['id']=i.id
            d['vaccancy_request_date']=i.vaccancy_request_date
            d['company_name']=i.VACCANCY.COMPANY.company_name
            d['title']=i.VACCANCY.title
            d['description']=i.VACCANCY.description
            d['status']=i.status
            skill_obj=vaccancy_skills.objects.filter(VACCANCY_id=i.VACCANCY_id)
            req_skill=[]        # required skills

            for j in skill_obj:

                req_skill.append(j.SKILLS.skill)

            d['skill_name']=", ".join(req_skill)
            res.append(d)



        return render(request, 'Workers/View_sent_vacc_req.html',{'data':res})

    else:
        return render(request,'Login.html')


def worker_delete_sent_vaccancy_request(request,vaccancy_id):
    delete_obj=vaccancy_request.objects.get(id=vaccancy_id)
    delete_obj.delete()
    return workers_view_sent_vaccancy_request(request)



def workers_view_user_request_and_approval(request):
    if request.session['lg'] == "yes":
        worker_id=request.session['worker_id']
        work_request_obj=work_request.objects.filter(WORKS__WORKER_SKILL__WORKER_id=worker_id)
        return render(request, 'Workers/View_user_request&approval.html',{'data':work_request_obj})
    else:
        return render(request,'Login.html')
def workers_view_user_request_and_approval_post(request):
    title=request.POST['textfield']
    worker_id=request.session['worker_id']
    work_request_obj=work_request.objects.filter(WORKS__WORKER_SKILL__WORKER_id=worker_id,WORKS__title__contains=title)
    return render(request, 'Workers/View_user_request&approval.html',{'data':work_request_obj})
        






def workers_approve_user_request(request,request_id):
    if request.session['lg'] == "yes":
        work_request_obj=work_request.objects.get(id=request_id)
        work_request_obj.status='Approved'
        work_request_obj.seen='false'
        work_request_obj.save()

        work_name=work_request_obj.WORKS.title
        user_eml=work_request_obj.USER.email
        worker_name=work_request_obj.WORKS.WORKER_SKILL.WORKER.name
        worker_eml=work_request_obj.WORKS.WORKER_SKILL.WORKER.email
        worker_phn=work_request_obj.WORKS.WORKER_SKILL.WORKER.phone


        import smtplib
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login("workerapp035@gmail.com", "@workerapp21")
        msg = MIMEMultipart()  # create a message.........."
        message = "Messege from WORKER APP"
        msg['From'] = "workerapp035@gmail.com"
        msg['To'] = user_eml
        msg['Subject'] = "Work Request Accepted"
        body = "Your request for "+work_name +" has been approved. For more details contact :\nWorker name : " + worker_name
        body+="\nEmail : "+worker_eml+"\nPhone : "+worker_phn
        msg.attach(MIMEText(body, 'plain'))
        s.send_message(msg)

        # return workers_view_user_request_and_approval(request)
        return HttpResponse(
            "<script>alert('Successfully approved');window.location='/newapp/workers_view_user_request_and_approval/'</script>")

    else:
        return render(request,'Login.html')
def workers_reject_user_request(request,request_id):
    work_request_obj=work_request.objects.get(id=request_id)
    work_request_obj.status='Rejected'
    work_request_obj.seen='false'
    work_request_obj.save()

    work_name = work_request_obj.WORKS.title
    user_eml = work_request_obj.USER.email
    worker_name = work_request_obj.WORKS.WORKER_SKILL.WORKER.name
    worker_eml = work_request_obj.WORKS.WORKER_SKILL.WORKER.email
    worker_phn = work_request_obj.WORKS.WORKER_SKILL.WORKER.phone

    import smtplib
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login("workerapp035@gmail.com", "@workerapp21")
    msg = MIMEMultipart()  # create a message.........."
    message = "Messege from WORKER APP"
    msg['From'] = "workerapp035@gmail.com"
    msg['To'] = user_eml
    msg['Subject'] = "Work Request Rejected"
    body = "Your request for " + work_name + " has been rejected. For more details contact :\nWorker name : " + worker_name
    body += "\nEmail : " + worker_eml + "\nPhone : " + worker_phn
    msg.attach(MIMEText(body, 'plain'))
    s.send_message(msg)
    # return workers_view_user_request_and_approval(request)
    return HttpResponse(
        "<script>alert('Successfully rejected');window.location='/newapp/workers_view_user_request_and_approval/'</script>")




def wokers_view_payment_details(request,work_request_id):
    # work_request_id=request.session['work_request_id']
    if request.session['lg'] == "yes":
        work_req_obj=work_request.objects.get(id=work_request_id)
        pay_obj=payment.objects.filter(WORK_REQUEST_id=work_request_id)
        if pay_obj.exists():
            res = []
            # print("************",pay_obj)
            for i in pay_obj:
                d = {'id': i.id, 'payment_date': i.payment_date, 'account':i.accno, 'amount': i.amount, 'type':i.type}
                res.append(d)


            data2={'req_date': work_req_obj.work_request_date,'work_image': work_req_obj.WORKS.works_image ,'title': work_req_obj.WORKS.title  ,'amount':work_req_obj.WORKS.amount  ,
                     'user_name':work_req_obj.USER.name,'user_image':work_req_obj.USER.image,'house_name':work_req_obj.USER.house_name,
                   'pin':work_req_obj.USER.pin,'district':work_req_obj.USER.district,
                   'city':work_req_obj.USER.city,'phone':work_req_obj.USER.phone,'email':work_req_obj.USER.email}
            return render(request,'Workers/View_payment_details.html',{'data':res,'data2':data2})
        else:
            return HttpResponse("<script>alert('payment not Completed');window.location='/newapp/workers_view_user_request_and_approval/'</script>")
    else:
        return render(request,'Login.html')
def workers_chat_with_user(request, userid):
    request.session['sel_uid']=userid
    return render(request, 'Workers/Chat_with_user.html')

def workersviewmsg(request):
    UID=request.session['sel_uid']
    wid=request.session['worker_id']
    obj=chat.objects.filter(WORKER_id=wid,USER_id=UID)
    user_data=user.objects.get(id=UID)
    print("********************",obj)

    res = []
    for i in obj:
        s = {'id':i.pk, 'date':i.chat_date,'msg':i.chat,'type':i.chat_type,'time':i.chat_time}
        res.append(s)
    print(user_data.name, user_data.image)




    return JsonResponse({'status': 'ok', 'data': res,'name':user_data.name,'image':user_data.image})



def workers_insert_chat(request,msg):
    worker_id= request.session["worker_id"]
    UID = request.session['sel_uid']

    obj=chat()
    obj.USER_id=UID
    obj.WORKER_id=worker_id
    obj.chat=msg
    obj.chat_type='worker'
    obj.chat_date=datetime.datetime.now().date()
    time=str(datetime.datetime.now().time()).split(".")[0]
    obj.chat_time=time
    obj.save()
    print("hi")
    return JsonResponse({'status':'ok'})




def workers_send_feedback_about_companies(request):
    if request.session['lg'] == "yes":
        company_obj=company.objects.all()
        return render(request, 'Workers/Send_feedback_abt_comp.html',{'data':company_obj})
    else:
        return render(request,'Login.html')
def workers_send_feedback_about_companies_post(request):
    company_name=request.POST['textfield']
    company_obj=company.objects.filter(company_name__contains=company_name)
    return render(request, 'Workers/Send_feedback_abt_comp.html',{'data':company_obj})


def workers_send_feedback(request,comp_lid):
    if request.session['lg'] == "yes":
        request.session['comp_lid']=comp_lid
        res_company_feed = feedback.objects.filter(TO_ID_id=comp_lid, feedback_type='company')
        res=[]

        for i in res_company_feed:
            logid_from=i.FROM_ID
            worker_obj=worker.objects.get(LOGIN=logid_from)

            d={
            'wname':worker_obj.name,
            'wimage':worker_obj.image,
            'wphone':worker_obj.phone,
            'wemail':worker_obj.email,
            'feedback':i.feedback,
            'feedback_date':i.feedback_date,


            }
            res.append(d)
        return render(request, 'Workers/Send_feedback.html',{'data':res})
    else:
        return render(request,'Login.html')
def workers_send_feedback_post(request):
    worker_id=request.session['worker_id']
    worker_obj=worker.objects.get(id=worker_id)

    feed=request.POST['textarea']
    comp_lid=request.session['comp_lid']
    curdate=datetime.datetime.now().date()
    feedback_obj=feedback()
    feedback_obj.feedback=feed
    feedback_obj.feedback_date=curdate
    feedback_obj.feedback_type='company'
    feedback_obj.FROM_ID=worker_obj.LOGIN
    feedback_obj.TO_ID_id=comp_lid
    feedback_obj.save()
    return workers_send_feedback(request,comp_lid)




def workers_view_feedback_from_user(request):
    if request.session['lg'] == "yes":
        worker_id=request.session['worker_id']
        worker_obj=worker.objects.get(id=worker_id)
        res_user_feed = feedback.objects.filter(TO_ID=worker_obj.LOGIN, feedback_type='worker')
        res=[]

        for i in res_user_feed:
            logid_from=i.FROM_ID
            user_obj=user.objects.get(LOGIN=logid_from)

            d={
            'uname':user_obj.name,
            'uimage':user_obj.image,
            'uphone':user_obj.phone,
            'uemail':user_obj.email,
            'feedback':i.feedback,
            'feedback_date':i.feedback_date,


            }
            res.append(d)

        return render(request, 'Workers/View_feedback_from_user.html',{'data':res})
    else:
        return render(request,'Login.html')
def workers_view_feedback_from_user_post(request):
    fromdate=request.POST['textfield']
    todate=request.POST['textfield2']
    worker_id=request.session['worker_id']
    worker_obj=worker.objects.get(id=worker_id)
    res_user_feed = feedback.objects.filter(feedback_date__range=(fromdate,todate),TO_ID=worker_obj.LOGIN, feedback_type='worker')
    res=[]

    for i in res_user_feed:
        logid_from=i.FROM_ID
        user_obj=user.objects.get(LOGIN=logid_from)
        
        d={
        'uname':user_obj.name,
        'uimage':user_obj.image,
        'uphone':user_obj.phone,
        'uemail':user_obj.email,
        'feedback':i.feedback,
        'feedback_date':i.feedback_date,


        }
        res.append(d)


    return render(request, 'Workers/View_feedback_from_user.html',{'data':res})


# def cube(request,c):
#     return HttpResponse("Cube of "+str(c) +"is"+str(c*c*c))
#
#
# def large(request,x,y):
#     if x>y:
#         return HttpResponse(str(x)+" is greater")
#     else:
#         return HttpResponse(str(y)+" is greater")
#
#
# def input_no(request):
#     return render(request,"input_no.html")
#
# def submit(request):
#     a=request.POST['textfield']
#     print(a)
#     return render(request,"input_no.html")
#
# def first_get(request):
#     return render(request,"first.html")
# def first_post(request):
#     a=request.POST['textfield3']
#     b=request.POST['textfield4']
#     data={'fname':a,'lname':b}
#     return render(request,"second.html",{'data':data})


def abc(request):
    return render(request,'admin_index.html')




def forgot_load(request):
    return render(request,'Forgot_password.html')

def forgot_post(request):
    email=request.POST['textfield']
    log_obj=login.objects.filter(username=email)
    if log_obj.exists():
        log_obj=log_obj[0]
        password=log_obj.password
        import smtplib
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login("workerapp035@gmail.com", "@workerapp21")
        msg = MIMEMultipart()  # create a message.........."
        message = "Messege from WORKER APP"
        msg['From'] = "workerapp035@gmail.com"
        msg['To'] = email
        msg['Subject'] = "Your Password for WORKER APP"
        body = "Your Password is:- - " + str(password)
        msg.attach(MIMEText(body, 'plain'))
        s.send_message(msg)
        return render(request,"Login.html")
    else:
        return HttpResponse("Email not registered")

#########################################       ANDROID
def and_login(request):
    username=request.POST['username']
    password=request.POST['password']
    log_obj=login.objects.filter(username=username,password=password)
    if log_obj.exists():
        log_obj=log_obj[0]
        type=log_obj.logintype
        if  type=="user":
            user_obj=user.objects.get(LOGIN=log_obj)
            return JsonResponse({'status':'ok','id':user_obj.id})
        else:
            return JsonResponse({'status':'Invalid user'})
    else:
        return JsonResponse({'status':"invalid details"})


def and_forgot_password(request):
    email=request.POST['email']
    log_obj=login.objects.filter(username=email)
    if log_obj.exists():
        log_obj=log_obj[0]
        password=log_obj.password
        import smtplib
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login("workerapp035@gmail.com", "@workerapp21")
        msg = MIMEMultipart()  # create a message.........."
        message = "Messege from WORKER APP"
        msg['From'] = "workerapp035@gmail.com"
        msg['To'] = email
        msg['Subject'] = "Your Password for WORKER APP"
        body = "Your Password is:- - " + str(password)
        msg.attach(MIMEText(body, 'plain'))
        s.send_message(msg)
        return JsonResponse({'status':'ok'})
    else:
        return JsonResponse({'status':'no'})


def and_signup(request):
    name=request.POST['name']
    gender=request.POST['gender']
    dob=request.POST['dob']
    district=request.POST['district']
    city=request.POST['city']
    house_name=request.POST['house_name']
    pin=request.POST['pin']
    phone=request.POST['phone']
    email=request.POST['email']
    image=request.POST['image']
    password=request.POST['password']

    timestr = time.strftime("%Y%m%d-%H%M%S")
    a = base64.b64decode(image)
    fh = open(media_path + timestr + ".jpg", "wb")
    fh.write(a)
    fh.close()
    path = "/media/" + timestr + ".jpg"


    log_obj=login()
    log_obj.username=email
    log_obj.password=password
    log_obj.logintype='user'
    log_obj.save()


    user_obj=user()
    user_obj.name=name
    user_obj.gender=gender
    user_obj.dob=dob
    user_obj.district=district
    user_obj.city=city
    user_obj.house_name=house_name
    user_obj.pin=pin
    user_obj.phone=phone
    user_obj.email=email
    user_obj.image=path
    user_obj.LOGIN=log_obj
    user_obj.save()
    return JsonResponse({'status':'ok'})

def and_view_profile(request):
    user_id=request.POST['user_id']
    user_obj=user.objects.get(id=user_id)

    return JsonResponse({'status':'ok','name':user_obj.name,'gender':user_obj.gender,'dob':user_obj.dob,'district':user_obj.district,'city':user_obj.city,'house_name':user_obj.house_name,'pin':user_obj.pin,
        'phone':user_obj.phone,'email':user_obj.email,'image':user_obj.image})


def and_update_profile(request):
    userid=request.POST['uid']
    name=request.POST['name']
    gender=request.POST['gender']
    dob=request.POST['dob']
    district=request.POST['district']
    city=request.POST['city']
    house_name=request.POST['house_name']
    pin=request.POST['pin']
    phone=request.POST['phone']
    email=request.POST['email']
    image=request.POST['image']

    print("HHH",house_name)


    user_obj=user.objects.get(id=userid)
    user_obj.name=name
    user_obj.gender=gender
    user_obj.dob=dob
    user_obj.district=district
    user_obj.city=city
    user_obj.house_name=house_name
    user_obj.pin=pin
    user_obj.phone=phone
    user_obj.email=email
    if image!="":
        timestr = time.strftime("%Y%m%d-%H%M%S")
        a = base64.b64decode(image)
        fh = open(media_path + timestr + ".jpg", "wb")
        fh.write(a)
        fh.close()
        path = "/media/" + timestr + ".jpg"
        user_obj.image=path
    user_obj.save()


    log_obj=login.objects.get(id=user_obj.LOGIN_id)
    log_obj.username=email
    log_obj.save()
    return JsonResponse({'status':'ok'})

def and_view_workers(request):
    worker_obj=worker.objects.filter(LOGIN__logintype='worker')
    res=[]
    for i in worker_obj:
        d={'id':i.id,'name':i.name,'description':i.description,
             'phone':i.phone,'email':i.email,'image':i.image}
        res.append(d)     
    return JsonResponse({'status':'ok','data':res})


def and_view_previous_works(request):
    worker_id=request.POST['worker_id']
    worker_obj=worker.objects.get(id=worker_id)
    address=worker_obj.house_name+"\n"+worker_obj.city+", "+worker_obj.district+", "+worker_obj.pin
    works_obj=works.objects.filter(WORKER_SKILL__WORKER_id=worker_id)
    res=[]
    for i in works_obj:
        d={'id':i.id,'works_image':i.works_image,'title':i.title,
        'description':i.description,'amount':i.amount,'skill':i.WORKER_SKILL.SKILL.skill}
        res.append(d)
    print(res)
    return JsonResponse({'status':'ok','data':res, 'image':worker_obj.image,'phone':worker_obj.phone,
                         'email':worker_obj.email,'address':address,'name':worker_obj.name,
                         'description':worker_obj.description})

def and_request_work(request):
    user_id=request.POST['user_id']
    works_id=request.POST['works_id']
    curdate=datetime.datetime.now().date()
    req_obj=work_request.objects.filter(WORKS_id=works_id,USER_id=user_id,status="pending")
    if req_obj.exists():
        return JsonResponse({'status': 'Exist'})
    else:
        work_request_obj=work_request()
        work_request_obj.WORKS_id=works_id
        work_request_obj.USER_id=user_id
        work_request_obj.work_request_date=curdate
        work_request_obj.status='pending'
        work_request_obj.save()

        #_______________________________mailing----------------
        workerinfo=works.objects.get(id=works_id)
        worker_email=workerinfo.WORKER_SKILL.WORKER.email

        userinfo=user.objects.get(id=user_id)
        username=userinfo.name

        import smtplib
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login("workerapp035@gmail.com", "@workerapp21")
        msg = MIMEMultipart()  # create a message.........."
        message = "Messege from WORKER APP"
        msg['From'] = "workerapp035@gmail.com"
        msg['To'] = worker_email
        msg['Subject'] = "Work request"
        body = "You have a request from user " + username
        msg.attach(MIMEText(body, 'plain'))
        s.send_message(msg)

        return JsonResponse({'status':'ok'})

def and_delete_request(request):
    request_id=request.POST['request_id']
    request_obj=work_request.objects.get(id=request_id)
    request_obj.delete()
    return JsonResponse({'status':'ok'})


def and_view_request_status(request):
    user_id=request.POST['user_id']
    request_obj=work_request.objects.filter(USER_id=user_id)
    res=[]
    for i in request_obj:
        d={'rid':i.id,'work_request_date':i.work_request_date,'status':i.status,'image':i.WORKS.WORKER_SKILL.WORKER.image,
            'title':i.WORKS.title,'description':i.WORKS.description,'worker_name':i.WORKS.WORKER_SKILL.WORKER.name,
            'phone':i.WORKS.WORKER_SKILL.WORKER.phone,'wid':i.WORKS.WORKER_SKILL.WORKER_id,'amount':i.WORKS.amount
        }
        pay_obj=payment.objects.filter(WORK_REQUEST=i)
        if pay_obj.exists():
            if len(pay_obj)==2:         #####       2 partial payments
                d['pay_status'] = "PAID"
            elif len(pay_obj) == 1:       #####        single transaction(full payment or 1 partial payment)
                pay_obj=pay_obj[0]
                if pay_obj.type=="Full Payment":
                    d['pay_status'] = "PAID"
                else:
                    d['pay_status'] = pay_obj.type

        else:
            d['pay_status']="NOT PAID"
        res.append(d)
    return JsonResponse({'status':'ok','data':res})  



def and_send_feedback(request):
    user_id=request.POST['user_id']
    user_obj=user.objects.get(id=user_id)
    worker_id=request.POST['worker_id']
    worker_obj=worker.objects.get(id=worker_id)
    feed=request.POST['feed']
    curdate=datetime.datetime.now().date()
    feedback_obj=feedback()
    feedback_obj.feedback=feed
    feedback_obj.feedback_date=curdate
    feedback_obj.feedback_type='worker'
    feedback_obj.FROM_ID=user_obj.LOGIN
    feedback_obj.TO_ID=worker_obj.LOGIN
    feedback_obj.save()
    return JsonResponse({'status':'ok'})


def and_view_feedback(request):
    worker_id=request.POST['worker_id']
    worker_obj=worker.objects.get(id=worker_id)
    feedback_obj=feedback.objects.filter(TO_ID=worker_obj.LOGIN)
    res=[]
    for i in feedback_obj:
        from_id=i.FROM_ID
        user_obj=user.objects.get(LOGIN=from_id)
        d={'id':i.id,'feedback':i.feedback,'feedback_date':i.feedback_date,'user_name':user_obj.name,'image':user_obj.image}
        res.append(d)
    return JsonResponse({'status':'ok','data':res})


def and_payment(request):
    request_id=request.POST['request_id']
    accno=request.POST['accno']
    passw=request.POST['pass']
    amount=request.POST['amount']
    bname=request.POST['bank']
    sel_ptype=request.POST['sel_ptype']
    amount=amount.split(":")[-1]
    amount=amount.strip()
    bank_obj=bank.objects.filter(bank_name=bname, accno=accno, password=passw)
    if bank_obj.exists():
        bank_obj=bank_obj[0]
        bal=bank_obj.balance
        if float(bal)>float(amount):
            pay_obj=payment()
            pay_obj.amount=amount
            pay_obj.accno=accno
            pay_obj.type=sel_ptype
            pay_obj.WORK_REQUEST_id=request_id
            curdate = datetime.datetime.now().date()
            pay_obj.payment_date=curdate
            pay_obj.save()
            bank_obj.balance=float(bal)-float(amount)
            bank_obj.save()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'insufficient'})
    else:
        return JsonResponse({'status': 'invalid'})



def and_send_complaint(request):
    user_id=request.POST['user_id']
    user_obj=user.objects.get(id=user_id)
    comp=request.POST['complaint']
    curdate=datetime.datetime.now().date()
    complaint_obj=complaint()
    complaint_obj.complaint=comp
    complaint_obj.complaint_date=curdate
    complaint_obj.complaint_type='user'
    complaint_obj.reply='pending'
    complaint_obj.status='pending'
    complaint_obj.LOGIN=user_obj.LOGIN
    complaint_obj.save()
    return JsonResponse({'status':'ok'})


def and_view_complaint_reply(request):

    user_id=request.POST['user_id']
    user_obj=user.objects.get(id=user_id)
    complaint_obj=complaint.objects.filter(LOGIN=user_obj.LOGIN)
    res=[]
    for i in complaint_obj:
        d={'id':i.id,'complaint':i.complaint,'complaint_date':i.complaint_date,'status':i.status,'reply':i.reply}
        res.append(d)
    return JsonResponse({'status':'ok','data':res})


def and_delete_complaint(request):
    complaint_id=request.POST['complaint_id']
    complaint_obj=complaint.objects.filter(id=complaint_id)
    complaint_obj.delete()
    return JsonResponse({'status':'ok'})


def and_send_block_request(request):
    user_id=request.POST['user_id']
    worker_id=request.POST['worker_id']
    description=request.POST['description']
    block_obj=block_request.objects.filter(WORKER_id=worker_id, USER_id=user_id, status='pending')
    if block_obj.exists():
        block_obj=block_obj[0]
        block_obj.description = description
        block_obj.save()
    else:
        block_request_obj=block_request()
        block_request_obj.description=description
        block_request_obj.status='pending'
        block_request_obj.WORKER_id=worker_id
        block_request_obj.USER_id=user_id
        block_request_obj.save()
    return JsonResponse({'status':'ok'})


def and_delete_block_request(request):
    block_request_id=request.POST['block_request_id']
    block_request_obj=block_request.objects.filter(id=block_request_id)
    block_request_obj.delete()
    return JsonResponse({'status':'ok'})


def and_view_block_request_status(request):
    user_id=request.POST['user_id']
    block_request_obj=block_request.objects.filter(USER_id=user_id)
    res=[]
    for i in block_request_obj:
        d={'id':i.id,'description':i.description,'status':i.status,'worker_name':i.WORKER.name,'worker_image':i.WORKER.image}
        res.append(d)
    return JsonResponse({'status':'ok','data':res})

def inmessage(request):
    user_id=request.POST['user_id']
    worker_id=request.POST['worker_id']
    msg=request.POST['msg']
    ch=chat()
    ch.chat_date=datetime.datetime.now().date()
    ch.WORKER_id=worker_id
    ch.USER_id=user_id
    ch.chat=msg
    ch.chat_type="user"
    time=str(datetime.datetime.now().time()).split(".")[0]
    ch.chat_time=time

    ch.save()
    return JsonResponse({'status':'ok'})

def view_message2(request):
    user_id = request.POST['user_id']
    worker_id = request.POST['worker_id']
    lmid=request.POST['lastmsgid']


    cha = chat.objects.filter(WORKER_id=worker_id, USER_id=user_id, pk__gte=lmid)

    if cha.exists():
        a = []
        for i in cha:
            if i.pk > int(lmid):
                a.append({'id': i.pk, 'msg': i.chat, 'date': i.chat_date, 'type': i.chat_type,'time':i.chat_time})
        return JsonResponse({'status': 'ok', 'data': a})
    else:
        return JsonResponse({'status': 'no'})


def and_view_all_skill(request):
    skill_obj=skills.objects.all().order_by('skill')
    res=[]
    for i in skill_obj:
        d={"id":i.id,"skill":i.skill}
        res.append(d)
    return JsonResponse({'status': 'ok','data':res})


def and_view_workers_by_skill(request):
    skill_id=request.POST['skill_id']
    worker_skill_obj=worker_skill.objects.filter(SKILL_id=skill_id)
    res=[]
    for i in worker_skill_obj:
        d={'wid':i.WORKER.id,'name':i.WORKER.name,'district':i.WORKER.district,'city':i.WORKER.city,'description':i.WORKER.description,
             'phone':i.WORKER.phone,'email':i.WORKER.email,'image':i.WORKER.image}
        res.append(d)
    return JsonResponse({'status':'ok','data':res})



def and_view_works_homepage(request):
    works_obj=works.objects.all()
    res=[]
    for i in works_obj:
        d={'wid':i.id,'title':i.title,'description':i.description,
             'amount':i.amount,'image':i.works_image,'wrkr_id':i.WORKER_SKILL.WORKER_id}
        res.append(d)
    return JsonResponse({'status':'ok','data':res})


def and_get_request_notification(request):
    user_id = request.POST['user_id']
    work_request_obj=work_request.objects.filter(USER_id=user_id, seen='false')
    if work_request_obj.exists():
        work_request_obj=work_request_obj[0]
        return JsonResponse({'status':'ok','rid':work_request_obj.id, 'req_status':work_request_obj.status, 'wname':work_request_obj.WORKS.title, 'wrkr_name':work_request_obj.WORKS.WORKER_SKILL.WORKER.name})
    else:
        return JsonResponse({'status':'no'})

def and_update_request_seen_status(request):
    rid=request.POST['req_id']
    request_obj=work_request.objects.get(id=rid)
    request_obj.seen='true'
    request_obj.save()

    return JsonResponse({'status':'ok', 'work_request_date':request_obj.work_request_date, 'amount':request_obj.WORKS.amount,
                         'req_status':request_obj.status,'image':request_obj.WORKS.WORKER_SKILL.WORKER.image,
                        'title':request_obj.WORKS.title,'description':request_obj.WORKS.description,
                         'worker_name':request_obj.WORKS.WORKER_SKILL.WORKER.name,'phone':request_obj.WORKS.WORKER_SKILL.WORKER.phone,
                         })



def worker_reg_index(request):
    return render(request,'worker_reg_index.html')


def and_view_works_images(request):
    wid=request.POST['wid']
    img_obj=work_image.objects.filter(WORKS_id=wid)
    res=[]
    for i in img_obj:
        d={'path':i.path}
        res.append(d)
    return JsonResponse({'status':'ok','data':res})



def and_get_chat_notification(request):
    user_id = request.POST['user_id']
    print("uuu",user_id)

    last_msgid=request.POST['last_msgid']
    print("hhhhhhh", last_msgid)
    chat_obj=chat.objects.filter(USER_id=user_id,id__gt=last_msgid)
    if chat_obj.exists():
        chat_obj=chat_obj[0]
        return JsonResponse({'status':'ok','id':chat_obj.id,'wid':chat_obj.WORKER.id, 'chat_type':chat_obj.chat_type,'chat_time':chat_obj.chat_time, 'chat_date':chat_obj.chat_date, 'wname':chat_obj.WORKER.name})
    else:
        return JsonResponse({'status':'no'})


def and_search_category_or_works(request):
    name=request.POST['name']
    sel_tab=request.POST['sel_tab']
    if sel_tab=="0":
        skill_obj=skills.objects.filter(skill__icontains=name)
        res = []
        for i in skill_obj:
            d = {"id": i.id, "skill": i.skill}
            res.append(d)

        return JsonResponse({'status': 'ok', 'data': res})

    elif sel_tab=="1":
        works_obj = works.objects.filter(title__icontains=name)
        res = []
        for i in works_obj:
            d = {'wid': i.id, 'title': i.title, 'description': i.description,
                 'amount': i.amount, 'image': i.works_image, 'wrkr_id': i.WORKER_SKILL.WORKER_id}
            res.append(d)
        return JsonResponse({'status': 'ok', 'data': res})




def and_ratings(request):
    user_id=request.POST['uid']
    rate=request.POST['rate']
    rate=rate.split('.')[0]
    curdate = datetime.datetime.now().date()
    rate_obj = rating.objects.filter(USER_id=user_id)
    if rate_obj.exists():
        rate_obj=rate_obj[0]
        rate_obj.rate = int(rate)
        rate_obj.date = curdate
        rate_obj.save()
    else:
        rate_obj = rating()
        rate_obj.USER_id=user_id
        rate_obj.rate=int(rate)
        rate_obj.date=curdate
        rate_obj.save()
    return JsonResponse({'status': 'ok'})