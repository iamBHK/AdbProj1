from datetime import date
from hashlib import pbkdf2_hmac
import json
from unicodedata import category
from xml.sax import SAXParseException
from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
import os
import pymongo
from passlib.hash import pbkdf2_sha256
from functools import wraps
from bson.objectid import ObjectId
import uuid
import itertools

views = Blueprint('views', __name__)

try:
    mongodb = pymongo.MongoClient('localhost', 27017, serverSelectionTimeoutMS=1000)
    db = mongodb.IMS
    mongodb.server_info()

except:
    print("Database connection error!")


@views.route('/home')
def home():
    if "ulogin" in session:
        ulogin = session['ulogin']
        return render_template("home.html")
    else:
        return redirect(url_for('views.login'))


@views.route('/master', methods=['GET','POST'])
def master():
    if request.method == 'POST':
        admLogin = db.MasterAdmin.find_one({
            'Email' : request.form.get('admemail')
        })
        if admLogin and pbkdf2_sha256.verify(request.form.get('admpassword'), admLogin['Password']):
            Maulogin = request.form.get('admemail')
            session['Maulogin'] = Maulogin
            return redirect(url_for('views.register'))
        else:
            flash("Credentials mismatch", category='error')
            return redirect(url_for('views.master'))
    else:
        if 'Maulogin' in session:
            return redirect(url_for('views.register'))
        else:
            return render_template('master.html')    


@views.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        userlogin = db.Registration.find_one({
            'Email' : request.form.get('email')
        })
        ulogin = request.form.get('email')
        if userlogin and pbkdf2_sha256.verify(request.form.get('password'), userlogin['Password']):
            session['ulogin'] = ulogin
            return redirect(url_for('views.home'))
        else:
            flash("Credentials mismatch", category='error')
            return redirect(url_for('views.login'))
    else:
        if 'ulogin' in session:
            return redirect(url_for('views.home'))
        else:
            return render_template('login.html')    

@views.route('/logout')
def logout():
    if "ulogin" in session:
        session.pop("ulogin", None)
        flash('Logged out successfully', category='success')
        return render_template('login.html')
    else:
        return redirect(url_for('views.register'))

@views.route('/malogout')
def malogout():
    if "Maulogin" in session:
        session.pop("Maulogin", None)
        flash('Logged out successfully', category='success')
        return render_template('master.html')
    else:
        return redirect(url_for('views.home'))

@views.route('/register', methods=['GET','POST'])
def register():
    if "Maulogin" in session:
        Maulogin = session['Maulogin']
        if request.method == "POST":
            regdata = {
                'First_Name' : request.form.get('fname'),
                'Last_Name' : request.form.get('lname'),
                'Email' : request.form.get('email'),
                'Mobile_Number' : request.form.get('mobile'),
                'Password' : request.form.get('pwd1'),
                'Password2' : request.form.get('pwd2')
            }
            if len(regdata['First_Name']) < 4:
                flash("First Name should be atleast 4 characters.", category='error')
            elif len(regdata['Last_Name']) < 4:
                flash("Last Name should be atleast 4 characters.", category='error')
            elif len(regdata['Email']) < 5:
                flash("Email is not in correct format.", category='error')
            elif len(regdata['Mobile_Number']) < 10 :
                flash("Mobile Number should be atleast 10 numbers.", category='error')
            elif len(regdata['Password']) < 6 :
                flash("Password should be atleast 6 characters.", category='error')
            elif len(regdata['Password']) != len(regdata['Password2']):
                flash("Password not matched.", category='error')
            else:
                if db.Registration.find_one({ 'Email': regdata['Email'] }):
                    flash("Email id already registered.", category='error')
                else:
                    regdata['Password'] = pbkdf2_sha256.encrypt(regdata['Password'])
                    db.Registration.insert_one(regdata)
                    # db.Registration.commit()
                    flash('Added new employee successfully', category='success')
                    return redirect(url_for('views.register'))

        return render_template("register.html")
    else:
        return redirect(url_for('views.login'))

