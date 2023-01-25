from django.test import TestCase
import unittest
from django.test import Client

from lexscool.schemas import (
    SchoolBase,
    SchoolPatch,
    HeadMasterPost,
    HeadMasterPatch,
    TeacherPost,
    TeacherPatch,
    StudentPost,
    TclassesPost,
    TclassesPatch   
)
from lexscool.api import (
    school_create,
    school_get_by_id,
    school_patch_by_id,
    school_update_by_id,
    school_delete,
    headmaster_create,
    headmaster_get_by_id,
    headmaster_put_by_id,
    headmaster_patch_by_id,
    headmaster_delete_by_id,
    teacher_create,
    teacher_get_by_id,
    teacher_put_by_id,
    teacher_patch_by_id,
    teacher_delete_by_id,
    student_create,
    student_get_by_id,
    student_put_by_id,
    student_patch_by_id,
    student_delete_by_id,
    tclasses_create,
    tclasses_get_by_id,
    tclasses_patch_by_id,
    tclasses_put_by_id,
    tclasses_delete_by_id
)

from lexscool.models import schools

SCHOOL_IN_1 = SchoolBase(
    name="school 1",
    email="school 1",
    address="school 1",
    tel="school 1",
)

SCHOOL_IN_2 = SchoolBase(
    name="school 2",
    email="school 2",
    address="school 2",
    tel="school 2",
)

SCHOOL_IN_3 = SchoolBase(
    name="school 3",
    email="school 3",
    address="school 3",
    tel="school 3",
)

SCHOOL_PUT_1 = SchoolPatch(
    name="put",
    email="put",
    address="put",
    tel="put",
)

SCHOOL_PATCH_1 = SchoolPatch(
    name="PATCH",
    email="PATCH"
)

HEADMASTER_IN_1 = HeadMasterPost(
    name="H1",
    email="H1",
    tel="H1",
    school_id=1
)

HEADMASTER_IN_2 = HeadMasterPost(
    name="H2",
    email="H2",
    tel="H2",
    school_id=2
)

HEADMASTER_IN_3 = HeadMasterPost(
    name="H3",
    email="H3",
    tel="H3",
    school_id=3
)

HEADMASTER_PUT_1 = HeadMasterPatch(
    name="PUT",
    email="PUT",
    tel="PUT",
    school_id=1
)

HEADMASTER_PATCH_1 = HeadMasterPatch(
    name="PATCH",
    email="PATCH",
    school=1
)

TEACHER_IN_1 = TeacherPost(
    name="T1",
    email="T1",
    tel="T1",
    school_id=1
)

TEACHER_IN_2 = TeacherPost(
    name="T2",
    email="T2",
    tel="T2",
    school_id=2
)

TEACHER_IN_3 = TeacherPost(
    name="T3",
    email="T3",
    tel="T3",
    school_id=3
)

TEACHER_IN_999 = TeacherPost(
    name="T2 999",
    email="T2 999",
    tel="T2 999",
    school_id=999
)

TEACHER_IN_PATCH = TeacherPatch(
    name="PATCH",
    email="PATCH",
)

STUDENT_IN1 = StudentPost(
    name="std 11",
    year="1",
    school_id=1,
    teacher_id=1
)

STUDENT_IN2 = StudentPost(
    name="std 12",
    year="2",
    school_id=1,
    teacher_id=2
)

STUDENT_IN3 = StudentPost(
    name="std 21",
    year="2",
    school_id=1,
    teacher_id=1
)

STUDENT_SCHOOL999 = StudentPost(
    name="std 21",
    year="2",
    school_id=999,
    teacher_id=1
)

STUDENT_TEACHER999 = StudentPost(
    name="std 999",
    year="2",
    school_id=1,
    teacher_id=999
)

STUDENT_PUT = StudentPost(
    name="std 999",
    year="2",
    school_id=1,
    teacher_id=1
)

STUDENT_PATCH_NO_CHOICE = StudentPost(
    name="PATCH",
    school_id=1,
    teacher_id=1
)

TCLASSES_IN1 = TclassesPost(
    title="class1",
    description="class1 class1",
    school_id=1,
    teacher_id=1,
    student_list=[1]
)

TCLASSES_IN2 = TclassesPost(
    title="class2",
    description="class2 class2",
    school_id=2,
    teacher_id=2,
    student_list=[2]
)

TCLASSES_IN12 = TclassesPost(
    title="class12",
    description="class12 class12",
    school_id=2,
    teacher_id=1,
    student_list=[1, 2]
)

