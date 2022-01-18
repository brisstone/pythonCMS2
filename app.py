import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy.orm import sessionmaker
from json import dumps
import mysql.connector
from sqlalchemy import create_engine, MetaData,Table,Column,Integer,Boolean,String,TEXT,FLOAT
from sqlalchemy.orm import declarative_base,sessionmaker
from dotenv import load_dotenv
import dotenv
project_folder = os.path.expanduser('~/cms2-main')
load_dotenv(os.path.join(project_folder, '.env'))
load_dotenv(dotenv.find_dotenv())
import base64
from PIL import Image
from io import BytesIO
from base64 import b64decode

# from cryptography.fernet import Fernet

# key = Fernet.generate_key()

# Instance the Fernet class with the key
# fernet = Fernet(key)


# import pycryptodome
# from Crypto.Cipher import AES
# from Crypto import Random




HOST = os.getenv("HOST")
USERS = os.getenv("USERS")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")
# HOST='sql4.freemysqlhosting.net'
print(PASSWORD)

mydb = mysql.connector.connect(host=HOST,user= USERS,password=PASSWORD,database=DATABASE)

engine = create_engine("mysql+pymysql://"+USERS+":"+PASSWORD+"@" + HOST + "/" + DATABASE)

# mydb = mysql.connector.connect(host='sql4.freemysqlhosting.net',user='sq14466461',password='BIVmKhmJCu',database='sq14466461')
# engine = create_engine("mysql+pymysql://sq14466461:password@sql4.freemysqlhosting.net/sq14466461")

engine.connect()

meta = MetaData()

users = Table(
    'users', meta,
    Column('1d', Integer, primary_key= True),
    Column('Email', String(66), unique=True),
    Column('Password', String(20)),
    Column('Adm', Boolean, default=0),
    Column('FullName' ,String(200)),
    Column('DateOfBirth', String(20)),
    Column('Picture', String(20)),
    Column('SchoolStartYear', String(20)),
    Column('MajorFieldOfStudy', String(100)),
    Column('MinorFieldOfStudy', String(100)),
    Column('Courses', TEXT),
    Column('AdCourses',TEXT),
    Column('Average', FLOAT(8)),
    Column('Comments', TEXT),
    Column('Suspended', Boolean, default=0),
    Column('Remark', TEXT),
    Column("Degree", TEXT),
)
#meta.create_all(engine)
print(engine)

Session=sessionmaker()
myc = mydb.cursor(buffered=True)
#DO NOT RUN THIS LINE AGAIN THE DATABASE HAS BEEN CREATED EXCEPT YOU WANT TO CREATE ONE ON A NEW SERVER
# myc.execute('CREATE TABLE users(id INT AUTO_INCREMENT PRIMARY KEY, Email VARCHAR(66) UNIQUE, Password VARCHAR(20), Adm INT(1) DEFAULT 0, FullName VARCHAR(200), DateOfBirth VARCHAR(20), Picture VARCHAR(10), SchoolStartYear VARCHAR(50), MajorFieldOfStudy VARCHAR(100),MinorFieldOfStudy VARCHAR(100), Courses TEXT, AdCourses TEXT, Average FLOAT(8) , Comments TEXT, Suspended INT(1) DEFAULT 0, Remark TEXT, Degree VARCHAR(100))')