@views.route('/CreateClass', methods=['GET','POST'])
# #@login_req
def CreateClass():
    if "ulogin" in session:
        ulogin = session['ulogin']
        InstData = db.Instructor.find()
        InstDataOP = [{item: data[item] for item in data if item != '_id'} for data in InstData]

        if request.method == "POST":
            classdata = {
                'classid' : request.form.get('calssid'),
                'standard' : request.form.get('standard'),
                'year' : request.form.get('year'),
                'semester' : request.form.get('semester'),
                # 'section' : request.form.get('section'),
                'room' : request.form.get('room'),
                'ctimings' : request.form.get('ctimings'),
                'instructorid' : request.form.get('instructorid')
            }
            if len(classdata['classid']) !=5:
                flash("Class id should be 5 characters.", category='error')
            elif len(classdata['standard']) < 4:
                flash("Standard should be atleast 4 characters.", category='error')
            elif len(classdata['year']) !=4:
                flash("Year should be 4 characters.", category='error')
            elif len(classdata['semester']) < 4:
                flash("Semester should be 4 characters.", category='error')
            # elif len(classdata['section']) < 2:
            #     flash("Section should be 2 characters.", category='error')
            elif len(classdata['room']) < 4:
                flash("Room Number should be atleast 4 characters.", category='error')
            elif len(classdata['ctimings']) < 10:
                flash("Please use the suggested timings format.", category='error')
            elif len(classdata['instructorid']) < 2:
                flash("Should assign Instructor.", category='error')
            
            else:
                if db.ClassSchedule.find_one({"classid" : classdata['classid']}):
                    flash("Class is already created.", category='error')
                else:
                    db.ClassSchedule.insert_one(classdata)
                    flash('Class created successfully', category='success')
                    return redirect(url_for('views.CreateClass'))

        return render_template("Create Class.html", InsDt = InstDataOP)
    else:
        return redirect(url_for('views.login'))

# @views.route('/ShowClass', methods=['GET'])
# def ShowClass():
#     if "ulogin" in session:
#         ulogin = session['ulogin']
        
#         ClassData = db.ClassStuDetails.find()
#         ClsOPA = [{item: data[item] for item in data if item != '_id'} for data in ClassData]
#         # #     ClsData = db.ClassStuDetails.find({'classid': itemlist['classid']})
#         # #     ClsDataOPB = [{item: data[item] for item in data if item != '_id'} for data in ClsData]
#         # #     for inslistB in ClsDataOPB:
#         # #         StuData = db.StudentDetails.find({'StudentId': inslistB['StudentId']})
#         # #         StuDataOPA = [{item: data[item] for item in data if item != '_id'} for data in StuData]
#         return render_template("Show Class.html", ClsData=ClsOPA)
#         # # , , StuDataa=StuDataOPA
            
#         # return render_template("Show Class.html")
#     else:
#         return redirect(url_for('views.login'))
@views.route('/ShowClass', methods=['GET'])
def ShowClass():
    if "ulogin" in session:
        ulogin = session['ulogin']
        
        ClassData = db.StudentDetails.find()
        ClsOPA = [{item: data[item] for item in data if item != '_id'} for data in ClassData]
        # #     ClsData = db.ClassStuDetails.find({'classid': itemlist['classid']})
        # #     ClsDataOPB = [{item: data[item] for item in data if item != '_id'} for data in ClsData]
        # #     for inslistB in ClsDataOPB:
        # #         StuData = db.StudentDetails.find({'StudentId': inslistB['StudentId']})
        # #         StuDataOPA = [{item: data[item] for item in data if item != '_id'} for data in StuData]
        return render_template("Show Class.html", ClsData=ClsOPA)
        # # , , StuDataa=StuDataOPA
            
        # return render_template("Show Class.html")
    else:
        return redirect(url_for('views.login'))

@views.route('/DeleteEnrol/<string:StudentId>', methods=['POST'])
def DeleteEnrol(StudentId):
    if "ulogin" in session:
        ulogin = session['ulogin']
    
        if request.method == "POST":
            stuid = {
                'StudentId': request.form.get('StudentId')
            }
            db.ClassStuDetails.delete_one(stuid)
            flash('Deleted record successfully', category='success')
            return redirect(url_for('views.ShowClass'))

        else:
            return redirect(url_for('views.ShowClass'))
    else:
        return redirect(url_for('views.login'))