TCLASSES_NO_TEACHER = TclassesPost(
    title="class2",
    description="class2 class2",
    school_id=2,
    teacher_id=999,
    student_list=[2]

)

TCLASSES_NO_SCHOOL = TclassesPost(
    title="class2",
    description="class2 class2",
    school_id=999,
    teacher_id=1,
    student_list=[2]
)

TCLASSES_NO_TEACHERSCHOOL = TclassesPost(
    title="class2",
    description="class2 class2",
    school_id=2,
    teacher_id=1,
    student_list=[2]
)

TCLASSES_INPATCH = TclassesPatch(
    title="PATCH",
)

class GetSchool(TestCase):
    def setUp(self):
        school1 = school_create(None, SCHOOL_IN_1)
        school2 = school_create(None, SCHOOL_IN_2)
        school3 = school_create(None, SCHOOL_IN_3)

    def test_get_school_1(self):
        result = (200, schools.objects.get(id=1))
        response = school_get_by_id(None, school_id=1)
        self.assertEqual(result, response)

    def test_get_school_2(self):
        result = (200, schools.objects.get(id=2))
        response = school_get_by_id(None, school_id=2)
        self.assertEqual(result, response)

    def test_get_school_3(self):
        result = (200, schools.objects.get(id=3))
        response = school_get_by_id(None, school_id=3)
        self.assertEqual(result, response)

    def test_get_No_school(self):
        response = school_get_by_id(None, 999)
        status, *data = response
        self.assertEqual(status, 404)
        self.assertEqual(data[0], {'message': 'Not Found'})

class PostSchool(TestCase):
    def setUp(self):
        school1 = school_create(None, SCHOOL_IN_1)
        school2 = school_create(None, SCHOOL_IN_2)

    def test_no_duplicate_School(self):
        before = schools.objects.all().count()
        response = school_create(None, SCHOOL_IN_2)
        after = schools.objects.all().count()
        self.assertEqual(after, before)
        self.assertEqual(response, (200, schools.objects.get(pk=2)))

class PutSchool(TestCase):
    def setUp(self):
        school1 = school_create(None, SCHOOL_IN_1)
        school2 = school_create(None, SCHOOL_IN_2)
        school3 = school_create(None, SCHOOL_IN_3)

    # all data will change to put
    def test_put_school(self):
        response = school_update_by_id(None, 1, payload=SCHOOL_PUT_1)
        status, *data = response
        self.assertEqual(status, 200)
        self.assertEqual(data[0].name, "put")
        self.assertEqual(data[0].address, "put")
        self.assertEqual(data[0].email, "put")
        self.assertEqual(data[0].tel, "put")

    def test_put_no_school(self):
        response = school_update_by_id(None, 999, payload=SCHOOL_PUT_1)
        status, *data = response
        self.assertEqual(status, 404)
        self.assertEqual(data[0], {'message': 'Not Found'})

class PatchSchool(TestCase):
    def setUp(self):
        school1 = school_create(None, SCHOOL_IN_1)
        school2 = school_create(None, SCHOOL_IN_2)
        school3 = school_create(None, SCHOOL_IN_3)

    def test_patch_basic(self):
        response = school_patch_by_id(None, 1, payload=SCHOOL_PATCH_1)
        status, *data = response
        self.assertEqual(status, 200)
        self.assertEqual(data[0].name, 'PATCH')
        self.assertEqual(data[0].email, 'PATCH')

    def test_patch_school_no_obj(self):
        response = school_patch_by_id(None, 999, payload=SCHOOL_PATCH_1)
        status, *data = response
        self.assertEqual(status, 404)
        self.assertEqual(data[0], {'message': 'Not Found'})


class DeleteSchool(TestCase):
    def setUp(self):
        school1 = school_create(None, SCHOOL_IN_1)
        school2 = school_create(None, SCHOOL_IN_2)

    def test_delete(self):
        response = school_delete(None, 1)
        status, *data = response
        self.assertEqual(status, 204)
        self.assertEqual(data[0], None)

        response = school_delete(None, 2)
        status, *data = response
        self.assertEqual(status, 204)
        self.assertEqual(data[0], None)

    def test_delete_no_obj(self):
        response = school_delete(None, 999)
        status, *data = response
        self.assertEqual(status, 404)
        self.assertEqual(data[0], {'message': 'Not Found'})


