import os,glob
import numpy as np
import re
import matplotlib.pyplot as plt

#Initial parametrs
sec_frame  = 20
nm_px = 100

#lists for full data
mean = []
angle = []
lenght = []

name_dir = []

#index of opened directory
i=0

#dictionary for results
#store data divided by types of MT.
# store temperatures that were in experiments in the order that files were opened.
#store indexes of corresponding files
#store calculated rates (velocity)
results = {'GMPCPP_temp': [],
            'GMPCPP_indexes': [],
            'GMPCPP_rate': [],
            'Taxol_temp': [],
            'Taxol_indexes': [],
            'Taxol_rate': []}

#calculating shortening rate
#Считаем скорость для каждой кимограммы и потом вычисляем среднее
def v_calc(ang, temp):
   if temp == 32:
      #иногда на кимограммах плюс конец путался с минус концом, поэтому угол получался зеркольно отраженным. Исправляем.
      ang[ang < -90] = -180 - ang[ang < -90]
      v = (nm_px * 60) / (np.tan(np.pi * ang / 180) * 1000 * sec_frame)
   else:
      ang[ang>-90] = -180-ang[ang>-90]
      v = - (nm_px * 60)/(np.tan(np.pi * ang/ 180)*1000*sec_frame)
   # print("v_calc, ang ", ang)
   print('v = ', np.mean(v))
   return np.mean(v)

#searching all results in all experiments
#папка с данными со всех эксп
# folder/*/*/Results.csv
for filename in glob.glob("C:\\Users\\YummyPolly\\Documents\\LAB\\MT_cooling\\*\\*\\Results.csv", recursive=True):
   with open(filename, 'r') as f:
      data = np.loadtxt(f, delimiter=',', skiprows=1)
      data = data.transpose()
      dir = os.path.split(os.path.dirname(filename))

      #вынимаем из названия температуру охлаждения. Не понятно, что делать с ростом.
      m = re.search('_(..)C', dir[1])
      if m:
         cur_temp = m.group(1)
      print("temp ", int(cur_temp))
      #temperature += [int(found)]

      name_dir += dir
      # print(name_dir)

      #на всякий случай записываем все данные
      mean += [data[1, :]]
      angle += [data[2, :]]
      lenght += [data[3, :]]

      #делаем разделение по типам МТ.
      if 'GMPCPP' in dir[0]:
         temp = 'GMPCPP_temp'
         index = 'GMPCPP_indexes'
         rate = 'GMPCPP_rate'
      else:
         temp = "Taxol_temp"
         index = 'Taxol_indexes'
         rate = 'Taxol_rate'
      #добавляем новые значения в словарь
      tmp = results[temp]
      tmp += [int(cur_temp)]
      results[temp] = tmp

      tmp = results[index]
      tmp += [i]
      results[index] = tmp

      tmp = results[rate]
      tmp += [v_calc(data[2, :], int(cur_temp))]#вычисленная скорость
      results[rate] = tmp

      # print(filename, name_dir)
      i += 1#идем открывать следующий файл

# print(len(mean))
# print(results)
# print(*angle, sep='\n')

#plotting results
fig, (ax1, ax2) = plt.subplots(2, 1)

ax1.scatter(results['GMPCPP_temp'], results['GMPCPP_rate'], linewidth=2.0)
ax1.set_title('GMPCPP shortening rate')
ax1.set_xlabel('temperature')
ax1.set_ylabel('rate []')
ax1.grid(True)

ax2.scatter(results['Taxol_temp'], results['Taxol_rate'], linewidth=2.0)
ax2.set_title('Taxol shortening rate')
ax2.set_xlabel('temperature')
ax2.set_ylabel('rate []')
ax2.grid(True)

plt.show()

# print("tau", tau)
# print("A", A)
# print("size tau, A", tau.shape, A.shape)

# with open("output/" + "params.txt", "wb") as f:
#    np.savetxt(f, np.stack([tau, A], axis=1))
# with open("output/" + "power.txt", "wb") as f:
#    np.savetxt(f, power)
