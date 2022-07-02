from flask import Blueprint, render_template, redirect, url_for, request, flash, session
import pymongo

auth = Blueprint('auth', __name__)

connection = pymongo.MongoClient('localhost', 27017)
database = connection['IMS']
print("Database connection is successful")
StuDetails = database['StudentDetails']
StuScore = database['ScoreDetails']
StuInst = database['Instructor']


def get_StuDetails():
        return StuDetails.find()

def get_StuScore():
        return StuScore.find()

def get_StuInst():
        return StuInst.find()