@views.route('/Instructor', methods=['GET','POST'])
#@login_req
def Instructor():
    if "ulogin" in session:
        ulogin = session['ulogin']
        
        dbcount = db.Instructor.count_documents({})
        month = date.today().month
        
        if request.method == "POST":
            instdata = {
                'ifname' : request.form.get('ifname'),
                'ilname' : request.form.get('ilname'),
                'iemail' : request.form.get('iemail'),
                'imobile' : request.form.get('imobile'),
                'ipaddress' : request.form.get('ipaddress'),
                'itaddress' : request.form.get('itaddress'),
                'iequalification' : request.form.get('iequalification'),
                'instructorid' : 200+month+dbcount
            }
            if len(instdata['ifname']) < 3:
                flash('First Name should be atleast 3 characters', category='error')
            elif len(instdata['ilname']) < 3:
                flash('Last Name should be atleast 3 characters', category='error')
            elif len(instdata['iemail']) < 4:
                flash('Email should be atleast 4 characters', category='error')
            elif len(instdata['imobile']) < 10:
                flash('Mobile number should be atleast 10 characters', category='error')
            elif len(instdata['ipaddress']) < 10:
                flash('Permanent Address should be atleast 10 characters', category='error')
            elif len(instdata['itaddress']) < 10:
                flash('Temporary Address should be atleast 10 characters', category='error')
            elif len(instdata['iequalification']) < 4:
                flash('Education Qualification should be atleast 4 characters', category='error')
            else:
                if db.Instructor.find_one({ 'iemail': instdata['iemail'] }):
                    flash("Email id already in use.", category='error')
                else:
                    db.Instructor.insert_one(instdata)
                    flash('Added new employee successfully', category='success')
                    return redirect(url_for('views.Instructor'))

        return render_template("Instructor.html")

    else:
        return redirect(url_for('views.login'))

# @views.route('/StudentToClass', methods=['GET','POST'])
# def StudentToClass():
#     if "ulogin" in session:
#         ulogin = session['ulogin']
#         if request.method == "POST":
#             StuintoClass = db.ClassStuDetails.find_one({
#                 'classid' : request.form.get('classid')
#             })
#             # if StuintoClass and ((request.form.get('studentid'), StuintoClass['StudentId'])):
#             #     flash('Student already enrolled into class', category='error')
#             #     return redirect(url_for('views.StudentToClass'))
#             # else:
#             #     # EncSid = pbkdf2_sha256.encrypt(request.form.get('studentid'))
#             db.ClassStuDetails.insert_one({"classid":request.form.get('classid'), "StudentId":request.form.get('studentid'), "SectionId":request.form.get('sectionid')})
#             flash('Enrolled student into class', category='success')
#             return redirect(url_for('views.StudentToClass'))
                

#         return render_template("Add_Student_Class.html")
#     else:
#         return redirect(url_for('views.login'))