""" The HTTP request handler """
class RequestHandler(BaseHTTPRequestHandler):

  def _send_cors_headers(self):
      """ Sets headers required for CORS """
      self.send_header("Access-Control-Allow-Origin", "*")
      self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
      self.send_header("Access-Control-Allow-Headers", "x-api-key,Content-Type")

  def send_dict_response(self, d):
      """ Sends a dictionary (JSON) back to the client """
      self.wfile.write(bytes(dumps(d), "utf8"))

  def do_OPTIONS(self):
      self.send_response(200)
      self._send_cors_headers()
      self.end_headers()

  def do_GET(self):
      self.send_response(200)
      self._send_cors_headers()
      self.end_headers()


      response = {}
      response="WELCOME YOU DID NOT USE METHODS"
      self.send_dict_response(response)

  def do_POST(self):
      if self.path.endswith('/login'):
          self.send_response(200)
          self._send_cors_headers()
          self.send_header("Content-Type", "application/json")
          self.end_headers()

          dataLength = int(self.headers["Content-Length"])
          data = self.rfile.read(dataLength)

          data.strip()

          # convert from json
          y = json.loads(data)
          response = y
          if "email" in y:
              a = y["email"]
              b = y["password"]
              print(a)
              print('iiiiiii',b)

          myc.execute("SELECT * FROM users WHERE Email= %(unm)s", {'unm': a})

          for j in myc:
              print("ffffffff",j)

          mydb.commit()

          check = myc.execute("SELECT * FROM users WHERE Email= %(unm)s", {'unm': a})
          print(check)
          for i in myc:
              print(i)

              if i[2] == b:
                  k = "Password correct OK"
                  response = {}
                  response["status"] = f"{i[3]},{j},{k}"

                  res1 = {}
                  res1["Adm"] = f"{i[3]}"
                  res2 = {}
                  res2["Status"] = f"{k}"
                  res3 = {}
                  res3["Info"] = f"{j}"

                  el = [res1, res2, res3]

                  self.wfile.write(bytes(dumps(el), "utf8"))

                  check = True

                  # self.send_dict_response(response)

              else:
                  k = "Incorrect Password"
                  response = {}
                  response["status"] = f"{k}"

                  res4 = {}
                  res4["IncorrectPassword"] = f"{k}"

                  el2 = [res4]
                  self.wfile.write(bytes(dumps(el2), "utf8"))
                  check = True

          if not check:
              l = "Email Does not exist"
              response = {}
              response["status"] = f"{l}"

              res5 = {}
              res5["NoUserFound"] = f"{l}"

              el3 = [res5]
              self.wfile.write(bytes(dumps(el3), "utf8"))
              # self.send_dict_response(response)
          # ll="Server Error"
          # response = {}
          # response["status"] = f"{ll}"
          #
          # res55 = {}
          # res55["Server Error"] = f"{ll}"
          #
          # el33 = [res55]
          # self.wfile.write(bytes(dumps(el33), "utf8"))
          # self.send_dict_response(response)
          mydb.commit()

      if self.path.endswith('/register'):
          self.send_response(200)
          self._send_cors_headers()
          self.send_header("Content-Type", "application/json")
          self.end_headers()

          dataLength = int(self.headers["Content-Length"])
          data = self.rfile.read(dataLength)

          data.strip()

          print(data)
          # convert from json
          y = json.loads(data)
          response = y
          if "email" in y:
              a = y["email"]
              b = y["password"]

              print(a)
              print(b)

              # check = myc.execute("SELECT Email FROM users WHERE EMAIL= %(unm)s", {'unm':a})

              # new_user = users(email=a, password=b)

              ins = users.insert().values(Email=a, Password=b, FullName="")
              conn = engine.connect()
              conn.execute(ins)
              self.send_dict_response(response)

      if self.path.endswith('/admregister'):
          self.send_response(200)
          self._send_cors_headers()
          self.send_header("Content-Type", "application/json")
          self.end_headers()

          dataLength = int(self.headers["Content-Length"])
          data = self.rfile.read(dataLength)

          data.strip()

          print(data)
          # convert from json
          y = json.loads(data)
          response = y
          if "email" in y:
              a = y["email"]
              b = y["Password"]

              b = base64.b64decode(b+"=")
              print("ok1", b)
              # b= b.split("[']")[1]

              # b= BytesIO(b64decode(b))
              # print("ok22", b)

              c = y["Adm"]
              d = y["FullName"]

              e = y["DateOfBirth"]
              z = y["Picture"]
              # print('me',y.myFile)

              w = z["myFile"]
              f = w.split(',')[1]

              # print('yoooou',f.get("myFile"))
              # f = Image.open(BytesIO(b64decode(w.split(',')[1])))
              # f.save("image.png")
              # FA = w.split(',')[1]));

              g = y["SchoolStartYear"]
              h = y["MajorFieldOfStudy"]
              i = y["MinorFieldOfStudy"]
              j = ','.join(y["AdCourses"])
              # k = y["Average"]
              l = y["Comments"]
              m = y["Remark"]
              n = ','.join(y["Courses"])
              o = y['Degree']
              ss = y['Suspended']
              print(a)
              # print(b)
              print(j)

              # raw = pad(b)
              # key = "hello"
              # iv = Random.new().read(AES.block_size)
              # cipher = AES.new(key, AES.MODE_CBC, iv)
              # return base64.b64encode(iv + cipher.encrypt(raw))

              # b = fernet.decrypt(b).decode()





              # check = myc.execute("SELECT Email FROM users WHERE EMAIL= %(unm)s", {'unm':a})

              # new_user = users(email=a, password=b)

              check = myc.execute("SELECT * FROM users WHERE Email= %(unm)s", {'unm': a})
              print(check)
              for i in myc:
                  print(i)
                  print('aaaaaa')

                  if i[1] == a:
                      print('kill')
                      kp = "Email Already Exists"
                      response = {}
                      response["status"] = f"{kp}"

                      res6 = {}
                      res6["EmailAlreadyExist"] = f"{kp}"

                      el6 = [res6]
                      self.wfile.write(bytes(dumps(el6), "utf8"))

                  else:
                      print('lokd')
                      kpp = "sthwrong"
                      response["sthwrong"] = f"{kpp}"


              mydb.commit()

          print('junjfjdd')
          ins = users.insert().values(Email=a, Password=b, Adm=bool(c), FullName=d, DateOfBirth=e,
                                      SchoolStartYear=g, MajorFieldOfStudy=h, MinorFieldOfStudy=i,
                                      AdCourses=j, Courses=n, Comments= l, Remark =m, Degree =o,
                                      Suspended = ss, Picture=f)
          conn = engine.connect()
          conn.execute(ins)

          print("yaga")

          pp = "SUCCESS"
          response = {}
          response["status"] = f"{pp}"

          res7 = {}
          res7["SUCCESS"] = f"{pp}"

          el7 = [res7]
          self.wfile.write(bytes(dumps(el7), "utf8"))

      if self.path.endswith('/admsearch'):
          self.send_response(200)
          self._send_cors_headers()
          self.send_header("Content-Type", "application/json")
          self.end_headers()

          dataLength = int(self.headers["Content-Length"])
          data = self.rfile.read(dataLength)

          data.strip()

          print(data)
          # convert from json
          y = json.loads(data)

          ob = ["id", "Email", "Password", "Adm", "FullName", "DateOfBirth", "Picture", "SchoolStartYear",
                "MajorFieldOfStudy", "MinorFieldOfStudy", "Courses", "AdCourses", "Average", "Comments",
                "Suspended", "Remark", "Degree"]
          counter = 0
          fndcount = []

          if "search" in y:
              a = y["search"]

              t = str(a)

              query = "SELECT * FROM users WHERE Email LIKE %s"
              name = ("%" + t + "%",)
              # name = ("%W%",)
              myc.execute(query, name)

              check = myc.fetchall()

              for res in check:

                  print(res)
                  sndcount = []
                  obj = {}
                  for pl in res:
                      obj[ob[counter]] = pl

                      counter = counter + 1

                  # sndcount.append({ob[counter]:pl})

                  fndcount.append(obj)
                  counter = 0

                  response = {}
                  response["userinfo"] = eval(f"{fndcount}")
          self.wfile.write(bytes(dumps(response), "utf8"))

      # UPDATING THE STUDENT PROFILE REQUIRES THE Email OF THE ADMIN THATS UPDATING THE STATUS AS(admemail) THEN ALL THE STUDENT INFO
      # THE COURSES AND ADDITIONAL COURSES SHOULD BE IN ARRAY FORMAT

      if self.path.endswith('/updatestudentinfo'):
          self.send_response(200)
          self._send_cors_headers()
          self.send_header("Content-Type", "application/json")
          self.end_headers()

          dataLength = int(self.headers["Content-Length"])
          data = self.rfile.read(dataLength)

          data.strip()

          print(data)
          # convert from json
          y = json.loads(data)

          if "admemail" in y:
              admcheck = y["admemail"]
              a = y["Email"]
              d = y["FullName"]
              e = y["DateOfBirth"]
              # f = y["Picture"]
              # g = y["SchoolStartYear"]
              h = y["MajorFieldOfStudy"]
              i = y["MinorFieldOfStudy"]
              j = ','.join(y["AdCourses"])
              # k = y["Average"]
              # l = y["Comments"]
              # m = y["Remark"]
              n = y["id"]
              o = ','.join(y["Courses"])
              p = y["Degree"]

              tid = int(n)

          myc.execute("SELECT Adm FROM users WHERE Email= %(unm)s", {'unm': admcheck})

          check = myc.fetchall()

          for res in check:
              for rr in res:
                  if rr == 1:
                      print('Admin stats true')
                      myc.execute(
                          'UPDATE users SET Email = %s ,FullName = %s ,DateOfBirth = %s ,MajorFieldOfStudy = %s ,MinorFieldOfStudy = %s,Courses=%s ,AdCourses = %s, Degree = %s WHERE id = %s ',
                          (a, d, e, h, i, o, j, p, tid))
                      mydb.commit()
                      response = {}
                      response["status"] = "done"

                      res4 = {}
                      res4["Success"] = "done"

                      el2 = [res4]
                      self.wfile.write(bytes(dumps(el2), "utf8"))

                  else:
                      print("Admin stats false")

          print(check)

      # STUDENT UPDATES HIS ADDITIONAL COURSES REQUIRES THE ADDITIONAL COURSES IN AN ARRAY AND HIS EMAIL
      if self.path.endswith('/updteadcourses'):
          self.send_response(200)
          self._send_cors_headers()
          self.send_header("Content-Type", "application/json")
          self.end_headers()

          dataLength = int(self.headers["Content-Length"])
          data = self.rfile.read(dataLength)

          data.strip()

          print(data)
          # convert from json
          y = json.loads(data)

          if "AdCourses" in y:
              courses = ','.join(y["AdCourses"])
              print(courses, 'djjdjddjkj')
              a = y["Email"]

          myc.execute('UPDATE users SET AdCourses = %s WHERE Email = %s ', (courses, a))
          mydb.commit()
          response = {}
          response["status"] = "done"

          res4 = {}
          res4["Success"] = "done"

          el2 = [res4]
          self.wfile.write(bytes(dumps(el2), "utf8"))

      # SUSPENDING THE STUDENT REQUIRES THE ADMIN Email AS(admemail) THEN THE STUDENT EMAIL AND A STRING OF "1" OR "0" FOR THE BOOLIAN STATUS
      if self.path.endswith('/suspendstudent'):
          self.send_response(200)
          self._send_cors_headers()
          self.send_header("Content-Type", "application/json")
          self.end_headers()

          dataLength = int(self.headers["Content-Length"])
          data = self.rfile.read(dataLength)

          data.strip()

          print(data)
          # convert from json
          y = json.loads(data)

          if "admemail" in y:
              admcheck = y["admemail"]
              a = y["email"]
              b = y["stats"]

              tid = int(b)

          myc.execute("SELECT Adm FROM users WHERE Email= %(unm)s", {'unm': admcheck})

          check = myc.fetchall()

          for res in check:
              for rr in res:
                  if rr == 1:
                      print('Admin stats true')
                      myc.execute('UPDATE users SET Suspended = %s WHERE Email = %s ', (tid, a))
                      mydb.commit()
                  else:
                      print("Admin stats false")

      # MAKING A NEW ADMIN REQUIRES THE ADMIN Email AS(admemail) THEN THE OTHER EMAIL AND A STRING OF "1" OR "0" FOR THE BOOLIAN STATUS
      if self.path.endswith('/mknewadmin'):
          self.send_response(200)
          self._send_cors_headers()
          self.send_header("Content-Type", "application/json")
          self.end_headers()

          dataLength = int(self.headers["Content-Length"])
          data = self.rfile.read(dataLength)

          data.strip()

          print(data)
          # convert from json
          y = json.loads(data)

          if "admemail" in y:
              admcheck = y["admemail"]
              a = y["email"]
              b = y["stats"]

              tid = int(b)

          myc.execute("SELECT Adm FROM users WHERE Email= %(unm)s", {'unm': admcheck})

          check = myc.fetchall()

          for res in check:
              for rr in res:
                  if rr == 1:
                      print('Admin stats true')
                      myc.execute('UPDATE users SET Adm = %s WHERE Email = %s ', (tid, a))
                      mydb.commit()
                  else:
                      print("Admin stats false")

      #  RETURNS ALL USERS REQUIRES THE ADMIN EMAIL AS INPUT FOR VERIFICATION
      if self.path.endswith('/getalluser'):
          self.send_response(200)
          self._send_cors_headers()
          self.send_header("Content-Type", "application/json")
          self.end_headers()

          dataLength = int(self.headers["Content-Length"])
          data = self.rfile.read(dataLength)

          data.strip()

          print(data)
          # convert from json
          y = json.loads(data)

          if "admemail" in y:
              admcheck = y["admemail"]

              print(admcheck, 'uuuuuuuuuuu')

          myc.execute("SELECT Adm FROM users WHERE Email= %(unm)s", {'unm': admcheck})

          check = myc.fetchall()

          for res in check:
              for rr in res:
                  if rr == 1:
                      print('Admin stats true')

                      ob = ["id", "Email", "Password", "Adm", "FullName", "DateOfBirth", "Picture",
                            "SchoolStartYear",
                            "MajorFieldOfStudy", "MinorFieldOfStudy", "Courses", "AdCourses", "Average", "Comments",
                            "Suspended", "Remark", "Degree"]
                      counter = 0
                      fndcount = []

                      # myc.execute('SELECT * FROM users WHERE Adm = %s', (0,))
                      myc.execute('SELECT * FROM users')
                      check = myc.fetchall()

                      # print(check, 'lalalallalalalalallalalalal')

                      for res in check:

                          print(res)
                          sndcount = []
                          obj = {}
                          for pl in res:
                              obj[ob[counter]] = pl

                              counter = counter + 1

                          # sndcount.append({ob[counter]:pl})

                          fndcount.append(obj)
                          counter = 0

                          resp = {}
                          resp["userinfo"] = eval(f"{fndcount}")
                      self.wfile.write(bytes(dumps(resp), "utf8"))
                  else:
                      print("Admin stats false")

      # RETURNS THE STUDENTS INFO REQUIRES THE STUDENT EMAIL AS INPUT
      if self.path.endswith('/getstudentinfo'):
          self.send_response(200)
          self._send_cors_headers()
          self.send_header("Content-Type", "application/json")
          self.end_headers()

          dataLength = int(self.headers["Content-Length"])
          data = self.rfile.read(dataLength)

          data.strip()

          print(data)
          # convert from json
          y = json.loads(data)

          if "email" in y:
              a = y["email"]

          myc.execute('SELECT * FROM users WHERE Email= %s', (a,))

          check = myc.fetchall()

          ob = ["id", "Email", "Password", "Adm", "FullName", "DateOfBirth", "Picture",
                "SchoolStartYear",
                "MajorFieldOfStudy", "MinorFieldOfStudy", "Courses", "AdCourses", "Average", "Comments",
                "Suspended", "Remark", "Degree"]
          counter = 0
          fndcount = []

          for res in check:

              print(res)
              sndcount = []
              obj = {}
              for pl in res:
                  obj[ob[counter]] = pl

                  counter = counter + 1

              # sndcount.append({ob[counter]:pl})

              fndcount.append(obj)
              counter = 0

              response = {}
              response["userinfo"] = eval(f"{fndcount}")
          self.wfile.write(bytes(dumps(response), "utf8"))








      #self.send_dict_response(response)

# if __name__ == '__main__':
#     test(RequestHandler, HTTPServer, port=int(sys.argv[1]) if len(sys.argv) > 1 else 9000)

print("Starting servetr now")
port = int(os.environ.get("PORT", 8000))

httpd = HTTPServer(("0.0.0.0", port), RequestHandler)
print("Hosting server on port 8000")
httpd.serve_forever()