
import flask
import time
import re
from flask import Flask, request, template_rendered
from flask import url_for, redirect, flash
from flask import render_template
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime
from numpy import identity, product
import random, string
from sqlalchemy import null
import cx_Oracle

#### Oracle 連線
cx_Oracle.init_oracle_client(lib_dir="C:/instantclient/instantclient_21_3")
connection = cx_Oracle.connect('Group17',"group017",cx_Oracle.makedsn("140.117.69.58",1521,"orcl"),encoding='UTF-8', nencoding='UTF-8')
cursor =connection.cursor()


app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = False
app.secret_key = 'Your Key'
login_manager = LoginManager(app)
login_manager.login_view = 'login' # 假如沒有登入的話，要登入會導入 login 這個頁面



@app.route('/')
def index():
    title = "Chili"
    return render_template('starter.html',title = title )


@app.route('/home')
def home ():

    return render_template('home.html')


##新增櫃位
@app.route('/counter', methods=['GET', 'POST'])
def counter():

    if request.method == 'POST':

        cursor.prepare('SELECT * FROM COUNTER WHERE COID=:COID')
        data = ""

        while ( data != None): #裡面沒有才跳出回圈

            number = str(random.randrange( 10000, 99999))
            en = random.choice(string.ascii_letters)
            COID = en + number #隨機編號
            cursor.execute(None, {'COID':COID})
            data = cursor.fetchone()

        CO_NAME = request.values.get('CO_NAME')
        RATE = request.values.get('RATE')
        CO_TIME = request.values.get('CO_TIME')
        CO_TYPE = request.values.get('CO_TYPE')


        if not CO_NAME or not RATE or not CO_TIME or not CO_TYPE:
            error_statement =" All the fields are required...."
            return render_template('counter.html', error_statement = error_statement, CO_NAME =CO_NAME, RATE = RATE, CO_TIME = CO_TIME, CO_TYPE = CO_TYPE )



        cursor.prepare('INSERT INTO COUNTER VALUES (:COID, :CO_NAME, :RATE, :CO_TIME,:CO_TYPE)')
        cursor.execute(None, {'COID': COID,'CO_NAME':CO_NAME, 'RATE':RATE,'CO_TIME':CO_TIME , "CO_TYPE":CO_TYPE})
        connection.commit()



    return render_template('counter.html')

##新增客戶
@app.route('/customer', methods=['GET', 'POST'])
def customer():

    if request.method == 'POST':

        cursor.prepare('SELECT * FROM CUSTOMER WHERE CID=:CID AND LAST_BUY =:LAST_BUY AND LAST_BUY_TIME =:LAST_BUY_TIME')
        data = ""

        while ( data != None): #裡面沒有才跳出回圈
            #隨機生成客戶編號
            number = str(random.randrange( 10000, 99999))
            en = random.choice(string.ascii_letters)
            CID = en + number #隨機編號

            #隨機生成上次購買日期
            a1=(1996,1,1,0,0,0,0,0,0)
            a2=(2021,12,31,23,59,59,0,0,0)
            start=time.mktime(a1)
            end=time.mktime(a2)
            t=random.randint(start,end) #在開始和結束時間戳中隨機取出一個
            date_touple=time.localtime(t) #將時間戳生成時間元組
            date=time.strftime("%Y-%m-%d ",date_touple) #將時間元組轉成格式化字符串（1976-05-21）

            #隨機生成上次購買時間
            t1=(2000,12,1,10,0,0,0,0,0)
            t2=(2000,12,1,22,59,59,0,0,0)
            start_TIME=time.mktime(t1)
            end_TIME=time.mktime(t2)
            TIME=random.randint(start_TIME,end_TIME)
            date_touple=time.localtime(TIME)
            TIME=time.strftime("%H:%M:%S",date_touple)



            cursor.execute(None, {'CID':CID, 'LAST_BUY':date , 'LAST_BUY_TIME':TIME})
            data = cursor.fetchone()

        NAME = request.values.get('NAME')
        EMAIL = request.values.get('EMAIL')
        AGE = request.values.get('AGE')


        if not NAME or not EMAIL or not AGE :
            error_statement =" All the fields are required...."
            return render_template('customer.html', error_statement = error_statement, NAME =NAME, EMAIL = EMAIL, AGE = AGE ) ##加上上次購買紀錄


        cursor.prepare('INSERT INTO CUSTOMER VALUES (:CID, :NAME, :EMAIL, :AGE,:LAST_BUY , :LAST_BUY_TIME)')
        cursor.execute(None, {'CID': CID,'NAME':NAME, 'EMAIL':EMAIL,'AGE':AGE, 'LAST_BUY':date , 'LAST_BUY_TIME':TIME })
        connection.commit()



    return render_template('customer.html')
