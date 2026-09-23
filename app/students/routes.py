from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from sqlalchemy import or_

from app.students import students
from app.students.forms import StudentForm

from app.extensions import db
from app.models.student import Student
from app.models.transaction import Transaction


# -----------------------------
# View All Students + Search
# -----------------------------
@students.route("/")
@login_required
def index():

    search = request.args.get("search", "").strip()

    query = Student.query

    if search:

        query = query.filter(

            or_(

                Student.student_id.ilike(f"%{search}%"),

                Student.name.ilike(f"%{search}%"),

                Student.email.ilike(f"%{search}%"),

                Student.course.ilike(f"%{search}%")

            )

        )

    students_list = query.order_by(Student.id.desc()).all()

    return render_template(
        "students/index.html",
        students=students_list,
        search=search
    )


# -----------------------------
# Add Student
# -----------------------------
@students.route("/add", methods=["GET", "POST"])
@login_required
def add_student():

    form = StudentForm()

    if form.validate_on_submit():

        student = Student(
            student_id=form.student_id.data,
            name=form.name.data,
            email=form.email.data,
            course=form.course.data,
            semester=form.semester.data,
            phone=form.phone.data
        )

        db.session.add(student)
        db.session.commit()

        flash("Student added successfully!", "success")

        return redirect(url_for("students.index"))

    return render_template(
        "students/add_student.html",
        form=form
    )


# -----------------------------
# Edit Student
# -----------------------------
@students.route("/edit/<int:student_id>", methods=["GET", "POST"])
@login_required
def edit_student(student_id):

    student = Student.query.get_or_404(student_id)

    form = StudentForm()

    if form.validate_on_submit():

        student.student_id = form.student_id.data
        student.name = form.name.data
        student.email = form.email.data
        student.course = form.course.data
        student.semester = form.semester.data
        student.phone = form.phone.data

        db.session.commit()

        flash("Student updated successfully!", "success")

        return redirect(url_for("students.index"))

    form.student_id.data = student.student_id
    form.name.data = student.name
    form.email.data = student.email
    form.course.data = student.course
    form.semester.data = student.semester
    form.phone.data = student.phone

    return render_template(
        "students/edit_student.html",
        form=form
    )


# -----------------------------
# Delete Student
# -----------------------------
@students.route("/delete/<int:student_id>", methods=["POST"])
@login_required
def delete_student(student_id):

    student = Student.query.get_or_404(student_id)

    if Transaction.query.filter_by(student_id=student.id).first():

        flash(
            "Cannot delete this student because transaction records exist.",
            "danger"
        )

        return redirect(url_for("students.index"))

    db.session.delete(student)
    db.session.commit()

    flash("Student deleted successfully!", "success")

    return redirect(url_for("students.index"))