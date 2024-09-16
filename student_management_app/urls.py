
from django.urls import path, include
from . import views
from .import HodViews, StaffViews, StudentViews, StudentViewss


#test ****************

#from django.contrib import admin
#from django.urls import path
from django.views.generic import TemplateView

from student_management_app.StaffViews import (
    create_book,
    create_book_form,
    detail_book,
    update_book,
    delete_book,
    home_book,

    creer_progressions,
    detail_chapitre,
    create_chapitre_form,
    update_chapitre,
    delete_chapitre,

    creer_lecons,
    lecons_detail,
    editer_lecon,
    supprimer_lecon
    #create_lecon_form
   
)

#fin test ****************

urlpatterns = [
    
    #test ********************************

     path('gerer_progressions/', StaffViews.gerer_progressions, name="gerer_progressions"),
     path('matiere/<pk>/', creer_progressions, name='creer_progressions'),
     path('htmx/chapitre/<pk>/', detail_chapitre, name="detail_chapitre"),
     path('create_chapitre_form/', create_chapitre_form, name='create_chapitre_form'),
     #path('creer_chapitre/', creer_chapitre, name='creer_chapitre'),
     path('htmx/chapitre/<pk>/update/', update_chapitre, name="update_chapitre"),
     path('htmx/chapitre/<pk>/delete/', delete_chapitre, name="delete_chapitre"),

     # ************ for lecon************
     path('creer_lecons/<pk>/', creer_lecons, name='creer_lecons'),
     path('lecons_detail/<pk>', lecons_detail, name='lecons_detail'),
     path('lecons_detail/<pk>/editer', editer_lecon, name='editer_lecon'),
     path('lecons_detail/<pk>/supprimer', supprimer_lecon, name='supprimer_lecon'),
     #path('create_lecon_form/', create_lecon_form, name='create_lecon_form'),

     

    #path('admin/', admin.site.urls),
   #path('', TemplateView.as_view(template_name="home.html"), name='create-book'),
    path('home_book/', home_book, name='home_book'),
    path('create_book/', create_book, name='create_book'),
    path('htmx/book/<pk>/', detail_book, name="detail-book"),
    path('htmx/book/<pk>/update/', update_book, name="update-book"),
    path('htmx/book/<pk>/delete/', delete_book, name="delete-book"),
    path('htmx/create_book_form/', create_book_form, name='create_book_form'),



    # fin test ****************************



    path('', views.loginPage, name="login"),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('get_user_details/', views.get_user_details, name="get_user_details"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('admin_home/', HodViews.admin_home, name="admin_home"),
    path('add_staff/', HodViews.add_staff, name="add_staff"),
    path('add_staff_save/', HodViews.add_staff_save, name="add_staff_save"),
    path('manage_staff/', HodViews.manage_staff, name="manage_staff"),
    path('edit_staff/<staff_id>/', HodViews.edit_staff, name="edit_staff"),
    path('edit_staff_save/', HodViews.edit_staff_save, name="edit_staff_save"),
    path('delete_staff/<staff_id>/', HodViews.delete_staff, name="delete_staff"),
    path('add_course/', HodViews.add_course, name="add_course"),
    path('add_course_save/', HodViews.add_course_save, name="add_course_save"),
    path('manage_course/', HodViews.manage_course, name="manage_course"),
    path('edit_course/<course_id>/', HodViews.edit_course, name="edit_course"),
    path('edit_course_save/', HodViews.edit_course_save, name="edit_course_save"),
    path('delete_course/<course_id>/',
         HodViews.delete_course, name="delete_course"),
    path('manage_session/', HodViews.manage_session, name="manage_session"),
    path('add_session/', HodViews.add_session, name="add_session"),
    path('add_session_save/', HodViews.add_session_save, name="add_session_save"),
    path('edit_session/<session_id>', HodViews.edit_session, name="edit_session"),
    path('edit_session_save/', HodViews.edit_session_save,
         name="edit_session_save"),
    path('delete_session/<session_id>/',
         HodViews.delete_session, name="delete_session"),
    path('add_student/', HodViews.add_student, name="add_student"),
    path('add_student_save/', HodViews.add_student_save, name="add_student_save"),
    path('edit_student/<student_id>', HodViews.edit_student, name="edit_student"),
    path('edit_student_save/', HodViews.edit_student_save,
         name="edit_student_save"),
    path('manage_student/', HodViews.manage_student, name="manage_student"),
    path('delete_student/<student_id>/',
         HodViews.delete_student, name="delete_student"),
    path('add_subject/', HodViews.add_subject, name="add_subject"),
    path('add_subject_save/', HodViews.add_subject_save, name="add_subject_save"),
    path('manage_subject/', HodViews.manage_subject, name="manage_subject"),
    path('edit_subject/<subject_id>/',
         HodViews.edit_subject, name="edit_subject"),
    path('edit_subject_save/', HodViews.edit_subject_save,
         name="edit_subject_save"),
    path('delete_subject/<subject_id>/',
         HodViews.delete_subject, name="delete_subject"),
    path('check_email_exist/', HodViews.check_email_exist,
         name="check_email_exist"),
    path('check_username_exist/', HodViews.check_username_exist,
         name="check_username_exist"),
    path('student_feedback_message/', HodViews.student_feedback_message,
         name="student_feedback_message"),
    path('student_feedback_message_reply/', HodViews.student_feedback_message_reply,
         name="student_feedback_message_reply"),
    path('staff_feedback_message/', HodViews.staff_feedback_message,
         name="staff_feedback_message"),
    path('staff_feedback_message_reply/', HodViews.staff_feedback_message_reply,
         name="staff_feedback_message_reply"),
         #----- feedback search-----
     path('admin_search_feedback/', HodViews.admin_search_feedback,
         name="admin_search_feedback"),
         
    path('student_leave_view/', HodViews.student_leave_view,
         name="student_leave_view"),
    path('student_leave_approve/<leave_id>/',
         HodViews.student_leave_approve, name="student_leave_approve"),
    path('student_leave_reject/<leave_id>/',
         HodViews.student_leave_reject, name="student_leave_reject"),
    path('staff_leave_view/', HodViews.staff_leave_view, name="staff_leave_view"),
    path('staff_leave_approve/<leave_id>/',
         HodViews.staff_leave_approve, name="staff_leave_approve"),
    path('staff_leave_reject/<leave_id>/',
         HodViews.staff_leave_reject, name="staff_leave_reject"),
    path('admin_view_attendance/', HodViews.admin_view_attendance,
         name="admin_view_attendance"),
    path('admin_get_attendance_dates/', HodViews.admin_get_attendance_dates,
         name="admin_get_attendance_dates"),
    path('admin_get_attendance_student/', HodViews.admin_get_attendance_student,
         name="admin_get_attendance_student"),
    path('admin_profile/', HodViews.admin_profile, name="admin_profile"),
    path('admin_profile_update/', HodViews.admin_profile_update,
         name="admin_profile_update"),

    # Syllabus
    path('creer_annees_scolaires/', HodViews.creer_annees_scolaires, name="creer_annees_scolaires"),
    path('creer_annees_scolaires_save/', HodViews.creer_annees_scolaires_save, name="creer_annees_scolaires_save"),
    path('manage_sessionAnnee/', HodViews.manage_sessionAnnee, name="manage_sessionAnnee"),
#     path('add_sessionAnnee/', HodViews.add_sessionAnnee, name="add_sessionAnnee"),
#     path('add_session_saveAnnee/', HodViews.add_session_saveAnnee, name="add_session_saveAnnee"),
    path('admin_search_annee/', HodViews.admin_search_annee, name="admin_search_annee"),
    path('edit_sessionAnnee/<session_id>', HodViews.edit_sessionAnnee, name="edit_sessionAnnee"),
    path('edit_session_saveAnnee/', HodViews.edit_session_saveAnnee,
         name="edit_session_saveAnnee"),
    path('delete_sessionAnnee/<session_id>/',
         HodViews.delete_sessionAnnee, name="delete_sessionAnnee"),

    path('creer_niveaux/', HodViews.creer_niveaux, name="creer_niveaux"),
    path('creer_niveaux_save/', HodViews.creer_niveaux_save,
         name="creer_niveaux_save"),
    path('gerer_niveaux/', HodViews.gerer_niveaux, name="gerer_niveaux"),
    path('admin_search_niveaux/', HodViews.admin_search_niveaux, name="admin_search_niveaux"),
    
    path('editer_niveaux/<niveaux_id>/',
         HodViews.editer_niveaux, name="editer_niveaux"),
    path('editer_niveaux_save/', HodViews.editer_niveaux_save,
         name="editer_niveaux_save"),
    path('supprimer_niveaux/<niveaux_id>/',
         HodViews.supprimer_niveaux, name="supprimer_niveaux"),

    path('creer_matieres/', HodViews.creer_matieres, name="creer_matieres"),
    path('creer_matieres_save/', HodViews.creer_matieres_save,
         name="creer_matieres_save"),
    path('modules_profs_name_admin/', HodViews.modules_profs_name_admin, name="modules_profs_name_admin"),
    path('modules_profs_edit_name_admin/', HodViews.modules_profs_edit_name_admin, name="modules_profs_edit_name_admin"),
    path('gerer_matieres/', HodViews.gerer_matieres, name="gerer_matieres"),
    path('admin_search_matieres/', HodViews.admin_search_matieres, name="admin_search_matieres"),
    path('editer_matieres/<matieres_id>/',
         HodViews.editer_matieres, name="editer_matieres"),
    path('editer_matieres_save/', HodViews.editer_matieres_save,
         name="editer_matieres_save"),
    path('supprimer_matieres/<matieres_id>/',
         HodViews.supprimer_matieres, name="supprimer_matieres"),

    path('creer_classes/', HodViews.creer_classes, name="creer_classes"),
    path('creer_classes_save/', HodViews.creer_classes_save,
         name="creer_classes_save"),
    path('gerer_classes/', HodViews.gerer_classes, name="gerer_classes"),
    path('admin_search_classes/', HodViews.admin_search_classes, name="admin_search_classes"),
    path('editer_classes/<classes_id>/',
         HodViews.editer_classes, name="editer_classes"),
    path('editer_classes_save/', HodViews.editer_classes_save,
         name="editer_classes_save"),
    path('supprimer_classes/<classes_id>/',
         HodViews.supprimer_classes, name="supprimer_classes"),

     path('creer_professeurs/', HodViews.creer_professeurs, name="creer_professeurs"),
     path('creer_professeurs_save/', HodViews.creer_professeurs_save, name="creer_professeurs_save"),
     path('gerer_professeurs/', HodViews.gerer_professeurs, name="gerer_professeurs"),
     path('admin_search_professeurs/', HodViews.admin_search_professeurs, name="admin_search_professeurs"),
     path('editer_professeurs/<staff_id>/',
         HodViews.editer_professeurs, name="editer_professeurs"),
     path('editer_professeurs_save/', HodViews.editer_professeurs_save,
         name="editer_professeurs_save"),
     path('supprimer_professeurs/<staff_id>/',
         HodViews.supprimer_professeurs, name="supprimer_professeurs"),
  
    # URLS for Staff
    path('staff_home/', StaffViews.staff_home, name="staff_home"),
    path('staff_take_attendance/', StaffViews.staff_take_attendance,
         name="staff_take_attendance"),
    path('get_students/', StaffViews.get_students, name="get_students"),
    path('save_attendance_data/', StaffViews.save_attendance_data,
         name="save_attendance_data"),
    path('staff_update_attendance/', StaffViews.staff_update_attendance,
         name="staff_update_attendance"),
    path('get_attendance_dates/', StaffViews.get_attendance_dates,
         name="get_attendance_dates"),
    path('get_attendance_student/', StaffViews.get_attendance_student,
         name="get_attendance_student"),
    path('update_attendance_data/', StaffViews.update_attendance_data,
         name="update_attendance_data"),
    path('staff_apply_leave/', StaffViews.staff_apply_leave,
         name="staff_apply_leave"),
    path('staff_apply_leave_save/', StaffViews.staff_apply_leave_save,
         name="staff_apply_leave_save"),
    path('staff_feedback/', StaffViews.staff_feedback, name="staff_feedback"),
    #------ feedback search -------
    path('staff_search_feedback/', StaffViews.staff_search_feedback, name="staff_search_feedback"),

    path('staff_feedback_save/', StaffViews.staff_feedback_save,
         name="staff_feedback_save"),
    path('staff_profile/', StaffViews.staff_profile, name="staff_profile"),
    path('staff_profile_update/', StaffViews.staff_profile_update,
         name="staff_profile_update"),
    path('staff_add_result/', StaffViews.staff_add_result, name="staff_add_result"),
    path('staff_add_result_save/', StaffViews.staff_add_result_save,
         name="staff_add_result_save"),

    # URSL for Student
    path('student_home/', StudentViews.student_home, name="student_home"),
    path('student_view_attendance/', StudentViews.student_view_attendance,
         name="student_view_attendance"),
    path('student_view_attendance_post/', StudentViews.student_view_attendance_post,
         name="student_view_attendance_post"),
    path('student_apply_leave/', StudentViews.student_apply_leave,
         name="student_apply_leave"),
    path('student_apply_leave_save/', StudentViews.student_apply_leave_save,
         name="student_apply_leave_save"),
    path('student_feedback/', StudentViews.student_feedback,
         name="student_feedback"),
    path('student_feedback_save/', StudentViews.student_feedback_save,
         name="student_feedback_save"),
    path('student_profile/', StudentViews.student_profile, name="student_profile"),
    path('student_profile_update/', StudentViews.student_profile_update,
         name="student_profile_update"),
    path('student_view_result/', StudentViews.student_view_result,
         name="student_view_result"),

    path('prof_creer_progression/', StudentViews.prof_creer_progression,
         name="prof_creer_progression"),
    # path('add_student_save/', StudentViewss.add_student_save,
    #     name="add_student_save"),
    # path('add_subject/', StudentViewss.add_subject, name="add_subject"),
    path('add_subject_saves/', StudentViewss.add_subject_saves,
         name="add_subject_saves"),

     # *********** for semaines ****************
     #path('gerer_semaines/', HodViews.gerer_semaines, name="gerer_semaines"),
     #path('creer_semaines/', HodViews.creer_semaines, name="creer_semaines"),
     path('creer_semaines/<annee_pk>', HodViews.creer_semaines, name="creer_semaines"),
     path('gerer_semaines/<annee_pk>/', HodViews.gerer_semaines, name="gerer_semaines"),
     #path('creer_semaines/<pk>/', HodViews.creer_semaines, name="creer_semaines"),
     path("click-to-edit/<pk>/",HodViews.initial_state,name="click-to-edit-initial-state",),
     path("creer_semaines/<pk>/editer_semaines/",HodViews.editer_semaines,name="editer_semaines"),
     path('creer_semaines/<pk>/',HodViews.detail_semaines,name="detail_semaines"),
     path('creer_semaines/<pk>/supprimer_semaines/', HodViews.supprimer_semaines, name='supprimer_semaines'),
     
     #************ for staff progression tracking ******
     path('staff_suivi_progression/<pk>', StaffViews.staff_suivi_progression, name="staff_suivi_progression"),
     path('staff_suivi_progression/<pk>/list', StaffViews.staff_progression_list, name='staff_progression_list'),
     path("staff_suivi_progression/<pk>/editer_status/",StaffViews.editer_status,name="editer_status"),
     path("staff_search_progressions/",StaffViews.staff_search_progressions,name="staff_search_progressions"),

     #************ for evaluation *********************
     #path("staff_apply_leave_save1/<pk>/",StaffViews.staff_apply_leave_save1,name="staff_apply_leave_save1"),
     #path("staff_suivi_progression/<pk>/staff_creer_MAJ_progession/",StaffViews.staff_creer_MAJ_progession,name="staff_creer_MAJ_progession"),

 
     #************ for tracking by the admin **********
     path("admin_view_progressions/",HodViews.admin_view_progressions,name="admin_view_progressions"),
     path('modules_classe_name_admin/',HodViews.modules_classe_name_admin, name='modules_classe_name_admin'),
     path('modules_matiere_name_admin/',HodViews.modules_matiere_name_admin, name='modules_matiere_name_admin'),
     path('admin_get_progression_matiere/',HodViews.admin_get_progression_matiere, name='admin_get_progression_matiere'),

     #********** test rechercher ****************
     path('rechercher/', HodViews.rechercher, name='rechercher'),
     path('search/', HodViews.search, name='search'),
     #           fin test rechercher 
       
     path('modules/', StaffViews.modules_classe_name, name='modules'),

     #****************** Home page admin ***********
     #- Evaluation par matiere
     path('admin_evaluation_par_matiere/', HodViews.admin_evaluation_par_matiere, name='admin_evaluation_par_matiere'),
     path('modules_matiere_name_admin_home/', HodViews.modules_matiere_name_admin_home, name='modules_matiere_name_admin_home'),
     path('modules_class_and_prof_name/', HodViews.modules_class_and_prof_name, name='modules_class_and_prof_name'),
     path('admin_get_eval_par_matiere_js/', HodViews.admin_get_eval_par_matiere_js, name='admin_get_eval_par_matiere_js'),

]

