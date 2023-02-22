# Import libraries

from sklearn.linear_model import Ridge
import PySimpleGUI as sg
import pandas as pd


# Setting theme and layouts
#_____________________________________
sg.theme('DarkGrey13')

layout0 = [[sg.Text('Выберите номер плотины')],
           [sg.Combo(['1-2','3','4','5'], size=(10,5), key='-C-', enable_events=True)],
           [sg.Submit()]]

layout1 = [[sg.Text('Плотина номер')],
           [],
           [sg.Text('Введите количество соседних датчиков для расчета')],
           [sg.InputText()],
           [sg.Submit()]]

layout2 = [[sg.Text('Плотина номер')],
           [sg.Image('1-2.png', size=(1200,302))],
           [sg.Text('Плохой датчик')],
           [sg.InputText()],
           [sg.Text('Список соседних датчиков')]]

layout3 = []
#__________________________________________

# Window0
#__________________________________________
window0 = sg.Window('NNGES sensors', layout0)

while True:             # Event Loop
    event0, values0 = window0.read()
    print(event0, values0)
    if event0 == sg.WIN_CLOSED or event0 == 'Exit' or event0 == 'Submit':
        break
    if event0 == '-C-KEY DOWN':
        window0['-C-'].Widget.event_generate('<Down>')
window0.close()
#___________________________________________

# After closing Window0
#___________________________________________
layout1[0].append(sg.Text(values0['-C-']))
layout1[1] = [sg.Image(values0['-C-'] + '.png')]
#___________________________________________

# Window1
#___________________________________________
window1 = sg.Window('NNGES sensors', layout1)

while True:             # Event Loop
    event1, values1 = window1.read()
    print(event1, values1)
    if event1 == sg.WIN_CLOSED or event1 == 'Exit' or event1 == 'Submit':
        break
window1.close()
#___________________________________________

# After closing Window1
#___________________________________________
num_neighbors = int(values1[1])

layout2[0].append(sg.Text(values0['-C-']))
for i in range(num_neighbors):
    layout2.append([sg.Text(str(i+1)+':'), sg.InputText()])
layout2.append([sg.Submit()])

layout2[1] = [sg.Image(values0['-C-'] + '.png')]
#___________________________________________

# Window2
#___________________________________________
window2 = sg.Window('NNGES sensors', layout2)

while True:             # Event Loop
    event2, values2 = window2.read()
    print(event2, values2)
    if event2 == sg.WIN_CLOSED or event2 == 'Exit' or event2 == 'Submit':
        break
window2.close()
#___________________________________________

# After closing Window2
#___________________________________________
bad_sensor = values2[1]
neighbors = []
for i in range(num_neighbors):
    neighbors.append(values2[i+2])

table1 = pd.read_excel(values0['-C-'] + '_показания.xls', index_col=0)
table = table1.dropna(axis=0)

rid = Ridge(alpha=0.005)

X = table[neighbors]
Y = table[bad_sensor]

rid.fit(X, Y)

cfr = rid.coef_
intcfr = rid.intercept_

for i in range(num_neighbors):
    layout3.append([sg.Text(neighbors[i]), sg.Text(cfr[i])])
layout3.append([sg.Text('Свободный член'), sg.Text(intcfr)])
#___________________________________________

# Window3
#___________________________________________
window3 = sg.Window('NNGES sensors', layout3)
event3, values3 = window3.read()
window3.close()
#___________________________________________

# Output file
#___________________________________________
f = open("output.txt", "w")
for i in range(num_neighbors):
    f.write(str(cfr[i]) + ' * ' + '(' + neighbors[i] + ') + ')
f.write(str(intcfr))
f.close()
#___________________________________________
