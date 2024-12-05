from flask import Flask,render_template,request,redirect,session,send_file,jsonify
import mysql.connector
import math
connection=mysql.connector.connect(host='localhost',
                                 database='duplicate',
                                 user='root',
                                 password='15032')
cursor=connection.cursor(buffered=True)
app=Flask(__name__)
app.secret_key="vamsi"
app.config['UPLOAD_FOLDER']='uploads/'
login_user_id=""
id=""
new_detail=""
old_vehicle_detail=""

@app.route('/')
def main_page():
    return render_template('main.html')

 ## ADMIN LOGIN PAGE

@app.route('/AdminLogin')
def AdminLogin():
    return render_template("AdminLogin.html")

@app.route('/validate',methods=["POST"])
def validate():
    one="false"
    two="false"
    global id
    id=request.form.get('admin_id')
    password=request.form.get('admin_password')
    result=''
    query=f"select admin_password from duplicate.admin where admin_id={id}"
    cursor.execute(query)
    result=cursor.fetchone()
    if result==None:
        one="true"
        return render_template("AdminLogin.html",one=one)
    elif result[0]!=password:
        two="true"
        return render_template("AdminLogin.html",two=two)
    else:
        return render_template('admin_home.html')
    # for i in result :
    #     if(i[0]==id and i[1]==password):
    #         return('<h1>Success</h1>')
    #     elif(i[0]==id):
    #         return render_template("AdminLogin.html",error="error at password",one="true")
    #     else:
    #         return render_template("AdminLogin.html",error="error at both userid and password",one="true")

            
## user Registeration   
        
@app.route('/UserRegister')
def userRegister1():
    error_at_id="false"
    return render_template("UserRegister1.html",error_at_id=error_at_id)

@app.route('/validate_user_signup',methods=["POST"])
def validate_user_signup():
    error_at_id="false"
    user_name=request.form.get('user_name')
    user_id=request.form.get('user_id')
    user_password=request.form.get('user_password')
    user_phone=request.form.get('user_phone')
    try:
        query="create table if not exists duplicate.user(user_name varchar(20),user_id varchar(20),user_password varchar(20),user_phone integer(12),constraint pk_use primary key(user_id))"
        cursor.execute(query)
        connection.commit()
        insert_query=f"insert into duplicate.user values('{user_name}','{user_id}','{user_password}','{user_phone}')"
        cursor.execute(insert_query)
        connection.commit()
    except mysql.connector.Error as e:
        error_at_id="true"
        return render_template("UserRegister1.html",error_at_id=error_at_id)

    return redirect('/UserLogin')

## USER LOGIN 

@app.route('/UserLogin')
def UserLogin():
    return render_template('UserLogin.html')

@app.route('/validate_login_user',methods=["POST"])
def validate_login_user():
    error1="false"
    error2="false"
    global login_user_id
    login_user_id=request.form.get('login_user_id')
    login_user_password=request.form.get('login_user_password')
    try:
        query=f"select user_password from duplicate.user where user_id={login_user_id}"
        cursor.execute(query)
        password=cursor.fetchone()
        if(password==None):
            error1="true"
            return render_template('UserLogin.html',error1=error1)
        elif(password[0]==login_user_password):
            return render_template('user_home.html',login_user_id=login_user_id)
        
        else:
            error2="true"
            return render_template('UserLogin.html',error2=error2)
    
        
    except mysql.connector.Error as er:
        error1="true"
        return render_template('UserLogin.html',error1=error1)
    
    return "suceess login "
 
 ## GO BACK TO USER HOME PAGE FROM VIEW DETAILS(NO DATA)

@app.route('/go_back_user_home')
def go_back_user_home():
    return render_template('user_home.html',login_user_id=login_user_id)

## USER PERSONAL DETAILS

@app.route('/personal_details')
def personal():
    edit_result=""
    return render_template('personal_details2.html',edit_result=edit_result,edit="false")


