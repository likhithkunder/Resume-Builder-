from flask import Flask, request, redirect, url_for, jsonify, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
import hashlib
from datetime import datetime
from sqlalchemy import text
from dotenv import dotenv_values
import secrets
import time

app = Flask(__name__)

app.static_folder = 'static'

conf = dotenv_values(".env.local")

username = conf['USERNAME']
password = conf['PASSWORD']
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:{username}%{password}@localhost/resume_db'
app.secret_key = conf['SECRET']
db = SQLAlchemy(app)

def generate_unique_id():
    current_datetime = datetime.now().strftime('%Y%m%d%H%M%S')  
    unique_hash = hashlib.md5(current_datetime.encode()).hexdigest()[-5:]  
    return unique_hash

def validate(table_name, table_name_id_column, id):
    try:
        result = db.session.execute(
            text("CALL validate_id(:table_name, :table_name_id_column, :id, @is_valid)"),
            {'table_name': table_name, 'table_name_id_column': table_name_id_column, 'id': id}
        )

        result = db.session.execute(text("SELECT @is_valid")).fetchone()
        is_valid = result[0]

        print("number:",is_valid)
        return is_valid

    except Exception as e:
        print(f"An error occurred during ID validation: {str(e)}")
        return False

@app.route('/', methods=['GET'])
def reg():
    return render_template("register.html", who = "User", bType = "user") 

@app.route('/recReg', methods=['GET'])
def recReg():
    return render_template("register.html", who = "Recruiter", bType = "rec")

@app.route('/login', methods=['GET'])
def log():
    return render_template("login.html", who = "User", bType = "user")

@app.route('/recLog', methods=['GET'])
def recLog():
    return render_template("login.html", who = "Recruiter", bType = "rec")  

@app.route('/cardFill', methods=['POST'])
def cardFill():
    buttonType = request.form.get('type')
    return render_template("buttons.html", message = buttonType)

@app.route('/transfer', methods=['POST'])
def transfer():
    r_lType = request.form.get('type')
    who = request.form.get('which')
    if r_lType == "register":
        if who == "user":
            return redirect("/recReg")
        elif who == "rec":
            return redirect("/")
    if r_lType == "login":
        if who == "user":
            return redirect("/recLog")
        elif who == "rec":
            return redirect("/login")

@app.route('/buttonClick', methods=['POST'])
def buttonClick():
    # global current_user_id
    buttonType = request.form.get('type')
    buttonName = request.form.get('button_class')
    if buttonType == 'education':
        if buttonName == 'insert':
            return render_template("form1.html")
        else:
            # conn = db.session.connection()
            conn = db.engine.connect()
            cursor = conn.connection.cursor()

            sql_query = "SELECT ed_id, institute_name, degree, graduation_year FROM education WHERE user_id = %s"
            cursor.execute(sql_query, (session['current_user_id'],))
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            attributes = ["Education ID", "Institute Name", "Degree", "Graduation Year"]
            if buttonName == 'update':
                return render_template('upDel.html', data=data, title="Education", columns=attributes, info=buttonName)
            elif buttonName == 'delete':
                return render_template('upDel.html', data=data, title="Education", columns=attributes, info=buttonName)

    
    elif buttonType == 'workExp':
        if buttonName == 'insert':
            return render_template("form2.html")
        else:
            conn = db.engine.connect()
            cursor = conn.connection.cursor()

            sql_query = "SELECT exp_id, company, job_title, job_desc, no_of_years FROM works_exp WHERE user_id = %s"
            cursor.execute(sql_query, (session['current_user_id'],))
            # print(current_user_id)
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            attributes = ["Experience ID", "Company", "Job Title", "Job Description", "Number of Years"]
            if buttonName == 'update':
                return render_template('upDel.html', data=data, title="Work Experience", columns=attributes, info=buttonName)
            elif buttonName == 'delete':
                return render_template('upDel.html', data=data, title="Work Experience", columns=attributes, info=buttonName)
        
    elif buttonType == 'projects':
        if buttonName == 'insert':
            return render_template("form3.html")
        else:
            conn = db.engine.connect()
            cursor = conn.connection.cursor()

            sql_query = "SELECT project_id, project_name, proj_desc FROM projects WHERE user_id = %s"
            cursor.execute(sql_query, (session['current_user_id'],))
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            attributes = ["Project ID", "Project Name", "Project Description"]
            if buttonName == 'update':
                return render_template('upDel.html', data=data, title="Projects", columns=attributes, info=buttonName)
            elif buttonName == 'delete':
                return render_template('upDel.html', data=data, title="Projects", columns=attributes, info=buttonName)
    
    elif buttonType == 'certificates':
        if buttonName == 'insert':
            return render_template("form4.html")
        else:
            conn = db.engine.connect()
            cursor = conn.connection.cursor()

            sql_query = "SELECT c_id, certificate_name, organisation, issue_date FROM certificates WHERE user_id = %s"
            cursor.execute(sql_query, (session['current_user_id'],))
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            attributes = ["Certificate ID", "Certificate Name", "Organisation", "Issue Date"]
            if buttonName == 'update':
                return render_template('upDel.html', data=data, title="Certificates", columns=attributes, info=buttonName)
            elif buttonName == 'delete':
                return render_template('upDel.html', data=data, title="Certificates", columns=attributes, info=buttonName)
    
    elif buttonType == 'skills':
        if buttonName == 'insert':
            return render_template("form5.html")
        else:
            conn = db.engine.connect()
            cursor = conn.connection.cursor()

            sql_query = "SELECT skill_id, skill_name, proficiency FROM skills WHERE user_id = %s"
            cursor.execute(sql_query, (session['current_user_id'],))
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            #return jsonify(data)
            #print(data)
            attributes = ["Skill ID", "Skill Name", "Proficiency"]
            if buttonName == 'update':
                return render_template('upDel.html', data=data, title="Skills", columns=attributes, info=buttonName)
            elif buttonName == 'delete':
                return render_template('upDel.html', data=data, title="Skills", columns=attributes, info=buttonName)
        
    