@views.route('/StudentToClass', methods=['GET','POST'])
def StudentToClass():
    if "ulogin" in session:
        ulogin = session['ulogin']
        Classes = db.ClassSchedule.find()
        OnlyCid = [{item: data[item] for item in data if item != '_id'} for data in Classes]
        
        if request.method == "POST":
            GetStudentId = db.StudentDetails.find_one({
                'StudentId' : request.form.get('studentid')
            })
            GetClass = {
                'classid' : [
                    request.form.get('classid')
                ],
                'StudentId' : request.form.get('studentid')
            }
            if not GetStudentId :
                if not db.StudentDetails.find_one({"Class_Enrolled": GetClass['classid']}):
                # db.StudentDetails.find({"StudentId" : GetClass['StudentId']})
                    GetEnrClass = db.StudentDetails.find({"StudentId": GetClass['StudentId']})
                    GetEC = [{item: data[item] for item in data if item != '_id'} for data in GetEnrClass]
                    GetStuid = db.StudentDetails.find({"Class_Enrolled": GetClass['classid']})
                    GetSid = [{item: data[item] for item in data if item != '_id'} for data in GetStuid]
                    # if not GetSid:
                    #     # # FetchSid = db.ClassStuDetails.find_one({ 'StudentId' : request.form.get('studentid') })
                    #     # if GetEC or GetSid:
                    #     # # if FetchSid and db.ClassStuDetails.find_one({ 'Class_Enrolled' : scoredata['ClassId'] }):
                    #     #     # db.StudentDetails.find_one({'Class_Enrolled':{$elemMatch : {'Class_Enrolled' : scoredata['ClassId']}}}}).pretty();
                        
                    db.StudentDetails.update_one(
                        {"StudentId": GetClass['StudentId']},
                        {'$set':{'Class_Enrolled': GetClass['classid']}}
                    )
                    # db.StudentDetails.insert_one(GetClass)
                    flash('Student added successfully', category='success')
                    return redirect(url_for('views.StudentToClass'))
                else:
                    flash('Student record not exists.', category='error')
                    return redirect(url_for('views.StudentToClass'))
            else:
                flash('Student Id not exists.', category='error')
                return redirect(url_for('views.StudentToClass'))
            #     GetEnrolledClass = db.StudentDetails.find_one({
            #         "Class_Enrolled": request.form.get('classid'),
            #         'StudentId' : request.form.get('studentid')
            #     })
            #     if GetStudentId and GetEnrolledClass:
            #         flash('Already enrolled in class', category='error')
            #         return redirect(url_for('views.StudentToClass'))
            #     else:
            # db.StudentDetails.update_one({"StudentId": request.form.get('studentid') },{'$push':{"Class_Enrolled": request.form.get('classid')}})
            # db.ClassStuDetails.insert_one({"StudentId": request.form.get('studentid'), "ClassId": request.form.get('classid')})
            # flash('Enrolled into class successfully', category='success')
            # return redirect(url_for('views.StudentToClass'))
            # else:
            #     flash("Invalid student id", category='error')

            return redirect(url_for('views.StudentToClass'))
        else:
            return render_template("Add_Student_Class.html", GetClasses = OnlyCid)
    else:
        return redirect(url_for('views.login'))



# @views.route('/StudentToClass', methods=['GET','POST'])
# def StudentToClass():
#     if "ulogin" in session:
#         ulogin = session['ulogin']
#         Classes = db.ClassSchedule.find()
#         OnlyCid = [{item: data[item] for item in data if item != '_id'} for data in Classes]
        
#         if request.method == "POST":
#             GetStudentId = db.ClassStuDetails.find_one({
#                 'StudentId' : request.form.get('studentid'),
#                 'ClassId' : request.form.get('classid')
#             })
#             getSInfo = {
#                 'Sid' : request.form.get('studentid')
#             }
#             getCinfo = {
#                 'Cid' : request.form.get('classid')            
#             }
#             if not GetStudentId:
#                 db.StudentDetails.update_one({"StudentId": request.form.get('studentid') },{'$push':{"Class_Enrolled": request.form.get('classid')}})
#                 flash("Success.", category='success')    
#                 return redirect(url_for('views.StudentToClass'))    
#             else:
#                 flash("Already enrolled.", category='error')
#                 return redirect(url_for('views.StudentToClass'))

#             # CheckStu = db.StudentDetails.find_one({"StudentId": request.form.get('studentid')})
            
#             # if not CheckStu:
#             #     if not GetStudentId:
#             #         db.StudentDetails.update_one({
#             #             "StudentId": request.form.get('studentid') },
#             #             {'$push':{"Class_Enrolled": request.form.get('classid')}})
#             #         # db.StudentDetails.update_one({
#             #         #     "StudentId": request.form.get('studentid') },
#             #         #     {'$push':{"Class_Enrolled": request.form.get('classid')}
#             #         # })
#             #         db.ClassStuDetails.insert_one({"StudentId": request.form.get('studentid'), "ClassId": request.form.get('classid')})
#             #         flash('Enrolled into class successfully', category='success')
#             #         return redirect(url_for('views.StudentToClass'))
#             #     else:
#             #         flash('Details mismatch / already in class', category='error')
#             #         return redirect(url_for('views.StudentToClass'))

#             # else:
#             #    flash('Invalid student Id', category='error')
#             #    return redirect(url_for('views.StudentToClass'))
                
#         else:
#             return render_template("Add_Student_Class.html", GetClasses = OnlyCid)
#     else:
#         return redirect(url_for('views.login'))


