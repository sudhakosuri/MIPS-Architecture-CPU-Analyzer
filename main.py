import inst
import reg
import instructionCache
import dataCache
import config
import sys

IF = 0
ID = 0
EX = 0
WB = 0
RAW = 'N'
WAR = 'N'
WAW = 'N'
Struct = 'N'
index = 0
total_Icache_hits = 0
total_Dcache_hits = 0
total_Icache_requests = 0
total_Dcache_requests = 0
hasBranchInstruction = False
length = len(inst.instructions)
fromWriteBack = False
fromExecute = False
iCache_penalty = 2 * (config.memory + config.iCache)
dCache_penalty = 2 * (config.memory + config.dCache)
loop_number = 1
final_instructions = []
Load_StructureHazard = ['LW','SW','SD','S.D','L.D','LD','DADDI','DSUBI','ANDI','ORI']
Double_Add_Sub_StructureHazard = ['ADD.D','ADDD','SUB.D','SUBD']
Integer_Add_Sub_StructureHazard = ['DADD','DSUB']
IsCompleted = False

write_file = open(sys.argv[5],'w+')

class final_instruction:
    def __init__(self, fetch, decode, execute, write_back,raw,war,waw,struct_hazard):
        self.fetch = fetch
        self.decode = decode
        self.execute = execute
        self.write_back = write_back
        self.raw = raw
        self.war = war
        self.waw = waw
        self.struct_hazard = struct_hazard




def fetch(index):
    first_IF = 0
    second_IF = 0
    global IF, total_Icache_hits, total_Icache_requests
    cache_index = (index % length)
    #print(index==0)
    #print("FETCHHHHHHHHHHHHHHHHHHHHHHHH")

    if (index == 0 and loop_number == 1):
        IF = iCache_penalty
        instructionCache.isInstructionCacheMiss(inst.instructions[0], 0)
        #final_instructions[index].fetch = IF
        return
    else:
        #print("index",index)

        #print("Yes",instructionCache.isInstructionCacheMiss(inst.instructions[0], 0))
        #print("No",instructionCache.isInstructionCacheMiss(inst.instructions[1], 1))

        total_Icache_requests += 1
        if(instructionCache.isInstructionCacheMiss(inst.instructions[cache_index],cache_index)):

            #print("Is a miss")
            first_IF = final_instructions[index-1].fetch+iCache_penalty
        else:
            total_Icache_hits += 1
            first_IF = final_instructions[index-1].fetch+config.iCache
            #print("Is not a miss")



        second_IF = final_instructions[index-1].decode
        IF = max(first_IF,second_IF)