@app.route("/validate_personal/<edit>",methods=["POST"])
def validate_personal(edit):
    #user_id=request.form.get('user_id')
    vehicle_type=request.form.get('vehicle_type')
    model_name=request.form.get('model_name')
    manufacture_year=request.form.get("manufacture_year")
    user_id=login_user_id
    fname=request.form.get('fname')
    lname=request.form.get('lname')
    email=request.form.get('email')
    phone=request.form.get('phone')
    dno=request.form.get('dno')
    city=request.form.get('city')
    district=request.form.get('district')
    state=request.form.get('state')
    state_code=request.form.get('state_code')
    pincode=request.form.get('pincode')
    proof=request.form.get('proof')
    document_id=request.form.get('document_id')
    file = request.files['file']
    file.save(app.config['UPLOAD_FOLDER'] + file.filename)
   ## sql = "INSERT INTO duplicate.files (id,name, data) VALUES (%s,%s, %s)"

  
    query1="create table if not exists duplicate.personal_detail(user_id varchar(20),fname varchar(20),lname varchar(20),email varchar(30),phone varchar(10),constraint pkpd primary key(user_id),constraint fkpda foreign key(user_id) references duplicate.user(user_id) on delete cascade)"
    query2="create table if not exists duplicate.address(user_id varchar(20),dno varchar(12),city varchar(20),district varchar(20),state varchar(20),state_code varchar(20),pincode integer(6),constraint pka primary key(user_id),constraint fka foreign key(user_id) references duplicate.user(user_id) on delete cascade)"
    query3="create table if not exists duplicate.vehicle(user_id varchar(20),vehicle_type varchar(20),model_name varchar(20),manufacture_year varchar(20),registration_status varchar(20),constraint pkv primary key(user_id),constraint fkv foreign key(user_id) references duplicate.user(user_id) on delete cascade)"
    query4="create table if not exists duplicate.documents(user_id varchar(20),proof varchar(20),document_id varchar(20),name varchar (256),data longblob,constraint fkd foreign key(user_id) references duplicate.user(user_id) on delete cascade)"
    #query11="alter table duplicate.personal_detail add constraint fkpd foreign key(user_id) references duplicate.user(user_id)"
    #query22="alter table duplicate.address add constraint fka foreign key(user_id) references duplicate.user(user_id)"
    cursor.execute(query1)
    cursor.execute(query2)
    cursor.execute(query3)
    cursor.execute(query4)
    #cursor.execute(query11)
    #cursor.execute(query22)
    #cursor.execute(query2)
    connection.commit()
    ## update the edit details
    if(edit=="true"):
        try:
            edit_query1="create table if not exists duplicate.personal_detail_edit(user_id varchar(20),fname varchar(20),lname varchar(20),email varchar(30),phone varchar(10),constraint pkpde primary key(user_id),constraint fkpdae foreign key(user_id) references duplicate.user(user_id) on delete cascade)"
            edit_query2="create table if not exists duplicate.address_edit(user_id varchar(20),dno varchar(12),city varchar(20),district varchar(20),state varchar(20),state_code varchar(20),pincode integer(6),constraint pkae primary key(user_id),constraint fkae foreign key(user_id) references duplicate.user(user_id) on delete cascade)"
            edit_query3="create table if not exists duplicate.documents_edit(user_id varchar(20),proof varchar(20),document_id varchar(20),name varchar (256),data longblob,constraint fkde foreign key(user_id) references duplicate.user(user_id) on delete cascade)"
            cursor.execute(edit_query1)
            cursor.execute(edit_query2)
            cursor.execute(edit_query3)
            edit_insert_query1=f"insert into duplicate.personal_detail_edit values('{user_id}','{fname}','{lname}','{email}','{phone}')"
            edit_insert_query2=f"insert into duplicate.address_edit values('{user_id}','{dno}','{city}','{district}','{state}','{state_code}','{pincode}')"
            cursor.execute(edit_insert_query1)
            cursor.execute(edit_insert_query2)
            with open(app.config['UPLOAD_FOLDER'] + file.filename, 'rb') as f:
                file_data = f.read()
            insert_query_edit= "INSERT INTO duplicate.documents_edit (user_id, proof, document_id, name, data) VALUES (%s, %s, %s, %s, %s)"
            insert_values_edit = (user_id, proof, document_id, file.filename, file_data)
            cursor.execute(insert_query_edit,insert_values_edit)
            connection.commit()
            
        ## NOTE DO NEXT TIME
        except mysql.connector.Error as e:
            error_at_id="true"
            return render_template("personal_details2.html",error_at_id=error_at_id)
        return redirect('/go_back_user_home')
        ## IMPORTANT 
        # update_query1=f"update duplicate.personal_detail set fname='{fname}',lname='{lname}',email='{email}',phone='{phone}' where user_id='{login_user_id}'"
        # update_query2=f"update duplicate.address set dno='{dno}',city='{city}',district='{district}',state='{state}' where user_id='{login_user_id}'"
        # ##update_query3=f"update duplicate.vehicle set registration_status='update' where user_id='{login_user_id}'"
        # cursor.execute(update_query1)
        # cursor.execute(update_query2)
         
       ## cursor.execute(update_query3)
        connection.commit()

    ## Normal query new Registration
    else:
        insert_query1=f"insert into duplicate.personal_detail values('{user_id}','{fname}','{lname}','{email}','{phone}')"
        insert_query2=f"insert into duplicate.address values('{user_id}','{dno}','{city}','{district}','{state}','{state_code}','{pincode}')"
        insert_query3=f"insert into duplicate.vehicle values('{user_id}','{vehicle_type}','{model_name}','{manufacture_year}','no')"
        ##insert_query4=f"insert into duplicate.documents values('{user_id}','{proof}','{document_id}','{file.filename}','{file_data}')"
        cursor.execute(insert_query1)
        cursor.execute(insert_query2)
        cursor.execute(insert_query3)
        ##cursor.execute(insert_query4)
        with open(app.config['UPLOAD_FOLDER'] + file.filename, 'rb') as f:
            file_data = f.read()
        ##insert_query4=f"insert into duplicate.documents values('{user_id}','{proof}','{document_id}','{file.filename}','{file_data}')"
        ##cursor.execute(insert_query4)
        insert_query = "INSERT INTO duplicate.documents (user_id, proof, document_id, name, data) VALUES (%s, %s, %s, %s, %s)"
        insert_values = (user_id, proof, document_id, file.filename, file_data)
        cursor.execute(insert_query, insert_values)
        connection.commit()
        ##cursor.execute(sql, ("3",file.filename, file_data))
        connection.commit()
        return redirect('/other_vehicle_registration')