class GetHeadMaster(TestCase):
    def setUp(self):
        school_create(None, SCHOOL_IN_1)
        school_create(None, SCHOOL_IN_2)
        school_create(None, SCHOOL_IN_3)
        headmaster_create(None, HEADMASTER_IN_1)
        headmaster_create(None, HEADMASTER_IN_2)
        headmaster_create(None, HEADMASTER_IN_3)

    def test_get_by_id_1(self):
        response = headmaster_get_by_id(None, 1)
        status, *data = response
        self.assertEquals(status, 200)
        self.assertEqual(data[0].name, 'H1')
        self.assertEqual(data[0].school.name, 'school 1')

    def test_get_by_id_2(self):
        response = headmaster_get_by_id(None, 2)
        status, *data = response
        self.assertEquals(status, 200)
        self.assertEqual(data[0].name, 'H2')
        self.assertEqual(data[0].school.name, 'school 2')

    def test_get_by_id_3(self):
        response = headmaster_get_by_id(None, 3)
        status, *data = response
        self.assertEquals(status, 200)
        self.assertEqual(data[0].name, 'H3')
        self.assertEqual(data[0].school.name, 'school 3')

    def test_get_by_id_999(self):
        response = headmaster_get_by_id(None, 999)
        status, *data = response
        self.assertEquals(status, 404)
        self.assertEqual(data[0], {'message': 'Not Found'})


class PostHeadMaster(TestCase):
    def setUp(self):
        school_create(None, SCHOOL_IN_1)

    def test_post(self):
        response2 = headmaster_create(None, HEADMASTER_IN_1)
        response = headmaster_get_by_id(None, 1)
        status, *data = response
        status2, *data2 = response2
        self.assertEquals(status, 200)
        self.assertEquals(status2, 201)
        self.assertEquals(data[0].name, 'H1')
        self.assertEquals(data2[0].name, 'H1')
        self.assertEquals(data[0].school.name, 'school 1')
        self.assertEquals(data2[0].school.name, 'school 1')

class PatchHeadMaster(TestCase):
    def setUp(self):
        school_create(None, SCHOOL_IN_1)
        headmaster_create(None, HEADMASTER_IN_1)

    def test_patch_headmaster(self):
        response = headmaster_patch_by_id(None, 1, payload=HEADMASTER_PATCH_1)
        status, *data = response
        self.assertEquals(status, 200)
        self.assertEquals(data[0].name, 'PATCH')
        self.assertEquals(data[0].email, 'PATCH')
        self.assertEquals(data[0].tel, 'H1')

    def test_patch_headmaster_no_obj(self):
        response = headmaster_patch_by_id(
            None, 999, payload=HEADMASTER_PATCH_1)
        status, *data = response
        self.assertEquals(status, 404)

class PutHeadMaster(TestCase):
    def setUp(self):
        school_create(None, SCHOOL_IN_1)
        headmaster_create(None, HEADMASTER_IN_1)

    def test_put_headmaster_basic(self):
        response = headmaster_put_by_id(None, 1, payload=HEADMASTER_PUT_1)
        status, *data = response
        self.assertEquals(status, 200)
        self.assertEquals(data[0].name, 'PUT')
        self.assertEquals(data[0].email, 'PUT')
        self.assertEquals(data[0].tel, 'PUT')

    def test_put_headmaster_no_obj(self):
        response = headmaster_put_by_id(None, 999, payload=HEADMASTER_PUT_1)
        status, *data = response
        self.assertEquals(status, 404)
        self.assertEquals(data[0], {'message': 'Not Found'})

class DeleteHeadMaster(TestCase):
    def setUp(self):
        school_create(None, SCHOOL_IN_1)
        headmaster_create(None, HEADMASTER_IN_1)

    def test_delete_headmaster_by_id(self):
        response = headmaster_delete_by_id(None, 1)
        status, *data = response
        self.assertEqual(status, 204)
        self.assertEqual(data[0], None)
        response = headmaster_get_by_id(None, 1)
        status, *data = response
        self.assertEquals(status, 404)
        self.assertEquals(data[0], {'message': 'Not Found'})


class PostGetTeacher(TestCase):
    def setUp(self):
        school_create(None, SCHOOL_IN_1)
        headmaster_create(None, HEADMASTER_IN_1)
        school_create(None, SCHOOL_IN_2)
        headmaster_create(None, HEADMASTER_IN_2)
        teacher_create(None, TEACHER_IN_2)

    def test_post_teacher(self):
        response = teacher_create(None, TEACHER_IN_1)
        status, *data = response
        self.assertEqual(status, 201)
        self.assertEqual(data[0].school.name, 'school 1')
        self.assertEqual(data[0].name, 'T1')

    def test_get_teacher(self):
        response = teacher_get_by_id(None, 1)
        status, *data = response
        self.assertEqual(status, 200)
        self.assertEqual(data[0].school.name, 'school 2')
        self.assertEqual(data[0].name, 'T2')


