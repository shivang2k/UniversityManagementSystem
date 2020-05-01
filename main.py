from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)
myconn = mysql.connector.connect(host = "localhost", user = "root",passwd = "qwerty1234", database="university")
print(myconn)

@app.route('/')
def hello():
    return render_template('hello.html')


@app.route('/admin')
def admin():
    return render_template('login_admin.html')


@app.route('/students')
def std():
    return render_template('login.html')


@app.route('/parents')
def par():
    return render_template('login_par.html')


@app.route('/faculty')
def fac():
    return render_template('login_fac.html')


@app.route('/login',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      rid = result["rid"]
      pas = result["pass"]
      mycursor = myconn.cursor()
      query_string = "SELECT Password FROM studentlogin where RegistrationNumber = %s"
      mycursor.execute(query_string, (rid,))
      myresult = mycursor.fetchall()
      if(myresult == []):
          return render_template("fail.html")
      for row in myresult:
          #print ("%s" % (row["Password"]))
          res = row[0]
      if res == pas:
          query_string = "SELECT * FROM students where RegistrationNumber = %s"
          mycursor.execute(query_string, (rid,))
          myresult = mycursor.fetchall()
          for row in myresult:
              pid = row[11]
          print(pid)
          query2 = "SELECT * FROM parents where ParentID = %s"
          mycursor = myconn.cursor()
          mycursor.execute(query2, (pid,))
          myresult.append(mycursor.fetchall()[0])
          query3 = "SELECT SubjectName from students_studies_subjects join subjects on RegistrationNumber = %s and students_studies_subjects.SubjectID = subjects.SubjectID;"
          mycursor = myconn.cursor()
          mycursor.execute(query3, (rid,))
          myresult.append(mycursor.fetchall())
          query4 = "Select marks.Component, MarksScored, MaxMarks, subjects.SubjectName from marks join subjects on RegistrationNumber = %s and marks.SubjectID = subjects.SubjectID;"
          mycursor = myconn.cursor()
          mycursor.execute(query4, (rid,))
          myresult.append(mycursor.fetchall())
          print(myresult)
          return render_template("main_page.html",result = myresult)
      else:
          return render_template("fail.html")


@app.route('/login_par',methods = ['POST', 'GET'])
def result_par():
   if request.method == 'POST':
      result = request.form
      pid = result["pid"]
      pas = result["pass"]
      mycursor = myconn.cursor()
      query_string = "SELECT Password FROM parentlogin where ParentID = %s"
      mycursor.execute(query_string, (pid,))
      myresult = mycursor.fetchall()
      if(myresult == []):
          return render_template("fail.html")
      for row in myresult:
          res = row[0]
      if res == pas:
          query2 = "SELECT * FROM students where ParentID = %s"
          mycursor.execute(query2, (pid,))
          myresult = mycursor.fetchall()
          print(myresult)
          return render_template("main_page_par.html",result = myresult)
      else:
          return render_template("fail.html")


@app.route('/login_fac',methods = ['POST', 'GET'])
def result_fac():
   if request.method == 'POST':
      result = request.form
      fid = result["fid"]
      pas = result["pass"]
      mycursor = myconn.cursor()
      query_string = "SELECT Password FROM facultylogin where facultyID = %s"
      mycursor.execute(query_string, (fid,))
      myresult = mycursor.fetchall()
      if(myresult == []):
          return render_template("fail.html")
      for row in myresult:
          res = row[0]
      if res == pas:
          query2 = "SELECT * FROM faculty where FacultyID = %s"
          mycursor.execute(query2, (fid,))
          myresult = mycursor.fetchall()
          for row in myresult:
              sal = row[-1]
              desid = row[-2]
              depid = row[-3]

          query2 = "SELECT DepartmentName, Salary, Designation FROM department, salary, designation where DesignationID = %s and SalaryID = %s and DepartmentID = %s;"
          mycursor.execute(query2, (desid, sal, depid,))
          myresult.append(mycursor.fetchall()[0])
          query2 = "SELECT SubjectName FROM university.faculty_teaches_subjects join subjects on FacultyID = %s and faculty_teaches_subjects.SubjectID = subjects.SubjectID;"
          mycursor.execute(query2, (fid,))
          myresult.append(mycursor.fetchall())
          print(myresult)
          return render_template("main_page_fac.html",result = myresult)
      else:
          return render_template("fail.html")


@app.route('/login_fac/marks',methods = ['POST', 'GET'])
def result_fac_marks():
   if request.method == 'POST':
      result = request.form
      rid = result["rid"]
      sid = result["sid"]
      comp = result["comp"]
      marks = result["m"]
      maxmarks = result["mm"]
      sem = result["sem"]
      mycursor = myconn.cursor()
      query = "INSERT INTO university.marks VALUES(%s, %s, %s, %s, %s, %s);"
      mycursor.execute(query, (rid,sid,comp,marks,maxmarks,sem,))
      myconn.commit()
      return render_template("main_page_fac_inserted.html")



@app.route('/login_admin',methods = ['POST', 'GET'])
def result_admin():
   if request.method == 'POST':
      result = request.form
      aid = result["aid"]
      pas = result["pass"]
      if(pas == 'ABC'):
          return render_template("main_admin.html")
      else:
          return render_template("fail.html")


@app.route('/login_admin/student',methods = ['POST', 'GET'])
def result_admin_student():
   if request.method == 'POST':
      result = request.form
      rid = result["rid"]
      mycursor = myconn.cursor()
      query = "CREATE VIEW Details AS SELECT RegistrationNumber, FirstName, LastName, CGPA, students.DepartmentID, Semester, Fees, department.DepartmentName, students.ParentID, FatherName, MotherName, FatherPhoneNumber, MotherPhoneNumber, parents.Email FROM students, parents, department where RegistrationNumber = %s and parents.ParentID = students.ParentID and department.DepartmentID = students.DepartmentID;"
      mycursor.execute(query, (rid,))
      query2 = "SELECT * FROM Details;"
      mycursor.execute(query2)
      myresult = mycursor.fetchall()
      mycursor.execute("DROP VIEW Details;")
      return render_template("main_admin.html", result = myresult, students = True)


@app.route('/login_admin/faculty',methods = ['POST', 'GET'])
def result_admin_faculty():
   if request.method == 'POST':
      result = request.form
      fid = result["fid"]
      mycursor = myconn.cursor()
      query = "CREATE VIEW Details AS SELECT FacultyID, FirstName, LastName, DepartmentName, Designation, Salary FROM university.faculty, salary, designation, department where FacultyID = %s and department.DepartmentID = faculty.DepartmentID and designation.DesignationID = faculty.DesignationID and salary.SalaryID = faculty.SalaryID;"
      mycursor.execute(query, (fid,))
      query2 = "SELECT * FROM Details;"
      mycursor.execute(query2)
      myresult = mycursor.fetchall()
      query3 = "SELECT SubjectName FROM university.faculty_teaches_subjects join subjects on FacultyID = %s and faculty_teaches_subjects.SubjectID = subjects.SubjectID;"
      mycursor.execute(query3, (fid,))
      myresult.append(mycursor.fetchall())
      mycursor.execute("DROP VIEW Details;")
      return render_template("main_admin.html", result = myresult, faculty = True)


if __name__ == '__main__':
    app.run(debug=True)
