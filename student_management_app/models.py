from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver



##################################

class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects = models.Manager()

 # Overriding the Default Django Auth User and adding One More Field (user_type)


class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    user_type_data = ((1, "HOD"), (2, "Staff"),
                      (3, "Student"))
    user_type = models.CharField(
        default=1, choices=user_type_data, max_length=10)


class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

# files ############################# 
# class UploadedFile(models.Model):
#     file = models.FileField(upload_to='uploads/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)

# Annee scolaire ####################

class AnneeScolaire(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects = models.Manager()
   

# Semaine ##############################
class Semaines(models.Model):
    id = models.AutoField(primary_key=True)
    annee_scolaire_id = models.ForeignKey(
        #  AnneeScolaire, on_delete=models.CASCADE, default=2)
         AnneeScolaire, on_delete=models.PROTECT, default=2) # IMPOSSIBLE DE SUPPRIMER ANNEE SI SEMAINE
    # annee_scolaire_id = models.ForeignKey(
    #      AnneeScolaire, on_delete=models.CASCADE)
    numero_semaines = models.PositiveIntegerField(default=1)
    debut_semaines = models.DateField()
    fin_semaines = models.DateField()
   
    def __str__(self):
        return self.name

  
# Professeurs /staffs ##############################

class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    #null=True in lieu of default = 1
    #to handle the foreignKey failed
    annee_scolaire_id = models.ForeignKey(
        AnneeScolaire, on_delete=models.CASCADE, null=True) 
        #  AnneeScolaire, on_delete=models.PROTECT, null=True)  # IMPOSSIBLE DE SUPPRIMER ANNEE SI STAFF
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

# Cycle     ########################
 
class Cycles(models.Model):
    id = models.AutoField(primary_key=True)
    nom_cycles = models.CharField(max_length=255)
    objects = models.Manager()
# Niveau     ########################

class Niveaux(models.Model):
    id = models.AutoField(primary_key=True)
    cycles_id = models.ForeignKey(
        Cycles, on_delete=models.CASCADE, default=1)
    nom_niveaux = models.CharField(max_length=255)
    objects = models.Manager()

# Classes/courses #################

class Classess(models.Model):
    id = models.AutoField(primary_key=True)
    nom_classes = models.TextField()
    # need to give defauult course
    niveaux_id = models.ForeignKey(
        Niveaux, on_delete=models.CASCADE, default=1)
    objects = models.Manager()

# Disciplines#######################
class Disciplines(models.Model):
    id = models.AutoField(primary_key=True)
    nom_disciplines = models.CharField(max_length=255)
    objects = models.Manager()

# Matieres /subjects ###############


class Matieres(models.Model):
    id = models.AutoField(primary_key=True)
    nom_matieres = models.ForeignKey(
        Disciplines, on_delete=models.CASCADE, default=1) # nom_matieres = disciplines_id
    classes_id = models.ForeignKey(
        Classess, on_delete=models.CASCADE, default=1)
    professeurs_id = models.ForeignKey(
        Staffs, on_delete=models.CASCADE, default=1)
    objects = models.Manager()
    class Meta:
        unique_together = ["nom_matieres", "classes_id", "professeurs_id"]
 
# Chapitres  ###############

class Chapitres(models.Model):
    id = models.AutoField(primary_key=True)
    titre_chapitres = models.CharField(max_length=100)
    numero_chapitres  = models.PositiveIntegerField(default=1)
    matieres_id = models.ForeignKey(
        Matieres, on_delete=models.CASCADE, default=1)
    

class Lecons(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_heures = models.PositiveIntegerField(default=1)
    detail_lecons  = models.CharField(max_length=200) 
    chapitres_id = models.ForeignKey(
        Chapitres, on_delete=models.CASCADE, default=1)
    semaines = models.ManyToManyField(Semaines, through= 'SemainesLecons')

    def __str__(self):
        return self.name
    
class SemainesLecons(models.Model):
     id = models.AutoField(primary_key=True)
     semaines_id = models.ForeignKey(Semaines,on_delete=models.CASCADE)
     lecons_id = models.ForeignKey(Lecons,on_delete=models.CASCADE)
     #lecon_duree_reelle = models.PositiveIntegerField(default=0)
     status = models.CharField(max_length=2, choices=(('1','En attente'),('2','En cours'),('3','Terminer')), default=1)
     objects = models.Manager()

    #  def __str__(self):
    #     return self.name

class SemainesLeconsReelle(models.Model):
     id = models.AutoField(primary_key=True)
     semaines_id_Relle = models.ForeignKey(Semaines,on_delete=models.CASCADE)
     lecons_id_relle = models.ForeignKey(Lecons,on_delete=models.CASCADE)
     lecon_duree_reelle = models.PositiveIntegerField(default=0)
     #status = models.CharField(max_length=2, choices=(('1','En attente'),('2','En cours'),('3','Terminer')), default=1)
     objects = models.Manager()

class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    # def __str__(self):
    #     return self.course_name


class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    # need to give defauult course
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    profile_pic = models.FileField()
    address = models.TextField()
    course_id = models.ForeignKey(
        Courses, on_delete=models.DO_NOTHING, default=1)
    session_year_id = models.ForeignKey(
        SessionYearModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Attendance(models.Model):
    # Subject Attendance
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField()
    session_year_id = models.ForeignKey(
        SessionYearModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class AttendanceReport(models.Model):
    # Individual Student Attendance
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class NotificationStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    stafff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class StudentResult(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    subject_exam_marks = models.FloatField(default=0)
    subject_assignment_marks = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


# Creating Django Signals

# It's like trigger in database. It will run only when Data is Added in CustomUser model

@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Staffs.objects.create(admin=instance)
        if instance.user_type == 3:
            Students.objects.create(admin=instance, course_id=Courses.objects.get(
                id=1), session_year_id=SessionYearModel.objects.get(id=1), address="", profile_pic="", gender="")


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staffs.save()
    if instance.user_type == 3:
        instance.students.save()
