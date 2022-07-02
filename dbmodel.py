from flask import Blueprint, render_template, redirect, url_for, request, flash
import os
from templates import db

# dbmodel = Blueprint('dbmodel', __name__)


# @dbmodel.route('/AddStudent', methods=['GET','POST'])
# def AddStudent():
#     if request.method == "POST":
#         sfname = request.form.get('sfname')
#         slname = request.form.get('slname')
#         sparentdetails = request.form.get('sparentdetails')
#         sp_address = request.form.get('sp_address')
#         st_address = request.form.get('st_address')
#         sclasses = request.form.get('sclasses')
#         studentid = request.form.get('studentid')

#         AddStu = db.StudentDetails.insert({"First Name":"sfname", "Last Name":"slname","Parent Name":"sparentdetails", "Permanene Address":"sp_address","Temporary Address":"st_address", "Class Enrolled":"sclasses", "StudentId":"studentid"})
#         db.StudentDetails.insert(AddStu)
#         db.StudentDetails.commit()

#         flash('Student Details addedd successfully', category='success')
#         return redirect(url_for('views.AddStudent'))

#     return render_template("Add_Student.html")