@app.route('/add_people', methods=['POST'])
def add_user():
    if request.method == 'POST':
        buttonType = request.form.get("buttonType")

        if buttonType == "user":
            # user_id = generate_unique_id()
            user_name = request.form['user_name']
            password = request.form['password']
            conf_password = request.form['conf_password']
            email = request.form['email']
            name = request.form['name']
            dob = str(datetime.strptime(request.form['dob'], '%Y-%m-%d').date())
            phone_no = request.form['phone_no']

            if password == conf_password:
                new_user = {
                    # 'user_id': user_id,
                    'user_name': user_name,
                    'password': password,
                    'email': email,
                    'name': name,
                    'dob': dob,
                    'phone_no': phone_no
                }

                try:
                    insert_query = text(f"INSERT INTO user ({', '.join(new_user.keys())}) VALUES ({', '.join([':' + key for key in new_user.keys()])})")
                    db.session.execute(insert_query, new_user)
                    db.session.commit()
                    return redirect('/login')
                except Exception as e:
                    return redirect('/')
            else:
                return redirect('/')
            
        elif buttonType == "rec":
            recruiter_name = request.form['user_name']
            password = request.form['password']
            conf_password = request.form['conf_password']
            email = request.form['email']
            name = request.form['name']
            dob = str(datetime.strptime(request.form['dob'], '%Y-%m-%d').date())
            phone_no = request.form['phone_no']

            if password == conf_password:
                new_recruiter = {
                    'recruiter_name': recruiter_name,
                    'password': password,
                    'email': email,
                    'name': name,
                    'dob': dob,
                    'phone_no': phone_no
                }

                try:
                    insert_query = text(f"INSERT INTO recruiter ({', '.join(new_recruiter.keys())}) VALUES ({', '.join([':' + key for key in new_recruiter.keys()])})")
                    db.session.execute(insert_query, new_recruiter)
                    db.session.commit()
                    return redirect('/recLog')
                except Exception as e:
                    error_message = str(e)  # Convert the exception to a string
                    return error_message
            else:
                return redirect('/recReg')

