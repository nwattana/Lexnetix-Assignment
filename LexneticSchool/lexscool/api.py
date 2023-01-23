from ninja import NinjaAPI, Form
from .schemas import *
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
api = NinjaAPI()

#####################
##      School     ##
#####################

@api.get('/school', response=list[SchoolSchemaListed])
def school_get_all(request:HttpRequest):
    all_school = schools.objects.all()
    return all_school

@api.post('/school', response={201:SchoolSchemaListed})
def school_create(request:HttpRequest, payload:SchoolBase):
    try:
        new_school = schools.objects.get(name=payload.name)
    except:
        new_school = schools.objects.create(**payload.dict())
    return 201, new_school

@api.get('/school/{school_id}', response={200:SchoolSchemaListed})
def school_get_by_id(request:HttpRequest, school_id:int):
    school = get_object_or_404(schools, pk=school_id)
    return 200, school

@api.put('/school/{school_id}', response={200:SchoolSchemaListed})
def school_update_by_id(request:HttpRequest, school_id:int, payload:SchoolBase):
    school_to_update = get_object_or_404(schools, pk=school_id)
    school_to_update.name = payload.name
    school_to_update.email = payload.email
    school_to_update.address = payload.address 
    school_to_update.tel = payload.tel
    school_to_update.save()
    return 200, school_to_update