class PutPatchTeacher(TestCase):
    def setUp(self):
        school_create(None, SCHOOL_IN_1)
        school_create(None, SCHOOL_IN_2)
        headmaster_create(None, HEADMASTER_IN_1)
        headmaster_create(None, HEADMASTER_IN_2)
        teacher_create(None, TEACHER_IN_1)

    def test_put_teacher_1(self):
        response = teacher_put_by_id(None, TEACHER_IN_2, 1)
        status, *data = response
        self.assertEqual(status, 200)
        self.assertEqual(data[0].school.name, 'school 2')
        self.assertEqual(data[0].name, 'T2')

    def test_put_teacher_no_school(self):
        response = teacher_put_by_id(None, TEACHER_IN_999, 1)
        status, *data = response
        self.assertEquals(status, 404)
        self.assertEquals(data[0], {'message': 'Not Found'})

    def test_put_teacher_no_teacher(self):
        response = teacher_put_by_id(None, TEACHER_IN_2, 999)
        status, *data = response
        self.assertEquals(status, 404)
        self.assertEquals(data[0], {'message': 'Not Found'})

    def test_patch_teacher_basic(self):
        response = teacher_patch_by_id(None, 1, TEACHER_IN_2)
        status, *data = response
        self.assertEqual(status, 200)
        self.assertEqual(data[0].school.name, 'school 2')
        self.assertEqual(data[0].name, 'T2')
        response = teacher_patch_by_id(None, 1, TEACHER_IN_PATCH)
        status, *data = response
        self.assertEqual(status, 200)
        self.assertEqual(data[0].name, 'PATCH')
        self.assertEqual(data[0].email, 'PATCH')

    def test_patch_teacher_no_teacher(self):
        response = teacher_patch_by_id(None, 999, TEACHER_IN_2)
        status, *data = response
        self.assertEquals(status, 404)
        self.assertEquals(data[0], {'message': 'Not Found'})

    def test_patch_teacher_no_school(self):
        response = teacher_patch_by_id(None, 1, TEACHER_IN_999)
        status, *data = response
        self.assertEquals(status, 404)
        self.assertEquals(data[0], {'message': 'Not Found'})


class DeleteTeacher(TestCase):
    def setUp(self):
        school_create(None, SCHOOL_IN_1)
        school_create(None, SCHOOL_IN_2)
        headmaster_create(None, HEADMASTER_IN_1)
        headmaster_create(None, HEADMASTER_IN_2)
        teacher_create(None, TEACHER_IN_1)

    def test_delete_teacher_basic(self):
        response = teacher_delete_by_id(None, 1)
        status, *data = response
        self.assertEqual(status, 204)
        self.assertEqual(data[0], None)
        response = teacher_get_by_id(None, 1)
        status, *data = response
        self.assertEquals(status, 404)
        self.assertEquals(data[0], {'message': 'Not Found'})

    def test_delete_teacher_no_teacher(self):
        response = teacher_delete_by_id(None, 999)
        status, *data = response
        self.assertEquals(status, 404)
        self.assertEquals(data[0], {'message': 'Not Found'})


class GetStudent(TestCase):
    def setUp(self):
        school_create(None, SCHOOL_IN_1)
        school_create(None, SCHOOL_IN_2)
        headmaster_create(None, HEADMASTER_IN_1)
        headmaster_create(None, HEADMASTER_IN_2)
        teacher_create(None, TEACHER_IN_1)
        teacher_create(None, TEACHER_IN_2)

    def test_post_student_basic(self):
        response = student_create(None, STUDENT_IN1)
        status, *data = response
        self.assertEqual(status, 201)
        self.assertEqual(data[0].name, "std 11")
        self.assertEqual(data[0].school.name, "school 1")
        self.assertEqual(data[0].teacher.name, "T1")

    def test_get_student_basic(self):
        student_create(None, STUDENT_IN1)
        response = student_get_by_id(None, 1)
        status, *data = response
        self.assertEqual(status, 200)
        self.assertEqual(data[0].name, "std 11")
        self.assertEqual(data[0].school.name, "school 1")
        self.assertEqual(data[0].teacher.name, "T1")

    def test_post_student_no_school(self):
        response = student_create(None, STUDENT_SCHOOL999)
        status, *data = response
        self.assertEquals(status, 404)
        self.assertEquals(data[0], {'message': 'Not Found'})

    def test_post_student_no_teacher(self):
        response = student_create(None, STUDENT_TEACHER999)
        status, *data = response
        self.assertEquals(status, 404)
        self.assertEquals(data[0], {'message': 'Not Found'})

    def test_get_student_no_student(self):
        response = student_get_by_id(None, 999)
        status, *data = response
        self.assertEquals(status, 404)
        self.assertEquals(data[0], {'message': 'Not Found'})