@app.route('/check_people', methods=['POST'])
def check_user():
    buttonType = request.form.get("buttonType")

    if buttonType == "user":
        global current_user_id
        global current_rec_id

        if request.method == 'POST':
            user_name = request.form['user_name']
            password = request.form['password']

            query = text("SELECT user_id FROM user WHERE user_name = :user_name AND password = :password")
            result = db.session.execute(query,{"user_name": user_name, "password": password})

            user = result.fetchone()

            if user:
                # user_dict = {
                #     "user_id": user[0],
                #     "user_name": user[1],
                #     "email": user[2],
                #     "name": user[3],
                #     "dob": user[4],
                #     "phone_no": user[5]
                # }
                # return jsonify(user_dict)
                session['current_user_id'] = user[0]
                # user_id = user[0]
                # current_user_id = user_id
                return render_template('cards.html', message = "success", info = "Logged in Successfully")
            else:
                return redirect('/')
        
    elif buttonType == "rec":
        recruiter_name = request.form['user_name']
        password = request.form['password']
        query = text("SELECT recruiter_id FROM recruiter WHERE recruiter_name = :recruiter_name AND password = :password")
        result = db.session.execute(query,{"recruiter_name": recruiter_name, "password": password})
        recruiter = result.fetchone()
        if recruiter:
            session['current_rec_id'] = recruiter[0]
            return render_template('rec.html', message = "success", info = "Logged in Successfully")
        else:
            return redirect('/recReg')

@app.route('/proceed', methods=['POST'])
def proceed():
    selected_option = request.form.get('option') 
    if selected_option == "sk_wE":
        return render_template('recsel.html', title = "Skills and Work Experience", tag1 = "Skill Name", tag2 = "Work Experience", info = "first")
    elif selected_option == "ce_pr":
        return render_template('recsel.html', title = "Certificates and Projects", tag1 = "Certificate Name", tag2 = "Project Name", info = "second")
    elif selected_option == "ed_sk":
        return render_template('recsel.html', title = "Education and Job", tag1 = "Graduation Year", tag2 = "Job Title", info = "third")
    elif selected_option == "no_pro":
        return render_template('recsel.html', title = "Number of projects", tag1 = "remove", tag2 = "remove", info = "forth")
    elif selected_option == "no_jo":
        return render_template('recsel.html', title = "Number of jobs worked", tag1 = "remove", tag2 = "remove", info = "fifth")
    elif selected_option == "no_cer":
        return render_template('recsel.html', title = "Number of certificates", tag1 = "remove", tag2 = "remove", info = "sixth")
    elif selected_option == "":
        return render_template('rec.html', message = "error", info = "Please select an option")

@app.route('/get_userId', methods=['GET'])
def get_userId():
    if request.method == 'GET':
        user_name = request.form['user_name']
        password = request.form['password']

        query = text("SELECT user_id, user_name, email, name, dob, phone_no FROM user WHERE user_name = :user_name AND password = :password")
        result = db.session.execute(query,{"user_name": user_name, "password": password})

        user = result.fetchone()

        if user:
            return user[0]
        else:
            return "No user found."

@app.route('/add_skills', methods=['POST'])
def add_skills():
    # global current_user_id
    if request.method == 'POST':
        # skill_id = generate_unique_id()
        user_id = session['current_user_id']
        skill_name = request.form['skill_name']
        proficiency = request.form['proficiency'].capitalize()

        new_skill = {
            # 'skill_id': skill_id,
            'user_id': user_id,
            'skill_name': skill_name,
            'proficiency': proficiency
        }

        try:
            insert_query = text(f"INSERT INTO skills ({', '.join(new_skill.keys())}) VALUES ({', '.join([':' + key for key in new_skill.keys()])})")
            db.session.execute(insert_query, new_skill)

            db.session.commit()
            return render_template('cards.html', message = "success", info = "Details inserted successfully")
        except Exception as e:
            return render_template('cards.html', message="error", info="An error occurred")
        
@app.route('/add_certificates', methods=['POST'])
def add_certificates():
    # global current_user_id
    if request.method == 'POST':
        # c_id = generate_unique_id()
        user_id = session['current_user_id']
        certificate_name = request.form['certificate_name']
        organisation = request.form['organisation']
        issue_date = request.form['issue_date']

        new_cert = {
            # 'c_id': c_id,
            'user_id': user_id,
            'certificate_name': certificate_name,
            'organisation': organisation,
            'issue_date': datetime.strptime(issue_date, '%Y-%m-%d').date()
        }

        try:
            insert_query = text(f"INSERT INTO certificates ({', '.join(new_cert.keys())}) VALUES ({', '.join([':' + key for key in new_cert.keys()])})")
            db.session.execute(insert_query, new_cert)
            
            db.session.commit()
            return render_template('cards.html', message = "success", info = "Details inserted successfully")
        except Exception as e:
            return render_template('cards.html', message="error", info="An error occurred")

