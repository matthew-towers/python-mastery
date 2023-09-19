import os
import time

def follow(filename):
    '''
    Generator that produces a sequence of lines being written at the end of a file.
    '''
    try:
        with open(filename,'r') as f:
            f.seek(0,os.SEEK_END)
            while True:
                 line = f.readline()
                 if line == '':
                     time.sleep(0.1)    # Sleep briefly to avoid busy wait
                     continue
                 yield line
    except GeneratorExit:
        print('Following Done')

# Example use
if __name__ == '__main__':
    for line in follow('Data/stocklog.csv'):
        row = line.split(',')
        name = row[0].strip('"')
        price = float(row[1])
        change = float(row[4])
        if change < 0:
            print('%10s %10.2f %10.2f' % (name, price, change))

# f = open('Data/stocklog.csv')
# f.seek(0, os.SEEK_END)   # Move file pointer 0 bytes from end of file

# Modify the code so that the file-reading is performed by 
# a generator function `follow(filename)`.   Make it so the following code
# works:
# >>> for line in follow('Data/stocklog.csv'):
#           print(line, end='')

# def follow(filename):
#     f = open(filename)
#     f.seek(0, os.SEEK_END)
#     while True:
#         line = f.readline()
#         if line == '':
#             time.sleep(0.1)
#             continue
#         fields = line.split(',')
#         name = fields[0].strip('"')
#         price = float(fields[1])
#         change = float(fields[4])
#         if change < 0:
#             yield '%10s %10.2f %10.2f' % (name, price, change)

# for line in follow('Data/stocklog.csv'):
#     print(line, end='\n')

# while True:
#     line = f.readline()
#     if line == '':
#         time.sleep(0.1)   # Sleep briefly and retry
#         continue
#     fields = line.split(',')
#     name = fields[0].strip('"')
#     price = float(fields[1])
#     change = float(fields[4])
#     if change < 0:
#         print('%10s %10.2f %10.2f' % (name, price, change))
