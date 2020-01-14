import sys

file_values = open(sys.argv[3],'r')

R = []

for value in file_values:
    value_clean = value.strip(' ')
    integer_data = int(value_clean,2)
    R.append(integer_data)
    #print(integer_data)


file_values.close()