@app.route('/add_education', methods=['POST'])
def add_education():
    # global current_user_id
    if request.method == 'POST':
        # ed_id = generate_unique_id()
        user_id = session['current_user_id']
        institute_name = request.form['institute_name']
        degree = request.form['degree']
        graduation_year = request.form['graduation_year']

        new_education = {
            # 'ed_id': ed_id,
            'user_id': user_id,
            'institute_name': institute_name,
            'degree': degree,
            'graduation_year': int(graduation_year)
        }

        try:
            insert_query = text(f"INSERT INTO education ({', '.join(new_education.keys())}) VALUES ({', '.join([':' + key for key in new_education.keys()])})")
            db.session.execute(insert_query, new_education)
            
            db.session.commit()
            return render_template('cards.html', message = "success", info = "Details inserted successfully")
        except Exception as e:
            return render_template('cards.html', message="error", info="An error occurred")

@app.route('/add_projects', methods=['POST'])
def add_project():
    # global current_user_id
    if request.method == 'POST':
        # project_id = generate_unique_id()
        user_id = session['current_user_id']
        project_name = request.form['project_name']
        proj_desc = request.form['proj_desc']

        new_project = {
            # 'project_id': project_id,
            'user_id': user_id,
            'project_name': project_name,
            'proj_desc': proj_desc
        }

        try:
            insert_query = text(f"INSERT INTO projects ({', '.join(new_project.keys())}) VALUES ({', '.join([':' + key for key in new_project.keys()])})")
            db.session.execute(insert_query, new_project)
            
            db.session.commit()
            return render_template('cards.html', message = "success", info = "Details inserted successfully")
        except Exception as e:
            return render_template('cards.html', message="error", info="An error occurred")

@app.route('/add_workExp', methods=['POST'])
def add_workExp():
    # global current_user_id
    if request.method == 'POST':
        # exp_id = generate_unique_id()
        user_id = session['current_user_id']
        company = request.form['company']
        job_title = request.form['job_title']
        job_desc = request.form['job_desc']
        no_of_years = request.form['no_of_years']

        new_workExp = {
            # 'exp_id': exp_id,
            'user_id': user_id,
            'company': company,
            'job_title': job_title,
            'job_desc': job_desc,
            'no_of_years': int(no_of_years)
        }

        try:
            insert_query = text(f"INSERT INTO works_exp ({', '.join(new_workExp.keys())}) VALUES ({', '.join([':' + key for key in new_workExp.keys()])})")
            db.session.execute(insert_query, new_workExp)
            
            db.session.commit()
            return render_template('cards.html', message = "success", info = "Details inserted successfully")
        except Exception as e:
            # return f"An error occurred: {str(e)}"     
            return render_template('cards.html', message="error", info="An error occurred")      