def decode(index):
    global ID
    global WAW,RAW,WAR
    cache_index = (index % length)
    first_ID = 0
    second_ID = 0
    third_ID = 0
    fourth_ID = 0

    if(inst.instructions[cache_index].operation == 'HLT'):
        ID = 0
        return

    first_ID = IF + 1

    current_operation = inst.instructions[cache_index].operation
    current_operand1 = inst.instructions[cache_index].operand1
    current_operand2 = inst.instructions[cache_index].operand2
    current_operand3 = inst.instructions[cache_index].operand3


    sec_op = 0
    third_op = 0

    if (index != 0):


        if (current_operation in ('LW','LD','L.D')):
            sec_op = 0
            third_op = 0

            for i in range(index-1, 0, -1):

                cache_index_loop = i % length

                prev_operation = inst.instructions[cache_index_loop].operation
                prev_operand1 = inst.instructions[cache_index_loop].operand1
                prev_operand2 = inst.instructions[cache_index_loop].operand2
                prev_operand3 = inst.instructions[cache_index_loop].operand3

                if ((prev_operation not in ('SW','SD','S.D')) and prev_operand1 == current_operand2 and final_instructions[i].write_back > first_ID):
                    sec_op = final_instructions[i].write_back
                    RAW = 'Y'
            second_ID = sec_op


        if (current_operation in ('SW','SD','S.D')):

            for i in range(index - 1, 0, -1):

                cache_index_loop = i % length

                prev_operation = inst.instructions[cache_index_loop].operation
                prev_operand1 = inst.instructions[cache_index_loop].operand1


                if (prev_operand1 == current_operand1 and final_instructions[i].write_back > first_ID):
                    sec_op = final_instructions[i].write_back
                    RAW = 'Y'
            second_ID = sec_op


        if (current_operation in ('DADD','DSUB','ADD.D','ADDD','SUB.D','SUBD','MULD','MUL.D','DIV.D','DIVD','AND','OR')):

            sec_op = 0
            third_op = 0
            for i in range(index-1, 0, -1):

                cache_index_loop = i % length

                prev_operation = inst.instructions[cache_index_loop].operation
                prev_operand1 = inst.instructions[cache_index_loop].operand1
                prev_operand2 = inst.instructions[cache_index_loop].operand2
                prev_operand3 = inst.instructions[cache_index_loop].operand3

                if ((prev_operation not in ('SW','SD','S.D')) and current_operand2 == prev_operand1 and final_instructions[i].write_back > first_ID):
                    sec_op = final_instructions[i].write_back
                    RAW = 'Y'
                if ((prev_operation not in ('SW','SD','S.D')) and current_operand3 == prev_operand1 and final_instructions[i].write_back > first_ID):
                    third_op = final_instructions[i].write_back
                    RAW = 'Y'
            second_ID = max(sec_op,third_op)

        if (current_operation in ('DADDI','DSUBI','ANDI','ORI')):
            sec_op = 0
            for i in range(index-1, 0, -1):

                cache_index_loop = i % length

                prev_operation = inst.instructions[cache_index_loop].operation
                prev_operand1 = inst.instructions[cache_index_loop].operand1
                prev_operand2 = inst.instructions[cache_index_loop].operand2
                prev_operand3 = inst.instructions[cache_index_loop].operand3

                if ((prev_operation not in ('SW','SD','S.D')) and prev_operand1 == current_operand2 and final_instructions[i].write_back > first_ID):
                    sec_op = final_instructions[i].write_back
                    RAW = 'Y'

            second_ID = sec_op

        if(current_operation in ('DADD', 'DADDI', 'DSUB', 'DSUBI', 'AND', 'ANDI', 'OR', 'ORI')):
            for i in range(index - 1, 0, -1):
                cache_index_loop = i % length

                prev_operation = inst.instructions[cache_index_loop].operation
                if(prev_operation in ('DADD', 'DADDI', 'DSUB', 'DSUBI', 'AND', 'ANDI', 'OR', 'ORI')):
                    if (((final_instructions[i].execute - 1) - (final_instructions[i].decode + 1)) > 1):
                        second_ID = final_instructions[i].execute - 1


        if (current_operation in ('BNE','BEQ')):
            sec_op = 0
            for i in range(index-1, 0, -1):

                cache_index_loop = i % length

                prev_operation = inst.instructions[cache_index_loop].operation
                prev_operand1 = inst.instructions[cache_index_loop].operand1
                prev_operand2 = inst.instructions[cache_index_loop].operand2
                prev_operand3 = inst.instructions[cache_index_loop].operand3

                if ((prev_operation not in ('SW','SD','S.D')) and prev_operand2 == current_operand1 and final_instructions[i].write_back > first_ID):
                    sec_op = final_instructions[i].write_back
                    RAW = 'Y'
                    break

            second_ID = sec_op

        for i in range(index-1, 0, -1):

            cache_index_loop = i % length

            prev_operation = inst.instructions[cache_index_loop].operation
            prev_op1 = inst.instructions[cache_index_loop].operand1
            if (((current_operation not in ('BNE','BEQ', 'J')) or (prev_operation not in ('BNE','BEQ','J'))) and (prev_op1 == current_operand1) and (final_instructions[i].write_back > first_ID)):
                third_ID = final_instructions[i].write_back
                WAW = 'Y'

        first_max = max(first_ID, second_ID)
        ID = max(first_max,third_ID)


    else:
        ID = first_ID




