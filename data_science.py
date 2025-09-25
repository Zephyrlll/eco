import csv
from rich.progress import track

li = ["年","月","日","植物","草食動物","肉食動物","人間","酸素","二酸化炭素","窒素","水"]
lis = [[],[],[],[],[],[],[],[],[],[],[]]
data = {"年": [],"月": [],"日": [],"植物": [],"草食動物": [],"肉食動物": [],"人間": [],"酸素": [],"二酸化炭素":[],"窒素": [],"水": []}

with open('ecosystem_log.csv', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in track(reader):
       for i in range(len(row)):
           # row = ["年","月","日","植物","草食動物","肉食動物","人間","酸素","二酸化炭素","窒素","水"]
           lis[i].append(int(round(float(row[i]))))

plant = round(sum(lis[3])/len(lis[3]))
herbivore = round(sum(lis[4])/len(lis[4]))
carnivore = round(sum(lis[5])/len(lis[5]))
human = round(sum(lis[6])/len(lis[6]))

print(plant,herbivore,carnivore,human)