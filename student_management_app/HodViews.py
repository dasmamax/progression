from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

from student_management_app.models import Semaines, SemainesLecons, Chapitres, Lecons, Niveaux, Matieres, Classess, AnneeScolaire, CustomUser, Staffs, Courses, Subjects, Students, SessionYearModel, FeedBackStudent, FeedBackStaffs, LeaveReportStudent, LeaveReportStaff, Attendance, AttendanceReport
from .forms import AddStudentForm, EditStudentForm
from .forms import SemainesForm
#from .forms_prof import AddProfesseurForm, EditStudentForm

############ lecon ##########
from django.http.response import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
#from rest_framework.decorators import api_view
#from rest_framework.response import Response


def admin_home(request):
    all_anneescolaires_count = AnneeScolaire.objects.all().count()
    all_staffs_count = Staffs.objects.all().count()
    all_niveaux_count = Niveaux.objects.all().count()
    all_classes_count = Classess.objects.all().count()
    all_matieres_count = Matieres.objects.all().count()
    all_chapitres_count = Chapitres.objects.all().count()
    all_semaines_count = Semaines.objects.all().count()
    all_lecons_count = Lecons.objects.all().count()

    


    all_student_count = Students.objects.all().count()
    subject_count = Subjects.objects.all().count()
    course_count = Courses.objects.all().count()
    staff_count = Staffs.objects.all().count()

    # Total Subjects and students in Each Course
    course_all = Courses.objects.all()
    course_name_list = []
    subject_count_list = []
    student_count_list_in_course = []

    for course in course_all:
        subjects = Subjects.objects.filter(course_id=course.id).count()
        students = Students.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        student_count_list_in_course.append(students)

    subject_all = Subjects.objects.all()
    subject_list = []
    student_count_list_in_subject = []
    for subject in subject_all:
        course = Courses.objects.get(id=subject.course_id.id)
        student_count = Students.objects.filter(course_id=course.id).count()
        subject_list.append(subject.subject_name)
        student_count_list_in_subject.append(student_count)

    # For Saffs
    staff_attendance_present_list = []
    staff_attendance_leave_list = []
    staff_name_list = []

    staffs = Staffs.objects.all()
    for staff in staffs:
        subject_ids = Subjects.objects.filter(staff_id=staff.admin.id)
        attendance = Attendance.objects.filter(
            subject_id__in=subject_ids).count()
        leaves = LeaveReportStaff.objects.filter(
            staff_id=staff.id, leave_status=1).count()
        staff_attendance_present_list.append(attendance)
        staff_attendance_leave_list.append(leaves)
        staff_name_list.append(staff.admin.first_name)

    # For Students
    student_attendance_present_list = []
    student_attendance_leave_list = []
    student_name_list = []

    students = Students.objects.all()
    for student in students:
        attendance = AttendanceReport.objects.filter(
            student_id=student.id, status=True).count()
        absent = AttendanceReport.objects.filter(
            student_id=student.id, status=False).count()
        leaves = LeaveReportStudent.objects.filter(
            student_id=student.id, leave_status=1).count()
        student_attendance_present_list.append(attendance)
        student_attendance_leave_list.append(leaves+absent)
        student_name_list.append(student.admin.first_name)

    context = {
        "all_student_count": all_student_count,
        "subject_count": subject_count,
        "course_count": course_count,
        "staff_count": staff_count,
        "course_name_list": course_name_list,
        "subject_count_list": subject_count_list,
        "student_count_list_in_course": student_count_list_in_course,
        "subject_list": subject_list,
        "student_count_list_in_subject": student_count_list_in_subject,
        "staff_attendance_present_list": staff_attendance_present_list,
        "staff_attendance_leave_list": staff_attendance_leave_list,
        "staff_name_list": staff_name_list,
        "student_attendance_present_list": student_attendance_present_list,
        "student_attendance_leave_list": student_attendance_leave_list,
        "student_name_list": student_name_list,
    }
    return render(request, "hod_template/home_content.html", context)

# Syllabus #######################
###################### Annee Scolaire ######################
def creer_annees_scolaires(request):
    return render(request, "hod_template/creer_annees_scolaires_template.html")


