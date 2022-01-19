# Data_parcer_v1.0 - позволяет парсить отдельный файл с измерениями в дата-фрейм, затем выкидывает оттуда лишние столбцы
# и строит график нужной функции
# Как это апгрейдить?
# Сделать так, чтобы он парсил серию измерений одного образца, усреднял по всем проходам и строил среднее

'''

Что происходит?

1) Считываем из папки где лежат результаты измерений все названия(заголовки) файлов в список wet_data
2) Функция file_pars получает на вход название файла и возвращает DataFrame (df) со столбцами в формате float64
3) matplotlib.pyplot строит график по выбранным столбцам из нашего DataFrame (df)

 '''


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob

#from matplotlib.backends.backend_pdf import PdfPages
# Рисовать графики сразу же
#%matplotlib inline

# прописываем путь к папке с результатами измерений
directory = 'C:/Users/mi/Python_programms/Test_data_for_data_parcer'

# считываем в отдельный список названия всех папок в каталоге
wet_data = os.listdir(directory)
wet_data

# Функция принимает название файла и возвращает дата-фрейм с данными из этого файла в формате float64

def file_pars(file_head):
    file_way_template = "C:/Users/mi/Python_programms/Test_data_for_data_parcer/{end}"
    df = pd.read_csv(file_way_template.format(end = file_head), header = 0, decimal=',', delim_whitespace = True)
    df.head()
    df.columns = ['dV','Vsd','Current','Time','Vg_out_1','Vg_out_2','First A','Second A']
    df = df.drop(['Vg_out_2', 'First A', 'Second A'], axis = 1)
    #df['Conductance'] = df['Current']*1e6/df['Vsd']

    return df

#file_pars(wet_data[2]).head()
Vg_grow_heads_list = []
Vg_fall_heads_list = [] 
i = 0

# Проверяем является ли первое значение в столбце с затворным напряжением
# меньше нуля. Если является, то пишем заголовок этого файла в список
# Vg_grow_heads_list, иначе пишем заголовок в список Vg_fall_heads_list.
while i < len(wet_data):
    if file_pars(wet_data[i])['Vsd'][1] <= 0: 
        Vg_grow_heads_list.append(wet_data[i])   
    else:                                          
        Vg_fall_heads_list.append(wet_data[i])
    i = i + 1
print('Growing gate:', Vg_grow_heads_list)
print('Falling gate:', Vg_fall_heads_list)

file_pars(wet_data[0]).head()
#file_pars(wet_data[2])['Vg_out_1'][0]

fig, ax = plt.subplots()
n_wet_data_1 = 3 # номер файла в списке wet_data
ax.plot(file_pars(Vg_grow_heads_list[n_wet_data_1])['Vsd'], \
        file_pars(Vg_grow_heads_list[n_wet_data_1])['Current'],'-', color='Red', label='Growing Vsd')
n_wet_data_2 = 3
ax.plot(file_pars(Vg_fall_heads_list[n_wet_data_2])['Vsd'], \
        file_pars(Vg_fall_heads_list[n_wet_data_2])['Current'],'-', color='blue', label='Falling Vsd')
plt.title("ВАХ")
plt.xlabel('V_sd (V)')
plt.ylabel('I ($\mu$S)')
plt.legend()
plt.show()
fig.savefig("GVg_buffer.png")