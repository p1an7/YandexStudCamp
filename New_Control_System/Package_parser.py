from Movement import Movement
from Manipulator import take_object_return
p = b'm/123/f/60'
def parse(package):
    m = Movement()
    package = str(package)[2:-1]
    normalize_package = package.split('/')

    return normalize_package
print(parse(p))
    if normalize_package[0]== 'm':
        if normalize_package[1] == '0':
            if normalize_package[2] == 'F':
                for i in int(normalize_package[3]):
                    m.forwardslow()
            elif normalize_package[2] == 'B':
                for i in int(normalize_package[3]):
                    m.backslow()
            elif normalize_package[2] == 'L':
                for i in int(normalize_package[3]):
                    m.leftslow()
            elif normalize_package[2] == 'R':
                for i in int(normalize_package[3]):
                    m.rightslow()
            elif normalize_package[2] == 'S':
                for i in int(normalize_package[3]):
                    m.stop()
        elif normalize_package[1] == '1':
            #TODO Написать поворот на угол
            pass

    elif normalize_package[0] == 's':
        if normalize_package[1] == '0':
            if normalize_package[2] == 'O':
                take_object_return()
            if normalize_package[2] == 'P':
                #TODO написать метод чтобы класть
                pass
            if normalize_package[2] == 'V':
                #TODO
                pass
        if normalize_package[1] == '1':





        elif normalize_package[1] == '1':





