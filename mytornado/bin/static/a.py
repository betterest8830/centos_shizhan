import sys,os

if __name__ == '__main__':
    for x in os.listdir('xml'):
        if x.endswith('.xml'):
            os.remove('xml/' + x)
            print x