@api.patch('/school/{school_id}', response={200:SchoolSchemaListed})
def school_patch_by_id(request:HttpRequest, school_id:int, payload:SchoolPatch):
    school_to_patch = get_object_or_404(schools, pk=school_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(school_to_patch, attr, value)
    school_to_patch.save()
    return 200, school_to_patch

@api.delete('/school/{school_id}', response={204:None})
def school_delete(request:HttpRequest, school_id:int):
    school_to_delete = get_object_or_404(schools, pk=school_id)
    school_to_delete.delete()
    return 204, None
    

#####################
##   Head Master   ##
#####################
@api.get('/headmaster', response=list[HeadMasterListed])
def headmaster_get_all(request:HttpRequest):
    all_headmaster = headmasters.objects.all()
    return all_headmaster

@api.post('/headmaster', response={201:HeadMasterListed, 409:ErrorSchema})
def headmaster_create(request:HttpRequest, payload:HeadMasterPost):
    try:
        add_school = schools.objects.get(pk=payload.school_id)
    except:
        add_school = None
    new_headmaster = headmasters(
        name = payload.name,
        email = payload.email,
        tel=payload.tel,
        school = add_school
        )
    try:
        new_headmaster.save()
    except:
        return 409, {'message': 'School Had Headmaster'}
    return 201, new_headmaster

@api.get('/headmaster/{headmaster_id}', response={200:HeadMasterListed,404:ErrorSchema})
def headmaster_get_by_id(request:HttpRequest, headmaster_id:int):
    try:
        headmaster = headmasters.objects.get(pk=headmaster_id)
    except:
        return 404,{'message':'Not Found'}
    return headmaster

@api.put('/headmaster/{headmaster_id}', response={200:HeadMasterListed})
def headmaster_update_by_id(request:HttpRequest, headmaster_id:int, payload:HeadMasterPost):
    to_update = get_object_or_404(headmasters, pk=headmaster_id)
    to_update.name = payload.name
    to_update.email = payload.email
    to_update.tel = payload.tel
    to_update.save()
    return to_update

@api.patch('/headmaster/{headmaster_id}', response={200:HeadMasterListed})
def headmaster_patch_by_id(request:HttpRequest, headmaster_id:int, payload:HeadMasterPatch):
    to_patch = get_object_or_404(headmasters, pk=headmaster_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(to_patch, attr, value)
    to_patch.save()
    return to_patch

@api.delete('/headmaster/{headmaster_id}', response={204:None})
def headmaster_delete_by_id(request:HttpRequest, headmaster_id:int):
    to_delete = get_object_or_404(headmasters, pk=headmaster_id)
    to_delete.delete()
    return 204, None
        
#####################
##      Teacher    ##
#####################
@api.get('/teacher', response={200:list[TeacherListed]})
def teacher_get_all(request:HttpRequest):
    all_teacher = teachers.objects.all()
    return all_teacher

@api.post('/teacher', response={201:TeacherListed})
def teacher_create(request:HttpRequest, payload:TeacherPost):
    dbschool = get_object_or_404(schools, pk=payload.school_id)
    new_teacher=teachers(
        name = payload.name,
        email = payload.email,
        tel = payload.tel,
        school = dbschool
    )
    new_teacher.save()
    return new_teacher

@api.get('/teacher/{teacher_id}', response={200:TeacherListed})
def teacher_get_by_id(request:HttpRequest, teacher_id:int):
    teacher = get_object_or_404(teachers, pk=teacher_id)
    return teacher

@api.put('/teacher/{teacher_id}', response={200:TeacherListed})
def teacher_update_by_id(request:HttpRequest, payload:TeacherPost, teacher_id:int):
    to_update = get_object_or_404(teachers, pk = teacher_id)
    to_update_school = get_object_or_404(schools, pk=payload.school_id)
    to_update.name = payload.name
    to_update.email = payload.email 
    to_update.tel = payload.tel
    to_update.school = to_update_school
    to_update.save()
    return 200, to_update

@api.patch('/teacher/{teacher_id}', response={200:TeacherListed})
def teacher_patch_by_id(request:HttpRequest, payload:TeacherPatch, teacher_id:int):
    to_patch_obj = get_object_or_404(teachers, pk = teacher_id)
    if payload.school_id:
        to_patch_school = get_object_or_404(schools, pk = payload.school_id)
    if payload.name:to_patch_obj.name = payload.name 
    if payload.email:to_patch_obj.email = payload.email 
    if payload.tel:to_patch_obj.tel= payload.tel
    if payload.school_id:to_patch_obj.school = to_patch_school
    to_patch_obj.save()
    return to_patch_obj

@api.delete('/teacher/{teacher_id}', response={204:None})
def teacher_delete_by_id(request:HttpRequest, teacher_id:int):
    to_delete = get_object_or_404(teachers, pk=teacher_id)
    return 204, None

#####################
##      student    ##
#####################

@api.get('/student', response={200:list[StudentListed]})
def student_get_all(request:HttpRequest):
    all_student = students.objects.all()
    return all_student

@api.post('/student', response={201:StudentListed, 406:ErrorSchema})
def student_create(request:HttpRequest, payload:StudentPost):
    get_school = get_object_or_404(schools, pk = payload.school_id)
    get_teacher = get_object_or_404(teachers, pk = payload.teacher_id)
    if get_school.id != get_teacher.school.id:
        return 406, {'message': 'advisor from other school??'}
    if payload.year not in ('1','2','3','4','5'):
        return 406, {'message': 'Wrong Yaer'}
    new_student = students(
        name = payload.name,
        year = payload.year,
        school = get_school,
        teacher = get_teacher
    )
    new_student.save()
    return 201, new_student

@api.get('/student/{student_id}', response={200:StudentListed})
def student_get_by_id(request:HttpRequest, student_id:int):
    get_student = get_object_or_404(students, pk=student_id)
    return get_student

@api.put('/student/{student_id}', response={200:StudentListed, 406:ErrorSchema})
def student_update_by_id(request:HttpRequest, payload:StudentPost, student_id:int):
    get_student = get_object_or_404(students, pk=student_id)
    school_obj = get_object_or_404(schools, pk=payload.school_id)
    teacher_obj = get_object_or_404(teachers, pk=payload.teacher_id)
    if payload.year in ['1', '2', '3', '4', '5']:
        get_student.year = payload.year
    else:
        return 406, {'message', 'Wrong or Empty Year'}
    if teacher_obj.school.id != school_obj.id:
        return 406, {'message', 'Teacher Not in school'}
    get_student.school = school_obj
    get_student.teacher = teacher_obj
    get_student.name = payload.name
    get_student.save()
    return  get_student
    
@api.patch('/student/{student_id}', response={200:StudentListed, 406:ErrorSchema})
def student_patch_by_id(request:HttpRequest, payload:StudentPost, student_id:int):
    get_student = get_object_or_404(students, pk=student_id)
    if payload.school_id:
        school_obj = get_object_or_404(schools, pk=payload.school_id)
    if payload.teacher_id:
        teacher_obj = get_object_or_404(teachers, pk=payload.teacher_id)  
    if payload.year in ['1', '2', '3', '4', '5']:
        get_student.year = payload.year
    else:
        return 406, {'message', 'Wrong or Empty Year'}
    if teacher_obj.school.id != school_obj.id:
        return 406, {'message', 'Teacher Not in school'}
    get_student.school = school_obj
    get_student.teacher = teacher_obj
    get_student.name = payload.name
    get_student.save()
    return get_student

@api.delete('/student/{student_id}', response={204:None})
def student_delete_by_id(request:HttpRequest, student_id:int):
    get_student = get_object_or_404(students, pk=student_id)
    get_student.delete()
    return 204

#####################
##       class     ##
#####################
@api.get('/tclasses', response=list[TclassesListed])
def tclasses_get_all(request:HttpRequest):
    all_class = tclasses.objects.all()
    return all_class

@api.post('/tclasses', response={201:TclassesListed,406:ErrorSchema})
def tclasses_create(request:HttpRequest, payload:TclassesPost):
    get_school = get_object_or_404(schools, pk=payload.school_id)
    get_teacher = get_object_or_404(teachers, pk=payload.teacher_id)
    if get_school.id != get_teacher.school.id:
        return 406, {'message', 'Our Teacher Not work acrosss school'}
    new_class = tclasses(
        title = payload.title,
        descript = payload.descript,
        school = get_school,
        teacher = get_teacher
    )
    new_class.save()
    return 201, new_class

## so it no need to put school right ? just get school from teacher
@api.get('/tclasses/{class_id}', response={200:TclassesListed})
def tclasses_get_by_id(request:HttpRequest, class_id:int):
    tclass = get_object_or_404(tclasses, pk=class_id)
    return tclass

@api.put('/tclasses/{class_id}', response={200:TclassesListed})
def tclasses_put_by_id(request:HttpRequest, payload:TclassesPatch, class_id:int):
    class_obj = get_object_or_404(tclasses, pk=class_id)
    school_obj = get_object_or_404(schools, pk=payload.school_id)
    teacher_obj = get_object_or_404(teachers, pk=payload.teacher_id)
    class_obj.title = payload.title
    class_obj.description = payload.description
    if school_obj.id == teacher_obj.school.id:
        class_obj.school = school_obj
        class_obj.teacher = teacher_obj
    else:
        return 409, {'message', 'Teacher Not in school'}
    class_obj.save()
    return 200, TclassesListed

@api.patch('/tclasses/{class_id}', response={200:TclassesListed})
def tclasses_patch_by_id(request:HttpRequest, payload:TclassesPatch, class_id:int):
    to_patch = get_object_or_404(tclasses, pk=class_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(to_patch, attr, value)
    return 200, to_patch

@api.delete('/tclasses/{class_id}', response={204:None})
def tclasses_delete_by_id(request:HttpRequest, class_id:int):
    to_delete = get_object_or_404(tclasses, pk=class_id)
    return 204, None
       

##########################
##       EnrollForm     ##
##########################

@api.patch('/tclasses',response={202:ErrorSchema, 406:ErrorSchema})
def enrolled_student(request:HttpRequest, payload:EnrollForm):
    for tclass in payload.class_id_list:
        tclass_obj = get_object_or_404(tclasses, pk=tclass)
        for student in payload.student_id_list:
            student_obj = get_object_or_404(students, pk=student)
            if tclass_obj.school != student_obj.school:
                return 406, {'message':'student can not enroll'}
    for tclass in payload.class_id_list:
        tclass_obj = get_object_or_404(tclasses, pk=tclass)
        for student in payload.student_id_list:
            student_obj = get_object_or_404(students, pk=student)
            tclass_obj.student.add(student_obj)
    return 202,{'message':'Done'}
            