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


class StudentMarks(models.Model):
    id = models.AutoField(primary_key=True)

    student_id = models.CharField(
        max_length=100,
        unique=True,
        db_column='student_pen'
    )

    exam_type = models.CharField(
        max_length=100,
        unique=True,
        db_column='types'
    )

    date_of_exam = models.DateField(db_column='date_of_exam')

    subject = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        db_column='subject'
    )

    max_marks = models.IntegerField(
        null=True,
        blank=True,
        db_column='total_marks'
    )

    marks = models.IntegerField(
        null=True,
        blank=True,
        db_column='scored_marks'
    )

    created_at = models.DateTimeField(db_column='created_at')

    class Meta:
        managed = False
        db_table = 'marks'

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
    student_pen = models.CharField(
    max_length=20,
    primary_key=True,
    db_column='student_pen')

    student_class = models.TextField(
        db_column='classes'
    )
    # id = models.BigIntegerField(
    #     db_column='student_pen'
    # )
    # student_class = models.ForeignKey(
    #     Classes,
    #     on_delete=models.CASCADE,
    #     db_column='classes',
    #     related_name='students'
    # )
    # class_name = models.TextField(
    #     db_column='classes',
    #     null=True,
    #     blank=True
    # )

    section = models.TextField(
        db_column='sections',
        null=True,
        blank=True
    )

    name = models.TextField(
        db_column='student_name',
        null=True,
        blank=True
    )

    gender = models.TextField(
        db_column='gender1',
        null=True,
        blank=True
    )
    father_name= models.TextField(
        db_column='father_name',
        null=True,
        blank=True
    )



    class Meta:
        managed = False
        db_table = 'student'