def creer_annees_scolaires_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('creer_annees_scolaires')
    else:
        session_start_year = request.POST.get('debut_annee_scolaire')
        session_end_year = request.POST.get('fin_annee_scolaire')

        try:
            sessionyear = AnneeScolaire(
                session_start_year=session_start_year, session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Annee scolaire creee!")
            return redirect("creer_annees_scolaires")
        except:
            messages.error(request, "Echec de creation de l'annee scolaire")
            return redirect("creer_annees_scolaires")


def manage_sessionAnnee(request):
    session_years = AnneeScolaire.objects.all()
    context = {
        "session_years": session_years
    }
    return render(request, "hod_template/manage_session_template.html", context)


# def add_sessionAnnee(request):
#     return render(request, "hod_template/add_session_template.html")


# def add_session_saveAnnee(request):
#     if request.method != "POST":
#         messages.error(request, "Invalid Method")
#         return redirect('add_course')
#     else:
#         session_start_year = request.POST.get('session_start_year')
#         session_end_year = request.POST.get('session_end_year')

#         try:
#             sessionyear = AnneeScolaire(
#                 session_start_year=session_start_year, session_end_year=session_end_year)
#             sessionyear.save()
#             messages.success(request, "Session Year added Successfully!")
#             return redirect("add_session")
#         except:
#             messages.error(request, "Failed to Add Session Year")
#             return redirect("add_session")


def edit_sessionAnnee(request, session_id):
    session_year = AnneeScolaire.objects.get(id=session_id)
    context = {
        "session_year": session_year
    }
    return render(request, "hod_template/edit_session_template.html", context)


def edit_session_saveAnnee(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_sessionAnnee')
    else:
        session_id = request.POST.get('session_id')
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        try:
            session_year = AnneeScolaire.objects.get(id=session_id)
            session_year.session_start_year = session_start_year
            session_year.session_end_year = session_end_year
            session_year.save()

            messages.success(request, "Annee scolaire mise a jour.")
            return redirect('/edit_sessionAnnee/'+session_id)
        except:
            messages.error(request, "Echec de la mise a jour.")
            return redirect('/edit_sessionAnnee/'+session_id)


def delete_sessionAnnee(request, session_id):
    session = AnneeScolaire.objects.get(id=session_id)
    try:
        session.delete()
        messages.success(request, "Annee scolaire supprimee.")
        return redirect('manage_sessionAnnee')
    except:
        messages.error(request, "Echec de la suppression.")
        return redirect('manage_sessionAnnee')

        
# ####################   Niveau             ####################################


def creer_niveaux(request):
    return render(request, "hod_template/creer_niveaux_template.html")


def creer_niveaux_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('creer_niveaux')
    else:
        course = request.POST.get('niveaux')
        try:
            course_model = Niveaux(nom_niveaux=course)
            course_model.save()
            messages.success(request, "Niveau creer avec succes!")
            return redirect('creer_niveaux')
        except:
            messages.error(request, "Echec de creation du niveau!")
            return redirect('creer_niveaux')


def gerer_niveaux(request):
    niveaux = Niveaux.objects.all()
    context = {
        "niveaux": niveaux
    }
    return render(request, 'hod_template/gerer_niveaux_template.html', context)


def editer_niveaux(request, niveaux_id):
    niveau = Niveaux.objects.get(id=niveaux_id)
    context = {
        "niveau": niveau,
        "id": niveaux_id
    }
    return render(request, 'hod_template/editer_niveaux_template.html', context)


def editer_niveaux_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        niveaux_id = request.POST.get('niveaux_id')
        nom_niveaux = request.POST.get('niveau')

        try:
            niveau = Niveaux.objects.get(id=niveaux_id)
            niveau.nom_niveaux = nom_niveaux
            niveau.save()

            messages.success(request, "Niveau mis a jour.")
            return redirect('/editer_niveaux/'+niveaux_id)

        except:
            messages.error(request, "Echec de la mise a jour.")
            return redirect('/editer_niveaux/'+niveaux_id)


def supprimer_niveaux(request, niveaux_id):
    niveau = Niveaux.objects.get(id=niveaux_id)
    try:
        niveau.delete()
        messages.success(request, "Niveau supprime.")
        return redirect('gerer_niveaux')
    except:
        messages.error(request, "Echec de la suppression.")
        return redirect('gerer_niveaux')

# ####################   Matieres


def creer_matieres(request):
    classes = Classess.objects.all()
    #staff = Staffs.objects.all()
    anneescolaires= AnneeScolaire.objects.all()
    #professeurs = CustomUser.objects.filter(user_type='2')
    context = {
        "classess": classes,
        #"staffs": staff,
        "anneescolaires": anneescolaires
    }
    return render(request, "hod_template/creer_matieres_template.html", context)

# pour recuperer les prof de l annee pour creer la matiere
def modules_profs_name_admin(request):
    anneescolaire = request.GET.get('anneescolaire') 
    staffs = Staffs.objects.filter(annee_scolaire_id_id=anneescolaire)
    context = {
                'staffs': staffs,
                }
    return render(request, 'hod_template/partial/modules_profs_name_admin.html', context)

def creer_matieres_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('creer_matieres')
    else:
        matiere = request.POST.get('matiere')
        classes_id = request.POST.get('classes')
        classe = Classess.objects.get(id=classes_id)
        staffs_id = request.POST.get('staffs')
        staff = Staffs.objects.get(id=staffs_id)
        
        try:
            matiere_model = Matieres(nom_matieres = matiere, classes_id = classe, professeurs_id = staff
                                     )
            matiere_model.save()
            messages.success(request, "Matiere creer avec succes!")
            return redirect('creer_matieres')
        except:
            messages.error(request, "Echec de creation de la matiere!")
            return redirect('creer_matieres')


def gerer_matieres(request):
    matieres = Matieres.objects.all()
    context = {
        "matieres": matieres
    }
    return render(request, 'hod_template/gerer_matieres_template.html', context)


def editer_matieres(request, matieres_id):
    matiere = Matieres.objects.get(id=matieres_id)
    classe = Classess.objects.all()
    staff = Staffs.objects.all()
    context = {
        "matiere": matiere,
        "id": matieres_id,
        "classess": classe,
        "staffs": staff
    }
    return render(request, 'hod_template/editer_matieres_template.html', context)


def editer_matieres_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        matieres_id = request.POST.get('matieres_id')
        nom_matieres = request.POST.get('matiere')
        classe_id = request.POST.get('classe')
        professeur_id = request.POST.get('professeur')



        try:
            matiere = Matieres.objects.get(id=matieres_id)
            matiere.nom_matieres = nom_matieres

            classe = Classess.objects.get(id=classe_id)
            matiere.classes_id = classe

            staff = Staffs.objects.get(id=professeur_id)
            matiere.professeurs_id = staff
            
            matiere.save()

            messages.success(request, "Matiere mise a jour.")
            return redirect('/editer_matieres/'+matieres_id)

        except:
            messages.error(request, "Echec de mise a jour de la matiere.")
            return redirect('/editer_matieres/'+matieres_id)


def supprimer_matieres(request, matieres_id):
    matiere = Matieres.objects.get(id=matieres_id)
    try:
        matiere.delete()
        messages.success(request, "Matiere supprimee.")
        return redirect('gerer_matieres')
    except:
        messages.error(request, "Echec de suppression de la matiere.")
        return redirect('gerer_matieres')

##########################   Classes  ##########


def creer_classes(request):
    niveaux = Niveaux.objects.all()
    context = {
        "niveaux": niveaux
    }
    return render(request, "hod_template/creer_classes_template.html", context)


def creer_classes_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('creer_classes')
    else:
        nom_classe = request.POST.get('classes')
        niveaux_id = request.POST.get('niveaux')
        niveaux = Niveaux.objects.get(id=niveaux_id)
        try:
            classe = Classess(nom_classes=nom_classe,
                              niveaux_id=niveaux)
            classe.save()
            messages.success(request, "Classe ajoutee!")
            return redirect('creer_classes')

        except:
            messages.error(request, "Echec de creation de la classe!")
            return redirect('creer_classes')


def gerer_classes(request):
    classes = Classess.objects.all()
    context = {
        "classes": classes
    }
    return render(request, 'hod_template/gerer_classes_template.html', context)


def editer_classes(request, classes_id):
    classe = Classess.objects.get(id=classes_id)
    niveau = Niveaux.objects.all()
    context = {
        "classe": classe,
        "id": classes_id,
        "niveaux": niveau
    }
    return render(request, 'hod_template/editer_classes_template.html', context)


def editer_classes_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        classes_id = request.POST.get('classes_id')
        nom_classes = request.POST.get('classe')
        niveau_id = request.POST.get('niveau')

        try:
            classe = Classess.objects.get(id=classes_id)
            classe.nom_classes = nom_classes

            niveau = Niveaux.objects.get(id=niveau_id)
            classe.niveaux_id = niveau

            classe.save()

            messages.success(request, "Classe mise a jour.")
            # return redirect('/editer_classes/'+classes_id)
            # return redirect('/edit_subject/'+subject_id)
            return HttpResponseRedirect(reverse("editer_classes", kwargs={"classes_id": classes_id}))
        except:
            messages.error(request, "Echec de mise a jour de la classe.")
            # return redirect('/editer_classes/'+classes_id)
            return HttpResponseRedirect(reverse("editer_classes", kwargs={"classes_id": classes_id}))


def supprimer_classes(request, classes_id):
    classe = Classess.objects.get(id=classes_id)
    try:
        classe.delete()
        messages.success(request, "Classe supprimee.")
        return redirect('gerer_classes')
    except:
        messages.error(request, "Echec de suppression de la classe.")
        return redirect('gerer_Classes')

####### Professeurs   ################################

def creer_professeurs(request):
    annee_scolaire = AnneeScolaire.objects.all()
    #session_year_list = []
    #for session_year in session_years:
    #    single_session_year = (session_year.id, str(session_year.session_start_year)+" to "+str(session_year.session_end_year))
    #    session_year_list.append(single_session_year) 
    context ={
        "anneescolaire": annee_scolaire
    }
    return render(request, 'hod_template/creer_professeurs_template.html', context)

def creer_professeurs_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('creer_professeurs')
    else:
        annee_scolaire_id = request.POST.get('annee_scolaire')
        annee_scolaire = AnneeScolaire.objects.get(id=annee_scolaire_id)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('addresse')
        try:
            user = CustomUser.objects.create_user(
                username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
            # utiliser la table staffs pour enregistrer les professeurs comme user numero 2 
            user.staffs.address = address
            user.staffs.annee_scolaire_id = annee_scolaire
            user.save()
            messages.success(request, "Le professeur a ete ajoute!")
            return redirect('creer_professeurs')
        except:
            messages.error(request, "Echec d'ajout de professeur!" +str(annee_scolaire) )
            return redirect('creer_professeurs')
        
def gerer_professeurs(request):
    staffs = Staffs.objects.all()
    context = {
        "staffs": staffs
    }
    return render(request, "hod_template/gerer_professeurs_template.html", context)

def editer_professeurs(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    annee_scolaire = AnneeScolaire.objects.all()
    context = {
        "staff": staff,
        "id": staff_id,
        "anneescolaire": annee_scolaire
    }
    return render(request, "hod_template/editer_professeurs_template.html", context)

def editer_professeurs_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Methode Non autorise</h2>")
    else:
        staff_id = request.POST.get('staff_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        annee_scolaire_id = request.POST.get('annee_scolaire')
        password = request.POST.get('password')
        annee_scolaire = AnneeScolaire.objects.get(id=annee_scolaire_id)


        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            if password != None and password != "":
                user.set_password(password)
            # user.staffs.annee_scolaire_id = annee_scolaire
            user.save()

            # INSERTING into Staff Model
            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.annee_scolaire_id = annee_scolaire
            staff_model.save()

            messages.success(request, "professeur mis a jour.")
            return redirect('/editer_professeurs/'+staff_id)

        except:
            messages.error(request, "Echec de mise a jour du professeur.")
            return redirect('/editer_professeurs/'+staff_id)

def supprimer_professeurs(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    try:
        staff.delete()
        messages.success(request, "Professeur supprime.")
        return redirect('gerer_professeurs')
    except:
        messages.error(request, "Echec de la suppression.")
        return redirect('manage_staff')


##################### Gestion semaine ###############################

# def creer_semaines(request):
#      ##semaines=Semaines.objects.all()
#      if request.method == "POST":
#          form = SemainesForm(request.POST or None)
#          if form.is_valid():
#              semaine = form.save()
#              ##semaines.delete()
#              context = {'semaine': semaine}
#              return render(request, "hod_template/partial/semaines_list.html", context)
     
#      return render(request, "hod_template/partial/semaines_form.html", 
#                    {'form': SemainesForm()} )


def creer_semaines(request, annee_pk):
    # annee_scolaire = AnneeScolaire.objects.all()
    # staff_obj = Staffs.objects.get(admin=request.user.id) # for new interface of progression with side-bar
    annee_scolaire = AnneeScolaire.objects.get(id = annee_pk)
    # annee_scolaire_id = annee_scolaire.id
    
    if request.method == "POST":
          form = SemainesForm(request.POST or None)
          if form.is_valid():
              semaine = form.save()
              semaine.annee_scolaire_id = annee_scolaire
              semaine.save()
              context = {'semaine': semaine}
              return render(request, "hod_template/partial/semaines_list.html", context)

    # if request.method == "POST":
    #     form = LeconForm(request.POST)
    #     if form.is_valid():
    #         lecon = form.save(commit=False)
    #         lecon.chapitres_id = chapitre
    #         lecon.save()
    #         response = HttpResponse(status=200)
    #         response["Hx-Trigger"] = json.dumps({"leconListChanged": None,
    #                       "showMessage": f"{lecon.detail_lecons} ajoutee."})
    #         return response
    return render(request, "hod_template/partial/semaines_form.html", 
                    {'form': SemainesForm(),
                     "anneescolaire": annee_scolaire,} )
    # else:
    #     form = LeconForm()
    # return render(request, "staff_template/partials/lecon_form.html", context={
    #         "form": form,
    #         "chapitres": chapitre,
    #         "anneescolaire": annee_scolaire,
    #         "staff": staff_obj
    # })



def gerer_semaines(request, annee_pk):
    #  anneescolaire = get_object_or_404(SessionYearModel, id=annee_pk)
    anneescolaire = get_object_or_404(AnneeScolaire, id=annee_pk)
    context ={ 'form': SemainesForm(), 
               'semaines':Semaines.objects.all(),
               'anneescolaire':anneescolaire}
    return render(request, "hod_template/gerer_semaines_template.html", context)


def initial_state(request, pk):
    context = {}
    semaine = get_object_or_404(Semaines, id=pk)
    #semaine = Semaines.objects.first()
    context["semaine"] = semaine
    return render(request, "hod_template/partial/semaines_list.html", context)

@require_http_methods(["GET"])
def editer_semaines(request, pk):
    context = {}
    semaine = get_object_or_404(Semaines, id=pk)

    form = SemainesForm(instance=semaine)
    context["form"] = form
    context["semaine"] = semaine
    return render(request, "hod_template/partial/editer_semaines.html", context)


def supprimer_semaines(request, pk):
    semaine = get_object_or_404(Semaines, id=pk)

    if request.method == "POST":
        semaine.delete()
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )

#@api_view(["GET", "PUT"])
def detail_semaines(request, pk):

    semaine = get_object_or_404(Semaines, id=pk)
    if request.method == "GET":
        return HttpResponseRedirect(reverse("click-to-edit-initial-state", args=[int(pk)]))
    form = SemainesForm(request.POST, instance=semaine)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("click-to-edit-initial-state", args=[int(pk)]))
    else:
        raise Http404
    

############ Suivi de la progression ########################

def admin_view_progressions(request):
    #matieres = Matieres.objects.all()
    #classess = Classess.objects.all()
    niveaux = Niveaux.objects.all()
    staffs = Staffs.objects.all()
    semaines =Semaines.objects.all()
    semaineslecons =SemainesLecons.objects.all()
    lecons= Lecons.objects.all()
    anneescolaires = AnneeScolaire.objects.all()
    context = {
        #"matieres": matieres,
        #"classess": classess,
        "niveaux": niveaux,
        "staffs": staffs,
        "semaines": semaines,
        "semaineslecons": semaineslecons,
        "lecons": lecons,
        "anneescolaires": anneescolaires
    }
    return render(request, "hod_template/admin_view_progressions.html", context)

#-------------  SUIVRE LES PROGRESSIONS: affichage des classes apres ----#
#                avoir selectionne l'annee scolaire                      #
def modules_classe_name_admin(request):
    anneescolaire = request.GET.get('anneescolaire')  
    staffs = Staffs.objects.filter(annee_scolaire_id_id=anneescolaire)
    matieres = Matieres.objects.filter(professeurs_id_id__in=staffs)
    classess = Classess.objects.filter(id__in=matieres)

    context = {
               'classess' : classess}
    return render(request, 'hod_template/partial/modules_classe_name_admin.html', context)

 
#-------------  SUIVRE LES PROGRESSIONS: affichage des matieres apres ----#
#                avoir selectionne la classe                             #
def modules_matiere_name_admin(request):
    classe = request.GET.get('classe')  
    matieres = Matieres.objects.filter(classes_id_id=classe)
    context = {
               'matieres' : matieres
               }
    return render(request, 'hod_template/partial/modules_matiere_name_admin.html', context)

#-------------  SUIVRE LES PROGRESSIONS: affichage des resultats     ----#
#                de la progression apres avoir selectionne la matiere    #
@csrf_exempt
def admin_get_progression_matiere(request):
    # Getting Values from Ajax POST 'Fetch Student'
    anneescolaire = request.POST.get('anneescolaire')
    classe = request.POST.get('classe')
    matiere = request.POST.get('matiere')

    # recuperer la matiere
    matiere_model = Matieres.objects.get(id=matiere)

    # recuperation de la liste des chapitres  de cette matiere        
    chapitres = Chapitres.objects.filter(matieres_id = matiere)  

    # recuperation des lecons de chaque chapitre
    list_data = []
    for chapitre in chapitres:
        lecons = Lecons.objects.filter(chapitres_id = chapitre.id)
        for lecon in lecons :
            semaineslecons = SemainesLecons.objects.filter(lecons_id = lecon.id)
            for semainelecon in semaineslecons:
                semaines = Semaines.objects.get(id = semainelecon.semaines_id_id)
                data_small = { 
                                "semaines_id"          :semaines.id,
                                "debut_fin_semaines"  :str(semaines.debut_semaines)+" -- "+str(semaines.fin_semaines),
                                "titre_chapitres"     :chapitre.titre_chapitres,
                                "detail_lecons"       :lecon.detail_lecons,
                                "nombre_heures"       :lecon.nombre_heures,
                                "semainelecon_id"     :semainelecon.id,
                                 "statut"              :semainelecon.status,

                                "lecon_id"           :lecon.id,
                                #   "classe"              :classe_model.nom_classes,
                                "matiere"             : matiere_model.nom_matieres,
                              }
                list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)

##############################################################

def add_staff(request):
    return render(request, "hod_template/add_staff_template.html")


def add_staff_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_staff')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            user = CustomUser.objects.create_user(
                username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
            user.staffs.address = address
            user.save()
            messages.success(request, "Staff Added Successfully!")
            return redirect('add_staff')
        except:
            messages.error(request, "Failed to Add Staff!")
            return redirect('add_staff')


def manage_staff(request):
    staffs = Staffs.objects.all()
    context = {
        "staffs": staffs
    }
    return render(request, "hod_template/manage_staff_template.html", context)


def edit_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)

    context = {
        "staff": staff,
        "id": staff_id
    }
    return render(request, "hod_template/edit_staff_template.html", context)


def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get('staff_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')

        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            # INSERTING into Staff Model
            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()

            messages.success(request, "Staff Updated Successfully.")
            return redirect('/edit_staff/'+staff_id)

        except:
            messages.error(request, "Failed to Update Staff.")
            return redirect('/edit_staff/'+staff_id)


def delete_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    try:
        staff.delete()
        messages.success(request, "Staff Deleted Successfully.")
        return redirect('manage_staff')
    except:
        messages.error(request, "Failed to Delete Staff.")
        return redirect('manage_staff')


def add_course(request):
    return render(request, "hod_template/add_course_template.html")


def add_course_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_course')
    else:
        course = request.POST.get('course')
        try:
            course_model = Courses(course_name=course)
            course_model.save()
            messages.success(request, "Course Added Successfully!")
            return redirect('add_course')
        except:
            messages.error(request, "Failed to Add Course!")
            return redirect('add_course')


def manage_course(request):
    courses = Courses.objects.all()
    context = {
        "courses": courses
    }
    return render(request, 'hod_template/manage_course_template.html', context)


def edit_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    context = {
        "course": course,
        "id": course_id
    }
    return render(request, 'hod_template/edit_course_template.html', context)


def edit_course_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        course_id = request.POST.get('course_id')
        course_name = request.POST.get('course')

        try:
            course = Courses.objects.get(id=course_id)
            course.course_name = course_name
            course.save()

            messages.success(request, "Course Updated Successfully.")
            return redirect('/edit_course/'+course_id)

        except:
            messages.error(request, "Failed to Update Course.")
            return redirect('/edit_course/'+course_id)


def delete_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    try:
        course.delete()
        messages.success(request, "Course Deleted Successfully.")
        return redirect('manage_course')
    except:
        messages.error(request, "Failed to Delete Course.")
        return redirect('manage_course')


def manage_session(request):
    session_years = SessionYearModel.objects.all()
    context = {
        "session_years": session_years
    }
    return render(request, "hod_template/manage_session_template.html", context)


def add_session(request):
    return render(request, "hod_template/add_session_template.html")


def add_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_course')
    else:
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        try:
            sessionyear = SessionYearModel(
                session_start_year=session_start_year, session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Session Year added Successfully!")
            return redirect("add_session")
        except:
            messages.error(request, "Failed to Add Session Year")
            return redirect("add_session")


def edit_session(request, session_id):
    session_year = SessionYearModel.objects.get(id=session_id)
    context = {
        "session_year": session_year
    }
    return render(request, "hod_template/edit_session_template.html", context)


def edit_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_session')
    else:
        session_id = request.POST.get('session_id')
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        try:
            session_year = SessionYearModel.objects.get(id=session_id)
            session_year.session_start_year = session_start_year
            session_year.session_end_year = session_end_year
            session_year.save()

            messages.success(request, "Session Year Updated Successfully.")
            return redirect('/edit_session/'+session_id)
        except:
            messages.error(request, "Failed to Update Session Year.")
            return redirect('/edit_session/'+session_id)


def delete_session(request, session_id):
    session = SessionYearModel.objects.get(id=session_id)
    try:
        session.delete()
        messages.success(request, "Session Deleted Successfully.")
        return redirect('manage_session')
    except:
        messages.error(request, "Failed to Delete Session.")
        return redirect('manage_session')


def add_student(request):
    form = AddStudentForm()
    context = {
        "form": form
    }
    return render(request, 'hod_template/add_student_template.html', context)


def add_student_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_student')
    else:
        form = AddStudentForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            session_year_id = form.cleaned_data['session_year_id']
            course_id = form.cleaned_data['course_id']
            gender = form.cleaned_data['gender']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                user = CustomUser.objects.create_user(
                    username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
                user.students.address = address

                course_obj = Courses.objects.get(id=course_id)
                user.students.course_id = course_obj

                session_year_obj = SessionYearModel.objects.get(
                    id=session_year_id)
                user.students.session_year_id = session_year_obj

                user.students.gender = gender
                user.students.profile_pic = profile_pic_url
                user.save()
                messages.success(request, "Student Added Successfully!")
                return redirect('add_student')
            except:
                messages.error(request, "Failed to Add Student!")
                return redirect('add_student')
        else:
            return redirect('add_student')


def manage_student(request):
    students = Students.objects.all()
    context = {
        "students": students
    }
    return render(request, 'hod_template/manage_student_template.html', context)


def edit_student(request, student_id):
    # Adding Student ID into Session Variable
    request.session['student_id'] = student_id

    student = Students.objects.get(admin=student_id)
    form = EditStudentForm()
    # Filling the form with Data from Database
    form.fields['email'].initial = student.admin.email
    form.fields['username'].initial = student.admin.username
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['address'].initial = student.address
    form.fields['course_id'].initial = student.course_id.id
    form.fields['gender'].initial = student.gender
    form.fields['session_year_id'].initial = student.session_year_id.id

    context = {
        "id": student_id,
        "username": student.admin.username,
        "form": form
    }
    return render(request, "hod_template/edit_student_template.html", context)


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        student_id = request.session.get('student_id')
        if student_id == None:
            return redirect('/manage_student')

        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            course_id = form.cleaned_data['course_id']
            gender = form.cleaned_data['gender']
            session_year_id = form.cleaned_data['session_year_id']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                # First Update into Custom User Model
                user = CustomUser.objects.get(id=student_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()

                # Then Update Students Table
                student_model = Students.objects.get(admin=student_id)
                student_model.address = address

                course = Courses.objects.get(id=course_id)
                student_model.course_id = course

                session_year_obj = SessionYearModel.objects.get(
                    id=session_year_id)
                student_model.session_year_id = session_year_obj

                student_model.gender = gender
                if profile_pic_url != None:
                    student_model.profile_pic = profile_pic_url
                student_model.save()
                # Delete student_id SESSION after the data is updated
                del request.session['student_id']

                messages.success(request, "Student Updated Successfully!")
                return redirect('/edit_student/'+student_id)
            except:
                messages.success(request, "Failed to Uupdate Student.")
                return redirect('/edit_student/'+student_id)
        else:
            return redirect('/edit_student/'+student_id)


def delete_student(request, student_id):
    student = Students.objects.get(admin=student_id)
    try:
        student.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect('manage_student')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('manage_student')


def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type='2')
    context = {
        "courses": courses,
        "staffs": staffs
    }
    return render(request, 'hod_template/add_subject_template.html', context)


def add_subject_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_subject')
    else:
        subject_name = request.POST.get('subject')

        course_id = request.POST.get('course')
        course = Courses.objects.get(id=course_id)

        staff_id = request.POST.get('staff')
        staff = CustomUser.objects.get(id=staff_id)

        try:
            subject = Subjects(subject_name=subject_name,
                               course_id=course, staff_id=staff)
            subject.save()
            messages.success(request, "Subject Added Successfully!")
            return redirect('add_subject')
        except:
            messages.error(request, "Failed to Add Subject!")
            return redirect('add_subject')


def manage_subject(request):
    subjects = Subjects.objects.all()
    context = {
        "subjects": subjects
    }
    return render(request, 'hod_template/manage_subject_template.html', context)


def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type='2')
    context = {
        "subject": subject,
        "courses": courses,
        "staffs": staffs,
        "id": subject_id
    }
    return render(request, 'hod_template/edit_subject_template.html', context)


def edit_subject_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject')
        course_id = request.POST.get('course')
        staff_id = request.POST.get('staff')

        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name

            course = Courses.objects.get(id=course_id)
            subject.course_id = course

            staff = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staff

            subject.save()

            messages.success(request, "Subject Updated Successfully.")
            # return redirect('/edit_subject/'+subject_id)
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id": subject_id}))

        except:
            messages.error(request, "Failed to Update Subject.")
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id": subject_id}))
            # return redirect('/edit_subject/'+subject_id)


def delete_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    try:
        subject.delete()
        messages.success(request, "Subject Deleted Successfully.")
        return redirect('manage_subject')
    except:
        messages.error(request, "Failed to Delete Subject.")
        return redirect('manage_subject')


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def student_feedback_message(request):
    feedbacks = FeedBackStudent.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/student_feedback_template.html', context)


@csrf_exempt
def student_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def staff_feedback_message(request):
    feedbacks = FeedBackStaffs.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/staff_feedback_template.html', context)


@csrf_exempt
def staff_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def student_leave_view(request):
    leaves = LeaveReportStudent.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'hod_template/student_leave_view.html', context)


def student_leave_approve(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('student_leave_view')


def student_leave_reject(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('student_leave_view')


def staff_leave_view(request):
    leaves = LeaveReportStaff.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'hod_template/staff_leave_view.html', context)


def staff_leave_approve(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('staff_leave_view')


def staff_leave_reject(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('staff_leave_view')


def admin_view_attendance(request):
    subjects = Subjects.objects.all()
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    return render(request, "hod_template/admin_view_attendance.html", context)


@csrf_exempt
def admin_get_attendance_dates(request):
    # Getting Values from Ajax POST 'Fetch Student'
    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year_id")

    # Students enroll to Course, Course has Subjects
    # Getting all data from subject model based on subject_id
    subject_model = Subjects.objects.get(id=subject_id)

    session_model = SessionYearModel.objects.get(id=session_year)

    # students = Students.objects.filter(course_id=subject_model.course_id, session_year_id=session_model)
    attendance = Attendance.objects.filter(
        subject_id=subject_model, session_year_id=session_model)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for attendance_single in attendance:
        data_small = {"id": attendance_single.id, "attendance_date": str(
            attendance_single.attendance_date), "session_year_id": attendance_single.session_year_id.id}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def admin_get_attendance_student(request):
    # Getting Values from Ajax POST 'Fetch Student'
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in attendance_data:
        data_small = {"id": student.student_id.admin.id, "name": student.student_id.admin.first_name +
                      " "+student.student_id.admin.last_name, "status": student.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context = {
        "user": user
    }
    return render(request, 'hod_template/admin_profile.html', context)


def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')


def staff_profile(request):
    pass


def student_profile(requtest):
    pass
