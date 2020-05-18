# coding:utf-8
import Tkinter as tk
import tkMessageBox

# from tkinter import messagebox
root = tk.Tk()

root.title("京东闪付 v1.0")
root.geometry("700x800")
lable = tk.Label(root, text="输入提取到的Cookie：", font=("Arial", 15), width=20, height=5, bg="green")
lable.pack()

info = tk.StringVar()  # 有（）
entry = tk.Entry(root, text=info)
info.set("defalt")

text = tk.Text(root, height=5)


def button_click():
    tmp = entry.get()
    print(123)
    text.insert("end", tmp + "\n")
    # entry.insert(0, "开始123")  entry.insert(2.3, "第二行的第三位")


button = tk.Button(root, text="开始", width=5, height=2, bg="red", command=button_click)  # 没有（）
entry.pack()
button.pack()
text.pack()
############################第二天##############################
var1 = tk.StringVar()
var2 = tk.StringVar()


def button2_clik():
    var2.set(listbox.get(listbox.curselection()))  # listbox.curselection() 已选中的位置
    text2.insert("end", listbox.get(listbox.curselection()) + "\n")


listbox = tk.Listbox(root, listvariable=var1)
var1.set(("123", "456", "789"))
listbox.pack(side=tk.LEFT)

button2 = tk.Button(root, text="增加", bg="red", font=(15), command=button2_clik)
button2.pack(side=tk.LEFT)

lable2 = tk.Label(root, width=10, height=8, textvariable=var2, bg="#1E90FF")
lable2.pack(side=tk.LEFT)

text2 = tk.Text(root, width=15, height=10)
text2.pack(side=tk.LEFT)

# 滚动条
bar = tk.Scrollbar(root, command=text2.yview)
bar.pack(side=tk.LEFT, fill=tk.Y)
var3 = tk.StringVar()


def radio_button_click():
    lable3.config(text="you have choice %s" % var3.get())


r1 = tk.Radiobutton(root, text="Options A", command=radio_button_click, variable=var3, value="A")
r1.pack()
r2 = tk.Radiobutton(root, text="Options B", command=radio_button_click, variable=var3, value="B")
r2.pack()
r3 = tk.Radiobutton(root, text="Options C", command=radio_button_click, variable=var3, value="C")
r3.pack()

lable3 = tk.Label(root, width=15, height=2, text="empty")
lable3.pack()


############################第三天 拖动条##############################
def seleted(value):
    lable.config(text="scale value:" + value)


scale = tk.Scale(root, label="scale title", orient=tk.HORIZONTAL, from_=2, to=12, length=200, showvalue=1,
                 tickinterval=2, resolution=0.01, command=seleted)
#  label:拖动条标题  orient：拖动条方向（横向，竖向） from_to：起始值—结束值  length：拖动条长度，单位pix  showvalue：显示当前值，0不显示，1显示
#################### tickinterval：拖动跨度单位  resolution：精确值  command：没次拖动触发的函数（传入当前位置）
scale.set(6)  # 设置默认值
scale.pack()

############################第四天 复选框，画布##############################
int_var1 = tk.IntVar()
int_var2 = tk.IntVar()


def print_seleced():
    lable.config(text="you choice Python!")


c1 = tk.Checkbutton(root, text="Python", onvalue=1, offvalue=0, variable=int_var1, command=print_seleced)
c2 = tk.Checkbutton(root, text="JAVA", onvalue=1, offvalue=0, variable=int_var2)
c1.pack()
c2.pack()

canvas = tk.Canvas(root, bg="#F8F8FF", height=100, width=200)  # 画布
image_file = tk.PhotoImage(file="07.gif")
image = canvas.create_image(10, 10, anchor="nw", image=image_file)  # 放照片：anchor锚点对应图片位置，nw左上角，center中间
line = canvas.create_line(5, 5, 30, 30)  # 画线： 起点 XY坐标，终点XY坐标
oval = canvas.create_oval(5, 5, 30, 30, fill="red")  # 画圆：
arc = canvas.create_arc(40, 40, 80, 80, start=0, extent=160, fill="blue")  # 画扇形：start起始角度，extent结束角度
rect = canvas.create_rectangle(100, 40, 100 + 20, 40 + 20, fill="yellow")  # 画四边形
canvas.pack()


def move_rect():
    canvas.move(rect, 0, 2)


def back_rect():
    canvas.move(rect, 0, -2)


button_canvas = tk.Button(root, text="move", command=move_rect)
button_canvas.pack()
button_canvas2 = tk.Button(root, text="back", command=back_rect)
button_canvas2.pack()


############################第五天 1.菜单按钮 2.Frame框架 3.弹出框##############################
def menu_click():
    lable.config(text="you have click menu!")


menubar = tk.Menu(root)

file_mebu = tk.Menu(menubar, tearoff=0)  # tearoff=1 菜单栏可以拖出来
menubar.add_cascade(label="File", menu=file_mebu)  # 增加菜单按钮
file_mebu.add_command(label="New", command=menu_click)  # 增加下拉菜单命令
file_mebu.add_command(label="Open", command=menu_click)
file_mebu.add_command(label="Save", command=menu_click)
file_mebu.add_separator()  # 分割线
file_mebu.add_command(label="Exit", command=root.quit)

edit_mebu = tk.Menu(menubar, tearoff=1)
menubar.add_cascade(label="Edit", menu=edit_mebu)  # 增加菜单按钮
edit_mebu.add_command(label="Copy", command=menu_click)  # 增加下拉菜单命令
edit_mebu.add_command(label="Cut", command=menu_click)
edit_mebu.add_command(label="Plaster", command=menu_click)

submenu = tk.Menu(file_mebu)
file_mebu.add_cascade(label="Import", menu=submenu, underline=1)
submenu.add_command(label="submenu", command=menu_click)
root.config(menu=menubar)
# frame框架
frame = tk.Frame(root)
frame.pack(side="left")


# 弹出框
def show_message():
    tkMessageBox.showinfo(title="my title", message="info!!!")
    tkMessageBox.showwarning(title="my title", message="warn!!!")
    tkMessageBox.showerror(title="my title", message="Error!!!")


button_messagebox = tk.Button(frame, text="show messagebox", command=show_message)
button_messagebox.pack(side="left")


def show_ask():
    print(tkMessageBox.askquestion(title="my title", message="ask question!!!"))  # return yes/no
    print(tkMessageBox.askyesno(title="my title", message="askyesno!!!"))  # return True/False
    print(tkMessageBox.askretrycancel(title="my title", message="askretrycancel!!!"))  # return True/False
    print(tkMessageBox.askokcancel(title="my title", message="askokcancel!!!"))  # return True/False
    print(tkMessageBox.askyesnocancel(title="my title", message="askyesnocancel!!!"))  # return True/False/None


button_ask = tk.Button(frame, text="show ask", command=show_ask)
button_ask.pack(side="left")


def close_window():
    exit_result = tkMessageBox.askokcancel(title="确认退出？", message="确认要关闭吗？")
    if exit_result:
        root.quit()
    else:
        return


root.protocol("WM_DELETE_WINDOW", close_window)
root.mainloop()