@app.route('/user_home')
def user_home():
    return render_template('user_home.html',login_user_id=login_user_id)

## insert vehicle details in vehicle html

@app.route('/other_vehicle_registration')
def other_vehicle_registration():
    return render_template('vehicle_details.html')

@app.route('/vehicle_details',methods=["POST"])
def vehicle_details():
    vehicle_type=request.form.get('vehicle_type')
    model_name=request.form.get('model_name')
    manufacture_year=request.form.get("manufacture_year")
    #document_id=request.form.get('document_id')
    file = request.files['file']
    file.save('/uploads'+ file.filename)
    query="create table if not exists duplicate.vehicle_detail(vehicle_id int auto_increment,user_id varchar(20),vehicle_type varchar(20),model_name varchar(20),manufacture_year varchar(20),registration_status varchar(20),doc_name varchar (256),doc_data longblob,constraint pkvs primary key(vehicle_id),constraint fkvs foreign key(user_id) references duplicate.user(user_id))"
    cursor.execute(query)
    connection.commit()
    ##insert_query=f"insert into duplicate.vehicle values('{login_user_id}','{vehicle_type}','{model_name}','{manufacture_year}','no','{document_id}','{}')"
    with open('/uploads' + file.filename, 'rb') as f:
        file_data = f.read()
    insert_query = "INSERT INTO duplicate.vehicle_detail(user_id,vehicle_type,model_name,manufacture_year,registration_status,doc_name,doc_data) VALUES (%s, %s, %s, %s, %s,%s, %s)"
    insert_values = (login_user_id,vehicle_type,model_name,manufacture_year,'no',file.filename,file_data)
    cursor.execute(insert_query, insert_values)
    connection.commit()   
    return redirect('/user_home') 



## ADMIN APPROVAL 