##新增活動
@app.route('/activity', methods=['GET', 'POST'])
def activity():

    if request.method == 'POST':

        cursor.prepare('SELECT * FROM ACTIVITY WHERE AID=:AID')
        data = ""

        while ( data != None): #裡面沒有才跳出回圈

            number = str(random.randrange( 10000, 99999))
            en = random.choice(string.ascii_letters)
            AID = en + number #隨機編號
            cursor.execute(None, {'AID':AID})
            data = cursor.fetchone()

        A_NAME = request.values.get('A_NAME')
        DISCOUNT = request.values.get('DISCOUNT')
        A_START = request.values.get('A_START')
        A_END = request.values.get('A_END')


        if not A_NAME or not DISCOUNT or not A_START or not A_END :
            error_statement =" All the fields are required...."
            return render_template('activity.html', error_statement = error_statement, A_NAME =A_NAME, DISCOUNT = DISCOUNT, A_START = A_START, A_END = A_END )



        cursor.prepare('INSERT INTO ACTIVITY VALUES (:AID, :A_NAME, :DISCOUNT, :A_START,:A_END)')
        cursor.execute(None, {'AID': AID,'A_NAME':A_NAME, 'DISCOUNT':DISCOUNT,'A_START':A_START , "A_END":A_END})
        connection.commit()


    return render_template('activity.html')