@views.route('/ShowInstructor', methods=['GET'])
#@login_req
def ShowInstructor():
    if "ulogin" in session:
        ulogin = session['ulogin']
        InsData = db.Instructor.find()
        InsOPA = [{item: data[item] for item in data if item != '_id'} for data in InsData]
        # for itemlist in InsOPA:
        #     InsCData = db.ClassSchedule.find({'instructorid': itemlist['instructorid']})
        #     InsCDataOPA = [{item: data[item] for item in data if item != '_id'} for data in InsCData]
        return render_template("Show_Teachers.html", InsData=InsOPA)
            
        return render_template("Show_Teachers.html")
    else:
        return redirect(url_for('views.login'))

@views.route('/AddStudent', methods=['GET','POST'])
#@login_req
def AddStudent():

    if "ulogin" in session:
        ulogin = session['ulogin']
        StuData = db.StudentDetails.find()
        MaxSidB = [{StudentId: data[StudentId] for StudentId in data if StudentId != '_id'} for data in StuData]
        MaxSid = MaxSidB
        
        dbcount = db.StudentDetails.count_documents({})

        yearr = date.today().year
        
        Classes = db.ClassSchedule.find()
        OnlyCid = [{item: data[item] for item in data if item != '_id'} for data in Classes]
        

        if request.method == "POST":
            insdata = {
                'First_Name' : request.form.get('sfname'),
                'Last_Name' : request.form.get('slname'),
                'Parent_Name' : 
                    [
                        request.form.get('fathername'),
                        request.form.get('mothername'),
                        request.form.get('guardianname')
                    ],
                'Perm_Address' : request.form.get('sp_address'),
                'Temp_Address' : request.form.get('st_address'),
                'StudentId' : 700+yearr+dbcount,
                # (db.StudentDetails.find({}, {'StudentId':1, '_id':0})),
                'Class_Enrolled' : [
                    request.form.get('ClassEnroll')
                ]
            }
            

            # StudentId = db.StudentDetails.find({'$inc':{"StudentId" : 1}})

            if len(insdata['First_Name']) < 4:
                flash("First Name should be atleast 4 characters.", category='error')
            elif len(insdata['Last_Name']) < 4:
                flash("Last Name should be atleast 4 characters.", category='error')
            # elif len(insdata['Parent_Name']) < 5:
            #     flash("Parent Name should be atleast 5 characters.", category='error')
            elif len(insdata['Perm_Address']) < 10 :
                flash("Permanent Address should be atleast 10 numbers.", category='error')
            elif len(insdata['Temp_Address']) < 10 :
                flash("Temporary Address should be atleast 10 characters.", category='error')
            # elif len(insdata['StudentId']) != 6 :
            #     flash("Student Id should be only 6 numbers.", category='error')
            else:
                # if insdata['Std1'] == request.form.get('studentid'):
                #     flash('Student Id is already in use', category='error')
                #     return redirect(url_for('views.AddStudent'))
                # else:
                db.StudentDetails.insert_one(insdata)
                # db.StudentDetails.insert_one({
                #     "First_Name": insdata['First_Name'], 
                #     "Last_Name": insdata['Last_Name'], 
                #     "Parent_Name": insdata['Parent_Name'], 
                #     "Perm_Address": insdata['Perm_Address'], 
                #     "Temp_Address": insdata['Temp_Address'], 
                #     "Class_Enrolled": insdata['Class_Enrolled'], 
                #     "StudentId": db.StudentDetails.update_one({"StudentId"},{'$inc':{"StudentId"}})
                # })
                flash('Added new student successfully', category='success')
                return redirect(url_for('views.AddStudent'))
                

        return render_template("Add_Student.html", MaxStudentid = MaxSid, GetClasses = OnlyCid)

        #     db.StudentDetails.insert_one(insdata)
        #     flash('Student Details addedd successfully', category='success')
        #     return redirect(url_for('views.AddStudent'))        
        
        # return render_template("Add_Student.html")
    else:
        return redirect(url_for('views.login'))