class PutStudent(TestCase):
    def setUp(self):
        school_create(None, SCHOOL_IN_1)
        school_create(None, SCHOOL_IN_2)
        headmaster_create(None, HEADMASTER_IN_1)
        headmaster_create(None, HEADMASTER_IN_2)
        teacher_create(None, TEACHER_IN_1)
        teacher_create(None, TEACHER_IN_2)
        student_create(None, STUDENT_IN1)
        student_create(None, STUDENT_IN2)

    def test_put_student_basic(self):
        response = student_put_by_id(None, 1, STUDENT_PUT)
        status, *data = response
        self.assertEquals(status, 200)
        self.assertEquals(data[0].name, "std 999")
        self.assertEquals(data[0].year, "2")

    def test_put_student_no_student(self):
        response = student_put_by_id(None, 999, STUDENT_PUT)
        status, *data = response
        self.assertEquals(status, 404)
        self.assertEquals(data[0], {'message': 'Not Found'})

    def test_put_student_no_school(self):
        response = student_put_by_id(None, 1, STUDENT_SCHOOL999)
        status, *data = response
        self.assertEquals(status, 404)
        self.assertEquals(data[0], {'message': 'Not Found'})

    def test_put_student_no_teacher(self):
        response = student_put_by_id(None, 1, STUDENT_TEACHER999)
        status, *data = response
        self.assertEquals(status, 404)
        self.assertEquals(data[0], {'message': 'Not Found'})

    def test_patch_student_basic(self):
        response = student_patch_by_id(None, 1, STUDENT_PUT)
        status, *data = response
        self.assertEquals(status, 200)
        self.assertEquals(data[0].name, "std 999")
        self.assertEquals(data[0].year, "2")

    def test_patch_student_no_choice(self):
        response = student_patch_by_id(None, 1, STUDENT_PATCH_NO_CHOICE)
        status, *data = response
        self.assertEquals(status, 406)
        self.assertEquals(data[0], {'message', 'Bad input'})


class DeleteStudent(TestCase):
    def setUp(self):
        school_create(None, SCHOOL_IN_1)
        school_create(None, SCHOOL_IN_2)
        headmaster_create(None, HEADMASTER_IN_1)
        headmaster_create(None, HEADMASTER_IN_2)
        teacher_create(None, TEACHER_IN_1)
        teacher_create(None, TEACHER_IN_2)
        student_create(None, STUDENT_IN1)
        student_create(None, STUDENT_IN2)

    def test_delete_student_basic(self):
        response = student_delete_by_id(None, 1)
        status, *data = response
        self.assertEquals(status, 204)
        self.assertEquals(data[0], None)
        response = student_put_by_id(None, STUDENT_PUT, 1)
        status, *data = response
        self.assertEquals(status, 404)
        self.assertEquals(data[0], {'message': 'Not Found'})

    def test_delete_student_no_student(self):
        response = student_delete_by_id(None, 999)
        status, *data = response
        self.assertEquals(status, 404)
        self.assertEquals(data[0], {'message': 'Not Found'})




class ClassesPost(TestCase):
    def setUp(self):
        school_create(None, SCHOOL_IN_1)
        school_create(None, SCHOOL_IN_2)
        teacher_create(None, TEACHER_IN_1)
        teacher_create(None, TEACHER_IN_2)

    def test_post_class_basic(self):
        response = tclasses_create(None, TCLASSES_IN1)
        status, *data = response
        self.assertEquals(status, 201)
        self.assertEquals(data[0].title, "class1")
        self.assertEquals(data[0].description, "class1 class1")
        self.assertEquals(data[0].school.id, 1)
        self.assertEquals(data[0].teacher.id, 1)

    def test_post_class_no_teacher(self):
        response = tclasses_create(None, TCLASSES_NO_TEACHER)
        status, *data = response
        self.assertEquals(status, 404)
        self.assertEquals(data[0], {'message': 'Not Found'})

    def test_post_class_no_school(self):
        response = tclasses_create(None, TCLASSES_NO_TEACHER)
        status, *data = response
        self.assertEquals(status, 404)
        self.assertEquals(data[0], {'message': 'Not Found'})

    def test_post_class_teacher_not_in_school(self):

        response = tclasses_create(None, TCLASSES_NO_TEACHERSCHOOL)
        status, *data = response
        self.assertEquals(status, 406)
        self.assertEquals(data[0], {'message', 'Bad Input'})