@app.route('/findDetails', methods=['POST'])
def findDetails():
    buttonType = request.form.get("type")
    if buttonType == "first":
        skill_name = request.form.get('detail1')
        work_experience = int(request.form.get('detail2'))

        query = text("""
            SELECT user.user_id, user.name, skills.skill_name, works_exp.no_of_years
            FROM user
            JOIN skills ON user.user_id = skills.user_id
            JOIN works_exp ON user.user_id = works_exp.user_id
            WHERE skills.skill_name = :skill_name AND works_exp.no_of_years = :work_experience
        """)
        # query = text("""
        #     SELECT distinct(user.user_id), user.name, skills.skill_name, works_exp.no_of_years
        #     FROM user
        #     JOIN skills ON user.user_id = skills.user_id
        #     JOIN works_exp ON user.user_id = works_exp.user_id
        #     WHERE skills.skill_name = :skill_name
            
        #     UNION
            
        #     SELECT distinct(user.user_id), user.name, skills.skill_name, works_exp.no_of_years
        #     FROM user
        #     JOIN skills ON user.user_id = skills.user_id
        #     JOIN works_exp ON user.user_id = works_exp.user_id
        #     WHERE works_exp.no_of_years = :work_experience;
        # """)
        result = db.session.execute(query, {'skill_name':skill_name, 'work_experience':work_experience})
        # print(result)
        result_list = [
            [row[0], row[1], row[2], row[3]]
            for row in result
        ]

        attributes = ["User ID", "Full Name", "Skill Name", "Work Experience"]

        return render_template('recsel.html', title = "Skills and Work Experience", tag1 = "Skill Name", tag2 = "Work Experience", info = "first", data = result_list, columns = attributes)
    elif buttonType == "second":
        certificate_name = request.form.get('detail1')
        project_name = request.form.get('detail2')

        query = text("""
            SELECT user.user_id, user.name, certificates.certificate_name, projects.project_name
            FROM user
            JOIN certificates ON user.user_id = certificates.user_id
            JOIN projects ON user.user_id = projects.user_id
            WHERE certificates.certificate_name = :certificate_name AND projects.project_name = :project_name
        """)
        # query = text("""
        #     SELECT distinct(user.user_id), user.name, certificates.certificate_name, projects.project_name
        #     FROM user
        #     JOIN certificates ON user.user_id = certificates.user_id
        #     JOIN projects ON user.user_id = projects.user_id
        #     WHERE certificates.certificate_name = :certificate_name
            
        #     UNION
            
        #     SELECT distinct(user.user_id), user.name, certificates.certificate_name, projects.project_name
        #     FROM user
        #     JOIN certificates ON user.user_id = certificates.user_id
        #     JOIN projects ON user.user_id = projects.user_id
        #     WHERE projects.project_name = :project_name
        # """)
        result = db.session.execute(query, {'project_name':project_name, 'certificate_name':certificate_name})
        # print(result)
        result_list = [
            [row[0], row[1], row[2], row[3]]
            for row in result
        ]

        attributes = ["User ID", "Full Name", "Certificate Name", "Project Name"]
        return render_template('recsel.html', title = "Certificates and Projects", tag1 = "Certificate Name", tag2 = "Project Name", info = "second", data = result_list, columns = attributes)
    elif buttonType == "third":
        graduation_year = request.form.get('detail1')
        job_title = request.form.get('detail2')

        query = text("""
            SELECT user.user_id, user.name, education.graduation_year, works_exp.job_title
            FROM user
            JOIN education ON user.user_id = education.user_id
            JOIN works_exp ON user.user_id = works_exp.user_id
            WHERE education.graduation_year = :graduation_year AND works_exp.job_title = :job_title
        """)
        
        result = db.session.execute(query, {'graduation_year':graduation_year, 'job_title':job_title})
        # print(result)
        result_list = [
            [row[0], row[1], row[2], row[3]]
            for row in result
        ]

        attributes = ["User ID", "Full Name", "Graduation Year", "Job Title"]
        return render_template('recsel.html', title = "Education and Job", tag1 = "Graduation Year", tag2 = "Job Title", info = "third", data = result_list, columns = attributes)
    elif buttonType == "forth":
        query = text("""
            SELECT user.user_id, user.name, GROUP_CONCAT(projects.project_name ORDER BY projects.project_name ASC) AS all_projects, COUNT(projects.project_id) AS no_of_projects
            FROM user
            JOIN projects ON user.user_id = projects.user_id
            GROUP BY user.user_id;
        """)
        result = db.session.execute(query)
        result_list = [
            [row[0], row[1], row[2], row[3]]
            for row in result
        ]
        print(result_list)
        attributes = ["User ID", "Full Name", "All Projects", "Number of projects"]
        return render_template('recsel.html', title = "Number of projects", tag1 = "remove", tag2 = "remove", info = "forth", data = result_list, columns = attributes)
    elif buttonType == "fifth":
        query = text("""
            SELECT user.user_id, user.name, GROUP_CONCAT(works_exp.job_title ORDER BY works_exp.job_title ASC) AS all_jobs, COUNT(works_exp.exp_id) AS no_of_jobs
            FROM user
            JOIN works_exp ON user.user_id = works_exp.user_id
            GROUP BY user.user_id;
        """)
        result = db.session.execute(query)
        result_list = [
            [row[0], row[1], row[2], row[3]]
            for row in result
        ]
        print(result_list)
        attributes = ["User ID", "Full Name", "All Jobs", "Number of jobs"]
        return render_template('recsel.html', title = "Number of jobs worked", tag1 = "remove", tag2 = "remove", info = "fifth", data = result_list, columns = attributes)

    elif buttonType == "sixth":
        query = text("""
            SELECT user.user_id, user.name, GROUP_CONCAT(certificates.certificate_name ORDER BY certificates.certificate_name ASC) AS all_certificates, COUNT(certificates.c_id) AS no_of_certificates
            FROM user
            JOIN certificates ON user.user_id = certificates.user_id
            GROUP BY user.user_id;
        """)
        result = db.session.execute(query)
        result_list = [
            [row[0], row[1], row[2], row[3]]
            for row in result
        ]
        print(result_list)
        attributes = ["User ID", "Full Name", "All Certificates", "Number of certificates"]
        return render_template('recsel.html', title = "Number of certificates", tag1 = "remove", tag2 = "remove", info = "sixth", data = result_list, columns = attributes)