@app.route('/admin_approval')
def admin_approval():
    query="select u.user_id,p.fname,p.lname,p.email,p.phone,a.dno,a.city,a.district,a.state,a.state_code,a.pincode,v.vehicle_type,v.model_name,v.manufacture_year,v.registration_status,v.vehicle_id from duplicate.user u,duplicate.personal_detail p,duplicate.address a,duplicate.vehicle_detail v where u.user_id=p.user_id and u.user_id=a.user_id and u.user_id=v.user_id order by v.registration_status"
    cursor.execute(query)
    result=cursor.fetchall()
    session['user']=result
    return render_template('admin_approval.html',admin_id=id,data=result)

@app.route('/view_details/<user_id>/<who>')
def view_details(user_id,who):
    #return f" user id={user_id}"
    
    cursor.execute(f"select vehicle_id,vehicle_type,model_name,manufacture_year,registration_status from duplicate.vehicle_detail where user_id={user_id}")
    vehicle_ids=cursor.fetchall()
    if who!="user":
        veh_id=who.split('_')
        new_query=f"select u.user_id,p.fname,p.lname,p.email,p.phone,a.dno,a.city,a.district,a.state,a.state_code,a.pincode,v.vehicle_type,v.model_name,v.manufacture_year,v.registration_status,v.vehicle_id from duplicate.user u,duplicate.personal_detail p,duplicate.address a,duplicate.vehicle_detail v where u.user_id={user_id} and v.vehicle_id={veh_id[0]} and u.user_id=p.user_id and u.user_id=a.user_id and u.user_id=v.user_id "
        cursor.execute(new_query)
        result2=cursor.fetchone()
        session['apro_user_id']=user_id
        st_query=f"select state_code from duplicate.address where user_id={user_id}"
        cursor.execute(st_query)
        result_stcode=cursor.fetchone()
        if(result2[14]=="no"):
            result_reger_no=0
        else:
            reger_no_query=f"select registration_no from duplicate.registration where user_id={user_id}"
            cursor.execute(reger_no_query)
            result_reger=cursor.fetchone()
            result_reger_no=result_reger[0]
        return render_template('view_details.html',data=result2,user_id=f"{user_id}",admin_id=id,st_code=result_stcode[0],u="admin",result_reger_no=result_reger_no,vehicle_ids=vehicle_ids)
    elif who=="user":
        #query="select u.user_id,p.fname,p.lname,p.email,p.phone,a.dno,a.city,a.district,a.state,a.state_code,a.pincode,v.vehicle_type,v.model_name,v.manufacture_year,v.registration_status from duplicate.user u,duplicate.personal_detail p,duplicate.address a,duplicate.vehicle v where u.user_id=p.user_id and u.user_id=a.user_id and u.user_id=v.user_id"
    
            new_query=f"select u.user_id,p.fname,p.lname,p.email,p.phone,a.dno,a.city,a.district,a.state,a.state_code,a.pincode,v.vehicle_type,v.model_name,v.manufacture_year,v.registration_status,v.vehicle_id from duplicate.user u,duplicate.personal_detail p,duplicate.address a,duplicate.vehicle_detail v where u.user_id={user_id} and u.user_id=p.user_id and u.user_id=a.user_id and u.user_id=v.user_id"
            cursor.execute(new_query)
            result1=cursor.fetchone()
            check_reg_status=f"select registration_status from duplicate.vehicle where user_id={user_id}"
            cursor.execute(check_reg_status)
            result_status=cursor.fetchone()
            if result1==None:
                no_data="true"
                return render_template('view_details.html',no_data=no_data)
            elif result1[14]=="no":
                result_reger_no=0
            else:
                reger_no_query=f"select registration_no from duplicate.registration where user_id={user_id}"
                cursor.execute(reger_no_query)
                result_reger=cursor.fetchone()
                result_reger_no=result_reger[0]
            return render_template('view_details.html',data=result1,user_id=f"{user_id}",u="user",result_reger_no=result_reger_no,vehicle_ids=vehicle_ids,vehicle_detail_id="")

