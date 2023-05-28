from bdb import effective
import tkinter as tk

class programm:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.resizable(0,0)

        self.label_time_modeling = tk.Label(text="Time of modeling")
        #self.label_time_modeling = tk.Label(text="Время моделирования")
        self.label_time_modeling.grid(row=0,column=0)

        self.entry_time_modeling = tk.Entry(textvariable=tk.StringVar(self.root,value='100'))
        self.entry_time_modeling.grid(row=0,column=1)

        self.label_alpha = tk.Label(text='Alpha')

        self.label_alpha.grid(row=0,column=2)

        self.entry_alpha = tk.Entry(textvariable=tk.StringVar(self.root,value='0.1'))
        self.entry_alpha.grid(row=0,column=3)

        self.label_betta = tk.Label(text='Betta')
        self.label_betta.grid(row=0,column=4)

        self.entry_betta = tk.Entry(textvariable=tk.StringVar(self.root,value='0.1'))
        self.entry_betta.grid(row=0,column=5)

        self.label_count_of_lines = tk.Label(text="Count of lines")
        #self.label_time_modeling = tk.Label(text="Время моделирования")
        self.label_count_of_lines.grid(row=1,column=0)

        self.entry_count_of_lines = tk.Entry(textvariable=tk.StringVar(self.root,value='3'))
        self.entry_count_of_lines.grid(row=1,column=1)

        self.label_storage = tk.Label(text='storage capacity')
        self.label_storage.grid(row=1,column=2)

        self.entry_storage = tk.Entry(textvariable=tk.StringVar(self.root,value='1'))
        self.entry_storage.grid(row=1,column=3)

        self.label_count_of_calls = tk.Label(text='count of calls')
        self.label_count_of_calls.grid(row=1,column=4)

        self.entry_count_of_calls = tk.Entry(textvariable=tk.StringVar(self.root,value='0'))
        self.entry_count_of_calls.config(state=tk.DISABLED)
        self.entry_count_of_calls.grid(row=1,column=5)

        self.label_busy_lines = tk.Label(text="busy lines")
        self.label_busy_lines.grid(row=2,column=0)

        self.entry_busy_lines = tk.Entry(textvariable=tk.StringVar(self.root,value='0'))
        self.entry_busy_lines.config(state=tk.DISABLED)
        self.entry_busy_lines.grid(row=2,column=1)

        self.label_busy_storage = tk.Label(text='busy storage')
        self.label_busy_storage.grid(row=2,column=2)

        self.entry_busy_storage = tk.Entry(textvariable=tk.StringVar(self.root,value='0'))
        self.entry_busy_storage.config(state=tk.DISABLED)
        self.entry_busy_storage.grid(row=2,column=3)

        self.label_rejected_calls = tk.Label(text='rejected calls')
        self.label_rejected_calls.grid(row=2,column=4)

        self.entry_rejected_calls = tk.Entry(textvariable=tk.StringVar(self.root,value='0'))
        self.entry_rejected_calls.config(state=tk.DISABLED)
        self.entry_rejected_calls.grid(row=2,column=5)

        self.label_efficiency = tk.Label(text = 'efficiency')
        self.label_efficiency.grid(row=0,column=6)

        self.entry_efficiency = tk.Entry(textvariable=tk.StringVar(self.root,value='0'))
        self.entry_efficiency.grid(row=1,column=6)

        self.button_run = tk.Button(text='build',command = self.build)
        self.button_run.grid(row=2,column=6)

        self.canv=tk.Canvas(width=800,height = 400,bg='white')
        self.canv.grid(row=3,column=0,columnspan=8)



        self.root.mainloop()

    def build(self):
        self.canv.delete('all')
        import random
        import numpy as np
        arr1=[]#координаты начала вызова
        arr2=[]#длительность вызова
        
        N = 0
        alpha = float(self.entry_alpha.get())
        beta = float(self.entry_betta.get())
        count_line = int(self.entry_count_of_lines.get())
        count_capacity = int(self.entry_storage.get())
        time = int(self.entry_time_modeling.get())
        
        length=0
        arr1.append((-np.log(np.random.random_sample())/alpha))
        arr2.append((np.random.random_sample())/beta)
        length+=arr2[-1]
        N+=1

        while (length < time):
            #arr1.append( (-np.log(np.random.random_sample())/alpha) )
            #arr2.append( (-np.log(np.random.random_sample())/beta) )

            #arr1.append( ((np.random.random_sample())/alpha) + arr1[-1])
            #arr2.append( ((np.random.random_sample())/beta) )

            arr1.append( (-np.log(np.random.random_sample())/alpha) + arr1[-1])
            arr2.append( ((np.random.random_sample())/beta) )
            length=arr1[-1]
            N+=1
        
        #arr1.sort()
        arr1=arr1[:-1]
        arr2=arr2[:-1]
        N-=1
        print(arr1)
        print(arr2)
        
        number_of_received_calls = 0 #число принятых вызовов
        #по факту это размер всех словарей
        number_of_rejected_calls = 0 #число отклоненных вызовов
        number_of_calls = 0 # общее число вызовов
        efficiency = 1 #эффективность
        busy_lines=0
        
        
        #distribution = np.zeros((count_line)) #двумерный список: словарь где ключ-начало, значение-длительность
        distribution = []
        for i in range(count_line):
            distribution.append(dict())
        #на 1 линию помещаем первый вызов
        distribution[0][arr1[0]]=arr2[0]
        min_arr=[]
        capacity=[]
        for j in range (1,N):
            count = 0
            t=True
            while (count < count_line):
                if (len(distribution[count]) == 0):
                    distribution[count][arr1[j]]=arr2[j]
                    t=False
                    break
                if (list(distribution[count].keys())[-1] + distribution[count][list(distribution[count].keys())[-1]] < arr1[j]):
                    distribution[count][arr1[j]]=arr2[j]
                    t=False
                    break
                count+=1 #смотрим следующую линию
            if count>busy_lines and count<count_line:
                busy_lines=count
            if t:
                ind = 0
                min_time_start = time
                for i in range(count_line):
                    if list(distribution[i].keys())[-1]<min_time_start:
                        min_time_start = list(distribution[i].keys())[-1]
                        ind = i
                cnt=0
                for i in range(len(capacity)):
                    if arr1[j]> capacity[i][0] and arr1[j]<capacity[i][1]:
                        cnt+=1
                if cnt<count_capacity:
                    distribution[ind][list(distribution[ind].keys())[-1]]+=arr2[j]
                    capacity.append([arr1[j], list(distribution[ind].keys())[-1] + distribution[ind][list(distribution[ind].keys())[-1]] ])
                else:
                    number_of_rejected_calls+=1
                    #number_of_calls-=1
            number_of_calls+=1
        #
        #    if t:
        #        
        #        pass
        #    if(len(capacity)<count_capacity): #если счетчик пока меньше емкости накопителя, то записываем в массив
        #        capacity.append(arr1[j]+arr2[j])#время начала вызова из очереди
        #        #Записываем чтобы следить за тем, чтобы освобождался накопитель в нужное время
        #        #если наступает момент когда начинается вызов из накопителя, то удаляем этот вызов из массива
        #
        #
        #        #найдем минимальный конец вызова(точка начала+длительность)
        #        #сравниваем точка начала(ключ)+длительность(значение) последнего элемента словаря и находим минимальное
        #        for i in range(count_line):
        #            min_arr.append(list(distribution[i].keys())[-1] + distribution[i][list(distribution[i].keys())[-1]])
        #        minimum = min(min_arr) #это время начала вызова из очереди накопителя, длительность по умолчанию
        #        i_min=min_arr.index(minimum) #номер линии с минимальным значением
        #        
        #        distribution[i_min][minimum]=arr2[j]
        #
        #    else:
        ##освобождение Накопителя происходит когда сравниваем новые поступившие В после заполения Н(else)
        ##если поступивший В < минимального значения(момент когда В выйдет из Н)- теряем, иначе -записываем В
        ## !!!!!!! удаляем из массива при новой записи тот В с которым прошло истинное сравнение(лучше перезаписывать???)
        #        if(min(capacity) > arr1[j]):
        #            capacity.append(arr1[j]+arr2[j])
        ##теряем вызов
        #        else:
        #            number_of_rejected_calls+=1
        for i in range(1,count_line+1):
            #first_arr=[]
            #second_arr=[]
            self.canv.create_line(20,60*i,780,60*i,fill='blue',width = 2)
            for k in distribution[i-1]:
                #print(k)
                self.canv.create_rectangle(20+760*k/time,60*i-5,20+760*k/time+760*distribution[i-1][k]/time,60*i+5,fill='red',width = 0)
        
        self.entry_count_of_calls.config(state=tk.NORMAL)
        self.entry_count_of_calls.config(textvariable=tk.StringVar(self.root,value=str(number_of_calls)))
        self.entry_count_of_calls.config(state=tk.DISABLED)
        self.entry_efficiency.config(state=tk.NORMAL)
        self.entry_efficiency.config(textvariable=tk.StringVar(self.root,value=str( number_of_calls/(number_of_rejected_calls+number_of_calls))))
        self.entry_efficiency.config(state=tk.DISABLED)
        self.entry_rejected_calls.config(state=tk.NORMAL)
        self.entry_rejected_calls.config(textvariable=tk.StringVar(self.root,value=str(number_of_rejected_calls)))
        self.entry_rejected_calls.config(state=tk.DISABLED)
        self.entry_busy_lines.config(state=tk.NORMAL)
        self.entry_busy_lines.config(textvariable=tk.StringVar(self.root,value=str(busy_lines+1)))
        self.entry_busy_lines.config(state=tk.DISABLED)
        busy_capacity=0
        for i in capacity:
            if i[0]<time and time<i[1]:
                busy_capacity+=1

        
        self.entry_busy_storage.config(state=tk.NORMAL)
        self.entry_busy_storage.config(textvariable=tk.StringVar(self.root,value=str(busy_capacity)))
        self.entry_busy_storage.config(state=tk.DISABLED)



programm()