@app.route('/generateResume', methods=['POST'])
def generateResume():
    # return render_template("res.html") 
    time.sleep(5)
    return redirect(f"/join_tables/{session['current_user_id']}")

@app.route('/submission', methods=['POST'])
def submission():
    info_type = request.form.get("type")
    title_name = request.form['title_name']
    print(title_name)
    # print(request.form)
    if info_type == 'update':
        if title_name == 'Education':
            try:
                transform = {'Institute Name': 'institute_name', 'Degree': 'degree', 'Graduation Year': 'graduation_year'}
                id = request.form['id']
                update_col = request.form['dropdown']
                update_val = request.form['update']
                
                is_valid = validate('education', 'ed_id', id)

                if is_valid:
                    update_query = text(f"UPDATE education SET {transform[update_col]} = :update_val WHERE ed_id = :id")
                    db.session.execute(update_query, {'update_val': update_val, 'id': id})
                    db.session.commit()
                    return render_template('cards.html', message = "success", info = "Details updated successfully")
                else:
                    return render_template('cards.html', message = "error", info = "ID not found")
                
                # conn = db.engine.connect()
                # cursor = conn.connection.cursor()

                # transform = {'Institute Name': 'institute_name', 'Degree': 'degree', 'Graduation Year': 'graduation_year'}
                # id = request.form['id']
                # update_col = request.form['dropdown']
                # update_val = request.form['update']

                # sql_query = f"UPDATE education SET {transform[update_col]} = %s WHERE ed_id = %s"
                # cursor.execute(sql_query, (update_val, id,))
            except Exception as e:
                # return f"An error occurred: {str(e)}"
                return render_template('cards.html', message="error", info="An error occurred")
        
        elif title_name == 'Skills':
            try:
                transform = {'Skill Name': 'skill_name', 'Proficiency': 'proficiency'}
                id = request.form['id']
                update_col = request.form['dropdown']
                if update_col == 'Proficiency':
                    update_val = request.form['update'].capitalize()
                else:
                    update_val = request.form['update']

                is_valid = validate('skills', 'skill_id', id)

                if is_valid:
                    update_query = text(f"UPDATE skills SET {transform[update_col]} = :update_val WHERE skill_id = :id")

                    db.session.execute(update_query, {'update_val': update_val, 'id': id})
                    db.session.commit()
                    return render_template('cards.html', message = "success", info = "Details updated successfully")
                else:
                    return render_template('cards.html', message = "error", info = "ID not found")
            except Exception as e:
                return render_template('cards.html', message="error", info="An error occurred")
        elif title_name == 'Projects':
            try:
                transform = {'Project Name': 'project_name', 'Project Description': 'proj_desc'}
                id = request.form['id']
                update_col = request.form['dropdown']
                update_val = request.form['update']

                is_valid = validate('projects', 'project_id', id)

                if is_valid:
                    update_query = text(f"UPDATE projects SET {transform[update_col]} = :update_val WHERE project_id = :id")

                    db.session.execute(update_query, {'update_val': update_val, 'id': id})
                    db.session.commit()
                    return render_template('cards.html', message = "success", info = "Details updated successfully")
                
                else:
                    return render_template('cards.html', message = "error", info = "ID not found")
            except Exception as e:
                return render_template('cards.html', message="error", info="An error occurred")
        
        elif title_name == 'Certificates':
            try:
                transform = {'Certificate Name': 'certificate_name', 'Organisation': 'organisation', 'Issue Date': 'issue_date'}
                id = request.form['id']
                update_col = request.form['dropdown']
                update_val = request.form['update']
                
                is_valid = validate('certificates', 'c_id', id)

                if is_valid:
                    update_query = text(f"UPDATE certificates SET {transform[update_col]} = :update_val WHERE c_id = :id")

                    db.session.execute(update_query, {'update_val': update_val, 'id': id})
                    db.session.commit()
                    return render_template('cards.html', message = "success", info = "Details updated successfully")
                
                else:
                    return render_template('cards.html', message = "error", info = "ID not found")
            except Exception as e:
                return render_template('cards.html', message="error", info="An error occurred")
        
        elif title_name == 'Work':
            try:
                transform = {'Company': 'company', 'Job Title': 'job_title', 'Job Description': 'job_desc', 'Number of Years': 'no_of_years'}
                id = request.form['id']
                update_col = request.form['dropdown']
                update_val = request.form['update']

                is_valid = validate('works_exp', 'exp_id', id)

                if is_valid:
                    update_query = text(f"UPDATE works_exp SET {transform[update_col]} = :update_val WHERE exp_id = :id")

                    db.session.execute(update_query, {'update_val': update_val, 'id': id})
                    db.session.commit()
                    return render_template('cards.html', message = "success", info = "Details updated successfully")
                
                else:
                    return render_template('cards.html', message = "error", info = "ID not found")
            except Exception as e:
                return render_template('cards.html', message="error", info="An error occurred")
        # return "update"

    elif info_type == 'delete':
        if title_name == 'Education':
            try:
                id = request.form['id']
                is_valid = validate('education', 'ed_id', id)

                if is_valid:
                    delete_query = text("DELETE FROM education WHERE ed_id=:id")
                    db.session.execute(delete_query, {"id": id})
                    db.session.commit()
                    return render_template('cards.html', message = "success", info = "Details deleted successfully")
                else:
                    return render_template('cards.html', message = "error", info = "ID not found")
            except Exception as e:
                return render_template('cards.html', message="error", info="An error occurred")
        
        elif title_name == 'Skills':
            try:
                id = request.form['id']

                is_valid = validate('skills', 'skill_id', id)

                if is_valid:
                    delete_query = text("DELETE FROM skills WHERE skill_id=:id")
                    db.session.execute(delete_query, {"id": id})
                    db.session.commit()
                    return render_template('cards.html', message = "success", info = "Details updated successfully")
                else:
                    return render_template('cards.html', message = "error", info = "ID not found")
            except Exception as e:
                return render_template('cards.html', message="error", info="An error occurred")
        
        elif title_name == 'Projects':
            try:
                id = request.form['id']
                is_valid = validate('projects', 'project_id', id)

                if is_valid:
                    delete_query = text("DELETE FROM projects WHERE project_id=:id")
                    db.session.execute(delete_query, {"id": id})
                    db.session.commit()
                    return render_template('cards.html', message = "success", info = "Details updated successfully")
                else:
                    return render_template('cards.html', message = "error", info = "ID not found")
            except Exception as e:
                return render_template('cards.html', message="error", info="An error occurred")
        
        elif title_name == 'Certificates':
            try:
                id = request.form['id']
                is_valid = validate('certificates', 'c_id', id)

                if is_valid:
                    delete_query = text("DELETE FROM certificates WHERE c_id=:id")
                    db.session.execute(delete_query, {"id": id})
                    db.session.commit()
                    return render_template('cards.html', message = "success", info = "Details updated successfully")
                else:
                    return render_template('cards.html', message = "error", info = "ID not found")
            except Exception as e:
                return render_template('cards.html', message="error", info="An error occurred")
        
        elif title_name == 'Work':
            try:
                id = request.form['id']
                is_valid = validate('works_exp', 'exp_id', id)

                if is_valid:
                    delete_query = text("DELETE FROM works_exp WHERE exp_id=:id")
                    db.session.execute(delete_query, {"id": id})
                    db.session.commit()
                    return render_template('cards.html', message = "success", info = "Details updated successfully")
                else:
                    return render_template('cards.html', message = "error", info = "ID not found")
            except Exception as e:
                return render_template('cards.html', message="error", info="An error occurred")
        #return "delete"

