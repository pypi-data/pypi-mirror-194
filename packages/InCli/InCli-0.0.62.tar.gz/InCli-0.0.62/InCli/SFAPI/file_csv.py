from . import  file

def read_as_lists(filepath):
    filepath = file.addExtension(filepath,".csv")

    lineslist = []
    f = open(f'{filepath}', 'r',encoding='utf-8-sig')
    lines = f.readlines()

    for line in lines:
        linelist = line.split(";")
        i = 0
        while i < len(linelist):
            linelist[i] = linelist[i].rstrip("\n")
            if linelist[i] == '':   #$$$$ Should there be a NULL?
                linelist[i] = None
            i = i +1

        lineslist.append(linelist)

    return lineslist

def read(filepath):
    filepath = file.addExtension(filepath,".csv")

    f = open(f'{filepath}', 'r',encoding='utf-8-sig')

    #f = open(f'{filepath}', 'r')
    lines = f.readlines()

    firstline = True    
    fieldsMap = []
    headers = None

    for line in lines:
        field = {}
        if firstline == True:
            headers = line.split(";")
            firstline = False
            continue

        items = line.split(";")

        i = 0
        for he in headers:
            value = items[i].rstrip("\n")
            if value == '':
                value = None
            field[he.rstrip("\n")] = value
            i = i +1

        fieldsMap.append(field)

    return fieldsMap

def write(filepath,obj):
    filepath = file.addExtension(filepath,".csv")
    f = write_open(filepath,obj,mode='w',header=True)
    write_close(f)
    return file.abspath(filepath)

def write_open(filepath,objects,mode="w",header=False):
    filepath = file.addExtension(filepath,".csv")
    f = open(filepath,mode)     

    write_objects(f,objects,header)
     
    return f

def write_objects(f,objects,header=False):
    def write_obj(obj):
        values = []
        for key in obj.keys():
            values.append(str(obj[key]))
        line = ";".join(values)
        print(line,file=f)       

    if header == True:
        if type(objects) is dict:
            keys = list(objects.keys())
        if type(objects) is list:
            keys = list(objects[0].keys())
        line = ";".join(keys)
        print(line,file=f)   

    if type(objects) is list:
        for obj in objects:
            write_obj(obj)   
    if type(objects) is dict:
        write_obj(objects)   

def write_close(f):
    f.close()