#@login_req
@views.route('/Student', methods=['GET'])
def Student():
    if "ulogin" in session:
        ulogin = session['ulogin']

        StuData = db.StudentDetails.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in StuData]
        # for out in output:
        #     ScoD = db.ScoreDetails.find({"StudentId": out['StudentId']})
        #     outputB = [{item: data[item] for item in data if item != '_id'} for data in ScoD]
        #     for outpurB in ScoD:
        #         ScoE = db.ScoreDetails.find({"StudentId": out['StudentId']})
        #         outputB = [{item: data[item] for item in data if item != '_id'} for data in ScoD]
        return render_template("Student_Details.html", SData=output)
        # SMark=outputB
    else:
        return redirect(url_for('views.login'))


@views.route('/Score', methods=['GET','POST'])
#@login_req
def Score():
    if "ulogin" in session:
        ulogin = session['ulogin']
        Classes = db.ClassSchedule.find()
        OnlyCid = [{item: data[item] for item in data if item != '_id'} for data in Classes]
        
        if request.method == "POST":
            scoredata = {
                'ClassId' : request.form.get('classid'),
                'StudentId' : request.form.get('studentid'),
                'FinalGPA' : request.form.get('finalgpa')
            }
            StuEnro = db.StudentDetails.find()
            StuEnr = [{item: data[item] for item in data if item != '_id'} for data in StuEnro]
            
            if len(scoredata['StudentId']) != 4:
                flash("Student Id should be 6 characters", category='error')
            elif float(scoredata['FinalGPA']) > 4:
                flash("Final GPA can be max 4", category='error')
            else:                
                GetEnrClass = db.StudentDetails.find({"StudentId": scoredata['StudentId']})
                GetEC = [{item: data[item] for item in data if item != '_id'} for data in GetEnrClass]
                GetStuid = db.StudentDetails.find({"Class_Enrolled": scoredata['ClassId']})
                GetSid = [{item: data[item] for item in data if item != '_id'} for data in GetStuid]
                if not GetEC and not GetSid:
                    # # FetchSid = db.ClassStuDetails.find_one({ 'StudentId' : request.form.get('studentid') })
                    # if GetEC or GetSid:
                    # # if FetchSid and db.ClassStuDetails.find_one({ 'Class_Enrolled' : scoredata['ClassId'] }):
                    #     # db.StudentDetails.find_one({'Class_Enrolled':{$elemMatch : {'Class_Enrolled' : scoredata['ClassId']}}}}).pretty();
                    db.ScoreDetails.insert_one(scoredata)
                    flash('Student Final GPA added successfully', category='success')
                    return redirect(url_for('views.Score'))
                else:
                    flash('Student GPA exists.', category='error')
                    return redirect(url_for('views.Score'))

        return render_template("Student_Score.html", GetClasses = OnlyCid)
    else:
        return redirect(url_for('views.login'))


@views.route('/ViewScore', methods=['GET'])
def ViewScore():
    if "ulogin" in session:
        ulogin = session['ulogin']
        StuScoData = db.ScoreDetails.find()
        StuScoDataOP = [{item: data[item] for item in data if item != '_id'} for data in StuScoData]
        return render_template("View_Score.html", StMark=StuScoDataOP)
    else:
        return redirect(url_for('views.login'))

@views.route('/SearchAll', methods=["POST"])
def SearchAll():
    if "ulogin" in session:
        ulogin = session['ulogin']
        if request.method == 'POST':
            GetInfo = {
                'id' : request.form.get('query_id')
            }
            if db.StudentDetails.find({"StudentId": GetInfo['id']}) :
                StuInfo = db.StudentDetails.find({"StudentId": GetInfo['id']})
                StAll = [{item: data[item] for item in data if item != '_id'} for data in StuInfo]
                return render_template('Search_Query.html', ShowSinfo = StAll)

            elif db.Instructor.find({"instructorid": GetInfo['id']}) :
                InstInfo = db.Instructor.find({"instructorid": GetInfo['id']})
                InsAll = [{item: data[item] for item in data if item != '_id'} for data in InstInfo]
                return render_template('Search_Query.html', ShowSinfo = InsAll)

            else:
                flash('No Matches found', category='error')
                return render_template('Search_Query.html')
        else:
            return redirect(url_for('views.home'))
    else:
        return redirect(url_for('views.login'))