@app.route('/join_tables/<user_id>', methods=['GET'])
def join_tables(user_id):
    query = text("""
        SELECT 
            u.user_id, u.user_name, u.email, u.name, u.dob, u.phone_no,
            s.skill_id, s.skill_name, s.proficiency,
            c.c_id, c.certificate_name, c.organisation, c.issue_date,
            e.ed_id, e.institute_name, e.degree, e.graduation_year,
            p.project_id, p.project_name, p.proj_desc,
            w.exp_id, w.company, w.job_title, w.job_desc, w.no_of_years
        FROM 
            user u
        LEFT JOIN 
            (SELECT * FROM skills WHERE user_id = :user_id) s ON u.user_id = s.user_id
        LEFT JOIN 
            (SELECT * FROM certificates WHERE user_id = :user_id) c ON u.user_id = c.user_id
        LEFT JOIN 
            (SELECT * FROM education WHERE user_id = :user_id) e ON u.user_id = e.user_id
        LEFT JOIN 
            (SELECT * FROM projects WHERE user_id = :user_id) p ON u.user_id = p.user_id
        LEFT JOIN 
            (SELECT * FROM works_exp WHERE user_id = :user_id) w ON u.user_id = w.user_id
        WHERE 
        u.user_id = :user_id;
    """)

    result = db.session.execute(query, {"user_id": user_id})

    rows = result.fetchall()

    if rows:
        user_info = {}
        user_info["user"] = {}
        user_info["skills"] = []
        user_info["certificates"] = []
        user_info["education"] = []
        user_info["projects"] = []
        user_info["works_exp"] = []

        for row in rows:
            #print(row)
            if not user_info["user"]:
                user_info["user"] = {
                    "user_id": row[0],
                    "user_name": row[1],
                    "email": row[2],
                    "name": row[3],
                    "dob": row[4].strftime("%d %B %Y"),
                    "phone_no": row[5],
                }

            if row[6]:
                skill_info = {
                    "skill_id": row[6],
                    "skill_name": row[7],
                    "proficiency": row[8],
                }
                if skill_info not in user_info["skills"]:
                    user_info["skills"].append(skill_info)

            if row[9]:
                certificate_info = {
                    "c_id": row[9],
                    "certificate_name": row[10],
                    "organisation": row[11],
                    "issue_date": row[12].strftime("%d-%m-%Y"),
                }
                if certificate_info not in user_info["certificates"]:
                    user_info["certificates"].append(certificate_info)

            if row[13]:
                education_info = {
                    "ed_id": row[13],
                    "institute_name": row[14],
                    "degree": row[15],
                    "graduation_year": row[16],
                }
                if education_info not in user_info["education"]:
                    user_info["education"].append(education_info)

            if row[17]:
                project_info = {
                    "project_id": row[17],
                    "project_name": row[18],
                    "proj_desc": row[19],
                }
                if project_info not in user_info["projects"]:
                    user_info["projects"].append(project_info)

            if row[20]:
                work_exp_info = {
                    "exp_id": row[20],
                    "company": row[21],
                    "job_title": row[22],
                    "job_desc": row[23],
                    "no_of_years": row[24],
                }
                if work_exp_info not in user_info["works_exp"]:
                    user_info["works_exp"].append(work_exp_info)


            # user_info["user"] = list(set(user_info["user"]))    
            # user_info["skills"] = list(set(user_info["skills"]))    
            # user_info["certificates"] = list(set(user_info["certificates"]))    
            # user_info["education"] = list(set(user_info["education"]))    
            # user_info["projects"] = list(set(user_info["projects"]))    
            # user_info["works_exp"] = list(set(user_info["works_exp"]))  
        # return user_info  
        return render_template('res.html', details = user_info)
    else:
        return "No user found."

@app.route('/back', methods =['POST'])
def back():
    return render_template('cards.html')

@app.route('/backRec', methods =['POST'])
def backRec():
    return render_template('rec.html')

@app.route('/logout', methods =['POST'])
def logout():
    buttonType = request.form.get("type")
    if buttonType == "user":
        session.pop('current_user_id', default=None)
        return redirect("/login")
    elif buttonType == "rec":
        session.pop('current_rec_id', default=None)
        return redirect("/recLog")

@app.route('/success')
def success():
    return "Success"

if __name__ == '__main__':
    app.run(debug=True)