## DISPLAY REGISTRATION NUMBER IF REGISTRATION 
@app.route('/check_register/<vehicle_id>')
def check_register(vehicle_id):
    html=''
    cursor.execute(f"select registration_status from duplicate.vehicle_detail where  vehicle_id={vehicle_id}")
    status_check=cursor.fetchall()
    for status in status_check:
        if status[0]=='yes':
            cursor.execute(f"select registration_no from duplicate.registration where vehicle_id={vehicle_id}")
            register_num=cursor.fetchone()
            html+=f'<h3>REGISTRATION NUMBER = {register_num[0]}</h3>'
        elif status[0]=='no':
            html+=f'<h3>REGISTRATION STATUS = PENDING </h3>'

    return html


## VALIDATE REGISTRATION BY ADMIN 
@app.route('/validate_registration/<reg_number>/<vehicle_id>')
def validate_registration(reg_number,vehicle_id):
    # reg_number=request.form.get('register_no')
    # vehicle_id=request.table.get('')
    query="create table if not exists duplicate.registration(user_id varchar(20) unique,registration_no varchar(20),vehicle_type varchar(20),vehicle_id int,constraint pkr primary key(registration_no),constraint fkr foreign key(user_id) references duplicate.user(user_id) on delete cascade)"
    cursor.execute(query)
    connection.commit()
    vehicle_query=f"select vehicle_type from duplicate.vehicle_detail where user_id={session['apro_user_id']} and vehicle_id={vehicle_id}" 
    cursor.execute(vehicle_query)
    vehicle_type=cursor.fetchone()
    insert_query=f"insert into duplicate.registration values('{session['apro_user_id']}','{reg_number}','{vehicle_type[0]+'wheeler'}','{vehicle_id}')"
    cursor.execute(insert_query)
    connection.commit()
    update_query_status=f"update duplicate.vehicle_detail set registration_status='yes' where user_id={session['apro_user_id']} and vehicle_id={vehicle_id}"
    cursor.execute(update_query_status)
    connection.commit()
    return redirect('/admin_home')

## GET THE VEHICLE DETAILS USING VEHICLE_ID,USER_ID
@app.route('/vehicle_details',methods=['POST'])
def vehicle_details_id():
    data = request.json
    selected_value = data.get('selectedValue')
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"select vehicle_id,vehicle_type,model_name,manufacture_year,registration_status from duplicate.vehicle_detail where user_id={login_user_id} and vehicle_id={selected_value}")
    ##cursor.execute("select * from duplicate.vehicle_detail")
    vehicle_detail_id=cursor.fetchone()
    return jsonify({'message':'Data received successfully'})
    # return jsonify(vehicle_detail_id) 


@app.route('/send_data', methods=['POST'])
def receive_data():
    data = request.json
    selected_value = data.get('selectedValue')
    # Now you can use this selected_value in your Python code
    # For example, print it
    print(f"variable accessed {selected_value}")
    return jsonify({'message': 'Data received successfully'})




## go back to admin home 
@app.route('/admin_home')
def admin_home():
    return render_template('admin_home.html')

## CHECKING REGISTRATION STATUS

@app.route('/regrestration_status/<regist_user_id>')
def registration_status(regist_user_id):
    status_div="false"
    status_query=f"select  v.registration_status from duplicate.vehicle_detail v where v.user_id={regist_user_id}"
    cursor.execute(status_query)
    status_result=cursor.fetchone()
    if status_result==None:
        return render_template('registration_status.html',registration_details="",status="no_data",login_user_id=regist_user_id)
    elif status_result[0]=="no":
        status_details_query=f"select  p.user_id,p.fname,p.lname,v.vehicle_type,v.model_name from duplicate.vehicle_detail v,duplicate.personal_detail p where v.user_id={regist_user_id} and v.user_id=p.user_id"
        cursor.execute(status_details_query)
        status_details_result=cursor.fetchone()
        return render_template('registration_status.html',registration_details=status_details_result,status="false",login_user_id=regist_user_id)
    elif status_result[0]=="yes":
        registration_status_details_query=f"select r.registration_no,p.fname,p.lname,v.vehicle_type,v.model_name,v.registration_status from duplicate.registration r,duplicate.personal_detail p,duplicate.vehicle_detail v,duplicate.user u where u.user_id={regist_user_id} and u.user_id=p.user_id and u.user_id=v.user_id and u.user_id=r.user_id"
        cursor.execute(registration_status_details_query)
        registration_status_detail_result=cursor.fetchone()
        return render_template('registration_status.html',registration_details=registration_status_detail_result,num_status="ok",login_user_id=regist_user_id)


