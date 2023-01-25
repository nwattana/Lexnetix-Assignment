from ninja import NinjaAPI, Form
from .schemas import *
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
api = NinjaAPI()

#####################
##      School     ##
#####################

@api.get('/school', response={200:list[SchoolSchemaListed]})
def school_get_all(request:HttpRequest):
    all_school = schools.objects.all()
    return 200,all_school

@api.post('/school', response={200:SchoolSchemaListed ,201:SchoolSchemaListed})
def school_create(request:HttpRequest, payload:SchoolBase = Form(...)):
    try:
        new_school = schools.objects.get(name=payload.name)
        return 200, new_school
    except:
        new_school = schools.objects.create(**payload.dict())
    return 201, new_school

@api.get('/school/{school_id}', response={200:SchoolSchemaListed, 404:ErrorSchema})
def school_get_by_id(request:HttpRequest, school_id:int):
    try:
        school = get_object_or_404(schools, pk=school_id)
    except:
        return 404, {'message':'Not Found'}
    return 200, school

@api.put('/school/{school_id}', response={200:SchoolSchemaListed, 404:ErrorSchema})
def school_update_by_id(request:HttpRequest, school_id:int, payload:SchoolBase = Form(...)):
    try:
         school_to_update = get_object_or_404(schools, pk=school_id)
    except:
        return 404, {'message':'Not Found'}
    school_to_update.name = payload.name
    school_to_update.email = payload.email
    school_to_update.address = payload.address 
    school_to_update.tel = payload.tel
    school_to_update.save()
    return 200, school_to_update

@api.patch('/school/{school_id}', response={200:SchoolSchemaListed, 404:ErrorSchema})
def school_patch_by_id(request:HttpRequest, school_id:int, payload:SchoolPatch = Form(...)):
    try:
        school_to_patch = get_object_or_404(schools, pk=school_id)
    except:
        return 404, {'message':'Not Found'}
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(school_to_patch, attr, value)
    school_to_patch.save()
    return 200, school_to_patch

@api.delete('/school/{school_id}', response={204:None, 404:ErrorSchema})
def school_delete(request:HttpRequest, school_id:int):
    try:
        school_to_delete = get_object_or_404(schools, pk=school_id)
    except:
        return 404, {'message':'Not Found'}
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
def headmaster_create(request:HttpRequest, payload:HeadMasterPost = Form(...)):
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
    return 200, headmaster

@api.put('/headmaster/{headmaster_id}', response={200:HeadMasterListed, 404:ErrorSchema})
def headmaster_put_by_id(request:HttpRequest, headmaster_id:int, payload:HeadMasterPost = Form(...)):
    try:
        to_put = get_object_or_404(headmasters, pk=headmaster_id)
    except:
        return 404, {'message':'Not Found'}
    to_put.name = payload.name
    to_put.email = payload.email
    to_put.tel = payload.tel
    to_put.save()
    return 200, to_put

@api.patch('/headmaster/{headmaster_id}', response={200:HeadMasterListed, 404:ErrorSchema})
def headmaster_patch_by_id(request:HttpRequest, headmaster_id:int, payload:HeadMasterPatch = Form(...)):
    try:
        to_patch = get_object_or_404(headmasters, pk=headmaster_id)
    except:
        return 404, {'message':'Not Found'}
    
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(to_patch, attr, value)
    to_patch.save()
    return 200,to_patch

@api.delete('/headmaster/{headmaster_id}', response={204:None})
def headmaster_delete_by_id(request:HttpRequest, headmaster_id:int):
    try:
        to_delete = get_object_or_404(headmasters, pk=headmaster_id)
    except:
        return 404, {'message':'Not Found'}
    to_delete.delete()
    return 204, None
        
#####################
##      Teacher    ##
#####################
@api.get('/teacher', response={200:list[TeacherListed]})
def teacher_get_all(request:HttpRequest):
    all_teacher = teachers.objects.all()
    return all_teacher

@api.post('/teacher', response={201:TeacherListed, 404:ErrorSchema})
def teacher_create(request:HttpRequest, payload:TeacherPost = Form(...)):
    try:
        setschool = get_object_or_404(schools, pk=payload.school_id)
    except:
        return 404, {'message':'Not Found'}
    new_teacher=teachers(
        name = payload.name,
        email = payload.email,
        tel = payload.tel,
        school = setschool
    )
    new_teacher.save()
    return 201, new_teacher

