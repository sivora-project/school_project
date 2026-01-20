from django.db import models

class UserCredential(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'user_credentials'

    def __str__(self):
        return self.username

class AcademicCalendar(models.Model):
    date = models.DateField(primary_key=True)

    is_working_day = models.BooleanField(
        unique=True,
        db_column='is_working_day'
    )

    reason = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_column='reason'
    )
    academic_year = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_column='academic_year'
    )


    class Meta:
        managed = False
        db_table = 'academic_calender'

class Attendance(models.Model):
    id = models.AutoField(primary_key=True)

    Student_pen = models.CharField(
        max_length=100,
        unique=True,
        db_column='student_pen'
    )

    attendance_date = models.DateField(db_column='attendance_date')

    status = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        db_column='status'
    )

    marked_by = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        db_column='marked_by'
    )

    created_at = models.DateTimeField(db_column='created_at')

    class Meta:
        managed = False
        db_table = 'attendence'

class Classes(models.Model):
    id = models.AutoField(primary_key=True)

    class_name = models.CharField(
        max_length=100,
        unique=True,
        db_column='class_name'
    )

    section = models.CharField(
        max_length=10,
        db_column='section'
    )

    academic_year = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        db_column='academic_year'
    )

    is_active = models.BooleanField(db_column='is_active')

    created_at = models.DateTimeField(db_column='created_at')

    class Meta:
        managed = False
        db_table = 'classes1'

class Student(models.Model):
    student_id = models.AutoField(
        primary_key=True,
        db_column='student_id'
    )

    student_pen = models.CharField(
        max_length=20,
        unique=True,
        db_column='student_pen'
    )

    student_class = models.TextField(db_column='classes')
    section = models.TextField(db_column='sections', null=True, blank=True)
    name = models.TextField(db_column='student_name', null=True, blank=True)
    gender = models.TextField(db_column='gender1', null=True, blank=True)
    father_name = models.TextField(db_column='father_name', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'student'


# =========================
# FEE MODULE (NEW - APPENDED)
# =========================

class FeeHead(models.Model):
    id = models.AutoField(primary_key=True)
    fee_code = models.CharField(max_length=30, unique=True)
    fee_name = models.CharField(max_length=100)
    is_term_fee = models.BooleanField(default=False)
    is_optional = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'fee_heads'

    def __str__(self):
        return self.fee_name


class FeeStructure(models.Model):
    id = models.AutoField(primary_key=True)
    class_ref = models.ForeignKey(
        Classes,
        on_delete=models.CASCADE,
        db_column='class_id'
    )
    academic_year = models.CharField(max_length=9)
    fee_head = models.ForeignKey(
        FeeHead,
        on_delete=models.SET_NULL,
        null=True,
        db_column='fee_head_id'
    )
    term_no = models.IntegerField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'fee_structure'


class StudentFee(models.Model):
    id = models.AutoField(primary_key=True)
    # student = models.ForeignKey(
    #     Student,
    #     on_delete=models.CASCADE,
    #     db_column='student_id',
    #     to_field='student_pen'
    # )
    student_id = models.IntegerField(db_column='student_id')

    academic_year = models.CharField(max_length=9)
    fee_head = models.ForeignKey(
        FeeHead,
        on_delete=models.SET_NULL,
        null=True,
        db_column='fee_head_id'
    )
    term_no = models.IntegerField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'student_fee'


class FeePayment(models.Model):
    id = models.AutoField(primary_key=True)
    student_fee = models.ForeignKey(
        StudentFee,
        on_delete=models.CASCADE,
        db_column='student_fee_id'
    )
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=30)
    receipt_no = models.CharField(max_length=50)
    utr_number = models.CharField(max_length=50, db_column='UTR_Number')
    class Meta:
        managed = False
        db_table = 'fee_payments'



# =========================
# SUBJECTS
# =========================
class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    subject_code = models.CharField(max_length=20, unique=True)
    subject_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'subjects'


# =========================
# EXAM MASTER
# =========================
class ExamMaster(models.Model):
    exam_code = models.CharField(max_length=10, primary_key=True)
    exam_name = models.CharField(max_length=50)
    term_no = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'exam_master'


# =========================
# STUDENT MARKS (NEW)
# =========================
class StudentMarks(models.Model):
    id = models.AutoField(primary_key=True)

    student = models.ForeignKey(
        Student,
        on_delete=models.DO_NOTHING,
        db_column='student_id',
        db_constraint=False  # 👈 IMPORTANT
    )
    class_id = models.IntegerField(db_column='class_id')
    subject_code = models.CharField(max_length=20)
    exam_code = models.CharField(max_length=10)
    academic_year = models.CharField(max_length=9)
    marks_obtained = models.IntegerField()
    is_absent = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'student_marks'






# class StudentMarks(models.Model):
#     id = models.AutoField(primary_key=True)
#
#     student_id = models.CharField(
#         max_length=100,
#         unique=True,
#         db_column='student_pen'
#     )
#
#     exam_type = models.CharField(
#         max_length=100,
#         unique=True,
#         db_column='types'
#     )
#
#     date_of_exam = models.DateField(db_column='date_of_exam')
#
#     subject = models.CharField(
#         max_length=50,
#         null=True,
#         blank=True,
#         db_column='subject'
#     )
#
#     max_marks = models.IntegerField(
#         null=True,
#         blank=True,
#         db_column='total_marks'
#     )
#
#     marks = models.IntegerField(
#         null=True,
#         blank=True,
#         db_column='scored_marks'
#     )
#
#     created_at = models.DateTimeField(db_column='created_at')
#
#     class Meta:
#         managed = False
#         db_table = 'marks'
