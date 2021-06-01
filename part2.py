import csv
#toppers in each subject
def topper(subject):
    with open('Student_marks_list.csv','r') as file:
        csv_reader=csv.DictReader(file)
        max1=0
        name=""
        for line in csv_reader:
            mark=int(line[subject])
            #print(type(mark))
            if mark > max1:
                max1=int(line[subject])
                name=line['Name']
        print("Topper in",subject,"is (",name.strip(),")") 
topper('Maths')
topper('Biology')
topper('English')
topper('Physics')
topper('Chemistry')
topper('Hindi')

#the top 3 students in the class

with open('Student_marks_list.csv','r') as file:
        csv_reader=csv.DictReader(file)
        data=dict()
        toppers=list()
        sum1=0
        for line in csv_reader:
            sum1=int(line['Maths'])+int(line['Biology'])+int(line['English'])+int(line['Physics'])+int(line['Chemistry'])+int(line['Hindi'])
            data[line['Name']]=sum1
        #print(data)
        i=3
        while i>0:
            maxMark=max(data,key=data.get)
            toppers.append(maxMark)
            data.pop(maxMark)
            i-=1
        print("Best students in the class are (",toppers[0].strip(),",",toppers[1].strip(),",",toppers[2].strip(),")")
        
