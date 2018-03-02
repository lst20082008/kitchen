#导入必要文件
from flask import Flask,render_template,request,redirect,url_for,session
import os
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO,emit
import json



#项目初始设置
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['SECRET_KEY'] = '288794613aA!@#'
#app.debug = True
db = SQLAlchemy(app)
socketio = SocketIO()
socketio.init_app(app)



#ORM
class User(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    userName = db.Column(db.String(80),unique=True)
    password = db.Column(db.String(255))
    def __init__(self,userName,password):
        self.userName = userName
        self.password = password
    def __repr__(self):
        print("<User>:%s"%self.userName)

class Food(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(80),unique=True)
    num = db.Column(db.Integer())
    unit = db.Column(db.String(16))
    def __init__(self,name,num = 0,unit = '个'):
        self.name = name
        self.num = num
        self.unit = unit



#app路由设置
@app.route('/')
def index():
    notZeroItems = Food.query.filter(Food.num != 0).all()
    zeroItems = Food.query.filter_by(num=0).all()

    #暂时用这个
    return  render_template('newIndex.html',notZeroItems=notZeroItems,zeroItems=zeroItems)

    if 'userName' in session:
        return  render_template('index.html',notZeroItems=notZeroItems,zeroItems=zeroItems)
    else:
        return  redirect(url_for('login'))

@app.route('/regist')
def regist():
    return render_template('regist.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/post_regist',methods=['POST'])
def post_regist():
    print("有人注册，账号是：",request.form['userName'],'密码是：',request.form['password'])
    user = User(request.form['userName'],request.form['password'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/post_login',methods=['POST'])
def post_login():
    print("有人登陆，账号是：",request.form['userName'],'密码是：',request.form['password'])
    if request.form['password'] == User.query.filter_by(userName=request.form['userName']).first().password:
        print('登陆成功')
        session['userName'] = request.form['userName']
    else:
        return '登录失败'
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('userName',None)
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    if 'userName' in session:
        return 'Welcome '+session['userName']
    else:
        return 'Please login first'



#socket.io设置
@socketio.on('connect',namespace='/ioconnect')
def socketio_connect():
    print("io connected:",request.sid)

@socketio.on('disconnect',namespace='/ioconnect')
def socketio_disconnect():
    print("io disconnected:",request.sid)

@socketio.on('send',namespace='/ioconnect')
def socketio_send(message):
    print("send:",message)
    emit('return',"received!",broadcast=True,namespace='/ioconnect')

@socketio.on('add',namespace='/ioconnect')
def socketio_add(message):
    print("add",message)
    Food.query.filter(Food.name == message).first().num += 1
    db.session.commit()
    now = Food.query.filter(Food.name == message).first()
    emit('update',json.dumps({'name':now.name,'num':now.num}),broadcast=True,namespace='/ioconnect')

@socketio.on('reduce',namespace='/ioconnect')
def socketio_reduce(message):
    print('reduece',message)
    Food.query.filter(Food.name == message).first().num -= 1
    db.session.commit()
    now = Food.query.filter(Food.name == message).first()
    emit('update',json.dumps({'name':now.name,'num':now.num}),broadcast=True,namespace='/ioconnect')



#启动
if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',port=2333)