def execute(index):

    global EX, Struct, IsCompleted, hasBranchInstruction, total_Dcache_hits, total_Dcache_requests, fromExecute
    global ID
    first_EX = 0
    second_EX = 0
    dCache_Index = (index % length)
    current_op = inst.instructions[dCache_Index].operation
    isFirst = True
    isDouble = False
    isCacheMiss = False
    isStrucHaz = False

    if (current_op == 'HLT'):
        EX = 0
        return


        EX = 0
        return

    if(current_op in ('LW','LD','L.D','S.D','SW','SD')):
        if(current_op in ('LW','SW')):
            isDouble = False
            first_EX = 0
            total_Dcache_requests += 1

        elif(current_op in ('LD','L.D','SD','S.D')):
            #print("Inside 1")
            isDouble = True
            first_EX = 1
            total_Dcache_requests += 2


        if(index == 0):
            isFirst = 0

            #print("Inside 2")
        else:
            isFirst = 1


        if(dataCache.isDataCacheMiss(inst.instructions[dCache_Index].operand2,inst.instructions[dCache_Index].displacement,isFirst,isDouble)):

            isCacheMiss = True
            second_EX = dCache_penalty
            if(current_op in ('SW','SD','S.D')):
                second_EX += 1
        else:

            if(current_op in ('LW','SW')):
                total_Dcache_hits += 1
            else:
                total_Dcache_hits += 2
            second_EX = config.dCache

        if(isStructuralHazard(index)):
           #print("Inside 5")
            EX = first_EX + second_EX + final_instructions[index-1].execute + 1 - 1
        else:
           #print("Inside 6")
            EX = first_EX + second_EX + ID + 1




    if (current_op in ('DADD', 'DADDI', 'DSUB', 'DSUBI', 'AND', 'ANDI', 'OR', 'ORI','ADD.D','ADDD','SUBD','SUB.D','MUL.D','MULD','DIV.D','DIVD')):

        if (current_op in ('DADD', 'DADDI', 'DSUB', 'DSUBI', 'AND', 'ANDI', 'OR', 'ORI')):

            op1 = int((inst.instructions[dCache_Index].operand1)[1:])
            op2 = int((inst.instructions[dCache_Index].operand2)[1:])

            if(current_op == 'DADD'):
                op3 = int((inst.instructions[dCache_Index].operand3)[1:])
                reg.R[op1] = reg.R[op2] + reg.R[op3]
            elif(current_op == 'DSUB'):
                op3 = int((inst.instructions[dCache_Index].operand3)[1:])
                reg.R[op1] = reg.R[op2] - reg.R[op3]
            elif (current_op == 'AND'):
                op3 = int((inst.instructions[index].operand3)[1:])
                reg.R[op1] = reg.R[op2] & reg.R[op3]
            elif (current_op == 'OR'):
                op3 = int((inst.instructions[index].operand3)[1:])
                reg.R[op1] = reg.R[op2] | reg.R[op3]
            elif (current_op == 'DADDI'):
                op3 = int(inst.instructions[dCache_Index].operand3)
                reg.R[op1] = reg.R[op2] + op3
            elif (current_op == 'DSUBI'):
                op3 = int(inst.instructions[dCache_Index].operand3)
                reg.R[op1] = reg.R[op2] - op3
            elif (current_op == 'ANDI'):
                op3 = int(inst.instructions[dCache_Index].operand3)
                reg.R[op1] = reg.R[op2] & op3
            elif (current_op == 'ORI'):
                op3 = int(inst.instructions[dCache_Index].operand3)
                reg.R[op1] = reg.R[op2] | op3


            if(current_op in ('DADD', 'DADDI', 'DSUB', 'DSUBI', 'AND', 'ANDI', 'OR', 'ORI')):
                for i in range(index - 1, 0, -1):
                    cache_index_loop = i % length
                    prev_operation = inst.instructions[cache_index_loop].operation
                    prev_operation2 = inst.instructions[cache_index_loop-1].operation
                    if ((prev_operation in ('DADD', 'DADDI', 'DSUB', 'DSUBI', 'AND', 'ANDI', 'OR', 'ORI','LD','LW','L.D','SD','S.D')) and ((final_instructions[i].execute>=(ID+2)) and ((ID+2)>=(final_instructions[i].decode+1)))):

                        Struct = 'Y'
                        EX = final_instructions[i].execute + 1
                        break
                    else:
                        EX = ID + 2





        elif(current_op in ('ADD.D','ADDD','SUBD','SUB.D')):

            for i in range(index-1, 0, -1):
                cache_index_loop = i % length
                prev_operation = inst.instructions[cache_index_loop].operation


                if ((prev_operation in Double_Add_Sub_StructureHazard) and final_instructions[i].execute > (ID+1) and config.isAdderPipelined == False):

                    EX = final_instructions[i].execute + config.adder
                    break
                else:

                    EX = ID + config.adder
        elif(current_op in ('MUL.D','MULD')):

            for i in range(index-1, 0, -1):
                cache_index_loop = i % length
                prev_operation = inst.instructions[cache_index_loop].operation
                if (prev_operation in ('MULD','MUL.D') and final_instructions[i].execute > (ID+1) and config.isMultiplierPipelined == False):
                    EX = final_instructions[i].execute + config.multiplier
                    break
                else:
                    EX = ID + config.multiplier

        elif(current_op in ('DIV.D','DIVD')):
            for i in range(index-1, 0, -1):
                cache_index_loop = i % length
                prev_operation = inst.instructions[cache_index_loop].operation
                if (prev_operation in ('DIVD','DIV.D') and final_instructions[i].execute > (ID+1) and config.isDividerPipelined == False):
                    EX = final_instructions[i].execute + config.divider
                    break
                else:
                    EX = ID + config.divider

    if (current_op in ('BNE', 'BEQ')):
        hasBranchInstruction = True
        EX = 0
        if (current_op == 'BNE'):
            oper1_index = int((inst.instructions[dCache_Index].operand1)[1:])
            oper2_index = int((inst.instructions[dCache_Index].operand2)[1:])

            if (reg.R[oper1_index] != reg.R[oper2_index]):
                IsCompleted = False
            else:
                IsCompleted = True

        elif (current_op == 'BEQ'):
            oper1_index = int((inst.instructions[dCache_Index].operand1)[1:])
            oper2_index = int((inst.instructions[dCache_Index].operand2)[1:])

            if (reg.R[oper1_index] == reg.R[oper2_index]):
                IsCompleted = False
            else:
                IsCompleted = True
        elif (current_op == 'J'):
            IsCompleted = False


    if (current_op in ('LW','LD','L.D')):
        found = False
        cache_index = (index+1) % length
        inst_obj = inst.instructions[cache_index]

        for row in instructionCache.I_Cache:
            for instruc in row:
                if inst_obj == instruc:
                    found = True

        if(found == False):
            EX = EX + 4






