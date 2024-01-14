import tkinter as tk
from tkinter import messagebox, font
import mysql.connector
import hashlib
from datetime import datetime
import cv2
import time
from PIL import Image,ImageTk


# 注册函数
def register():
    username = register_entry_username.get()
    password = register_entry_password.get()
    age = register_entry_age.get()

    # 如果小于3岁则报错
    if int(age) < 3:   messagebox.showerror("年龄不符","未满3岁,不能注册游戏")
    else:
        query = f"INSERT INTO Users (username, password, age) VALUES (%s,%s,%s)"
        # 密码使用sha256的哈希算法进行加密，这样即使数据库丢失也可以保证密码的明文无法被破解，以此保证数据的安全。
        values=(username,hashlib.sha256(password.encode('utf-8')).hexdigest(),int(age))
        cursor.execute(query,values)
        make_connect.commit()

        messagebox.showinfo("注册成功", "注册成功！")
    register_entry_username.delete(0, tk.END)
    register_entry_password.delete(0, tk.END)
    register_entry_age.delete(0,tk.END)

# 登录函数
def login():
    username = login_entry_username.get()
    password = login_entry_password.get()
    
    # SQL语句
    query = "SELECT * FROM Users"
    cursor.execute(query)
    users = cursor.fetchall()

    found = False

    for user in users:
        if user[1] == username:
            found = True
            if user[2] == hashlib.sha256(password.encode("utf-8")).hexdigest():
                messagebox.showinfo("登录成功", "登录成功！")
                # 使用global来给全局变量赋值
                global current_user_id
                current_user_id = user[0]
                # 将按钮的状态调整至normal，可以正常点击
                edit_button.config(state="normal")
                info_button.config(state="normal")
                account_button.config(state="normal")
                buy_fund_button.config(state="normal")
                detail_button.config(state="normal")
            else:
                messagebox.showerror("密码错误", "请输入正确密码")
    
    if found == False:  messagebox.showwarning("未找到用户", "未找到该用户,请先注册")
    
    # 清空输入框
    login_entry_username.delete(0, tk.END)
    login_entry_password.delete(0, tk.END)
