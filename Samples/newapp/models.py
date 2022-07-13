from django.db import models

# Create your models here.

class login(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    logintype=models.CharField(max_length=50)
    class Meta:
        db_table="login"

class company(models.Model):
    company_name=models.CharField(max_length=50)
    year=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    district=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    pin=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    image=models.CharField(max_length=500)
    description=models.CharField(max_length=300)
    LOGIN=models.ForeignKey(login, on_delete=models.CASCADE)
    class Meta:
        db_table="company"


class worker(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    dob= models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    city= models.CharField(max_length=50)
    house_name = models.CharField(max_length=50)
    pin= models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    image = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    LOGIN = models.ForeignKey(login,on_delete=models.CASCADE)
    class Meta:
        db_table="worker"

class complaint(models.Model):
    complaint = models.CharField(max_length=200)
    complaint_date = models.CharField(max_length=50)
    complaint_type= models.CharField(max_length=50)
    reply= models.CharField(max_length=200)
    status = models.CharField(max_length=50)
    LOGIN=models.ForeignKey(login,on_delete=models.CASCADE)
    class Meta:
        db_table="complaint"

class feedback(models.Model):
    feedback= models.CharField(max_length=100)
    feedback_date= models.CharField(max_length=100)
    feedback_type= models.CharField(max_length=100)
    FROM_ID=models.ForeignKey(login,on_delete=models.CASCADE, related_name="loginA")
    TO_ID=models.ForeignKey(login,on_delete=models.CASCADE, related_name="loginB")
    class Meta:
        db_table="feedback"


class skills(models.Model):
    skill = models.CharField(max_length=100)
    class Meta:
        db_table = "skills"
        


class worker_skill(models.Model):
    SKILL=models.ForeignKey(skills,on_delete=models.CASCADE)
    WORKER=models.ForeignKey(worker,on_delete=models.CASCADE)
    class Meta:
        db_table = "worker_skill"

class works(models.Model):
    works_image=models.CharField(max_length=500)
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    amount=models.CharField(max_length=50)
    WORKER_SKILL = models.ForeignKey(worker_skill, on_delete=models.CASCADE, default=1)
    class Meta:
        db_table = "works"

class user(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    dob = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    house_name = models.CharField(max_length=50)
    pin = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    image = models.CharField(max_length=50)
    
    LOGIN = models.ForeignKey(login, on_delete=models.CASCADE)

    class Meta:
        db_table = "user"


class work_request(models.Model):
    work_request_date=models.CharField(max_length=50)
    status=models.CharField(max_length=100)
    WORKS=models.ForeignKey(works,on_delete=models.CASCADE)
    USER=models.ForeignKey(user,on_delete=models.CASCADE)
    seen=models.CharField(max_length=100, default="pending")
    class Meta:
        db_table="work_request"



class block_request(models.Model):
    description = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    WORKER = models.ForeignKey(worker, on_delete=models.CASCADE)
    USER = models.ForeignKey(user, on_delete=models.CASCADE, default=1)
    class Meta:

        db_table = "block_request"

class vaccancy(models.Model):
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=200)
    date=models.CharField(max_length=50)
    COMPANY=models.ForeignKey(company, on_delete=models.CASCADE)
    class Meta:
        db_table="vaccancy"



class vaccancy_request(models.Model):
    vaccancy_request_date=models.CharField(max_length=50)
    status=models.CharField(max_length=50,default="1")
    VACCANCY=models.ForeignKey(vaccancy,on_delete=models.CASCADE)
    WORKER=models.ForeignKey(worker,on_delete=models.CASCADE)
    class Meta:
        db_table="vaccancy_request"

class chat(models.Model):
    chat=models.CharField(max_length=500)
    chat_date=models.CharField(max_length=50)
    chat_type=models.CharField(max_length=50)
    chat_time=models.CharField(max_length=50,default="")
    WORKER = models.ForeignKey(worker, on_delete=models.CASCADE)
    USER = models.ForeignKey(user, on_delete=models.CASCADE)
    class Meta:
        db_table="chat"

class vaccancy_skills(models.Model):
    SKILLS=models.ForeignKey(skills,on_delete=models.CASCADE)
    VACCANCY=models.ForeignKey(vaccancy,on_delete=models.CASCADE,default=1)
    class Meta:
        db_table="vaccancy_skills"

class payment(models.Model):
    amount=models.CharField(max_length=50)
    payment_date=models.CharField(max_length=50)
    accno=models.CharField(max_length=50, default="")
    type=models.CharField(max_length=50, default="")


    WORK_REQUEST=models.ForeignKey(work_request,on_delete=models.CASCADE)
    class Meta:
        db_table="payment"


class worker_resume(models.Model):
    date=models.CharField(max_length=50)
    resume_path=models.CharField(max_length=100)
    WORKER=models.ForeignKey(worker,on_delete=models.CASCADE)
    class Meta:
        db_table="worker_resume"


class bank(models.Model):
    bank_name=models.CharField(max_length=50)
    accno=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    balance=models.CharField(max_length=50)
    class Meta:
        db_table="bank"



class work_image(models.Model):
    WORKS=models.ForeignKey(works,on_delete=models.CASCADE)
    path=models.CharField(max_length=500)
    class Meta:
        db_table="work_image"


class rating(models.Model):
    USER = models.ForeignKey(user, on_delete=models.CASCADE)
    rate = models.CharField(max_length=50)
    date = models.CharField(max_length=50)

    class Meta:
        db_table = "rating"