##新增消費記錄
@app.route('/transaction', methods=['GET', 'POST'])
def transaction():

    if request.method == 'POST':

        cursor.prepare('SELECT * FROM TRANSACTION WHERE TID=:TID AND PAY_TIME =:PAY_TIME')
        data = ""

        while ( data != None): #裡面沒有才跳出回圈

            number = str(random.randrange( 10000, 99999))
            en = random.choice(string.ascii_letters)
            TID = en + number #隨機編號

            #自動產生消費日期
            PAY_TIME = str(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
            PAY_TIME_format = 'yyyy/mm/dd hh24:mi:ss'

            cursor.execute(None, {'TID':TID,'PAY_TIME':PAY_TIME})
            data = cursor.fetchone()

        CID = request.values.get('CID')
        COID = request.values.get('COID')
        AMOUNT = request.values.get('AMOUNT')
        PAY_TYPE = request.values.get('PAY_TYPE')

        #確認每個欄位都有被填寫：
        if not CID or not COID or not AMOUNT or not PAY_TYPE :
            error_statement =" All the fields are required...."
            return render_template('transaction.html', error_statement = error_statement, CID =CID, COID = COID, AMOUNT = AMOUNT, PAY_TYPE = PAY_TYPE )

        ##確認客戶ID（CID）存在：
        cursor.prepare('SELECT CID FROM CUSTOMER WHERE CID = :id ')
        cursor.execute(None, {'id': CID})
        cust = cursor.fetchall()

        try:
            cust[0]


        except:
            error_statement =" 客戶ID not exist..."
            return render_template('transaction.html', error_statement = error_statement, COID = COID, AMOUNT = AMOUNT, PAY_TYPE = PAY_TYPE )

        #  查看櫃位ID(COID)是否存在
        cursor.prepare('SELECT COID FROM COUNTER WHERE COID = :id ')
        cursor.execute(None, {'id': COID})
        counter = cursor.fetchall()
        try:
            counter[0]


        except:
            error_statement =" 櫃位ID not exist..."
            return render_template('transaction.html', error_statement = error_statement, CID = CID, AMOUNT = AMOUNT, PAY_TYPE = PAY_TYPE )



        cursor.prepare('INSERT INTO TRANSACTION VALUES (:TID, :CID, :COID, :AMOUNT,:PAY_TYPE,TO_DATE( :PAY_TIME, :PAY_TIME_format))')
        cursor.execute(None, {'TID': TID,'CID':CID, 'COID':COID,'AMOUNT':AMOUNT , "PAY_TYPE":PAY_TYPE,'PAY_TIME':PAY_TIME,'PAY_TIME_format':PAY_TIME_format})
        connection.commit()


    return render_template('transaction.html')


##新增停車資訊
@app.route('/parklot', methods=['GET', 'POST'])
def parklot():

    if request.method == 'POST':

        cursor.prepare('SELECT * FROM PARKING_LOT WHERE PID=:PID AND PARKTIME=:PARKTIME')
        data = ""

        while ( data != None): #裡面沒有才跳出回圈

            number = str(random.randrange( 10000, 99999))
            en = random.choice(string.ascii_letters)
            PID = en + number #隨機編號
            PARKTIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(None, {'PID':PID,'PARKTIME':PARKTIME})
            data = cursor.fetchone()

        REMAINING = request.values.get('REMAINING')
        AREA_LETTER = request.values.get('AREA_LETTER') #停車場區域
        NUMBER = request.values.get('NUMBER') #停車場區域號碼
        AREA = AREA_LETTER+NUMBER


        if not REMAINING:
            error_statement =" All the fields are required...."
            return render_template('parklot.html', error_statement = error_statement, REMAINING =REMAINING, AREA_LETTER =AREA_LETTER, NUMBER = NUMBER)



        cursor.prepare('INSERT INTO PARKING_LOT VALUES (:PID, :PARKTIME, :REMAINING,:AREA)')
        cursor.execute(None, {'PID':PID,'PARKTIME':PARKTIME, 'REMAINING':REMAINING,'AREA':AREA})
        connection.commit()




    return render_template('parklot.html')

##新增客戶停車資訊
@app.route('/park', methods=['GET', 'POST'])
def park():

    if request.method == 'POST':

        #確定停車編號、客戶編號沒有重複
        cursor.prepare('SELECT * FROM PARKING WHERE PID=:PID AND CID=:CID')

        PID = request.values.get('PID')
        CID = request.values.get('CID')
        CARTYPE = request.values.get('CARTYPE')
        CARMODEL = request.values.get('CARMODEL')

        if not PID or not CID:
            error_statement =" All the fields are required...."
            return render_template('park.html', error_statement = error_statement, PID = PID, CID = CID ,CARTYPE = CARTYPE, CARMODEL = CARMODEL )


        cursor.execute(None, {'PID': PID , 'CID':CID})



        ##確認停車編號PID存在：
        cursor.prepare('SELECT PID FROM PARKING_LOT WHERE PID = :id ')
        cursor.execute(None, {'id': PID})
        park = cursor.fetchall()

        try:
            park[0]


        except:
            error_statement =" 停車編號 not exist..."
            return render_template('park.html', error_statement = error_statement,  CID = CID, CARTYPE = CARTYPE, CARMODEL = CARMODEL )


        ##確認客戶編號CID存在：
        cursor.prepare('SELECT CID FROM CUSTOMER WHERE CID = :id ')
        cursor.execute(None, {'id': CID})
        cust = cursor.fetchall()

        try:
            cust[0]

        except:
            error_statement =" 客戶編號 not exist..."
            return render_template('park.html', error_statement = error_statement, PID = PID, CARTYPE = CARTYPE, CARMODEL = CARMODEL )


        cursor.prepare('INSERT INTO PARKING VALUES (:PID,:CID, :CARTYPE, :CARMODEL)')
        cursor.execute(None, {'PID':PID,'CID':CID, 'CARTYPE':CARTYPE,  'CARMODEL':CARMODEL})
        connection.commit()


    return render_template('park.html' )


## 建立客戶索引表
@app.route('/cust_table', methods=['GET', 'POST'])
def cust_table():

    sql = 'SELECT * FROM CUSTOMER'
    cursor.execute(sql)
    cust_row = cursor.fetchall()
    cust_data = []
    for i in cust_row:
        cust = {
            '客戶ID': i[0],
            '客戶名稱': i[1],
            '客戶信箱': i[2],
            '客戶年紀': i[3],
            '客戶上次消費日期': i[4],
            '客戶上次消費時間': i[5]
        }
        cust_data.append(cust) #將list 放進 disctionary

    #新增客戶
    if "add" in request.form:
        return render_template("customer.html")

    #刪除客戶資料
    if "delete" in request.form :
        cid = request.values.get('delete')
        cursor.prepare(' DELETE FROM CUSTOMER WHERE CID=:cid')
        cursor.execute(None, {'cid': cid})
        connection.commit() # 把這個刪掉

        return render_template('cust_table.html', cust_data=cust_data)

    ##編輯客戶資料
    if 'edit' in request.values:
        cid = request.values.get('edit')
        return redirect(url_for('cust_edit', cid=cid))

    return render_template('cust_table.html', cust_data=cust_data)




##重新編輯客戶資訊
@app.route('/cust_edit', methods=['GET', 'POST'])

def cust_edit():
    if request.method == 'POST':
        cid = request.values.get('cid')
        new_NAME = request.values.get('new_NAME')
        new_EMAIL = request.values.get('new_EMAIL')
        new_AGE = request.values.get('new_AGE')
        cursor.prepare('UPDATE CUSTOMER SET NAME=:new_NAME, EMAIL=:new_EMAIL, AGE=:new_AGE WHERE CID=:cid')
        cursor.execute(None, {'cid':cid,'new_NAME':new_NAME, 'new_EMAIL':new_EMAIL,'new_AGE':new_AGE})
        connection.commit()
        return redirect(url_for('cust_table'))

    else:
        customer  = show_cust()
        return render_template('cust_edit.html', customer=customer)

def show_cust():
    cid = request.args['cid']
    cursor.prepare('SELECT * FROM CUSTOMER WHERE CID = :cid ')
    cursor.execute(None, {'cid': cid})

    data = cursor.fetchone()
    name = data[1]
    mail = data[2]
    age = data[3]

    customer = {
    '客戶ID': cid,
    '客戶名稱': name,
    '客戶信箱': mail,
    '客戶年紀': age
    }
    return customer




## 建立櫃位索引表
@app.route('/counter_table', methods=['GET', 'POST'])
def counter_table():

    sql = 'SELECT * FROM COUNTER'
    cursor.execute(sql)
    counter_row = cursor.fetchall()
    counter_data = []
    for i in counter_row:
        counter = {
            '櫃位ID': i[0],
            '櫃位名稱': i[1],
            '櫃位抽成': i[2],
            '櫃位進駐時間': i[3],
            '櫃位類型': i[4]
        }
        counter_data.append(counter) #將list 放進 disctionary

    #新增櫃位
    if "add" in request.form:
        return render_template("counter.html")

    #刪除櫃位資料
    if "delete" in request.form :
        coid = request.values.get('delete')
        cursor.prepare(' DELETE FROM COUNTER WHERE COID=:coid')
        cursor.execute(None, {'coid': coid})
        connection.commit() # 把這個刪掉

        return render_template('counter_table.html', counter_data=counter_data)

    ##編輯櫃位資料
    if 'edit' in request.values:
        coid = request.values.get('edit')
        return redirect(url_for('counter_edit', coid=coid))

    return render_template('counter_table.html', counter_data=counter_data)




##重新編輯櫃位資訊
@app.route('/counter_edit', methods=['GET', 'POST'])
def counter_edit():
    if request.method == 'POST':
        coid = request.values.get('coid')
        new_NAME = request.values.get('new_NAME')
        new_RATE = request.values.get('new_RATE')
        new_CO_TYPE = request.values.get('new_CO_TYPE')
        new_CO_TIME = request.values.get('new_CO_TIME')
        cursor.prepare('UPDATE COUNTER SET CO_NAME=:new_NAME, RATE=:new_RATE, CO_TIME=:new_CO_TIME,CO_TYPE = :new_CO_TYPE WHERE COID=:coid')
        cursor.execute(None, {'coid':coid,'new_NAME':new_NAME, 'new_RATE':new_RATE,'new_CO_TYPE':new_CO_TYPE,'new_CO_TIME':new_CO_TIME})
        connection.commit()
        return redirect(url_for('counter_table'))

    else:
        counter  = show_counter()
        return render_template('counter_edit.html', counter=counter)

def show_counter():
    coid = request.args['coid']
    cursor.prepare('SELECT * FROM COUNTER WHERE COID = :coid ')
    cursor.execute(None, {'coid': coid})

    data = cursor.fetchone()

    counter = {
    '櫃位ID': coid,
    '櫃位名稱': data[1],
    '櫃位抽成': data[2],
    '櫃位進駐時間': data[3],
    '櫃位類型':data[4]
    }
    return counter



## 建立活動索引表
@app.route('/act_table', methods=['GET', 'POST'])
def act_table():

    sql = 'SELECT * FROM ACTIVITY'
    cursor.execute(sql)
    act_row = cursor.fetchall()
    act_data = []
    for i in act_row:
        act = {
            '活動ID': i[0],
            '活動名稱': i[1],
            '活動折扣': i[2],
            '活動開始時間': i[3],
            '活動結束時間': i[4]
        }
        act_data.append(act) #將list 放進 disctionary

    #新增活動
    if "add" in request.form:
        return render_template("activity.html")

    #刪除活動資料
    if "delete" in request.form :
        aid = request.values.get('delete')
        cursor.prepare(' DELETE FROM ACTIVITY WHERE AID=:aid')
        cursor.execute(None, {'aid': aid})
        connection.commit() # 把這個刪掉

        return render_template('act_table.html', act_data=act_data)

    ##編輯活動資料
    if 'edit' in request.values:
        aid = request.values.get('edit')
        return redirect(url_for('act_edit', aid=aid))

    return render_template('act_table.html', act_data=act_data)




##重新編輯活動資訊
@app.route('/act_edit', methods=['GET', 'POST'])
def act_edit():
    if request.method == 'POST':
        aid = request.values.get('aid')
        new_NAME = request.values.get('new_NAME')
        new_DISCOUNT = request.values.get('new_DISCOUNT')
        new_A_START = request.values.get('new_A_START')
        new_A_END = request.values.get('new_A_END')
        cursor.prepare('UPDATE ACTIVITY SET A_NAME=:new_NAME, DISCOUNT=:new_DISCOUNT, A_START=:new_A_START, A_END = :new_A_END WHERE AID=:aid')
        cursor.execute(None, {'aid':aid,'new_NAME':new_NAME, 'new_DISCOUNT':new_DISCOUNT,'new_A_START':new_A_START,'new_A_END':new_A_END})
        connection.commit()
        return redirect(url_for('act_table'))

    else:
        act  = show_activity()
        return render_template('act_edit.html', act=act)

def show_activity():
    aid = request.args['aid']
    cursor.prepare('SELECT * FROM ACTIVITY WHERE AID = :aid ')
    cursor.execute(None, {'aid': aid})

    data = cursor.fetchone()

    act = {
    '活動ID': aid,
    '活動名稱': data[1],
    '活動折扣': data[2],
    '活動開始時間': data[3],
    '活動結束時間':data[4]
    }
    return act

## 建立交易資料索引表
@app.route('/transaction_table', methods=['GET', 'POST'])
def trans_table():

    sql = 'SELECT * FROM TRANSACTION'
    cursor.execute(sql)
    trans_row = cursor.fetchall()
    trans_data = []
    for i in trans_row:
        trans = {
            '交易ID': i[0],
            '客戶ID': i[1],
            '櫃位ID': i[2],
            '消費金額': i[3],
            '付款方式': i[4],
            '消費時間': i[5]
        }
        trans_data.append(trans) #將list 放進 disctionary

    #新增交易
    if "add" in request.form:
        return render_template("transaction.html")

    #刪除交易資料
    if "delete" in request.form :
        tid = request.values.get('delete')
        cursor.prepare(' DELETE FROM TRANSACTION WHERE TID=:tid')
        cursor.execute(None, {'tid': tid})
        connection.commit() # 把這個刪掉

        return render_template('trans_table.html', trans_data=trans_data)

    ##編輯交易資料
    if 'edit' in request.values:
        tid = request.values.get('edit')
        return redirect(url_for('trans_edit', tid=tid))

    return render_template('trans_table.html', trans_data=trans_data)




##重新編輯交易資訊
@app.route('/transaction_edit', methods=['GET', 'POST'])
def trans_edit():
    if request.method == 'POST':
        tid = request.values.get('tid')
        new_CID = request.values.get('new_CID')
        new_COID = request.values.get('new_COID')
        new_AMOUNT = request.values.get('new_AMOUNT')
        new_PAY_TYPE = request.values.get('new_PAY_TYPE')
        cursor.prepare('UPDATE TRANSACTION SET CID=:new_CID, COID=:new_COID, AMOUNT=:new_AMOUNT, PAY_TYPE = :new_PAY_TYPE  WHERE TID=:tid')
        cursor.execute(None, {'tid':tid,'new_CID':new_CID, 'new_COID':new_COID,'new_AMOUNT':new_AMOUNT,'new_PAY_TYPE':new_PAY_TYPE})
        connection.commit()
        return redirect(url_for('trans_table'))

    else:
        trans  = show_transaction()
        return render_template('trans_edit.html', trans=trans)

def show_transaction():
    tid = request.args['tid']
    cursor.prepare('SELECT * FROM TRANSACTION WHERE TID = :tid ')
    cursor.execute(None, {'tid': tid})

    data = cursor.fetchone()

    trans = {
    '交易ID': tid,
    '客戶ID': data[1],
    '櫃位ID': data[2],
    '消費金額': data[3],
    '付款方式':data[4]
    }
    return trans



# 登入頁面
class User(UserMixin):

    pass

@login_manager.user_loader
def user_loader(userid):
    user = User()
    user.id = userid
    cursor.prepare('SELECT NAME FROM MEMBER WHERE MID = :id ')
    cursor.execute(None, {'id':userid})
    data = cursor.fetchone()
    user.name = data[0]
    return user

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':

        account = request.form['account']
        password = request.form['password']

        # 查詢看看有沒有這個資料
        # sql = 'SELECT ACCOUNT, PASSWORD, MID, IDENTITY, NAME FROM MEMBER WHERE ACCOUNT = \'' + account + '\''
        # cursor.execute(sql)
        cursor.prepare('SELECT ACCOUNT, PASSWORD, MID, NAME FROM MEMBER WHERE ACCOUNT = :id ')
        cursor.execute(None, {'id': account})

        data = cursor.fetchall() # 抓去這個帳號的資料

        # 但是可能他輸入的是沒有的，所以下面我們 try 看看抓不抓得到
        try:
            DB_password = data[0][1] # true password
            user_id = data[0][2] # user_id


        # 抓不到的話 flash message '沒有此帳號' 給頁面
        except:
            flash('*沒有此帳號')
            return redirect(url_for('login'))

        if( DB_password == password ):
            user = User()
            user.id = user_id
            login_user(user)
            return redirect(url_for('home'))



        # 假如密碼不符合 則會 flash message '密碼錯誤' 給頁面
        else:
            flash('*密碼錯誤，請再試一次')
            return redirect(url_for('login'))


    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    revenue = []
    dataa = []
    for i in range(1,13):
        cursor.prepare('SELECT EXTRACT(MONTH FROM PAY_TIME), SUM(AMOUNT) FROM COUNTER NATURAL JOIN TRANSACTION WHERE EXTRACT(MONTH FROM PAY_TIME)=:mon GROUP BY EXTRACT(MONTH FROM PAY_TIME)')
        cursor.execute(None, {"mon": i})
        
        row = cursor.fetchall()
        if cursor.rowcount == 0:
            revenue.append(0)
        else:
            for j in row:
                revenue.append(j[1])
        
        cursor.prepare('SELECT EXTRACT(MONTH FROM PAY_TIME), SUM(AMOUNT) FROM COUNTER NATURAL JOIN TRANSACTION WHERE EXTRACT(MONTH FROM PAY_TIME)=:mon GROUP BY EXTRACT(MONTH FROM PAY_TIME)')
        cursor.execute(None, {"mon": i})
        
        row = cursor.fetchall()
        if cursor.rowcount == 0:
            dataa.append(0)
        else:
            for k in row:
                dataa.append(k[1])
                print('k='+str(k[1]))
        print(i, row)
    cursor.prepare('Select COUNT(*),CARTYPE FROM PARKING GROUP BY CARTYPE')
    cursor.execute(None)
    row = cursor.fetchall()
    datab = []
    for i in row:
        temp = {
            'value': i[0],
            'name': i[1]
        }
        datab.append(temp)
    print('datab=', datab)    
    return render_template('dashboard.html', counter = counter, revenue = revenue, dataa = dataa, datab = datab)
        

# 註冊頁面
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user_name = request.form['username']
        user_account = request.form['account']
        user_password = request.form['password']


        # 抓取所有的會員帳號，因為下面要比對是否已經有這個帳號
        check_account =""" SELECT ACCOUNT FROM MEMBER """
        cursor.execute(check_account)
        exist_account = cursor.fetchall()
        account_list = []
        for i in exist_account:
            account_list.append(i[0])

        if(user_account in account_list):
            # 如果已經有這個帳號，就會給一個 flash message : 上面會顯示已經有這個帳號了
            flash('Falid!')
            return redirect(url_for('register'))
        else:
            # 在 SQL 裡有設定 member id 是 auto increment 所以第一個值給：null

            cursor.prepare('INSERT INTO MEMBER VALUES (:name, :account, :password,null)')
            cursor.execute(None, {'name': user_name, 'account':user_account, 'password':user_password})
            connection.commit()

            return redirect(url_for('login'))


    return render_template('register.html')

@app.route('/logout')
def logout():

    logout_user()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.debug = True #easy to debug
    app.secret_key = "Your Key"

app.run()