#ADMIN SEARCH FOR CUSTOMERS DETAILS USING REG_NO
@app.route('/search')
def search():
    return render_template('admin_search_details.html')   

@app.route('/search_customer',methods=["POST"])
def search_customer():
    error1="false"
    error2="false"
    register_no=request.form.get('register_no')
    try:
        user_id_query=f"select user_id,vehicle_id from duplicate.registration where registration_no='{register_no}'"
        cursor.execute(user_id_query)
        user_id=cursor.fetchone()
        if user_id!=None:
            return redirect(f'/view_details/{user_id[0]}/{user_id[1]}_admin')
        else:
            error2="true"
            return render_template('admin_search_details.html',error2=error2)
    
    except mysql.connector.Error as er:
        error1="true"
        return render_template('admin_search_details.html',error1=error1)
    
## EDIT THE DETAILS OF USER 
@app.route('/edit_details/<user_id>')
def edit_details(user_id):
    # edit_query=f"select p.*,v.*,d.* from personal_detail p join duplicate.vehicle v join duplicate.documents on user_id"
    edit_query=f"select p.*,a.*,d.*,v.* from duplicate.personal_detail p inner join duplicate.address a on p.user_id=a.user_id  inner join  duplicate.vehicle v on p.user_id=v.user_id inner join duplicate.documents d on p.user_id=d.user_id where p.user_id={user_id}"
    cursor.execute(edit_query)
    edit_result=cursor.fetchone()
    return render_template('personal_details2.html',edit_result=edit_result,edit="true")

## download the file from database

@app.route('/download/<int:file_id>/<normal>')
def download_file(file_id,normal):
    if(normal=="edit"):
        sql="SELECT name,data FROM duplicate.documents_edit WHERE user_id = %s"
        cursor.execute(sql, (file_id,))
    elif(normal!='0'):
        sql="SELECT doc_name,doc_data FROM duplicate.vehicle_detail where vehicle_id=%s"
        cursor.execute(sql, (normal,))
    else:
        sql = "SELECT name,data FROM duplicate.documents WHERE user_id = %s"
        cursor.execute(sql, (file_id,))
    
    
    file_data1 = cursor.fetchone()
    with open(app.config['UPLOAD_FOLDER'] + file_data1[0], 'wb') as f:
        f.write(file_data1[1])
    return send_file(app.config['UPLOAD_FOLDER'] + file_data1[0], as_attachment=True)

## delete the user details
@app.route('/delete_home_user')
def delete_home_user():
    return render_template('delete_user.html')


@app.route('/delete_user',methods=["POST"])
def delete_user():
    register_no=request.form.get('register_no')
    user_query=f"select r.user_id,r.vehicle_id from duplicate.registration r where r.registration_no='{register_no}'"
    cursor.execute(user_query)
    user_id_result=cursor.fetchone()
    if user_id_result==None:
        return render_template('delete_user.html',data="false")
    else:
        query=f"delete from duplicate.vehicle_detail where vehicle_id='{user_id_result[1]}'"
        cursor.execute(query)
        cursor.execute(f"delete from duplicate.registration where vehicle_id={user_id_result[1]}")
        connection.commit()
        return render_template('delete_user.html',data="true")

    
## ADMIN EDIT APPROVAL