##用户信息编辑
def editUserInfo():
    edit_window = tk.Toplevel(window)
    edit_window.title("编辑用户信息")
    edit_window.geometry(f"300x220+{(screen_width-300)//2}+{(screen_height-220)//2}")
    window.resizable(False, False)

    # 数据库查询用户信息
    query = "SELECT * FROM Users WHERE userId=%s"
    cursor.execute(query,(current_user_id,))
    user = cursor.fetchone()
    username = user[1]
    address = user[3]
    phonenumber = user[4]

    def updateInfo():
        username = edit_username_entry.get()
        address = edit_address_entry.get()
        phonenumber = edit_phonenumber_entry.get()

        query = "UPDATE Users SET username=%s,address=%s,phone_number=%s WHERE userId=%s"
        values = (username, address, phonenumber, current_user_id)
        cursor.execute(query,values)
        make_connect.commit()

        messagebox.showinfo("成功","修改用户信息成功!")
        edit_window.destroy()

    def updatePwd():
        updatePwd_window = tk.Toplevel(edit_window)
        updatePwd_window.title("修改密码")
        updatePwd_window.geometry(f"150x100+{(screen_width-150)//2}+{(screen_height-100)//2}")

        def newPwdToDB():
            if hashlib.sha256(old_pwd_entry.get().encode('utf-8')).hexdigest() != user[2]:
                messagebox.showerror("密码错误","原始密码输入错误")
            else:
                query = "UPDATE Users SET password=%s where userId=%s"
                cursor.execute(query,(hashlib.sha256(new_pwd_entry.get().encode('utf-8')).hexdigest(),current_user_id))
                make_connect.commit()
                messagebox.showinfo("成功","修改密码成功!")
                updatePwd_window.destroy()
        
        def newPwdCancel():
            updatePwd_window.destroy()

        old_pwd_label = tk.Label(updatePwd_window,text="原始密码:")
        old_pwd_label.place(x=10,y=10,width=50,height=25)
        old_pwd_entry = tk.Entry(updatePwd_window)
        old_pwd_entry.place(x=70,y=10,width=70,height=25)

        new_pwd_label = tk.Label(updatePwd_window,text="新密码:")
        new_pwd_label.place(x=10,y=40,width=40,height=25)
        new_pwd_entry = tk.Entry(updatePwd_window)
        new_pwd_entry.place(x=70,y=40,width=70,height=25)

        confirm_pwd_button = tk.Button(updatePwd_window, text="确认", command=newPwdToDB)
        confirm_pwd_button.place(x=20,y=70,width=40,height=20)

        cancel_pwd_button = tk.Button(updatePwd_window, text="取消", command=newPwdCancel)
        cancel_pwd_button.place(x=90,y=70,width=40,height=20)

        updatePwd_window.mainloop()

    
    def cancel():
        edit_window.destroy()

    edit_username_label = tk.Label(edit_window, text="用户名:")
    edit_username_label.place(x=20,y=20,width=60,height=30)
    edit_username_entry = tk.Entry(edit_window)
    edit_username_entry.place(x=100,y=20,width=180,height=30)
    edit_username_entry.insert(tk.END,username)

    edit_address_label = tk.Label(edit_window, text="地址:")
    edit_address_label.place(x=20,y=70,width=60,height=30)
    edit_address_entry = tk.Entry(edit_window)
    edit_address_entry.place(x=100,y=70,width=180,height=30)
    if address is not None:   edit_address_entry.insert(tk.END,address)

    edit_phonenumber_label = tk.Label(edit_window, text="电话号:")
    edit_phonenumber_label.place(x=20,y=120,width=60,height=30)
    edit_phonenumber_entry = tk.Entry(edit_window)
    edit_phonenumber_entry.place(x=100,y=120,width=180,height=30)
    if phonenumber is not None:   edit_phonenumber_entry.insert(tk.END,phonenumber)

    confirm_button = tk.Button(edit_window, text="确认", command=updateInfo)
    confirm_button.place(x=20,y=170,width=80,height=30)

    changePwd_button = tk.Button(edit_window, text="修改密码",command=updatePwd)
    changePwd_button.place(x=110,y=170,width=80,height=30)

    cancel_button = tk.Button(edit_window, text="取消",command=cancel)
    cancel_button.place(x=200,y=170,width=80,height=30)

    edit_window.mainloop()

# 菜单 (Dodgeball介绍)
def Menu():
    Menu_window = tk.Toplevel(window)
    Menu_window.title("Dodgeball Introduction")
    Menu_window.geometry(f"1280x720")
    Menu_window.resizable(False,False)
    Menu_window.mainloop()

##功能1（左右躲避）
def leftAndRight():
   leftAndRight_window = tk.Toplevel(window)
   leftAndRight_window.title("Dodge left and right")
   leftAndRight_window.geometry(f"1280x720")  
   leftAndRight_window.resizable(False,False)
   leftAndRight_window.mainloop()

##功能2（前后躲避）
def fontAndBack():
   fontAndBack_window = tk.Toplevel(window)
   fontAndBack_window.title("Dodge back and forth")
   fontAndBack_window.geometry(f"1280x720")  
   fontAndBack_window.resizable(False,False)
   fontAndBack_window.mainloop()


##总积分显示
def score():
    score_window = tk.Toplevel(window)
    score_window.title("总积分")
    score_window.geometry(f"800x500+{(screen_width-800)//2}+{(screen_height-500)//2}")
    score_window.resizable(False,False)

##视频背景播放与Camera人像捕捉
def update_video_background():
    success, frame = video_cap.read()
    if success:
        frame = cv2.resize(frame, (1280, 720))  # 调整视频帧的大小以适应窗口
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 将颜色通道从BGR转换为RGB

        # 使用Pillow库中的Image.fromarray创建Image对象
        image = Image.fromarray(frame)
        # 使用ImageTk.PhotoImage创建Tkinter PhotoImage对象
        img = ImageTk.PhotoImage(image=image)

        # 更新Label的图像
        label_video.config(image=img)
        label_video.image = img
    if not success:
        # 重新设置视频捕获的位置到开头
        video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        

    
    window.after(10, update_video_background)


