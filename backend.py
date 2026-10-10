import mysql.connector 
import hashlib
def fetch(name,pwd):

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="innite"
    )
    mycursor = mydb.cursor()
    query = "select * from (users) where username=(%s)"
    mycursor.execute(query,(name,))
    myresult = mycursor.fetchall()
    if myresult[0][2]==encryption(pwd):
        return True

def githublogin(username):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="innite"
    )
    mycursor = mydb.cursor()
    query = "insert into users (username) values(%s)"
    mycursor.execute(query,(username,))
    mydb.commit()
    return True

def signup_user(name,pwd):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="innite"
    )
    mycursor = mydb.cursor()
    query = "insert into users (username, password) values(%s,%s)"
    val=encryption(pwd)
    mycursor.execute(query,(name,val))
    mydb.commit()
    return True
#     query="select * from users"
#     mycursor.execute(query)
#     myresult = mycursor.fetchall()
#     print(myresult)
# signup_user("admin","admin")

def available():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="innite"
    )
    mycursor = mydb.cursor(dictionary=True)
    query = "select * from room where availability=True"
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    #print(myresult[0]['room_id'])
    return myresult
#available()

def booking_db(uname,room_id,days,persons):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="innite"
    )
    mycursor = mydb.cursor(dictionary=True)
    query = "select * from room where room_id=(%s)"
    mycursor.execute(query,(room_id,))
    myresult = mycursor.fetchall()
    print(myresult)
    val=myresult[0]['availability']
    if myresult[0]['availability']==True and persons<=myresult[0]['capacity']:
        query = "update room set availability=False where room_id=(%s)"
        mycursor.execute(query,(room_id,))
        mydb.commit()
        q1="select uid from users where username=(%s)"
        mycursor.execute(q1,(uname,))
        result=mycursor.fetchall()
        uid=result[0]['uid']
        print(uid,room_id)
        q2="insert into linker values(%s,%s,%s,%s)"
        mycursor.execute(q2,(uid,room_id,days,persons))
        mydb.commit()
        q3="select * from linker"
        mycursor.execute(q3)
        res=mycursor.fetchall()
        price=myresult[0]['price']
        #print(res)
        #print("Successful!")
        return price
    else:
        #print("Unsuccessful!")
        return False
#booking_db("admin",1,1,1)

def encryption(password):
    val=hashlib.sha256(password.encode())
    return val.hexdigest()