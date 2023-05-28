import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter.filedialog as fd



class population(): #
    def __init__(self,  quantity:int, growth: float):
        # self.coeff = coeff #����� ��������������
        self.N = quantity #�����������
        self.alpha =growth #�������

#class System:
#    def __init__(self, size: int,list_of_population, scheme:int,B,T,dt):
#        self.populations = list_of_population
#        self.size = size
#        self.B=B
#        self.T=T
#        self.dt=dt
#        
#        self.scheme = scheme
#
#    def add_population(self, population):
#        self.populations.append(population)
#        self.size += 1
#
#
#    def moving(self):
#        from scipy.integrate import odeint
#        result = 0
#        y = []
#        N = np.zeros((len(self.B)))
#        t= np.linspace(0, self.T, self.T//self.dt)
#        for i in range(len(self.B)): 
#            N[i]=self.populations[i].N
#        for i in range(len(self.B)): #���������� ����� (���-�� �����)
#            
#            y.append(odeint(self.sim, N, t))
#        return y
#
#    def sim(self, N, t):
#        dN = np.zeros(len(self.B))
#        for i in range (len(self.B)):
#            sum_ = 0
#            N=self.populations[i].N
#            alpha=self.populations[i].alpha
#            for j in range(len(self.B)):   
#                sum_ += alpha * N + self.B[i][j] * N *self.populations[j].N 
#            dN[i] = alpha*N+sum_
#
#        return (dN)
#
#
#    
#    def setscheme(self, newscheme:int):
#        self.scheme = newscheme