if __name__ == "__main__":
    # 创建登录界面
    window = tk.Tk()
    window.title("Dodgeball Game")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"1280x720")
    window.resizable(False,False)
    label_video = tk.Label(window)
    label_video.pack()
    

    # 连接数据库
    make_connect=mysql.connector.connect(
        host="localhost",
        user="root",
        password="555125",
        database="final"
    )

    cursor = make_connect.cursor()
    # 打开视频文件
    video_cap = cv2.VideoCapture('D:/Program Files/Desktop/hyw.mp4')

    # 创建一个Label来显示视频帧
    label_video = tk.Label(window)
    label_video.pack()

    # 开始更新视频背景
    update_video_background()


    # 注册
    register_frame = tk.Frame(window,borderwidth=1,relief="solid")
    register_frame.place(x=0,y=0,width=300,height=360)
    register_font=font.Font(size=24,weight="bold")
    register_label = tk.Label(register_frame,text="注册",font=register_font)
    register_label.place(x=100,y=20,width=120,height=50)
    register_label_username = tk.Label(register_frame, text="用户名:")
    register_label_username.place(x=40,y=80,width=60,height=30)
    register_entry_username = tk.Entry(register_frame)
    register_entry_username.place(x=110,y=80,width=120,height=30)

    register_label_password = tk.Label(register_frame, text="密码:")
    register_label_password.place(x=40,y=140,width=60,height=30)
    register_entry_password = tk.Entry(register_frame, show="*")
    register_entry_password.place(x=110,y=140,width=120,height=30)

    register_label_age = tk.Label(register_frame, text="年龄:")
    register_label_age.place(x=40,y=200,width=60,height=30)
    register_entry_age = tk.Entry(register_frame)
    register_entry_age.place(x=110,y=200,width=120,height=30)

    button_register = tk.Button(register_frame, text="注册", command=register)
    button_register.place(x=110,y=270,width=120,height=30)


    # 登录
    login_frame = tk.Frame(window,borderwidth=1,relief="solid")
    login_frame.place(x=0,y=360,width=300,height=360)
    login_font=font.Font(size=24,weight="bold")
    login_label = tk.Label(login_frame,text="登录",font=login_font)
    login_label.place(x=100,y=50,width=120,height=50)
    login_label_username = tk.Label(login_frame, text="用户名:")
    login_label_username.place(x=40,y=120,width=80,height=40)
    login_entry_username = tk.Entry(login_frame)
    login_entry_username.place(x=110,y=120,width=120,height=30)

    login_label_password = tk.Label(login_frame, text="密码:")
    login_label_password.place(x=40,y=180,width=80,height=40)
    login_entry_password = tk.Entry(login_frame, show="*")
    login_entry_password.place(x=110,y=180,width=120,height=30)

    button_login = tk.Button(login_frame, text="登录", command=login)
    button_login.place(x=110,y=250,width=120,height=30)

    # 右侧五个功能按钮
    edit_button = tk.Button(window, text="修改个人信息",state="disabled",command=editUserInfo)
    edit_button.place(x=1020,y=50,width=220,height=50)

    info_button = tk.Button(window, text="游戏介绍",state="disabled", command=Menu)
    info_button.place(x=1020,y=180,width=220,height=50)

    account_button = tk.Button(window, text="左右躲避",state="disabled", command=leftAndRight)
    account_button.place(x=1020,y=310,width=220,height=50)

    buy_fund_button = tk.Button(window, text="前后躲避",state="disabled", command=fontAndBack)
    buy_fund_button.place(x=1020, y=440, width=220, height=50)

    detail_button = tk.Button(window, text="总得分显示",state="disabled", command=score)
    detail_button.place(x=1020,y=570,width=220,height=50)

    # 各种全局变量
    current_user_id=-1

    # 运行主循环
    window.mainloop()
    # 关闭视频文件
    video_cap.release()
    cursor.close()
    make_connect.close()