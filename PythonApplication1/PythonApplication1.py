from ctypes.wintypes import FILETIME
from doctest import master
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import matplotlib.pyplot as plt
import tkinter.filedialog as fd
import numpy as np
from matplotlib.animation import FuncAnimation
import math
import time

G = 6.674*10**(-11)

daysec = 60*60
dt = daysec

class Points:
    def __init__(self, x=0.0, y = 0.0):
        self.x = x
        self.y = y
   
    #def __repr__(self):
    #    return f"Points({self.x}, {self.y})"
    
    def __str__(self):
        return f"{self.x}x + {self.y}y"
    
    def __add__(self, other):
        return Points(
            self.x + other.x,
            self.y + other.y
        )
    def __sub__(self, other):
        return Points(
            self.x - other.x,
            self.y - other.y
        )

    def __mul__(self, other):
        if isinstance(other, Points):
            return(self.x * other.x+self.y * other.y)
        elif isinstance(other, (int, float )): 
            return Points(self.x * other,self.y * other)
        else:
            raise TypeError("Operand must be Points or number")

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Points(self.x / other,self.y / other)
        else:
            raise TypeError("Operand must be int or float")

    def get_module(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def get_scalar(self, other):
        return math.sqrt((self.x - other[0]) ** 2 + (self.y - other[1]) ** 2)
   
    def normalize(self):
        return Points(self.x /self.get_module(), self.y /self.get_module())

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError("There are only three elements in the vector")

class Planet:
    def __init__(self, position:Points, v: Points, m: float):
        self.position = position
        self.v = v
        self.a = Points()

        self.positionPrev = Points(position.x,position.y)
        self.vPrev = Points()
        self.aPrev = Points()

        self.m = m
    
    def __str__(self) -> str:
        return f"{self.position.x};{self.position.y};{self.v.x};{self.v.x};{self.m}"

   
    
class config_planet():
    def __init__(self,mas:list,count:int):
        self.root = tk.Tk()
        self.root.geometry("740x300")
        self.count_of_planet = 0
        self.array_of_planet = mas
        self.array_of_labels = []
        self.array_of_entrys = []
        self.button_append = tk.Button(master=self.root,text="append",command=self.append_planet)
        self.button_append.grid(row=0,column=0)
        self.button_append = tk.Button(master=self.root,text="delete",command=self.delete_planet)
        self.button_append.grid(row=0,column=1)

        if (len(self.array_of_planet)>0):
            for i in range(len(self.array_of_planet)):
                self.array_of_entrys.append([])
                self.array_of_labels.append([])

                entry=tk.Entry(master=self.root,textvariable=tk.StringVar(self.root,value=str(self.array_of_planet[i].position.x)))
                entry.grid(row=self.count_of_planet+1,column=1)
                self.array_of_entrys[-1].append(entry)
                label = tk.Label(master=self.root,text="x")
                label.grid(row=self.count_of_planet+1,column=0)
                self.array_of_labels[-1].append(label)
                entry=tk.Entry(master=self.root,textvariable=tk.StringVar(self.root,value=str(self.array_of_planet[i].position.y)))
                entry.grid(row=self.count_of_planet+1,column=3)
                self.array_of_entrys[-1].append(entry)
                label=tk.Label(master=self.root,text="y")
                label.grid(row=self.count_of_planet+1,column=2)
                self.array_of_labels[-1].append(label)
                entry=tk.Entry(master=self.root,textvariable=tk.StringVar(self.root,value=str(self.array_of_planet[i].v.x)))
                entry.grid(row=self.count_of_planet+1,column=5)
                self.array_of_entrys[-1].append(entry)
                label=tk.Label(master=self.root,text="Vx")
                label.grid(row=self.count_of_planet+1,column=4)
                self.array_of_labels[-1].append(label)
                entry = tk.Entry(master=self.root,textvariable=tk.StringVar(self.root,value=str(self.array_of_planet[i].v.y)))
                entry.grid(row=self.count_of_planet+1,column=7)
                self.array_of_entrys[-1].append(entry)
                label = tk.Label(master=self.root,text="Vy")
                label.grid(row=self.count_of_planet+1,column=6)
                self.array_of_labels[-1].append(label)
                entry = tk.Entry(master=self.root,textvariable=tk.StringVar(self.root,value=str(self.array_of_planet[i].m)))
                entry.grid(row=self.count_of_planet+1,column=9)
                self.array_of_entrys[-1].append(entry)
                label = tk.Label(master=self.root,text="m")
                label.grid(row=self.count_of_planet+1,column=8)
                self.array_of_labels[-1].append(label)
                self.count_of_planet+=1
        else:
            self.array_of_planet.append(Planet(Points(0,0),Points(0,0),1.2166e30))
            self.array_of_entrys.append([])
            self.array_of_labels.append([])
            entry=tk.Entry(master=self.root,textvariable=tk.StringVar(self.root,value=str(self.array_of_planet[-1].position.x)))
            entry.grid(row=self.count_of_planet+1,column=1)
            self.array_of_entrys[-1].append(entry)
            label = tk.Label(master=self.root,text="x")
            label.grid(row=self.count_of_planet+1,column=0)
            self.array_of_labels[-1].append(label)
            entry=tk.Entry(master=self.root,textvariable=tk.StringVar(self.root,value=str(self.array_of_planet[-1].position.y)))
            entry.grid(row=self.count_of_planet+1,column=3)
            self.array_of_entrys[-1].append(entry)
            label=tk.Label(master=self.root,text="y")
            label.grid(row=self.count_of_planet+1,column=2)
            self.array_of_labels[-1].append(label)
            entry=tk.Entry(master=self.root,textvariable=tk.StringVar(self.root,value=str(self.array_of_planet[-1].v.x)))
            entry.grid(row=self.count_of_planet+1,column=5)
            self.array_of_entrys[-1].append(entry)
            label=tk.Label(master=self.root,text="Vx")
            label.grid(row=self.count_of_planet+1,column=4)
            self.array_of_labels[-1].append(label)
            entry = tk.Entry(master=self.root,textvariable=tk.StringVar(self.root,value=str(self.array_of_planet[-1].v.y)))
            entry.grid(row=self.count_of_planet+1,column=7)
            self.array_of_entrys[-1].append(entry)
            label = tk.Label(master=self.root,text="Vy")
            label.grid(row=self.count_of_planet+1,column=6)
            self.array_of_labels[-1].append(label)
            entry = tk.Entry(master=self.root,textvariable=tk.StringVar(self.root,value=str(self.array_of_planet[-1].m)))
            entry.grid(row=self.count_of_planet+1,column=9)
            self.array_of_entrys[-1].append(entry)
            label = tk.Label(master=self.root,text="m")
            label.grid(row=self.count_of_planet+1,column=8)
            self.array_of_labels[-1].append(label)
            self.count_of_planet+=1
            for i in range(count-1):
                self.append_planet()

        def on_closing():
            for i in range(len(self.array_of_entrys)):
                self.array_of_planet[i].position.x=float(self.array_of_entrys[i][0].get())
                self.array_of_planet[i].position.y=float(self.array_of_entrys[i][1].get())
                self.array_of_planet[i].v.x=float(self.array_of_entrys[i][2].get())
                self.array_of_planet[i].v.y=float(self.array_of_entrys[i][3].get())
                self.array_of_planet[i].m=float(self.array_of_entrys[i][4].get())
            

            self.root.destroy()


        self.root.protocol("WM_DELETE_WINDOW", on_closing)

        self.root.mainloop()
    def delete_planet(self):
        if self.count_of_planet==1:
            return
        for i in range(len(self.array_of_entrys[-1])):
            self.array_of_entrys[-1][i].destroy()
        for i in range(len(self.array_of_labels[-1])):
            self.array_of_labels[-1][i].destroy()
        self.array_of_planet.pop(-1)
        self.array_of_entrys.pop(-1)
        self.array_of_labels.pop(-1)
        self.count_of_planet-=1
    
    
    def append_planet(self):
        self.array_of_planet.append(Planet(Points(self.array_of_planet[-1].position.x + 149500000000,0),Points(0,0),(self.count_of_planet)*6.083e24))
        self.array_of_entrys.append([])
        self.array_of_labels.append([])
       
        entry=tk.Entry(master=self.root,textvariable=tk.StringVar(self.root,value=str(self.array_of_planet[-1].position.x)))
        entry.grid(row=self.count_of_planet+1,column=1)
        self.array_of_entrys[-1].append(entry)
        
        label = tk.Label(master=self.root,text="x")
        label.grid(row=self.count_of_planet+1,column=self.count_of_planet+1)
        self.array_of_labels[-1].append(label)
        
        entry=tk.Entry(master=self.root,textvariable=tk.StringVar(self.root,value=str(self.array_of_planet[-1].position.y)))
        entry.grid(row=self.count_of_planet+1,column=self.count_of_planet+1)
        self.array_of_entrys[-1].append(entry)
        
        label=tk.Label(master=self.root,text="y")
        label.grid(row=self.count_of_planet+1,column=2)
        self.array_of_labels[-1].append(label)
        
        #entry=tk.Entry(master=self.root,textvariable=tk.StringVar(self.root,value=str(self.array_of_planet[-1].v.x)))
        #entry.grid(row=self.count_of_planet+1,column=5)
        #self.array_of_entrys[-1].append(entry)
        #
        #label=tk.Label(master=self.root,text="Vx")
        #label.grid(row=self.count_of_planet+1,column=4)
        #self.array_of_labels[-1].append(label)
        #
        #entry = tk.Entry(master=self.root,textvariable=tk.StringVar(self.root,value=str(self.array_of_planet[-1].v.y)))
        #entry.grid(row=self.count_of_planet+1,column=7)
        #self.array_of_entrys[-1].append(entry)
        #
        #label = tk.Label(master=self.root,text="Vy")
        #label.grid(row=self.count_of_planet+1,column=6)
        #self.array_of_labels[-1].append(label)
        #
        #entry = tk.Entry(master=self.root,textvariable=tk.StringVar(self.root,value=str(self.array_of_planet[-1].m)))
        #entry.grid(row=self.count_of_planet+1,column=9)
        #self.array_of_entrys[-1].append(entry)
        #
        #label = tk.Label(master=self.root,text="m")
        #label.grid(row=self.count_of_planet+1,column=8)
        #self.array_of_labels[-1].append(label)
        
        self.count_of_planet+=1


def calculateAcceleration(planet, second):
        r = planet.position.get_scalar(second.position)
        a = planet.m * G / (r ** 2)
        return Points(a * (planet.position.x - second.position.x) / r,
                            a * (planet.position.y - second.position.y) / r)

class System:
    def __init__(self, size: int,list_of_planet, scheme:int):
        self.planets = list_of_planet
        self.size = size
        
        self.scheme = scheme

    def add_planet(self, planet):
        self.planets.append(planet)
        self.size += 1



    def acceleration(self):
        for planet in self.planets:
            for second in self.planets:
                if planet == second:
                    continue
        
                r = planet.position.get_scalar(second.position)
                force =  G * second.m / (r**3)

                planet.a.x +=  (planet.position[0]-second.position[0])*force
                planet.a.y +=  (planet.position[1]-second.position[1])*force
# F дать синусоидальный закон гравитационной постоянной
# Амплитура G+амлп*sin(время)

    def moving(self):
        acceleration = Points()
        positionPrev=Points()
        abc=Points()
        for first in self.planets:
            for second in self.planets:
                if first == second:
                    continue
                acceleration +=calculateAcceleration(second, first)
            if (self.scheme == 0): #�����

                first.position.x = first.position.x + first.v.x*dt
                first.position.y = first.position.y + first.v.y*dt
                first.v.x = first.v.x+acceleration.x*dt
                first.v.y = first.v.y+acceleration.y*dt
                
                
                print(first.position.x, first.position.y)
            elif (self.scheme == 1): #����� ????????????????��� ������ �� ��������������
                if first.positionPrev.x==first.position.x and first.positionPrev.y==first.position.y:
               
                    first.position.x = first.position.x + first.v.x*dt
                    first.position.y = first.position.y + first.v.y*dt
                    first.v.x = first.v.x+acceleration.x*dt
                    first.v.y = first.v.y+acceleration.y*dt

                    first.positionPrev = Points(first.position.x, first.position.y)
                    first.vPrev = Points(first.v.x, first.v.y)
                    first.aPrev = Points(acceleration.x,acceleration.y)
                else:
                    positionPrev = Points(first.position.x,first.position.y)
                    vPrev = Points(first.vPrev.x,first.vPrev.y)
                    aPrev = Points(first.aPrev.x,first.aPrev.y)

                    first.position.x = 2*first.position[0] - first.positionPrev[0] + acceleration[0]*dt
                    first.position.y = 2*first.position[1] - first.positionPrev[1] + acceleration[1]*dt
                    first.v.x = (first.position[0]-first.positionPrev[0])/(2*dt)
                    first.v.y = (first.position[1]-first.positionPrev[1])/(2*dt)
            
                    first.positionPrev = Points(positionPrev.x,positionPrev.y)
                    first.vPrev = Points(vPrev.x,vPrev.y)
                    first.aPrev = Points(aPrev.x,aPrev.y)
                
                print(first.position.x, first.position.y)
                print(first.positionPrev.x, first.positionPrev.y)
            elif (self.scheme == 2): #��
                first.v.x = first.v[0]+first.a[0]*dt
                first.v.y = first.v[1]+first.a[1]*dt
                first.position.x = first.position[0] + first.v[0]*dt
                first.position.y = first.position[1] + first.v[1]*dt

            elif (self.scheme == 3): #�����
                positionPrev = Points(first.position.x,first.position.y)
                vPrev = Points(first.v.x,first.v.y)
                aPrev = Points(acceleration.x,acceleration.y)

                first.position.x = first.position[0] + (first.v[0]*dt)-(4*acceleration[0]-first.aPrev[0])*(dt**2)/6
                first.position.y = first.position[1] + (first.v[1]*dt)-(4*acceleration[1]-first.aPrev[1])*(dt**2)/6
                
                usk=Points()
                for second in self.planets:
                    if first == second:
                        continue
                    usk +=calculateAcceleration(second, first)
                
                first.v.x = first.v[0]+(2*usk.x + 5*acceleration.x - first.aPrev.x)*(dt)/6
                first.v.y = first.v[1]+(2*usk.y + 5*acceleration.y - first.aPrev.y)*(dt)/6

                first.positionPrev = Points(positionPrev.x,positionPrev.y)
                first.vPrev = Points(vPrev.x,vPrev.y)
                first.aPrev = Points(aPrev.x,aPrev.y)
            
                print("bim",first.position.x, first.position.y)

            elif (self.scheme == 4): #метод рунге
                pointA= Points(acceleration.x, acceleration.y)
                pointV= Points(first.v.x, first.v.y)

                k1vx=k2vx=k3vx=k4vx=pointA.x

                k1x=pointV.x
                k2x=pointV.x+k1vx/2
                k3x=pointV.x+k2vx/2
                k4x=pointV.x+k3x


                k1vy=k2vy=k3vy=k4vy=pointA.y

                k1y=pointV.y
                k2y=pointV.y+k1vy/2
                k3y=pointV.y+k2vy/2
                k4y=pointV.y+k3y


                first.position.x = first.position.x + (k1x+2*k2x+2*k3x+k4x)*dt/6
                first.position.y = first.position.y + (k1y+2*k2y+2*k3y+k4y)*dt/6

                first.v.x = first.v.x + (k1vx + 2*k2vx + 2*k3vx + k4vx)*dt/6
                first.v.y = first.v.y + (k1vy + 2*k2vy + 2*k3vy + k4vy)*dt/6

                
            else:
                pass

    def centerMass(self):
        cm = Points()
        sum_= sumx_ = sumy_ = 0
        arr_pl = []
        for planet in self.planets:
            sum_+= planet.m
            sumx_ += planet.position[0]*planet.m
            sumy_ += planet.position[1]*planet.m   
        cm.x =sumx_/ sum_
        cm.y =sumy_/ sum_
        return cm

    def totalEnergy(self): #total mechanical energy=gravitational potential energy+kinetic energy 
        P=0
        for first in self.planets:
            for second in self.planets:
                if first == second:
                    continue
                r = first.position.get_scalar(second.position)
                P += first.m*second.m/(r)
        P = -P*G/2

        return P
    #-GMm/2r

    def potentialEnergy(self): #-GMm/r
        P=0
        for first in self.planets:
            for second in self.planets:
                if first == second:
                    continue
                r = first.position.get_scalar(second.position)
                P += first.m*second.m/(r)
        P = -P*G
        return P

    def kineticEnergy(self): #GMm/2r = (M+m)v**2/2
        P=0
        for first in self.planets:
            for second in self.planets:
                if first == second:
                    continue
                r = first.position.get_scalar(second.position)
                P += first.m*second.m/(r)
        P = P*G/2
        return P
    def setscheme(self, newscheme:int):
        self.scheme = newscheme


class programm():
    def __init__(self):
        self.list_of_planet=[]
        self.root=tk.Tk()
        self.root.geometry("870x505")
        self.root.resizable(width=0, height=0)
        self.fig=plt.figure()

        self.ax = plt.axes(xlim=(-50,150), ylim=(-50, 150))
        #self.ax = plt.axes()
        #self.line, = self.ax.plot([], [], lw=3)
        #self.line2, = self.ax.plot([], [], lw=3)
        #self.x=[[],[]]
        #self.y=[[],[]]
        self.max_x=0
        self.max_y=0
        self.delitel_x=1.0
        self.delitel_y=1.0

        #self.canv=FigureCanvasTkAgg(self.fig,master=self.root)
        #self.canv.get_tk_widget().grid(rowspan=25,column=1)
        self.canv=tk.Canvas(master=self.root,width=500,height=500,bg="white")
        self.canv.grid(rowspan=25,column=1)

        self.current_number_system=0
        self.varNS = tk.IntVar()
        self.varNS.set(0)
        self.sec = tk.Radiobutton(text="Seconds",command=self.changeNS,variable=self.varNS,value=0)
        self.sec.grid(row=4,column=2,padx=30)

        self.day = tk.Radiobutton(text="Days",command=self.change,variable=self.varNS,value=1)
        self.day.grid(row=4,column=3,padx=20)

        self.month = tk.Radiobutton(text="Months",command=self.changeNS,variable=self.varNS,value=2)
        self.month.grid(row=5,column=2,padx=30)

        self.year = tk.Radiobutton(text="Years",command=self.changeNS,variable=self.varNS,value=3)
        self.year.grid(row=5,column=3,padx=20)


        self.configurate_planet = tk.Button(text="configurate planet",command=self.configurate_planet)
        self.configurate_planet.grid(row=7,column=2,columnspan=2,padx=100)

        #�����
        self.label_step_by_time = tk.Label(text="Step by time")
        self.label_step_by_time.grid(row=2, column=2)

        self.entry_step_by_time = tk.Entry(textvariable=tk.StringVar(self.root,value='3600'))
        self.entry_step_by_time.grid(row=3,column=2)

        self.label_time = tk.Label(text="Time",anchor="e")
        self.label_time.grid(row=2, column=3)

        self.entry_time = tk.Entry(textvariable=tk.StringVar(self.root,value='360000'))
        self.entry_time.grid(row=3,column=3)
        self.cur_time=0.0


        #�����
        self.current_schem=0
        self.var = tk.IntVar()
        self.var.set(0)
        self.eiler = tk.Radiobutton(text="Scheme Eiler",command=self.change,variable=self.var,value=0)
        self.eiler.grid(row=9,column=2,padx=30)

        self.veler = tk.Radiobutton(text="Scheme Veler",command=self.change,variable=self.var,value=1)
        self.veler.grid(row=9,column=3,padx=30)

        self.eiler_krank = tk.Radiobutton(text="Scheme Eiler-Krank",command=self.change,variable=self.var,value=2)
        self.eiler_krank.grid(row=10,column=2,padx=20)

        self.biman = tk.Radiobutton(text="Scheme Biman",command=self.change,variable=self.var,value=3)
        self.biman.grid(row=10,column=3,padx=20)

        self.biman = tk.Radiobutton(text="Scheme Runge-Kutta",command=self.change,variable=self.var,value=4)
        self.biman.grid(row=8,column=2,padx=20)

        #save and load
        self.save_button = tk.Button(text="save",command=self.save)
        self.save_button.grid(row=20,column=2)
        self.load_button = tk.Button(text="load",command=self.load)
        self.load_button.grid(row=20,column=3)

        
        self.system_of_planet=System(len(self.list_of_planet),self.list_of_planet,self.current_schem)


        #build
        self.build_button = tk.Button(text="run",command=self.buildv2)
        self.build_button.grid(row=18,column=2)

        #stop
        self.build_button = tk.Button(text="stop",command=self.stop_button)
        self.build_button.grid(row=18,column=3)

        #energy
        self.label_energy = tk.Label(text="Energy",anchor="e")
        self.label_energy.grid(row=11,column=2)
        
        self.entry_energy = tk.Text(self.root, state=tk.DISABLED, width=17, height=1)
        self.entry_energy.grid(row=12,column=2)
        self.cur_energy=0.0

        #potential energy
        self.label_pEnergy = tk.Label(text="Potential energy",anchor="e")
        self.label_pEnergy.grid(row=13,column=2)
        
        self.entry_pEnergy = tk.Text(self.root, state=tk.DISABLED, width=17, height=1)
        self.entry_pEnergy.grid(row=14,column=2)
        self.cur_pEnergy=0.0

        #kinetic energy
        self.label_kEnergy = tk.Label(text="Kinetic energy",anchor="e")
        self.label_kEnergy.grid(row=15,column=2)
        
        self.entry_kEnergy = tk.Text(self.root, state=tk.DISABLED, width=17, height=1)
        self.entry_kEnergy.grid(row=16,column=2)
        self.cur_kEnergy=0.0
        #CM
        self.label_cm = tk.Label(text="Center Mass",anchor="e")
        self.label_cm.grid(row=11,column=3)

        #text1=Text(root,height=7,width=7,font='Arial 14',wrap=WORD)
        #text1.insert(1.0,'Добавим Текст\n\ в начало 1-й строки')

        self.entry_cmx = tk.Text(self.root, state=tk.DISABLED, width=15, height=1)
        self.entry_cmx.grid(row=12,column=3)
        #self.entry_cmx.insert(1.0, '0')
        self.entry_cmy = tk.Text(self.root, state=tk.DISABLED, width=15, height=1)
        #self.entry_cmy.insert(1.0, '0')
        self.entry_cmy.grid(row=13,column=3)
        self.cur_cmx=self.cur_cmy=0.0

        self.root.mainloop()

    def change(self):
        self.current_schem=self.var.get()

    def changeNS(self):
        self.current_number_system=self.varNS.get()

    def configurate_planet(self):
        a=config_planet(self.list_of_planet,2)
        self.system_of_planet = System(len(self.list_of_planet),self.list_of_planet,self.current_schem)
        
        #dt=float(self.entry_step_by_time.get())

    def save(self):
        #directory = fd.askdirectory(title="Open directory", initialdir="/")
        #if directory:
        #    print(directory)
        filetypes = (("Text file", "*.txt"),)
        name=fd.asksaveasfile(title="Save file",mode='w',defaultextension=".txt",filetypes=filetypes)
        if name:
            name.write(str(self.var.get())+'\n')
            for i in self.list_of_planet:
                name.write(str(i)+'\n')
            name.close

    def load(self):
        filetypes = (("Text file", "*.txt"),)
        filename = fd.askopenfilename(title="Open file", initialdir="/",
                                      filetypes=filetypes)
        if filename:
            f=open(filename,'r')
            a=f.read().split()
            try:
                self.var=int(a[0].get())
            except:
                pass

            for i in range(1,len(a)):
                try:
                    k=a[i].split(";")
                    self.list_of_planet.append(Planet(Points(int(k[0]),int(k[1])),Points(int(k[2]),int(k[3])),int(k[4])))
                except:
                    continue
    
    

    def create_planet(self,planet,number_of_planet):
        #return self.canv.create_oval((500/len(self.system_of_planet.planets))*number_of_planet+planet.position[0]/1000000000-5, (500/len(self.system_of_planet.planets))*number_of_planet+planet.position[1]/1000000000-5, (500/len(self.system_of_planet.planets))*number_of_planet+planet.position[0]/1000000000+5, (500/len(self.system_of_planet.planets))*number_of_planet+planet.position[1]/1000000000+5,fill="red",outline="red")
        ####if planet.position[0]!=0 and planet.position[1]!=0: 
        ####    return self.canv.create_oval(250+250*(planet.position[0]/self.system_of_planet.planets[-1].position[0] ) - 5,250+250*(planet.position[0]/self.system_of_planet.planets[-1].position[1] ) - 5,250+250*(planet.position[0]/self.system_of_planet.planets[-1].position[0] ) + 5,250+250*(planet.position[0]/self.system_of_planet.planets[-1].position[1] ) + 5,fill="red",outline="red")
        ####elif planet.position[0]!=0:
        ####    return self.canv.create_oval(250+250*(planet.position[0]/self.system_of_planet.planets[-1].position[0] ) - 5,250- 5,250 + 250*(planet.position[0]/self.system_of_planet.planets[-1].position[0] ) + 5,250 + 5,fill="red",outline="red")
        ####else: 
        ####    return self.canv.create_oval(250 - 5,250 - 5,250 + 5,250 + 5,fill="red",outline="red")
        #if self.max_x!=0 and self.max_y!=0:
        #    return self.canv.create_oval(250+250*(planet.position[0]/self.max_x ) - 5,250+250*(planet.position[1]/self.max_y ) - 5,250+250*(planet.position[0]/self.max_x ) + 5,250+250*(planet.position[1]/self.max_y ) + 5,fill="red",outline="red")
        #elif self.max_x!=0:
        #    return self.canv.create_oval(250+250*(planet.position[0]/self.max_x ) - 5,250 - 5,250+250*(planet.position[0]/self.max_x ) + 5,250 + 5,fill="red",outline="red")
        #else:
        #    return self.canv.create_oval(250 - 5,250 - 5,250 + 5,250 + 5,fill="red",outline="red")
        if self.delitel_x!=0 and self.delitel_y!=0:
            return self.canv.create_oval(250+(planet.position[0]*self.delitel_x ) - 5,250+(planet.position[1]*self.delitel_y ) - 5,250+(planet.position[0]*self.delitel_x ) + 5,250+(planet.position[1]*self.delitel_y ) + 5,fill="red",outline="red")
        elif self.delitel_x!=0:
            return self.canv.create_oval(250+(planet.position[0]*self.delitel_x ) - 5,250 - 5,250+(planet.position[0]*self.delitel_x ) + 5,250 + 5,fill="red",outline="red")
        else:
            return self.canv.create_oval(250 - 5,250 - 5,250 + 5,250 + 5,fill="red",outline="red")
        pass
            
    def move_planet(self,planetid,planet,number_of_planet):
        #self.canv.coords(planetid,[(500/len(self.system_of_planet.planets))*number_of_planet+planet.position[0]/1000000000-5, (500/len(self.system_of_planet.planets))*number_of_planet+planet.position[1]/1000000000-5, (500/len(self.system_of_planet.planets))*number_of_planet+planet.position[0]/1000000000+5, (500/len(self.system_of_planet.planets))*number_of_planet+planet.position[1]/1000000000+5])
        #self.canv.coords(planetid,[(500/len(self.system_of_planet.planets))*number_of_planet+planet.position[0]/1000000000-5, (500/len(self.system_of_planet.planets))*number_of_planet+planet.position[1]/1000000000-5, (500/len(self.system_of_planet.planets))*number_of_planet+planet.position[0]/1000000000+5, (500/len(self.system_of_planet.planets))*number_of_planet+planet.position[1]/1000000000+5])
        ####if planet.position[0]!=0 and planet.position[1]!=0: 
        ####    self.canv.coords(planetid,[250+250*(planet.position[0]/self.system_of_planet.planets[-1].position[0] ) - 5,250+250*(planet.position[0]/self.system_of_planet.planets[-1].position[1] ) - 5,250+250*(planet.position[0]/self.system_of_planet.planets[-1].position[0] ) + 5,250+250*(planet.position[0]/self.system_of_planet.planets[-1].position[1] ) + 5])
        ####elif planet.position[0]!=0:
        ####    self.canv.coords(planetid,[250+250*(planet.position[0]/self.system_of_planet.planets[-1].position[0] ) - 5,250- 5,250 + 250*(planet.position[0]/self.system_of_planet.planets[-1].position[0] ) + 5,250 + 5])
        ####else: 
        ####    self.canv.coords(planetid,[250 - 5,250 - 5,250 + 5,250 + 5])
        ##if self.max_x!=0 and self.max_y!=0: 
        ##    self.canv.coords(planetid,[250+250*(planet.position[0]/self.max_x ) - 5,250+250*(planet.position[1]/self.max_y ) - 5,250+250*(planet.position[0]/self.max_x ) + 5,250+250*(planet.position[1]/self.max_y ) + 5])
        ##elif self.max_x!=0:
        ##    self.canv.coords(planetid,[250+250*(planet.position[0]/self.max_x ) - 5,250 - 5,250+250*(planet.position[0]/self.max_x ) + 5,250 + 5])
        ##else: 
        ##    self.canv.coords(planetid,[250 - 5,250 - 5,250 + 5,250 + 5])
        #if self.delitel_x!=0 and self.delitel_y!=0:
        #    self.canv.coords(planetid,[250+(planet.position[0]*self.delitel_x ) - 5,250+(planet.position[1]*self.delitel_y ) - 5,250+(planet.position[0]*self.delitel_x ) + 5,250+(planet.position[1]*self.delitel_y ) + 5])
        #elif self.delitel_x!=0:
        #    self.canv.coords(planetid,[250+(planet.position[0]*self.delitel_x ) - 5,250 - 5,250+(planet.position[0]*self.delitel_x ) + 5,250 + 5])
        #else:
        #    self.canv.coords(planetid,[250 - 5,250 - 5,250 + 5,250 + 5])
        self.canv.coords(planetid,[250+(planet.position[0]*self.delitel_x ) - 5,250+(planet.position[1]*self.delitel_x ) - 5,250+(planet.position[0]*self.delitel_x ) + 5,250+(planet.position[1]*self.delitel_x ) + 5])

    def buildv2(self):
        #print(int(self.var.get()))
        self.system_of_planet.setscheme(int(self.var.get()))
        global dt
        if self.current_number_system==0:
            dt = int(self.entry_step_by_time.get())
        elif self.current_number_system==1:
            dt = int(self.entry_step_by_time.get())*(24*3600)
        elif self.current_number_system==2:
            dt = int(self.entry_step_by_time.get())*(24*3600*30)
        else:
            dt = int(self.entry_step_by_time.get())*(24*3600*365)
        for i in self.system_of_planet.planets:
            if i.position[0]>self.max_x:
                self.max_x = i.position[0]
            if i.position[1]>self.max_y:
                self.max_y = i.position[1]
        if self.max_x!=0:
            self.delitel_x=250/self.max_x
        else:
            self.delitel_x=0.0
        if self.max_y!=0:
            self.delitel_y=250/self.max_y
        else:
            self.delitel_y=0.0
        #print(self.max_x,self.max_y)
        self.list_of_planets_id=[]
        #self.list_of_preds=[]
        for j in range(len(self.system_of_planet.planets)):
            self.list_of_planets_id.append(self.create_planet(self.system_of_planet.planets[j],j))
            #self.list_of_preds.append([self.system_of_planet.planets[j].position[0],self.system_of_planet.planets[j].position[1]])
        for i in range(0,int(self.entry_time.get()) + int(self.entry_step_by_time.get()),int(self.entry_step_by_time.get())):
            #for i in self.system_of_planet.planets:
            #    if i.position[0]>self.max_x:
            #        self.max_x = i.position[0]
            #    if i.position[1]>self.max_y:
            #        self.max_y = i.position[1]
            #if self.max_x!=0:
            #    self.delitel_x=250/self.max_x
            #else:
            #    self.delitel_x=0.0
            #if self.max_y!=0:
            #    self.delitel_y=250/self.max_y
            #else:
            #    self.delitel_y=0.0
            self.system_of_planet.moving()
            for j in range(len(self.system_of_planet.planets)):
                self.move_planet(self.list_of_planets_id[j], self.system_of_planet.planets[j],j)
                #print("planet",j,"new coord", self.system_of_planet.planets[j].position[0], self.system_of_planet.planets[j].position[1])
                #self.canv.move(self.list_of_planets_id[j], self.system_of_planet.planets[j].position[0]/1000000000 - self.list_of_preds[j][0]/1000000000, self.system_of_planet.planets[j].position[1]/1000000000 - self.list_of_preds[j][1]/1000000000)
                #self.list_of_preds[j][0], self.list_of_preds[j][1] = self.system_of_planet.planets[j].position[0], self.system_of_planet.planets[j].position[1]
            self.root.update()
            time.sleep(0.001)
            #self.entry_energy.config(textvariable=tk.StringVar(self.root,value=str(self.system_of_planet.totalEnergy())))
            
            self.entry_energy.configure(state=tk.NORMAL)
            self.entry_energy.delete(1.0, tk.END)
            self.entry_energy.insert(1.0, str(self.system_of_planet.totalEnergy()))
            self.entry_energy.configure(state=tk.DISABLED)

            self.entry_pEnergy.configure(state=tk.NORMAL)
            self.entry_pEnergy.delete(1.0, tk.END)
            self.entry_pEnergy.insert(1.0, str(self.system_of_planet.potentialEnergy()))
            self.entry_pEnergy.configure(state=tk.DISABLED)

            self.entry_kEnergy.configure(state=tk.NORMAL)
            self.entry_kEnergy.delete(1.0, tk.END)
            self.entry_kEnergy.insert(1.0, str(self.system_of_planet.kineticEnergy()))
            self.entry_kEnergy.configure(state=tk.DISABLED)
            #self.write_text(self.entry_cmx) #не работает
            self.entry_cmx.configure(state=tk.NORMAL)
            self.entry_cmx.delete(1.0, tk.END)
            self.entry_cmx.insert(1.0, str(self.system_of_planet.centerMass()[0]/1000000000))
            self.entry_cmx.configure(state=tk.DISABLED)
           

            self.entry_cmy.configure(state=tk.NORMAL)
            self.entry_cmy.delete(1.0, tk.END)
            self.entry_cmy.insert(1.0, str(self.system_of_planet.centerMass()[1]/1000000000))
            self.entry_cmy.configure(state=tk.DISABLED)
           
    def write_text(self, text):
        text.configure(state=tk.NORMAL)
        text.delete(1.0, tk.END)
        text.insert(1.0, str(self.system_of_planet.centerMass()[0]/1000000000))
        text.configure(state=tk.DISABLED)

    def stop_button(self):
        for i in range(len(self.system_of_planet.planets)):
            self.system_of_planet.planets[i].position.x=149500000000*i
            self.system_of_planet.planets[i].position.y=0
            self.system_of_planet.planets[i].v.x=0
            self.system_of_planet.planets[i].v.y=0
        self.canv.delete("all")

main=programm()

#width/2 = 750/2=375
#(((width/2)/(count-1))-8)*i, i=(0, count-1) - пропорциональное расстояние между двумя планетами
#2планеты: 0; 750/(2*1)-8=367
#3планеты: 0; 750/(2*2)-8=179,5; 179,5*2 = 359
#4планеты: 0; 750/(2*3)-8=117; 117*2=234; 117*3=351
#5планет: 0; 750/(2*4)-10=83,5; 83,5*2=167,5; 83,5*3=251,25; 83,5*4=335