class System:
    def __init__(self, size: int,list_of_population, scheme:int,B,T,dt):
        self.populations = list_of_population
        self.size = size
        self.B=B
        self.T=T
        self.dt=dt
        
        self.scheme = scheme

    def setschem(self,schem):
        self.scheme=schem

    def add_population(self, population):
        self.populations.append(population)
        self.size += 1


    def moving(self):
        from scipy.integrate import odeint
        result = 0
        y1, y2=0, 0
        N = np.zeros((len(self.B)))
        t= np.linspace(0, self.T, self.T//self.dt)
        for i in range(len(self.B)): 
            N[i]=self.populations[i].N
        
        if (self.scheme == 1):
            y1 = odeint(self.sim, N, t)
        elif (self.scheme == 0):
            y1 = self.Euler(N, t)

        return y1

    def Euler(self, N_, t):
        y1 = np.zeros((len(t), len(N_)))
        y1[0]=N_
        for i in range((len(t)-1)):
            y1[i+1] = y1[i] + self.sim(y1[i], t[i]) * self.dt
        return y1
            
    

    def sim(self, N_, t):        
        N=[]
        for i in range (len(self.B)):
            N.append(N_[i])
            #alpha.append(self.populations[i].alpha)

        dN1 = np.zeros(len(self.B))
        for i in range (len(self.B)):
            sum_ = 0
            alpha=self.populations[i].alpha
            

            for j in range(len(self.B)):
                if i == j:
                    continue
                sum_ += self.B[i][j] * N[i] *N[j] 
            
            dN1[i] = alpha*N[i]+sum_

        return (dN1)
                 

    
    def setscheme(self, newscheme:int):
        self.scheme = newscheme

class configurate:
    def __init__(self,size=2,list_of_population=[],matrix=[]):
        self.size = size
        self.list_of_number_string=[]
        self.list_of_quantity_labels=[]
        self.list_of_growth_labels=[]
        self.list_of_number_columns_rigth=[]
        self.list_of_number_strings_rigth=[]
        self.matrix_of_rigth_table=matrix
        self.list_of_populations=list_of_population

        #window
        self.root = tk.Tk()
        self.root.geometry("670x220")
        self.root.resizable(width=0, height=0)

        #append_delete
        self.button_append = tk.Button(master=self.root,text="append",command=self.append_population)
        self.button_append.grid(row=0,column=0,pady=10)
        self.button_append = tk.Button(master=self.root,text="delete",command=self.delete_population)
        self.button_append.grid(row=0,column=1,pady=10)

        #left_grid
        self.size_label = tk.Label(master=self.root,text=str(self.size), width=7, relief="raised")
        self.size_label.grid(row=1,column=0)

        self.quantity_label = tk.Label(master=self.root,text="Quantity", width=7, relief="raised")
        self.quantity_label.grid(row=1,column=1)

        self.growth_label = tk.Label(master=self.root,text="Growth", width=7, relief="raised")
        self.growth_label.grid(row=1,column=2)


        #strings_of_left_table
        self.list_of_number_string.append(tk.Label(master=self.root,text='1', width=7, relief="raised"))
        self.list_of_number_string[-1].grid(row = 2, column = 0)
        
        if (len(self.matrix_of_rigth_table)==0):
            self.list_of_quantity_labels.append(tk.Entry(master=self.root, textvariable=tk.StringVar(self.root,value='100'), width=7 ))
        else:
            self.list_of_quantity_labels.append(tk.Entry(master=self.root, textvariable=tk.StringVar(self.root,value=str(self.list_of_populations[0].N)), width=7 ))
        self.list_of_quantity_labels[-1].grid(row = 2, column = 1)
        
        if (len(self.matrix_of_rigth_table)==0):
            self.list_of_growth_labels.append(tk.Entry(master=self.root, textvariable=tk.StringVar(self.root,value='0.01'), width=7 ))
        else:
            self.list_of_growth_labels.append(tk.Entry(master=self.root, textvariable=tk.StringVar(self.root,value=str(self.list_of_populations[0].alpha)), width=7 ))
        self.list_of_growth_labels[-1].grid(row = 2, column = 2)

        #rigth_table
        tk.Label(master=self.root,width=7).grid(row=1,column=3)
        self.size_label = tk.Label(master=self.root,text='', width=7, relief="raised")
        self.size_label.grid(row=1,column=4)


        self.list_of_number_columns_rigth.append(tk.Label(master=self.root,text='1', width=7, relief="raised"))
        self.list_of_number_columns_rigth[-1].grid(row=1,column=5)

        self.list_of_number_strings_rigth.append(tk.Label(master=self.root,text='1', width=7, relief="raised"))
        self.list_of_number_strings_rigth[-1].grid(row=2,column=4)

        if (len(self.matrix_of_rigth_table)==0):
            self.matrix_of_rigth_table.append([])
            self.matrix_of_rigth_table[-1].append(tk.Entry(master=self.root, textvariable=tk.StringVar(self.root,value='0'), width=7 ))
        else:
            self.matrix_of_rigth_table[0][0]=(tk.Entry(master=self.root, textvariable=tk.StringVar(self.root,value=str(self.matrix_of_rigth_table[0][0])), width=7 ))
        self.matrix_of_rigth_table[0][0].grid(row=2,column=5)

        if (len(self.matrix_of_rigth_table)==1):
            for i in range(1,self.size):
                self.append_population()
        else:
            for i in range(1,self.size):
                self.append_population_done()
            self.matrix_of_rigth_table[-1][-1]=tk.Entry(master=self.root, textvariable=tk.StringVar(self.root,value=str(self.matrix_of_rigth_table[-1][-1])), width=7 )
            self.matrix_of_rigth_table[-1][-1].grid(row=1+len(self.list_of_number_columns_rigth),column=4+len(self.list_of_number_columns_rigth))
    

        def on_closing():
            self.list_of_populations.clear()
            self.list_of_populations.append([])
            self.list_of_populations.append([])
            for i in range(len(self.list_of_quantity_labels)):
                self.list_of_populations[0].append(population(int(self.list_of_quantity_labels[i].get()),float(self.list_of_growth_labels[i].get())))
                #self.list_of_populations[0].append([])
                #self.list_of_populations[0][i].append(float(self.list_of_quantity_labels[i].get()))
                #self.list_of_populations[0][i].append(float(self.list_of_growth_labels[i].get()))
            
            for i in range(len(self.matrix_of_rigth_table)):
                self.list_of_populations[1].append([])
                for j in range(len(self.matrix_of_rigth_table[i])):
                    self.list_of_populations[1][i].append(float(self.matrix_of_rigth_table[i][j].get()))

            self.root.destroy()
            
        self.root.protocol("WM_DELETE_WINDOW", on_closing)

        self.root.mainloop()

    def append_population(self):
        self.list_of_number_string.append(tk.Label(master=self.root,text=str(len(self.list_of_number_string)+1), width=7, relief="raised"))
        self.list_of_number_string[-1].grid(row = 1+len(self.list_of_number_string), column = 0)

        self.list_of_quantity_labels.append(tk.Entry(master=self.root, textvariable=tk.StringVar(self.root,value=str(100*(len(self.list_of_quantity_labels)+1))), width=7 ))
        self.list_of_quantity_labels[-1].grid(row = 1+len(self.list_of_quantity_labels), column = 1)

        self.list_of_growth_labels.append(tk.Entry(master=self.root, textvariable=tk.StringVar(self.root,value='-0.01'), width=7 ))
        self.list_of_growth_labels[-1].grid(row = 1+len(self.list_of_growth_labels), column = 2)

        self.list_of_number_columns_rigth.append(tk.Label(master=self.root,text=str(len(self.list_of_number_columns_rigth)+1), width=7, relief="raised"))
        self.list_of_number_columns_rigth[-1].grid(row=1,column=4+len(self.list_of_number_columns_rigth))

        self.list_of_number_strings_rigth.append(tk.Label(master=self.root,text=str(len(self.list_of_number_strings_rigth)+1), width=7, relief="raised"))
        self.list_of_number_strings_rigth[-1].grid(row=1+len(self.list_of_number_strings_rigth),column=4)

        for i in range(len(self.matrix_of_rigth_table)):
            self.matrix_of_rigth_table[i].append(tk.Entry(master=self.root, textvariable=tk.StringVar(self.root,value='-0.0001'), width=7 ))
            self.matrix_of_rigth_table[i][-1].grid(row=2+i,column=4+len(self.matrix_of_rigth_table[i]))

        self.matrix_of_rigth_table.append([])
        for i in range(len(self.list_of_number_strings_rigth)):
            if i == len(self.matrix_of_rigth_table)-1:
                self.matrix_of_rigth_table[-1].append(tk.Entry(master=self.root, textvariable=tk.StringVar(self.root,value='0'), width=7 ))
            elif i<(len(self.matrix_of_rigth_table)-1):
                self.matrix_of_rigth_table[-1].append(tk.Entry(master=self.root, textvariable=tk.StringVar(self.root,value='0.0001'), width=7 ))
            elif i>(len(self.matrix_of_rigth_table)-1):
                self.matrix_of_rigth_table[-1].append(tk.Entry(master=self.root, textvariable=tk.StringVar(self.root,value='-0.0001'), width=7 ))
            self.matrix_of_rigth_table[-1][i].grid(row=1+len(self.list_of_number_strings_rigth),column=5+i)
        #self.matrix_of_rigth_table[-1].append(tk.Entry(master=self.root, textvariable=tk.StringVar(self.root,value='0'), width=7 ))
        #self.matrix_of_rigth_table[-1][-1].grid(row=2,column=5)

    def append_population_done(self):
        #return
        self.list_of_number_string.append(tk.Label(master=self.root,text=str(len(self.list_of_number_string)+1), width=7, relief="raised"))
        self.list_of_number_string[-1].grid(row = 1+len(self.list_of_number_string), column = 0)

        self.list_of_quantity_labels.append(tk.Entry(master=self.root, textvariable=tk.StringVar(self.root,value=str(self.list_of_populations[len(self.list_of_quantity_labels)].N)), width=7 ))
        self.list_of_quantity_labels[-1].grid(row = 1+len(self.list_of_quantity_labels), column = 1)

        self.list_of_growth_labels.append(tk.Entry(master=self.root, textvariable=tk.StringVar(self.root,value=str(self.list_of_populations[len(self.list_of_growth_labels)].alpha)), width=7 ))
        self.list_of_growth_labels[-1].grid(row = 1+len(self.list_of_growth_labels), column = 2)

        self.list_of_number_columns_rigth.append(tk.Label(master=self.root,text=str(len(self.list_of_number_columns_rigth)+1), width=7, relief="raised"))
        self.list_of_number_columns_rigth[-1].grid(row=1,column=4+len(self.list_of_number_columns_rigth))

        self.list_of_number_strings_rigth.append(tk.Label(master=self.root,text=str(len(self.list_of_number_strings_rigth)+1), width=7, relief="raised"))
        self.list_of_number_strings_rigth[-1].grid(row=1+len(self.list_of_number_strings_rigth),column=4)

        print(self.matrix_of_rigth_table)
        for i in range(len(self.list_of_number_columns_rigth)-1):
            print(i,len(self.list_of_number_columns_rigth)-1,self.matrix_of_rigth_table[i][len(self.list_of_number_columns_rigth)-1])
            self.matrix_of_rigth_table[i][len(self.list_of_number_columns_rigth)-1]=(tk.Entry(master=self.root, textvariable=tk.StringVar(self.root,value=str(self.matrix_of_rigth_table[i][len(self.list_of_number_columns_rigth)-1])), width=7 ))
            self.matrix_of_rigth_table[i][len(self.list_of_number_columns_rigth)-1].grid(row=2+i,column=4+len(self.list_of_number_columns_rigth))

        for i in range(len(self.matrix_of_rigth_table[len(self.list_of_number_columns_rigth)-1])):
            self.matrix_of_rigth_table[len(self.list_of_number_columns_rigth)-1][i]=(tk.Entry(master=self.root, textvariable=tk.StringVar(self.root,value=str(self.matrix_of_rigth_table[len(self.list_of_number_columns_rigth)-1][i])), width=7 ))
            self.matrix_of_rigth_table[len(self.list_of_number_columns_rigth)-1][i].grid(row=1+len(self.list_of_number_columns_rigth),column=5+i)

        
    def delete_population(self):
        pass

    

class programm:
    def __init__(self):
        self.system = []
        self.current_time=0

        self.root = tk.Tk()
        self.root.geometry("870x505")
        self.root.resizable(width=0, height=0)

        #canvas
        self.fig=plt.figure()
        self.canv=FigureCanvasTkAgg(self.fig,master=self.root)
        self.canv.get_tk_widget().config(width=500,height=500)
        self.canv.get_tk_widget().grid(rowspan=25,column=1)
        self.canv.draw()

        #time_entry
        self.label_step_by_time = tk.Label(text="Step by time")
        self.label_step_by_time.grid(row=2, column=2)

        self.entry_step_by_time = tk.Entry(textvariable=tk.StringVar(self.root,value='3600'))
        self.entry_step_by_time.grid(row=3,column=2)

        self.label_time = tk.Label(text="Time",anchor="e")
        self.label_time.grid(row=2, column=3)

        self.entry_time = tk.Entry(textvariable=tk.StringVar(self.root,value='360000'))
        self.entry_time.grid(row=3,column=3)

        #current_time_step
        self.current_type_time_step=0
        self.varNS = tk.IntVar()
        self.varNS.set(0)
        self.sec = tk.Radiobutton(text="Seconds",command=self.changeNS,variable=self.varNS,value=0)
        self.sec.grid(row=4,column=2,padx=30)

        self.day = tk.Radiobutton(text="Days",command=self.changeNS,variable=self.varNS,value=1)
        self.day.grid(row=4,column=3,padx=20)

        self.month = tk.Radiobutton(text="Months",command=self.changeNS,variable=self.varNS,value=2)
        self.month.grid(row=5,column=2,padx=30)

        self.year = tk.Radiobutton(text="Years",command=self.changeNS,variable=self.varNS,value=3)
        self.year.grid(row=5,column=3,padx=20)

        #configurate population
        self.configurate_population = tk.Button(text="configurate population",command=self.configurate_population)
        self.configurate_population.grid(row=7,column=2,columnspan=2,padx=100)

        #select_scheme
        self.current_schem=1
        self.var = tk.IntVar()
        self.var.set(1)
        self.eiler = tk.Radiobutton(text="Scheme Eiler",command=self.change,variable=self.var,value=0)
        self.eiler.grid(row=9,column=2,padx=30)

        self.veler = tk.Radiobutton(text="odeint",command=self.change,variable=self.var,value=1)
        self.veler.grid(row=9,column=3,padx=30)

        
        #output_layers
        self.label_count_of_population = tk.Label(text="Quantity of population")
        self.label_count_of_population.grid(row=11,column=2)

        self.label_of_time = tk.Label(text="Time")
        self.label_of_time.grid(row=11,column=3)

        self.text_count_of_population = tk.Text(state=tk.DISABLED, width=15, height=1)
        self.text_count_of_population.grid(row=12,column=2)

        self.text_time = tk.Text(state=tk.DISABLED, width=15, height=1)
        self.text_time.grid(row=12,column=3)

        #buttons
        #save and load
        self.save_button = tk.Button(text="save",command=self.save)
        self.save_button.grid(row=13,column=2)
        self.load_button = tk.Button(text="load",command=self.load)
        self.load_button.grid(row=13,column=3)

        #run and stop
        self.build_button = tk.Button(text="run",command=self.build)
        self.build_button.grid(row=14,column=2)
        self.build_button = tk.Button(text="stop",command=self.stop_button)
        self.build_button.grid(row=14,column=3)



        self.root.mainloop()

    def changeNS(self):
        self.current_type_time_step = int(self.varNS.get())
    
    def configurate_population(self):
        if (type(self.system)==list):
            self.system=[]
            a=configurate(list_of_population=self.system,matrix=[])
        else:
            self.system=[]
            a=configurate(list_of_population=self.system,matrix=[])


    def change(self):
        self.current_schem = int(self.var.get())

    def save(self):
        filetypes = (("Text file", "*.txt"),)
        name=fd.asksaveasfile(title="Save file",mode='w',defaultextension=".txt",filetypes=filetypes)
        if name:
            name.write(str(self.var.get())+'\n')
            name.write(str(len(self.system.populations))+'\n')
            for i in self.system.populations:
                name.write(str(i.N)+' '+str(i.alpha)+'\n')

            name.write(str(len(self.system.B))+'\n')
            for i in self.system.B:
                name.write(str(len(i))+'\n')
                for j in i:
                    name.write(str(j)+' ')
                name.write('\n')

            name.close

    def load(self):
        filetypes = (("Text file", "*.txt"),)
        filename = fd.askopenfilename(title="Open file", initialdir="/",
                                      filetypes=filetypes)
        if filename:
            f=open(filename,'r')
            a=f.read().split('\n')
            ind=0
            try:
                self.current_schem=int(a[0])
            except:
                return
            ind+=1
            count=0
            try:
                count=int(a[1])
            except:
                return
            ind+=1
            mas_populations=[]
            for i in range(ind,count+ind):
                mas_populations.append([])
                try:
                    a[i]=a[i].split()
                    for j in a[i]:

                        mas_populations[-1].append(float(j))
                except:
                    continue
                ind+=1
            print(mas_populations)
            matrix_populations=[]
            count2=0
            try:
                count2=int(a[ind])
            except:
                return
            print(count2)
            ind+=1
            for i in range(count2):
                matrix_populations.append([])
                countn=0
                try:
                    countn=int(a[ind])
                except:
                    return
                ind+=1
                a[ind]=a[ind].split()
                for j in a[ind]:
                    try:
                        matrix_populations[-1].append(float(j))
                    except:
                        continue
                ind+=1
                    #������� ����� ����� ���������� ������� ��������� ������������
            print(mas_populations, matrix_populations)

    def build(self):
        Time=int(self.entry_time.get())
        dt=int(self.entry_step_by_time.get())
        if self.varNS==1:
            Time*=(60*60*24)
            dt*=(60*60*24)
        elif self.varNS==2:
            Time*=(60*60*24*30)
            dt*=(60*60*24*30)
        elif self.varNS==3:
            Time*=(60*60*24*365)
            dt*=(60*60*24*365)
        print(self.current_schem)
        if (type(self.system) is list):
            self.system=System(len(self.system[0]),self.system[0],int(self.current_schem),self.system[1],Time,dt )
        else:
            self.system.setschem(int(self.current_schem))
        self.current_time = np.linspace(0,Time,Time//dt)

        y_s=self.system.moving()
        for i in range(int(self.system.size)):
            plt.plot(self.current_time,y_s[:,i])
        self.canv.draw()

        summa=0
        #for i in range(len(y_s)):
        #    for j in range(len(y_s[i])):
        #        summa+=y_s[i][j]
        summa=y_s[-1][0]+y_s[-1][1]

        self.text_count_of_population.configure(state=tk.NORMAL)
        self.text_count_of_population.delete(1.0, tk.END)
        self.text_count_of_population.insert(1.0, str(summa))
        self.text_count_of_population.configure(state=tk.DISABLED)

        self.text_time.configure(state=tk.NORMAL)
        self.text_time.delete(1.0, tk.END)
        self.text_time.insert(1.0, str(Time))
        self.text_time.configure(state=tk.DISABLED)

    def stop_button(self):
        plt.clf()
        self.canv.draw()


programm()