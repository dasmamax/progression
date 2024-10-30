from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse,Http404
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json


from student_management_app.models import CustomUser, Staffs, AnneeScolaire, Semaines, SemainesLecons, SemainesLeconsReelle, Courses, Subjects, Students, SessionYearModel, Attendance, AttendanceReport, LeaveReportStaff, FeedBackStaffs, StudentResult


#test ********************

from django.http.response import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404

from .models import Lecons, Matieres, Chapitres, Classess, Niveaux
from .forms import ChapitreForm, LeconForm, SemainesForm, StatutForm
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django.db.models import Q # for search rechercher
#for pagination
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
POSTS_PER_PAGE = 5

# gestion de pages intermediaire avant Htmx

def gerer_progressions(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    matieres = Matieres.objects.filter(professeurs_id=staff_obj)
    context = {
        "matieres": matieres,
        "staff": staff_obj
    }
    return render(request, 'staff_template/staff_gerer_progressions_template.html', context)
 

def editer_progessions(request, matieres_id):
   # matiere = Matieres.objects.get(id=matieres_id)
   # classe = Classess.objects.all()
    #staff = Staffs.objects.all()
    context = {
       # "matiere": matiere,
       # "id": matieres_id,
       # "classess": classe,
       # "staffs": staff
    }
    return render(request, 'staff_template/editer_progressions_template.html', context)

# test pagination de la page de gerer progression
 
def gerer_progessions_pagination(request):
    matieres, search = _search_posts_progessions(request)
    staff_obj = Staffs.objects.get(admin=request.user.id)
    context = {"matieres": matieres, "search": search, "staff":staff_obj}
    return render(request, 'staff_template/staff_gerer_progressions_template_pagination.html', context)

def staff_search_progressions_pagination(request):
    matieres, search = _search_posts_progessions(request)
    context = {"matieres": matieres, "search": search}
    return render(request, "staff_template/partials/staff_gerer_progr_list_pag.html", context)
 
def _search_posts_progessions(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    matieres = Matieres.objects.filter(professeurs_id=staff_obj)

    search = request.GET.get("search")
    page = request.GET.get("page")

    # matieres = Matieres.objects.all().order_by("nom_matieres__nom_disciplines")
    if search:
        matieres = matieres.filter(Q(nom_matieres__nom_disciplines__icontains=search) |
                                 Q(classes_id__nom_classes__icontains=search) |
                                 Q(classes_id__niveaux_id__nom_niveaux__icontains=search)) \
        .order_by("nom_matieres__nom_disciplines")

    paginator = Paginator(matieres, POSTS_PER_PAGE)
    try:
        matieres = paginator.page(page)
    except PageNotAnInteger:
        matieres = paginator.page(1)
    except EmptyPage:
        matieres = paginator.page(paginator.num_pages)

    return matieres, search or ""

# fin test pagination 
# fin test pagination 
# fin gestion page intermediaire avant Htmx

#gestion de la progression d'une matiere apres avoir choisi la matiere

def creer_progressions(request, pk):
    staff_obj = Staffs.objects.get(admin=request.user.id) # for new interface of progression with side-bar
    matiere = Matieres.objects.get(id = pk)
    chapitre = Chapitres.objects.filter(matieres_id = matiere) # matieres_id is the FK in Chapitre
    form = ChapitreForm(request.POST or None)
  
    if request.method == "POST":
        if form.is_valid():
            chapitre = form.save(commit=False)
            chapitre.matieres_id = matiere
            chapitre.save()
            return redirect("detail_chapitre", pk=chapitre.id)
        else:
            return render(request, "staff_template/partials/chapitre_form.html", context={
                "form": form
            })

    context = {
        "form": form,
        "staff": staff_obj, # for new interface of progression with side-bar
        "matiere": matiere,
        "chapitres": chapitre
    }
    return render(request, "staff_template/creer_progression.html", context)

def detail_chapitre(request, pk):
    chapitre = get_object_or_404(Chapitres, id=pk)
    lecon = Lecons.objects.filter(chapitres_id = chapitre)
    context = {
        "chapitres": chapitre,
        "lecons"   : lecon
    }
    return render(request, "staff_template/partials/chapitre_detail.html", context)


def create_chapitre_form(request):
    form = ChapitreForm()
    context = {
        "form": form
    }
    return render(request, "staff_template/partials/chapitre_form.html", context)

def update_chapitre(request, pk):
    chapitre = Chapitres.objects.get(id=pk)
    form = ChapitreForm(request.POST or None, instance=chapitre)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("detail_chapitre", pk=chapitre.id)

    context = {
        "form": form,
        "chapitres": chapitre
    }

    return render(request, "staff_template/partials/chapitre_form.html", context)


def delete_chapitre(request, pk):
    chapitre = get_object_or_404(Chapitres, id=pk)

    if request.method == "POST":
        chapitre.delete()
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )


#*************** gestion des lecons *********
def creer_lecons(request, pk):
    annee_scolaire = AnneeScolaire.objects.all()
    staff_obj = Staffs.objects.get(admin=request.user.id) # for new interface of progression with side-bar
    chapitre = Chapitres.objects.get(id = pk)
    
    # recuperation des semaines pour affichages
    semaine = Semaines.objects.filter(annee_scolaire_id = staff_obj.annee_scolaire_id)

    if request.method == "POST":
        form = LeconForm(request.POST)

        # recuperation de la semaines pour enregistrement
        semaine_id = request.POST.get('semaine')
        status = request.POST.get('statut')
       

        if form.is_valid():
            lecon = form.save(commit=False)
            lecon.chapitres_id = chapitre
            lecon.save()

            # enregistrement dans SemainesLecons
            semaine = Semaines.objects.get(id=semaine_id)
            SemainesLecons.objects.create(lecons_id = lecon, semaines_id = semaine, status = status)
            
            response = HttpResponse(status=200)
            response["Hx-Trigger"] = json.dumps({"leconListChanged": None,
                          "showMessage": f"{lecon.detail_lecons} ajoutee."})
            return response
            
    else:
        form = LeconForm()
    return render(request, "staff_template/partials/lecon_form.html", context={
            "form": form,
            "chapitres": chapitre,
            "anneescolaire": annee_scolaire,
            "staff": staff_obj,
            "semaines": semaine.order_by("numero_semaines")
    })


# pour afficher uniquement les lecons correspondant aux chapitres *****
def lecons_detail(request, pk):
    chapitre = get_object_or_404(Chapitres, id=pk)
    lecon = Lecons.objects.filter(chapitres_id = chapitre)

    # recuperation des semaines considerees
    semaineslecons = SemainesLecons.objects.all()
    semaines= Semaines.objects.all()
    
    return render(request, 'staff_template/partials/lecons_detail.html', {
        'lecons': lecon,
        "chapitres": chapitre,
        "semaineslecons": semaineslecons,
        "semaines" : semaines
    })


# pour afficher les lecons sans tenir compte des chapitre  **
#def lecons_detail(request):
    return render(request, 'staff_template/partials/lecons_detail.html', {
        'lecons': Lecons.objects.all(),
    })


#    context = {
#       "form": form,
#        "staff": staff_obj, # for new interface of progression with side-bar
#        "lecon": lecon,
#        "chapitres": chapitre
#    }
#    return render(request, "staff_template/creer_lecon.html", context)

def create_lecon_form(request):
    form = LeconForm()
    context = {
        "form": form
    }
    return render(request, "staff_template/partials/creer_lecon.html", context)

# editer une lecon
# def editer_lecon(request, pk):
#     lecon = get_object_or_404(Lecons, pk=pk)

#     #recuperation du chapitre concerne
#     chapitres = Chapitres.objects.get(id = lecon.chapitres_id_id) 
    

#     # # #recuperation des groupes semainesLecons
#     # semainelecons = SemainesLecons.objects.filter(lecons_id=lecon.id)

#     # # #recuperation de semaines
#     # semaine_R = Semaines.objects.get(id=semainelecon.lecons_id)

#     # # recuperation des semaines considerees
#     # # semaineslecons = SemainesLecons.objects.all()
#     # semaines= Semaines.objects.all()
    

#     if request.method == "POST":
#         form = LeconForm(request.POST, instance=lecon)
#         if form.is_valid():
#             form.save()
#             response = HttpResponse(status=200)
#             response["Hx-Trigger"] = json.dumps({"leconListChanged": None,
#                           "showMessage": f"{lecon.detail_lecons} mise a jour."})
#             return response
#     else:
#         form = LeconForm(instance=lecon)
#     return render(request, 'staff_template/partials/lecon_form.html', {
#         'form': form,
#         'lecons': lecon,
#         'chapitres': chapitres,

#     })

def editer_lecon(request, pk):
    semainelecon = get_object_or_404(SemainesLecons, pk=pk)
    lecon = Lecons.objects.get(id= semainelecon.lecons_id_id)
    semaine_R =  Semaines.objects.get(id= semainelecon.semaines_id_id)
    chapitres = Chapitres.objects.get(id=lecon.chapitres_id_id)

 # recuperation des semaines pour affichages
    staff_obj = Staffs.objects.get(admin=request.user.id) # for new interface of progression with side-bar
    semaines = Semaines.objects.filter(annee_scolaire_id = staff_obj.annee_scolaire_id)

    if request.method == "POST":
        form = LeconForm(request.POST, instance=lecon)
       # recuperation de la semaines pour enregistrement
        semaine_id = request.POST.get('semaine')
        status = request.POST.get('statut')
        if form.is_valid():
            lecons=form.save()

            #  mise a jour semainelecon
            # semainelecon.objects.update(semaine_id=semaine_id, lecons_id= lecons, status=status)
            # SemainesLecons.objects.update(semainelecon, semaines_id=semaine_id, lecons_id= lecons, status=status)
            semaine = Semaines.objects.get(id=semaine_id)
            semainelecon.semaines_id=semaine
            semainelecon.lecons_id= lecons
            semainelecon.status=status
            semainelecon.save()

            response = HttpResponse(status=200)
            response["Hx-Trigger"] = json.dumps({"leconListChanged": None,
                          "showMessage": f"{lecon.detail_lecons} mise a jour."})
            return response
    else:
        form = LeconForm(instance=lecon)
    return render(request, 'staff_template/partials/lecon_form.html', {
        'form': form,
        'lecons': lecon,
        'chapitres': chapitres,
        'semaine_R' :semaine_R,
        'semaines':semaines,
        'semainelecon' : semainelecon,

    })


# Supprimer une lecon
@ require_POST
def supprimer_lecon(request, pk):
    lecon = get_object_or_404(Lecons, pk=pk)
    lecon.delete()
    response = HttpResponse(status=200)
    response["Hx-Trigger"] = json.dumps({"leconListChanged": None,
                          "showMessage": f"{lecon.detail_lecons} supprimee."})
    return response

# def creer_lecons(request, pk):
   
    chapitre = Lecons.objects.get(id = pk)
    lecon = Lecons.objects.filter(chapitres_id = chapitre)

    form = LeconForm(request.POST or None)

    #matiere = Matieres.objects.get(id = pk)
    #chapitre = Chapitres.objects.filter(matieres_id = matiere) # matieres_id is the FK in Chapitre
    #form = ChapitreForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            lecon = form.save(commit=False)
            lecon.chapitres_id = chapitre
            lecon.save()
            return redirect("detail_lecon", pk=lecon.id)
            #chapitre = form.save(commit=False)
            #chapitre.matieres_id = matiere
            #chapitre.save()
            #return redirect("detail_chapitre", pk=chapitre.id)

        else:
            return render(request, "staff_template/partials/lecon_form.html", context={
            #return render(request, "staff_template/partials/chapitre_form.html", context={
                "form": form
            })

    context = {
        "form": form,
        "chapitre": chapitre,
        "lecons": lecon
    }

    #return render(request, "staff_template/creer_progression.html", context)
    return render(request, "staff_template/chapitre_detail.html", context)
 
#******************* gestion du suivi de la progression *************************
#******************* a partir de gerer les progressions ************************
def staff_suivi_progression (request, pk): #ancien
    staff_obj = Staffs.objects.get(admin=request.user.id)
   
    # recuperation de la matiere
    matiere = Matieres.objects.get(id = pk) 

    # recuperation de la liste des chapitres          
    chapitres = Chapitres.objects.filter(matieres_id = matiere.id)  
    
    #recuperation de la classe 
    classess = Classess.objects.get(id = matiere.classes_id_id)  

    lecons = Lecons.objects.all()
    semaines = Semaines.objects.all()
    semaineslecons = SemainesLecons.objects.all()

    #recuperation de l'annee scolaire
    anneescolaire = AnneeScolaire.objects.get(id = staff_obj.annee_scolaire_id_id)

    context = {
                "anneescolaire" : anneescolaire,
                "staff_obj"     : staff_obj,
                "chapitres"     : chapitres,
                "lecons"        : lecons,
                "semaines"      : semaines,
                "semaineslecons" : semaineslecons,
                "matieres"      : matiere,
                "classess"      :  classess
                }

    #( 
    # le fichier staff_suivi_progression2.html est la methode d'envoi de la 
    #  progression a l'administrateur pour evaluation.
    #return render(request, "staff_template/staff_suivi_progression2.html", context)
    #)
    return render(request, "staff_template/staff_suivi_progression.html", context)

def staff_search_progressions(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    matieres = Matieres.objects.filter(professeurs_id=staff_obj)
    q= request.GET.get('q')
    print(q)
     
    if q:
        # results =Matieres.objects.filter(Q(nom_matieres__nom_disciplines__icontains=q)) \
        results =matieres.filter(Q(nom_matieres__nom_disciplines__icontains=q) |
                                 Q(classes_id__nom_classes__icontains=q) |
                                 Q(classes_id__niveaux_id__nom_niveaux__icontains=q)) \
        .order_by("nom_matieres__nom_disciplines", "-id")[0:20] 
    else:
        results=[]
 
    return render(request, "staff_template/partials/search/staff_search_progressions.html", {"results":results})

#def staff_creer_MAJ_progession(request, pk): # pk = SemainesLecons.id
    semainelecon = get_object_or_404(SemainesLecons, id=pk)
    lecon = Lecons.objects.get(id= semainelecon.lecons_id_id)
    
 # recuperation des semaines pour affichages
    staff_obj = Staffs.objects.get(admin=request.user.id) # for new interface of progression with side-bar
    semaines = Semaines.objects.filter(annee_scolaire_id = staff_obj.annee_scolaire_id)

    if request.method == "POST":
        form = StaffMAJForm(request.POST) # nombre_heure R

        # recuperation de la semaines pour enregistrement
        semaine_id = request.POST.get('semaine')
        status = request.POST.get('statut')
       

        if form.is_valid():
            # lecon = form.save(commit=False)
            # lecon.chapitres_id = chapitre
            # lecon.save()

            # enregistrement dans SemainesLecons
            semaine = Semaines.objects.get(id=semaine_id)
            SemainesLecons.objects.create(lecons_id = lecon, semaines_id = semaine, status = status)
            
            response = HttpResponse(status=200)
            response["Hx-Trigger"] = json.dumps({"leconListChanged": None,
                          "showMessage": f"{lecon.detail_lecons} ajoutee."})
            return response
            
    else:
        form =StaffMAJForm()
    return render(request, "staff_template/partials/staff_MAJ_form.html", context={
            "form": form,
            "staff": staff_obj,
            "semaines": semaines, 
            "lecon" : lecon,
            "semainelecon": semainelecon
    })

def staff_editer_MAJ_progression():
    pass

def staff_supprimer_MAJ_progression():
    pass

def editer_status(request, pk):
    context = {}
    semainelecon = get_object_or_404(SemainesLecons, id=pk)
    #-------- MAJ
    #semainelecon = get_object_or_404(SemainesLecons, pk=pk)
    #lecon = Lecons.objects.get(id= semainelecon.lecons_id_id)
    #semaine_R =  Semaines.objects.get(id= semainelecon.semaines_id_id)
    
 # recuperation des semaines pour affichages
    #staff_obj = Staffs.objects.get(admin=request.user.id) # for new interface of progression with side-bar
    #semaines = Semaines.objects.filter(annee_scolaire_id = staff_obj.annee_scolaire_id)
#----------- Fin MAJ


    if request.method == "POST":
        form = StatutForm(request.POST, instance=semainelecon)
       # recuperation du statut pour enregistrement
        if form.is_valid():
            status=form.save()
            #  mise a jour semainelecon
            semainelecon.status=status
            response = HttpResponse(status=200)
            response["Hx-Trigger"] = json.dumps({"statutChanged": None,
                          "showMessage": f"{semainelecon.status} mise a jour."})
            return response
    else:
        #form_LeconForm = LeconForm(instance=lecon)
        form = StatutForm(instance=semainelecon)
        context["form"] = form
        context["semainelecon"] = semainelecon
        #--------- MAJ
        #context["semaines"] = semaines
        #context["semaine_R"] =semaine_R
        #context["form_leconForm"] = form_LeconForm
        #-------- MAJ
    return render(request, "staff_template/partials/editer_status_modal.html", context)


# **************** Pour envoyer le suivi de la progression a l'administrateur
#  *************** methode pour evaluation, avec staff_suivi_progression2.html
def staff_apply_leave_save1(request, pk):
    matieres = Matieres.objects.get(id = pk) 
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('staff_suivi_progression', pk=matieres.id)
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        staff_obj = Staffs.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStaff(staff_id=staff_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('staff_suivi_progression', pk=matieres.id)
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('staff_suivi_progression', pk=matieres.id)


def staff_progression_list(request, pk):
    matiere = Matieres.objects.get(id = pk) 

    # recuperation de la liste des chapitres          
    chapitres = Chapitres.objects.filter(matieres_id = matiere.id)  
    
    #recuperation de la classe 
    #classess = Classess.objects.get(id = matiere.classes_id_id)  

    lecons = Lecons.objects.all()
    semaines = Semaines.objects.all()
    semaineslecons = SemainesLecons.objects.all()

#--------------------- list trie----------------------------
    staff_suivi_progression_list =[]
    # semlecon_list=[]
    list=[]
    for chapitre in chapitres:
        for lecon in lecons:   
            if chapitre.id == lecon.chapitres_id_id:    # <!--recuperation des lecons du chapitre -->
                for semainelecon in semaineslecons:
                    if semainelecon.lecons_id_id == lecon.id:  # <!--recuperation des semaineslecons (statuts)      -->
                        for semaine in semaines:  
                            if semainelecon.semaines_id_id == semaine.id:  #<!--recuperation de la semaine -->
                                ay= str(semaine.debut_semaines) + " au " + str(semaine.fin_semaines)
                                # if semainelecon.status == '1':
                                #     leconstatut= "En attente"
                                # elif semainelecon.status == '2':
                                #     leconstatut= "En cours"
                                # elif semainelecon.status == '3':
                                #     leconstatut= "Termine"
                                list=[semaine.numero_semaines,
                                      ay,
                                    #   [semaine.debut_semaines,semaine.fin_semaines],
                                      chapitre.titre_chapitres,
                                      lecon.detail_lecons,
                                      lecon.nombre_heures,
                                    #   leconstatut,
                                      semainelecon.status,
                                      semainelecon.id
                                     ]
                                staff_suivi_progression_list.append(list)
                                # semlecon_list.append(semainelecon)
    context = {
        "staff_suivi_progression_list":sorted(staff_suivi_progression_list)
    } 
#--------------------- fin trie ---------------------------------
    # context = {
    #             "chapitres"     : chapitres,
    #             "lecons"        : lecons,
    #             "semaines"      : semaines,
    #             "semaineslecons" : semaineslecons,
    #             "matieres"      : matiere,
    #             }
    # return render(request, "staff_template/partials/staff_progression_list.html", context)
    return render(request, "staff_template/partials/staff_progression_list_trie.html", context)



#@api_view(["GET", "PUT"])
# def detail_status(request, pk):

#     semainelecon = get_object_or_404(SemainesLecons, id=pk)
#     if request.method == "GET":
#         return HttpResponseRedirect(reverse("click-pour-edit-initial-state", args=[int(pk)]))
#     form = StatutForm(request.POST, instance=semainelecon)
#     if form.is_valid():
#         form.save()
#         return HttpResponseRedirect(reverse("click-pour-edit-initial-state", args=[int(pk)]))
#     else:
#         raise Http404


#*********************************************
def staff_home(request):
    # Fetching All Students under Staff

    staff_obj = Staffs.objects.get(admin=request.user.id)
    matieres = Matieres.objects.filter(professeurs_id=staff_obj)

    classes_id_list = []
    for matiere in matieres:
        classe = Classess.objects.get(id=matiere.classes_id.id)
        classes_id_list.append(classe.id)
    
    # Remove the duplicate classes in list of classes' ids
    final_classe = []
    for classe_id in classes_id_list :
        if classe_id not in final_classe:
            final_classe.append(classe_id)

    # count classes and matieres
    classes_count = len(final_classe)
    matieres_count = matieres.count()

    # Fetching volume horaire total
    chapitres = Chapitres.objects.filter(matieres_id__in=matieres)
    lecons = Lecons.objects.filter(chapitres_id__in=chapitres)
    hours_list = []
    for lecon in lecons:
        hour = lecon.nombre_heures
        hours_list.append(hour)
    hours_count= sum(hours_list)

    # Fetching status of lecons of all the courses of the staff
    lecons_attente_gle_count = SemainesLecons.objects.filter(lecons_id__in=lecons, status= '1').count()
    lecons_encours_gle_count = SemainesLecons.objects.filter(lecons_id__in=lecons, status= '2').count()
    lecons_termine_gle_count = SemainesLecons.objects.filter(lecons_id__in=lecons, status= '3').count()

    # Fetching the status of lecons per courses
    matiere_list =[]
    lecons_attente_list=[]
    lecons_encours_list=[]
    lecons_termine_list=[]
    for matiere in matieres:
        matiere_list.append(matiere.nom_matieres.nom_disciplines+" "+matiere.classes_id.nom_classes) 
        # find chapters of one matiere
        chapitres = Chapitres.objects.filter(matieres_id_id=matiere.id)
        # Find list of lessons
        lecons = Lecons.objects.filter(chapitres_id__in=chapitres)
        lecons_attente_count = SemainesLecons.objects.filter(lecons_id__in=lecons, status= '1').count()
        lecons_encours_count = SemainesLecons.objects.filter(lecons_id__in=lecons, status= '2').count()
        lecons_termine_count = SemainesLecons.objects.filter(lecons_id__in=lecons, status= '3').count()
        lecons_attente_list.append(lecons_attente_count)
        lecons_encours_list.append(lecons_encours_count)
        lecons_termine_list.append(lecons_termine_count)
#*************************************** comment *************************************************
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    course_id_list = []
    for subject in subjects:
        course = Courses.objects.get(id=subject.course_id.id)
        course_id_list.append(course.id)
    
    final_course = []
    # Removing Duplicate Course Id
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)
    
    
    students_count = Students.objects.filter(course_id__in=final_course).count()
    subject_count = subjects.count()
#*****************************************************************************************
    # Fetch All Attendance Count
    attendance_count = Attendance.objects.filter(subject_id__in=subjects).count()
    # Fetch All Approve Leave
    staff = Staffs.objects.get(admin=request.user.id)
    leave_count = LeaveReportStaff.objects.filter(staff_id=staff.id, leave_status=1).count()

    #Fetch Attendance Data by Subjects
    subject_list = []
    attendance_list = []
    for subject in subjects:
        attendance_count1 = Attendance.objects.filter(subject_id=subject.id).count()
        subject_list.append(subject.subject_name)
        attendance_list.append(attendance_count1)

    students_attendance = Students.objects.filter(course_id__in=final_course)
    student_list = []
    student_list_attendance_present = []
    student_list_attendance_absent = []
    for student in students_attendance:
        attendance_present_count = AttendanceReport.objects.filter(status=True, student_id=student.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(status=False, student_id=student.id).count()
        student_list.append(student.admin.first_name+" "+ student.admin.last_name)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)

    context={
        "classes_count": classes_count,
        "matieres_count": matieres_count,
        "hours_count": hours_count,
        "lecons_attente_gle_count" : lecons_attente_gle_count,
        "lecons_encours_gle_count" :lecons_encours_gle_count,
        "lecons_termine_gle_count" :lecons_termine_gle_count,
        "matiere_list":matiere_list,
        "lecons_attente_list" :lecons_attente_list,
        "lecons_encours_list":lecons_encours_list,
        "lecons_termine_list":lecons_termine_list,

        "students_count": students_count,
        "attendance_count": attendance_count,
        "leave_count": leave_count,
        "subject_count": subject_count,
        "subject_list": subject_list,
        "attendance_list": attendance_list,
        "student_list": student_list,
        "attendance_present_list": student_list_attendance_present,
        "attendance_absent_list": student_list_attendance_absent
    }
    return render(request, "staff_template/staff_home_template.html", context)
 

# def staff_home(request):
    # Fetching All Students under Staff

    subjects = Subjects.objects.filter(staff_id=request.user.id)
    course_id_list = []
    for subject in subjects:
        course = Courses.objects.get(id=subject.course_id.id)
        course_id_list.append(course.id)
    
    final_course = []
    # Removing Duplicate Course Id
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)
    
    students_count = Students.objects.filter(course_id__in=final_course).count()
    subject_count = subjects.count()

    # Fetch All Attendance Count
    attendance_count = Attendance.objects.filter(subject_id__in=subjects).count()
    # Fetch All Approve Leave
    staff = Staffs.objects.get(admin=request.user.id)
    leave_count = LeaveReportStaff.objects.filter(staff_id=staff.id, leave_status=1).count()

    #Fetch Attendance Data by Subjects
    subject_list = []
    attendance_list = []
    for subject in subjects:
        attendance_count1 = Attendance.objects.filter(subject_id=subject.id).count()
        subject_list.append(subject.subject_name)
        attendance_list.append(attendance_count1)

    students_attendance = Students.objects.filter(course_id__in=final_course)
    student_list = []
    student_list_attendance_present = []
    student_list_attendance_absent = []
    for student in students_attendance:
        attendance_present_count = AttendanceReport.objects.filter(status=True, student_id=student.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(status=False, student_id=student.id).count()
        student_list.append(student.admin.first_name+" "+ student.admin.last_name)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)

    context={
        "students_count": students_count,
        "attendance_count": attendance_count,
        "leave_count": leave_count,
        "subject_count": subject_count,
        "subject_list": subject_list,
        "attendance_list": attendance_list,
        "student_list": student_list,
        "attendance_present_list": student_list_attendance_present,
        "attendance_absent_list": student_list_attendance_absent
    }
    return render(request, "staff_template/staff_home_template.html", context)


#***************************** gestion du suivi de la progression ******************
#***************************** a partir de suivre les progressions (menu lateral)***
def staff_take_attendance(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    matieres = Matieres.objects.filter(professeurs_id=staff_obj)
    context = {
        "matieres": matieres,
        "staff": staff_obj
    }
    
    return render(request, "staff_template/take_attendance_template.html", context)


# -------------- modules d'affichage automatique de la classe------#
#                  apres selection de la matiere                   #
def modules_classe_name(request):
    matiere_id = request.GET.get('matiere')  # matiere = matiere.id
    matiere = Matieres.objects.get(id=matiere_id)
    classe_name =  matiere.classes_id.nom_classes
    # modules = Module.objects.filter(course=course)
    context = {'classe_name': classe_name}
    return render(request, 'staff_template/partials/modules_classe_name.html', context)


# ------------------ module recupration des donnees pour affichage dans -#
#                    le tableau apres selection de la matiere            #
#                     WE don't need csrf_token when using Ajax
@csrf_exempt
def get_students(request):

    # Getting Values from Ajax POST 'Fetch Student'
    # classe_id = request.POST.get("classe")                        # subject
    matiere = request.POST.get("matiere")                 # session_year

    # Students enroll to Course, Course has Subjects
    # Getting all data from subject model based on subject_id
    # classe_model = Classess.objects.get(id=classe_id)

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
                                "matiere"             : matiere_model.nom_matieres.nom_disciplines,
                              } 
                list_data.append(data_small)
 

    # students = Students.objects.filter(course_id=subject_model.course_id, session_year_id=session_model)

    # Only Passing Student Id and Student Name Only
    # list_data = []

    # for student in students:
    #     data_small={"id":student.admin.id, "name":student.admin.first_name+" "+student.admin.last_name}
    #     list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)
 
#-----------------Mise a jour des statuts de toutes les ------------#
#                lecons de tous les chapitres d'un cours donnee     #
@csrf_exempt
def update_attendance_data(request):
    # Get Values from Staf Take Attendance form via AJAX (JavaScript)
    # Use getlist to access HTML Array/List Input Data
   
    #student_ids = request.POST.get("student_ids")                           # for json_student == json_lecon
    lecon_ids = request.POST.get("student_ids") 
    semaine_ids = request.POST.get("semaine_ids") 
    
    #subject_id = request.POST.get("subject_id")                            # for attendance        == semaine
    # subject_id = request.POST.get("subject_id")

    # attendance_date = request.POST.get("attendance_date")                   # for attendance        == semaine
   
    # session_year_id = request.POST.get("session_year_id")                   # for attendance        == semaine

    # subject_model = Subjects.objects.get(id=subject_id)
    # session_year_model = SessionYearModel.objects.get(id=session_year_id)

    #json_student = json.loads(student_ids)
    json_lecon = json.loads(lecon_ids)
    json_semaine = json.loads(semaine_ids)
    

    # print(student_ids)
    try:
        # First Attendance Data is Saved on Attendance Model                / attendance == semaine
        # attendance = Attendance(subject_id=subject_model, attendance_date=attendance_date, session_year_id=session_year_model)
        # attendance.save()

        for stud in json_lecon:
            # Attendance of Individual Student saved on AttendanceReport Model
            #student = Students.objects.get(admin=stud['id'])
            lecon = Lecons.objects.get(admin=stud['id'])
            semaine = Semaines.objects.get(admin=stud['semaine_id'])
            # attendance_report = AttendanceReport(student_id=student, 
            #                                      attendance_id=attendance, 
            #                                      status=stud['status'])
            semainelecon = SemainesLecons.objects.get(lecons_id=lecon, 
                                                 semaines_id=semaine, 
                                                 status=stud['status'])
            # attendance_report.save()
            semainelecon.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")




# def staff_take_attendance(request):
#     subjects = Subjects.objects.filter(staff_id=request.user.id)
#     session_years = SessionYearModel.objects.all()
#     context = {
#         "subjects": subjects,
#         "session_years": session_years
#     }
#     return render(request, "staff_template/take_attendance_template.html", context)


def staff_apply_leave(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    leave_data = LeaveReportStaff.objects.filter(staff_id=staff_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, "staff_template/staff_apply_leave_template.html", context)


def staff_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('staff_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        staff_obj = Staffs.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStaff(staff_id=staff_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('staff_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('staff_apply_leave')


def staff_feedback(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    feedback_data = FeedBackStaffs.objects.filter(staff_id=staff_obj)
    context = {
        "feedback_data":feedback_data
    }
    return render(request, "staff_template/staff_feedback_template.html", context)

def staff_search_feedback(request):
    q= request.GET.get('q')
    print(q)
 
    if q:
        results =FeedBackStaffs.objects.filter(Q(feedback__icontains=q) | Q(feedback_reply__icontains=q) | Q(staff_id__admin__first_name__icontains=q) | Q(staff_id__admin__last_name__icontains=q)) \
        .order_by("feedback", "-id")[0:20]
 
    else:
        results=[]
 
    return render(request, "staff_template/partials/search/staff_search_feedback.html", {"results":results})


def staff_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('staff_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        staff_obj = Staffs.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStaffs(staff_id=staff_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Message envoye.")
            return redirect('staff_feedback')
        except:
            messages.error(request, "Echec d'envoi.")
            return redirect('staff_feedback')





@csrf_exempt
def save_attendance_data(request):
    # Get Values from Staf Take Attendance form via AJAX (JavaScript)
    # Use getlist to access HTML Array/List Input Data
    student_ids = request.POST.get("student_ids")
    subject_id = request.POST.get("subject_id")
    attendance_date = request.POST.get("attendance_date")
    session_year_id = request.POST.get("session_year_id")

    subject_model = Subjects.objects.get(id=subject_id)
    session_year_model = SessionYearModel.objects.get(id=session_year_id)

    json_student = json.loads(student_ids)
    # print(dict_student[0]['id'])

    # print(student_ids)
    try:
        # First Attendance Data is Saved on Attendance Model
        attendance = Attendance(subject_id=subject_model, attendance_date=attendance_date, session_year_id=session_year_model)
        attendance.save()

        for stud in json_student:
            # Attendance of Individual Student saved on AttendanceReport Model
            student = Students.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport(student_id=student, attendance_id=attendance, status=stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")



def staff_update_attendance(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    return render(request, "staff_template/update_attendance_template.html", context)

@csrf_exempt
def get_attendance_dates(request):
    

    # Getting Values from Ajax POST 'Fetch Student'
    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year_id")

    # Students enroll to Course, Course has Subjects
    # Getting all data from subject model based on subject_id
    subject_model = Subjects.objects.get(id=subject_id)

    session_model = SessionYearModel.objects.get(id=session_year)

    # students = Students.objects.filter(course_id=subject_model.course_id, session_year_id=session_model)
    attendance = Attendance.objects.filter(subject_id=subject_model, session_year_id=session_model)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for attendance_single in attendance:
        data_small={"id":attendance_single.id, "attendance_date":str(attendance_single.attendance_date), "session_year_id":attendance_single.session_year_id.id}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def get_attendance_student(request):
    # Getting Values from Ajax POST 'Fetch Student'
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id, "name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name, "status":student.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


# @csrf_exempt
# def update_attendance_data(request):
    student_ids = request.POST.get("student_ids")

    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    json_student = json.loads(student_ids)

    try:
        
        for stud in json_student:
            # Attendance of Individual Student saved on AttendanceReport Model
            student = Students.objects.get(admin=stud['id'])

            attendance_report = AttendanceReport.objects.get(student_id=student, attendance_id=attendance)
            attendance_report.status=stud['status']

            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")




def staff_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff = Staffs.objects.get(admin=user)

    context={
        "user": user,
        "staff": staff
    }
    return render(request, 'staff_template/staff_profile.html', context)


def staff_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('staff_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save() 

            staff = Staffs.objects.get(admin=customuser.id)
            staff.address = address
            staff.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('staff_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('staff_profile')



def staff_add_result(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years,
    }
    return render(request, "staff_template/add_result_template.html", context)


def staff_add_result_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('staff_add_result')
    else:
        student_admin_id = request.POST.get('student_list')
        assignment_marks = request.POST.get('assignment_marks')
        exam_marks = request.POST.get('exam_marks')
        subject_id = request.POST.get('subject')

        student_obj = Students.objects.get(admin=student_admin_id)
        subject_obj = Subjects.objects.get(id=subject_id)

        try:
            # Check if Students Result Already Exists or not
            check_exist = StudentResult.objects.filter(subject_id=subject_obj, student_id=student_obj).exists()
            if check_exist:
                result = StudentResult.objects.get(subject_id=subject_obj, student_id=student_obj)
                result.subject_assignment_marks = assignment_marks
                result.subject_exam_marks = exam_marks
                result.save()
                messages.success(request, "Result Updated Successfully!")
                return redirect('staff_add_result')
            else:
                result = StudentResult(student_id=student_obj, subject_id=subject_obj, subject_exam_marks=exam_marks, subject_assignment_marks=assignment_marks)
                result.save()
                messages.success(request, "Result Added Successfully!")
                return redirect('staff_add_result')
        except:
            messages.error(request, "Failed to Add Result!")
            return redirect('staff_add_result')


#******************debut test book **************************
def home_book(request):
    form = BookForm()
    context = {
        "form": form
    }
    return render(request, "staff_template/create_book.html", context)
   
def create_book(request, pk):
    author = Author.objects.get(id=pk)
    books = Book.objects.filter(author=author)
    form = BookForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            book = form.save(commit=False)
            book.author = author
            book.save()
            return redirect("detail-book", pk=book.id)
        else:
            return render(request, "staff_template/partials/book_form.html", context={
                "form": form
            })

    context = {
        "form": form,
        "author": author,
        "books": books
    }

    return render(request, "staff_template/create_book.html", context)


def update_book(request, pk):
    book = Book.objects.get(id=pk)
    form = BookForm(request.POST or None, instance=book)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("detail-book", pk=book.id)

    context = {
        "form": form,
        "book": book
    }

    return render(request, "staff_template/partials/book_form.html", context)


def delete_book(request, pk):
    book = get_object_or_404(Book, id=pk)

    if request.method == "POST":
        book.delete()
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )


def detail_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    context = {
        "book": book
    }
    return render(request, "staff_template/partials/book_detail.html", context)


def create_book_form(request):
    form = BookForm()
    context = {
        "form": form
    }
    return render(request, "staff_template/partials/book_form.html", context)

# fin test ***************