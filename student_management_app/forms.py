from django import forms 
from django.forms import Form
from student_management_app.models import Courses, SessionYearModel

#test **************

from django import forms
from django.forms.models import inlineformset_factory



#*********** Syllabus ***************
from .models import Chapitres, Matieres, Lecons, Semaines, SemainesLecons, SemainesLeconsReelle

class LeconForm(forms.ModelForm):
    class Meta:
        model = Lecons
        fields = [
            'nombre_heures',
            'detail_lecons'
        ]

class ChapitreForm(forms.ModelForm):
    class Meta:
        model = Chapitres
        fields = (
            'titre_chapitres',
            'numero_chapitres'
        )

ChapitreFormSet = inlineformset_factory(
    Matieres,
    Chapitres,
    form=ChapitreForm,
    min_num=2,  # minimum number of forms that must be filled in
    extra=1,  # number of empty forms to display
    can_delete=False  # show a checkbox in each form to delete the row
)

LeconFormSet = inlineformset_factory(
    Chapitres,
    Lecons,
    form=LeconForm,
    min_num=2,  # minimum number of forms that must be filled in
    extra=1,  # number of empty forms to display
    can_delete=False  # show a checkbox in each form to delete the row
)

class SemainesForm(forms.ModelForm):
    class Meta:
        model = Semaines
        fields = (
            'numero_semaines',
            'debut_semaines',
            'fin_semaines'
        )
        widgets = {
            'numero_semaines': forms.NumberInput(attrs= { 'class' :"form-control" }),
            #'debut_semaines':forms.DateField(),
            #'fin_semaines': forms.DateField(),
            'debut_semaines':forms.DateInput(attrs= { 'class' :"form-control" }),
            'fin_semaines': forms.DateInput(attrs= { 'class' :"form-control" })
        }


class StatutForm(forms.ModelForm):
    class Meta:
        model = SemainesLecons
        fields = (
            'status',
        )
        statut_list = (
        ('1','En attente'),
        ('2','En cours'),
        ('3','Termine'),
        )
        status = forms.ChoiceField(label="Statut", choices=statut_list, widget=forms.Select(attrs={"class":"form-control"}))


#class StaffMAJForm(forms.ModelForm):
   # class Meta:
    #    model = SemainesLeconsReelle
    #    fields = [
    #        'lecon_duree_reelle'
    #    ]

# ********************* Fin syllabus 


class DateInput(forms.DateInput):
    input_type = "date"


class AddStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    #For Displaying Courses
    try:
        courses = Courses.objects.all()
        course_list = []
        for course in courses:
            single_course = (course.id, course.course_name)
            course_list.append(single_course)
    except:
        course_list = []
    
    #For Displaying Session Years
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (session_year.id, str(session_year.session_start_year)+" to "+str(session_year.session_end_year))
            session_year_list.append(single_session_year)
            
    except:
        session_year_list = []
    
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    
    course_id = forms.ChoiceField(label="Course", choices=course_list, widget=forms.Select(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year", choices=session_year_list, widget=forms.Select(attrs={"class":"form-control"}))
    # session_start_year = forms.DateField(label="Session Start", widget=DateInput(attrs={"class":"form-control"}))
    # session_end_year = forms.DateField(label="Session End", widget=DateInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))



class EditStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    #For Displaying Courses
    try:
        courses = Courses.objects.all()
        course_list = []
        for course in courses:
            single_course = (course.id, course.course_name)
            course_list.append(single_course)
    except:
        course_list = []

    #For Displaying Session Years
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (session_year.id, str(session_year.session_start_year)+" to "+str(session_year.session_end_year))
            session_year_list.append(single_session_year)
            
    except:
        session_year_list = []

    
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    
    course_id = forms.ChoiceField(label="Course", choices=course_list, widget=forms.Select(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year", choices=session_year_list, widget=forms.Select(attrs={"class":"form-control"}))
    # session_start_year = forms.DateField(label="Session Start", widget=DateInput(attrs={"class":"form-control"}))
    # session_end_year = forms.DateField(label="Session End", widget=DateInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))