@api.get('/teacher/{teacher_id}', response={200:TeacherListed, 404:ErrorSchema})
def teacher_get_by_id(request:HttpRequest, teacher_id:int):
    try:
        teacher = get_object_or_404(teachers, pk=teacher_id)
    except:
        return 404, {'message':'Not Found'}
    return 200, teacher

@api.put(
        '/teacher/{teacher_id}', 
         response={200:TeacherListed, 404:ErrorSchema}
         )
def teacher_put_by_id(
    request:HttpRequest, 
    payload:TeacherPost, 
    teacher_id:int):
    try:
        to_update = get_object_or_404(teachers, pk=teacher_id)
        to_update_school = get_object_or_404(schools, pk=payload.school_id)
    except:
        return 404, {'message':'Not Found'}
    to_update.name = payload.name
    to_update.email = payload.email 
    to_update.tel = payload.tel
    to_update.school = to_update_school
    to_update.save()
    return 200, to_update

@api.patch(
    '/teacher/{teacher_id}', 
    response={200:TeacherListed, 404:ErrorSchema})
def teacher_patch_by_id(request:HttpRequest, teacher_id:int, payload:TeacherPatch  = Form(...)):
    try:
        to_patch_obj = get_object_or_404(teachers, pk = teacher_id)
        if payload.school_id:
            to_patch_school = get_object_or_404(schools, pk = payload.school_id)
    except:
        return 404, {'message':'Not Found'}
    if payload.name:to_patch_obj.name = payload.name 
    if payload.email:to_patch_obj.email = payload.email 
    if payload.tel:to_patch_obj.tel= payload.tel
    if payload.school_id:to_patch_obj.school = to_patch_school
    to_patch_obj.save()
    return 200,to_patch_obj

@api.delete(
    '/teacher/{teacher_id}', 
    response={204:None, 404:ErrorSchema})
def teacher_delete_by_id(request:HttpRequest, teacher_id:int):
    try:
        to_delete = get_object_or_404(teachers, pk=teacher_id)
    except:
        return 404,{'message':'Not Found'}
    to_delete.delete()
    return 204, None

#####################
##      student    ##
#####################

@api.get('/student', response={200:list[StudentListed]})
def student_get_all(request:HttpRequest):
    all_student = students.objects.all()
    return all_student

@api.post('/student', response={201:StudentListed, 404:ErrorSchema,406:ErrorSchema})
def student_create(request:HttpRequest, payload:StudentPost = Form(...)):
    try:
        get_school = get_object_or_404(schools, pk = payload.school_id)
        get_teacher = get_object_or_404(teachers, pk = payload.teacher_id)
    except:
        return 404,{'message':'Not Found'}
    if get_school.id != get_teacher.school.id:
        return 406, {'message': 'Bad input'}
    if payload.year not in ('1','2','3','4','5'):
        return 406, {'message': 'Bad input'}
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
    try:
        get_student = get_object_or_404(students, pk=student_id)
    except:
        return 404, {'message':'Not Found'}
    return 200, get_student

@api.put('/student/{student_id}', response={200:StudentListed, 406:ErrorSchema})
def student_put_by_id(request:HttpRequest, student_id:int, payload:StudentPost = Form(...)):
    try:
        get_student = get_object_or_404(students, pk=student_id)
        school_obj = get_object_or_404(schools, pk=payload.school_id)
        teacher_obj = get_object_or_404(teachers, pk=payload.teacher_id)
    except:
        return 404, {'message':'Not Found'}
    if payload.year in ['1', '2', '3', '4', '5']:
        get_student.year = payload.year
    else:
        return 406, {'message', 'Bad input'}
    if teacher_obj.school.id != school_obj.id:
        return 406, {'message', 'Bad input'}
    get_student.school = school_obj
    get_student.teacher = teacher_obj
    get_student.name = payload.name
    get_student.save()
    return  200, get_student
    
@api.patch('/student/{student_id}', response={200:StudentListed, 406:ErrorSchema})
def student_patch_by_id(request:HttpRequest, student_id:int, payload:StudentPost = Form(...)):
    try:
        get_student = get_object_or_404(students, pk=student_id)
        if payload.school_id:
            school_obj = get_object_or_404(schools, pk=payload.school_id)
        if payload.teacher_id:
            teacher_obj = get_object_or_404(teachers, pk=payload.teacher_id)  
        if payload.year in ['1', '2', '3', '4', '5']:
            get_student.year = payload.year
        else:
            return 406, {'message', 'Bad input'}
        if teacher_obj.school.id != school_obj.id:
            return 406, {'message', 'Bad input'}
    except:
        return 404, {'message':'Not Found'}
    get_student.school = school_obj
    get_student.teacher = teacher_obj
    get_student.name = payload.name
    get_student.save()
    return 200, get_student

