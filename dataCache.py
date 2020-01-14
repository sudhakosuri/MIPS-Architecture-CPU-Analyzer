import reg

D_Cache = [[0 for x in range(8)] for y in range(2)]




val1 = 0
val2 = 0
val3 = 0
val4 = 0
dcache_hits = 0


def search(current_value, data_value, displacement, isDouble):
    global dcache_hits

    for row in range(0, 2):
        for d_value in range(0, 8):
            if (D_Cache[row][d_value] == current_value):
                dcache_hits += 1
                print(dcache_hits)
                print("Found!!")

                return False

    implement_setAssociativeCache(current_value,data_value, displacement, isDouble)
    #dcache_hits += 1
    return True




def isDataCacheMiss(data_value, displacement, isFirst, isDouble):
    global dcache_hits
    if(isFirst == 0):
        register_index_value = int(data_value[1:])
        current_value = reg.R[register_index_value] + displacement
        implement_setAssociativeCache(current_value,data_value, displacement, isDouble)
        dcache_hits += 1
        return True
    else:
        register_index_value = int(data_value[1:])
        current_value = reg.R[register_index_value] + displacement
        if(isDouble == False):
            return search(current_value,data_value, displacement, isDouble)
        else:
            if(isDouble == True):
                dcache_hits += 1
                return search(current_value+4,data_value, displacement, isDouble)





def implement_setAssociativeCache(current_value,data_value,displacement, isDouble):
    global D_Cache
    register_index_value = int(data_value[1:])
    word_address = current_value
    block_number = int(word_address/4)
    cache_word_address = block_number%4
    set_number = block_number%2


    if(cache_word_address == 1):
        val1 = word_address - 4
        val2 = val1+4
        val3 = val2+4
        val4 = val3+4

    if(cache_word_address == 2):
        val1 = word_address - 8
        val2 = word_address - 4
        val3 = word_address
        val4 = val3 + 4

    if(cache_word_address == 3):
        val1 = word_address - 12
        val2 = word_address - 8
        val3 = word_address - 4
        val4 = word_address

    if (cache_word_address == 0):
        val1 = word_address
        val2 = val1+4
        val3 = val2+4
        val4 = val3+4


    current = "current_MRU_None"
    if(D_Cache[set_number][0] == 0):
        D_Cache[set_number][0] = val1
        D_Cache[set_number][1] = val2
        D_Cache[set_number][2] = val3
        D_Cache[set_number][3] = val4
        current = 'current_MRU_'+str(set_number)+'_0'

    elif (D_Cache[set_number][4] == 0):
        D_Cache[set_number][4] = val1
        D_Cache[set_number][5] = val2
        D_Cache[set_number][6] = val3
        D_Cache[set_number][7] = val4
        current = 'current_MRU_'+str(set_number)+'_1'


    else:
        if(set_number == 0 and current == "current_MRU_0_0"):
            D_Cache[set_number][4] = val1
            D_Cache[set_number][5] = val2
            D_Cache[set_number][6] = val3
            D_Cache[set_number][7] = val4
            current = "current_MRU_0_1"
        elif(set_number == 0 and current == "current_MRU_0_1"):
            D_Cache[set_number][0] = val1
            D_Cache[set_number][1] = val2
            D_Cache[set_number][2] = val3
            D_Cache[set_number][3] = val4
            current = "current_MRU_0_0"
        elif(set_number == 1 and current == "current_MRU_1_0"):
            D_Cache[set_number][4] = val1
            D_Cache[set_number][5] = val2
            D_Cache[set_number][6] = val3
            D_Cache[set_number][7] = val4
            current = "current_MRU_1_1"
        elif(set_number == 1 and current == "current_MRU_1_1"):
            D_Cache[set_number][0] = val1
            D_Cache[set_number][1] = val2
            D_Cache[set_number][2] = val3
            D_Cache[set_number][3] = val4
            current = "current_MRU_1_0"




#print('Added succesfully !!')




'''print(isDataCacheMiss('R5', 12, 1,True))
print("heyyyyyyyyyyyyyyyyyyyyyyy")
print(D_Cache[1][0])
print(D_Cache[1][1])
print(D_Cache[1][2])
print(D_Cache[1][3])
print(D_Cache[1][4])
print(D_Cache[1][5])
print(D_Cache[1][6])
print(D_Cache[1][7])

print(D_Cache[0][0])
print(D_Cache[0][1])
print(D_Cache[0][2])
print(D_Cache[0][3])
print(D_Cache[0][4])
print(D_Cache[0][5])
print(D_Cache[0][6])
print(D_Cache[0][7])

print("hellooooooooooooooooooooooooooo")'''