@app.route('/edit_approval/<user_id>')
def edit_approval(user_id):
    query1="select u.user_id,p.fname,p.lname,p.email,p.phone,a.dno,a.city,a.district,a.state,a.state_code,a.pincode,d.proof,d.document_id,d.name,d.data from duplicate.user u,duplicate.personal_detail_edit p,duplicate.address_edit a,duplicate.documents_edit d where u.user_id=p.user_id and u.user_id=a.user_id and u.user_id=d.user_id"
    cursor.execute(query1)
    new_details=cursor.fetchall()
    query2="select v.user_id,v.vehicle_type,v.model_name,v.manufacture_year,r.registration_no from duplicate.registration r inner join duplicate.vehicle v on v.user_id=r.user_id"
    cursor.execute(query2)
    old_vehicle_details=cursor.fetchall()
    if(user_id=='02'):
        return render_template('admin_edit_approval.html',new_details=new_details,old_vehicle_details=old_vehicle_details)
    else:
        for x in new_details:
            for y in old_vehicle_details:
                if(x[0]==user_id and y[0]==user_id):
                    global new_detail,old_vehicle_detail
                    new_detail=x
                    old_vehicle_detail=y
                    return render_template('admin_edit_view_details.html',new_detail=x,old_vehicle_detail=y)

 ## ACCEPT THE EDIT DETAILS BY ADMIN;  

@app.route('/update/<changes>')
def update(changes):
    if changes=="accept":
        update_query1=f"update duplicate.personal_detail set fname='{new_detail[1]}',lname='{new_detail[2]}',email='{new_detail[3]}',phone='{new_detail[4]}' where user_id='{new_detail[0]}'"
        update_query2=f"update duplicate.address set dno='{new_detail[5]}',city='{new_detail[6]}',district='{new_detail[7]}' where user_id='{new_detail[0]}'"
        update_query3 = "UPDATE duplicate.documents SET proof = %s, document_id = %s, name = %s, data = %s WHERE user_id = %s"
        values = (new_detail[11], new_detail[12], new_detail[13], new_detail[14], new_detail[0])
        cursor.execute(update_query1)
        cursor.execute(update_query2)
        cursor.execute(update_query3,values)
    cursor.execute(f"delete from duplicate.personal_detail_edit where user_id='{new_detail[0]}'")
    cursor.execute(f"delete from duplicate.address_edit where user_id='{new_detail[0]}'")
    cursor.execute(f"delete from duplicate.documents_edit where user_id='{new_detail[0]}'")
    connection.commit()
    return redirect('/admin_home')

## REGISTRATION STATUS  

@app.route('/status', methods=['GET'])
def get_users():
    html=' Select the Vehicle ID & Vehicle Type: <select id="dropdown">'
    cursor.execute(f"SELECT * FROM duplicate.vehicle_detail where user_id={login_user_id}")
    users = cursor.fetchall()
    user_list = []
    for user in users:
        # user_dict = {
        #     'user_id': user[0],
        #     'registration_no': user[1],
        #     'vehicle_type': user[2],
        #     'vehicle_id':user[3]
        # }
        # user_list.append(user_dict)
        html+=f'<option value="{user[0]}" class="drop" >{user[0]}, {user[2]}Wheller</option>'

    html+='</select><br>'
    return html

@app.route('/update_details/<vehicle_id>')
def list(vehicle_id):
    html=''
    cursor.execute(f"select  v.vehicle_id,p.fname,p.lname,v.vehicle_type,v.model_name,v.registration_status from duplicate.vehicle_detail v inner join duplicate.personal_detail p on v.user_id=p.user_id where v.user_id={login_user_id} and v.vehicle_id={vehicle_id}")
    registration_details=cursor.fetchall()
    for details in registration_details:
        html+=f'<tr><td>Vehicle ID :</td><td>{details[0]}</td></tr>'
        html+=f'<tr><td>Vehicle Owner Name :</td><td>{details[1]} {details[2]}</td></tr>'
        html+=f'<tr><td>Vehicle Type :</td><td>{details[3]} Wheeler, {details[4]}</td></tr>'
        f'<h5>Registration Status :{details[5]}</h5>'
        if details[5]=='yes':
            cursor.execute(f"select registration_no from registration where vehicle_id={vehicle_id} and user_id={login_user_id}")
            regno=cursor.fetchone()
            html+=f'<tr><td><b>Registration Number </b>:</td><td><b>{regno[0]}</b></td></tr>'
        else:
            html+='<tr><td><b>Registration Status :</b></td><td><b>PENDING</b></td></tr>'
    return html

if __name__=='__main__':
    app.run(debug=True)