@api.delete('/student/{student_id}', response={204:None, 404:ErrorSchema})
def student_delete_by_id(request:HttpRequest, student_id:int):
    try:
        get_student = get_object_or_404(students, pk=student_id)
    except:
        return 404, {'message':'Not Found'}
    get_student.delete()
    return 204, None

#####################
##       class     ##
#####################
@api.get('/tclasses', response=list[TclassesListed])
def tclasses_get_all(request:HttpRequest):
    all_class = tclasses.objects.all()
    return all_class

@api.post('/tclasses', response={201:TclassesListed,404:ErrorSchema,406:ErrorSchema})
def tclasses_create(request:HttpRequest, payload:TclassesPost = Form(...)):
    
    try:
        get_school = get_object_or_404(schools, pk=payload.school_id)
        get_teacher = get_object_or_404(teachers, pk=payload.teacher_id)
        if get_school.id != get_teacher.school.id:
            return 406, {'message', 'Bad Input'}
    except:
        return 404, {'message':'Not Found'}
    new_class = tclasses(
        title = payload.title,
        description = payload.description,
        school = get_school,
        teacher = get_teacher
    )
    new_class.save()
    for tstd in payload.student_list:
        try:
            student = get_object_or_404(students, pk=tstd)
        except:
            return 404, {'message':'Not Found'}
        new_class.student.add(student)
    new_class.save()
    return 201, new_class

## so it no need to put school right ? just get school from teacher
@api.get('/tclasses/{class_id}', response={200:TclassesListed, 404:ErrorSchema})
def tclasses_get_by_id(request:HttpRequest, class_id:int):
    try:
        tclass = get_object_or_404(tclasses, pk=class_id)
    except:
        return 404, {'Message':'Not Found'}
    return 200,tclass

@api.put('/tclasses/{class_id}', response={200:TclassesListed, 404:ErrorSchema, 406:ErrorSchema})
def tclasses_put_by_id(request:HttpRequest, class_id:int, payload:TclassesPatch = Form(...)):
    try:
        class_obj = get_object_or_404(tclasses, pk=class_id)
        school_obj = get_object_or_404(schools, pk=payload.school_id)
        teacher_obj = get_object_or_404(teachers, pk=payload.teacher_id)
    except:
        return 404, {'Message':'Not Found'}        
    class_obj.title = payload.title
    class_obj.description = payload.description
    if school_obj.id == teacher_obj.school.id:
        class_obj.school = school_obj
        class_obj.teacher = teacher_obj
    else:
        return 406, {'Message', 'Bad Input'}
    class_obj.save()
    return 200, class_obj

@api.patch('/tclasses/{class_id}', response={200:TclassesListed, 404:ErrorSchema})
def tclasses_patch_by_id(request:HttpRequest, class_id:int, payload:TclassesPatch = Form(...)):
    try:
        to_patch = get_object_or_404(tclasses, pk=class_id)
    except:
        return 404, {'Message':'Not Found'}
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(to_patch, attr, value)
    return 200, to_patch

@api.delete('/tclasses/{class_id}', response={204:None, 404:ErrorSchema})
def tclasses_delete_by_id(request:HttpRequest, class_id:int):
    try:
        to_delete = get_object_or_404(tclasses, pk=class_id)
    except:
        return 404, {'Message':'Not Found'}
    to_delete.delete()
    return 204, None
       

##########################
##       EnrollForm     ##
##########################

@api.patch('/Enroll',response={202:ErrorSchema,404:ErrorSchema, 406:ErrorSchema})
def enrolled_student(request:HttpRequest, payload:EnrollForm):
    for tclass in payload.class_id_list:
        try:
            tclass_obj = get_object_or_404(tclasses, pk=tclass)
        except:
            return 404, {'message':'Non Found'}
        for student in payload.student_id_list:
            try:
                student_obj = get_object_or_404(students, pk=student)
            except:
                return 404, {'message':'Non Found'}
            if tclass_obj.school != student_obj.school:
                return 406, {'message':'Bad Input'}
    for tclass in payload.class_id_list:
        tclass_obj = get_object_or_404(tclasses, pk=tclass)
        for student in payload.student_id_list:
            student_obj = get_object_or_404(students, pk=student)
            tclass_obj.student.add(student_obj)
    return 202,{'message':'Done'}
            