class GetClasses(TestCase):
    def setUp(self):
        school_create(None, SCHOOL_IN_1)
        school_create(None, SCHOOL_IN_2)
        teacher_create(None, TEACHER_IN_1)
        teacher_create(None, TEACHER_IN_2)
        tclasses_create(None, TCLASSES_IN1)

    def test_get_class_basic(self):
        response = tclasses_get_by_id(None, 1)
        status, *data = response
        self.assertEquals(status, 200)
        self.assertEquals(data[0].title, 'class1')

    def test_get_class_no_class(self):
        response = tclasses_get_by_id(None, 999)
        status, *data = response
        self.assertEquals(status, 404)
        self.assertEquals(data[0], {'Message': 'Not Found'})


class PutPatchClass(TestCase):
    def setUp(self):
        school_create(None, SCHOOL_IN_1)
        school_create(None, SCHOOL_IN_2)
        teacher_create(None, TEACHER_IN_1)
        teacher_create(None, TEACHER_IN_2)
        tclasses_create(None, TCLASSES_IN1)

    def test_put_class_basic(self):
        response = tclasses_put_by_id(None, 1, TCLASSES_IN2)
        status, *data = response
        self.assertEquals(status, 200)
        self.assertEquals(data[0].title, "class2")
        self.assertEquals(data[0].description, "class2 class2")
        self.assertEquals(data[0].school.id, 2)
        self.assertEquals(data[0].teacher.id, 2)

    def test_put_class_no_class(self):
        response = tclasses_put_by_id(None, 999, TCLASSES_IN2)
        status, *data = response
        self.assertEquals(status, 404)
        self.assertEqual(data[0], {'Message': 'Not Found'})

    def test_put_class_no_school(self):
        response = tclasses_put_by_id(None, 1, TCLASSES_NO_SCHOOL)
        status, *data = response
        self.assertEquals(status, 404)
        self.assertEqual(data[0], {'Message': 'Not Found'})

    def test_put_class_no_techer(self):
        response = tclasses_put_by_id(None, 1, TCLASSES_NO_TEACHER)
        status, *data = response
        self.assertEquals(status, 404)
        self.assertEquals(data[0], {'Message': 'Not Found'})

    def test_put_class_no_teacher_in_school(self):
        response = tclasses_put_by_id(None, 1, TCLASSES_NO_TEACHERSCHOOL)
        status, *data = response
        self.assertEquals(status, 406)
        self.assertEquals(data[0], {'Message', 'Bad Input'})

    # patch
    def test_patch_class_basic(self):
        response = tclasses_patch_by_id(None, 1, TCLASSES_INPATCH)
        status, *data = response
        self.assertEquals(status, 200)
        self.assertEquals(data[0].title, "PATCH")
        self.assertEquals(data[0].description, "class1 class1")
        self.assertEquals(data[0].school.id, 1)
        self.assertEquals(data[0].teacher.id, 1)

    def test_patch_class_no_class(self):
        response = tclasses_patch_by_id(None, 999, TCLASSES_IN2)
        status, *data = response
        self.assertEquals(status, 404)
        self.assertEqual(data[0], {'Message': 'Not Found'})


class deleteClasses(TestCase):
    def setUp(self):
        school_create(None, SCHOOL_IN_1)
        school_create(None, SCHOOL_IN_2)
        teacher_create(None, TEACHER_IN_1)
        teacher_create(None, TEACHER_IN_2)
        tclasses_create(None, TCLASSES_IN1)

    def test_delete_classes_basic(self):
        response = tclasses_delete_by_id(None, 1)
        status, *data = response
        self.assertEquals(status, 204)
        self.assertEquals(data[0], None)
        response = tclasses_get_by_id(None, 1)
        status, *data = response
        self.assertEquals(status, 404)
        self.assertEquals(data[0], {'Message': 'Not Found'})

    def test_delete_class_no_class(self):
        response = tclasses_delete_by_id(None, 999)
        status, *data = response
        self.assertEquals(status, 404)
        self.assertEquals(data[0], {'Message': 'Not Found'})
