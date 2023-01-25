from ninja import Schema, ModelSchema
from .models import *
from datetime import datetime

##########################
##   No Relation Info   ##
##########################

class SchoolBase(Schema):
    name : str
    email : str
    address : str
    tel : str

class HeadmasterBase(Schema):
    name:str
    email:str
    tel:str        

class TeacherBase(Schema):
    name:str
    email:str
    tel:str
    
class StudentBase(Schema):
    name:str
    year:str
    
    @staticmethod
    def resolve_year(obj):
        return obj.get_year_display

class TclassesBase(Schema):
    title:str
    descript:str

##########################
##     for Listed       ##
##########################
class SchoolSchemaListed(ModelSchema):
    class Config:
        model = schools
        model_fields = ['id', 'name', 'address', 'email', 'tel']
    headmaster_name:str = None
    
    @staticmethod
    def resolve_headmaster_name(obj):
        try: 
            key = obj.headmasters.name
        except:
            key = None
        return key

class HeadMasterListed(Schema):
    id:int
    name:str
    email:str = None
    tel:str = None
    schoolname:str = None
    
    @staticmethod
    def resolve_schoolname(obj):
        if not obj.school:
            return None
        return obj.school.name

class TeacherListed(Schema):
    id:int
    name:str
    email:str = None
    tel:str = None
    schoolsname:str
    
    @staticmethod
    def resolve_schoolsname(obj):
        return obj.school.name

class StudentListed(Schema):
    id:int
    name:str
    year:str
    school:str = None
    teacher:str = None
    tclasses_list:list[TclassesBase] = None
    
    @staticmethod
    def resolve_tclasses_list(obj):
        return obj.tclasses_set.all()    
    
    @staticmethod
    def resolve_school(obj):
        try:
            return obj.school.name
        except:
            return None

    @staticmethod
    def resolve_teacher(obj):
        try:
            return obj.teacher.name
        except:
            return None
    @staticmethod
    def resolve_year(obj):
        return obj.get_year_display()
    
class TclassesListed(Schema):
    title: str
    description: str
    teacher: str
    student:list[StudentBase] = None
    school: str
    
    @staticmethod
    def resolve_student(obj):
        return obj.student.all()
    
    @staticmethod
    def resolve_teacher(obj):
        return obj.teacher.name
        
    @staticmethod
    def resolve_school(obj):
        return obj.school.name
    
##########################
##     for Post         ##
##########################
class HeadMasterPost(Schema):
    name: str
    email:str = None
    tel:str = None
    school_id:int
    
class TeacherPost(Schema):
    name:str
    email:str = None
    tel:str = None
    school_id:int
    
class StudentPost(Schema):
    name:str = None
    year:str = None
    school_id : int = None
    teacher_id: int = None
    
class TclassesPost(Schema):
    title:str
    description:str = None
    school_id : int
    teacher_id: int
    
##########################
##     for Patch        ##
##########################
class SchoolPatch(Schema):
    name : str = None
    email : str = None
    address : str = None
    tel : str = None

class HeadMasterPatch(Schema):
    name: str = None
    email:str = None
    tel:str = None
    school_id:int = None

class TeacherPatch(Schema):
    name:str = None
    email:str = None
    tel:str = None
    school_id:int = None

class TclassesPatch(Schema):
    title:str = None
    description:str = None
    school_id : int = None
    teacher_id: int = None

class EnrollForm(Schema):
    class_id_list:list
    student_id_list:list

## utility
class ErrorSchema(Schema):
    message:str