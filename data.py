import sys



file_data = open(sys.argv[2],'r')

data_decimal = []
data_binary =  []

for data_line in file_data:
    data_clean = data_line.strip(' ')
    data_binary.append(data_clean)
    dec_data = int(data_clean,2)
    data_decimal.append(dec_data)


file_data.close()