def write_back(index):
    global WB
    global EX,Struct, fromWriteBack
    cache_index = (index % length)
    current_op = inst.instructions[cache_index].operation

    if (inst.instructions[cache_index].operation == 'HLT'):
        WB = 0
        return

    if (current_op in ('BNE','BEQ')):
        WB = 0
        return

    WB = EX + 1

    for i in range(index-1,0,-1):
        if((WB == final_instructions[i].write_back)):
            EX = EX + 1
            WB = WB + 1
            Struct = 'Y'
            fromWriteBack = True








def isStructuralHazard(index):
    global Struct
    cache_index = (index % length) - 1
    current_operation = inst.instructions[cache_index].operation
    Struct = 'N'


    if ((index != 0) and (((ID + 2) >= (final_instructions[index - 1].decode + 2)) and ((ID + 2) <= (final_instructions[index - 1].execute)))):
        Struct = 'Y'
        return True



    '''if(current_operation in Load_StrutcureHazard):
        for i in range(index-1,0,-1):
            prev_operation = inst.instructions[i].operation
            if (prev_operation in Load_StructureHazard and final_instructions[i].write_back > first_IF):
                return True
        return False'''





def run_Instructions():
    global Struct, WAW, RAW, WAR, index
    total_halts = 0

    for instr in inst.instructions_string:


        index_of_current_instruction = index

        fetch(index_of_current_instruction)
        #print(final_instructions[index_of_current_instruction].IF)
        decode(index_of_current_instruction)
        execute(index_of_current_instruction)
        write_back(index_of_current_instruction)

        #print(index_of_current_instruction)
        final_instructions.append(final_instruction(IF, ID, EX, WB, RAW, WAR, WAW, Struct))
        Struct = 'N'
        WAW = 'N'
        WAR = 'N'
        RAW = 'N'
        print(instr.rstrip('\n'),"\t",final_instructions[index_of_current_instruction].fetch,"\t",final_instructions[index_of_current_instruction].decode,"\t",final_instructions[index_of_current_instruction].execute,"\t",final_instructions[index_of_current_instruction].write_back,"\t",final_instructions[index_of_current_instruction].raw,"\t",final_instructions[index_of_current_instruction].war,"\t",final_instructions[index_of_current_instruction].waw,"\t",final_instructions[index_of_current_instruction].struct_hazard)

        write_file.write(instr.rstrip('\n') + "\t" + str(final_instructions[index_of_current_instruction].fetch)  + "\t" + str(final_instructions[index_of_current_instruction].decode) + "\t" + str(final_instructions[index_of_current_instruction].execute) + "\t" + str(final_instructions[index_of_current_instruction].write_back) + "\t" + final_instructions[index_of_current_instruction].raw + "\t" + final_instructions[index_of_current_instruction].war + "\t" + final_instructions[index_of_current_instruction].waw + "\t" + final_instructions[index_of_current_instruction].struct_hazard + "\n")

        index = index + 1



while True:
    if (IsCompleted):
        break
    else:
        run_Instructions()
        if(not hasBranchInstruction):
            break
        loop_number = loop_number + 1

print("Total number of access requests for instruction cache: "+str(total_Icache_requests+2)+'\n')
print("Number of instruction cache hits: "+str(total_Icache_hits)+'\n')
print("Total number of access requests for data cache: "+str(total_Dcache_requests)+'\n')
print("Number of data cache hits: "+str(dataCache.dcache_hits)+'\n')


write_file.write("Total number of access requests for instruction cache: "+str(total_Icache_requests+2)+'\n')
write_file.write("Number of instruction cache hits: "+str(total_Icache_hits)+'\n')
write_file.write("Total number of access requests for data cache: "+str(total_Dcache_requests)+'\n')
write_file.write("Number of data cache hits: "+str(dataCache.dcache_hits)+'\n')

write_file.close()