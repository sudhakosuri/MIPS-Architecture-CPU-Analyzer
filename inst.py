import re
import reg
import sys


file_instructions = open(sys.argv[1],'r')



inst_count = 1
labels = []
instructions = []
instructions_string = []
isCompleted = False
LW_SW_Displacement = 0
allowed_operationTypes = ['LW','SW','LD','L.D','S.D','SD','DADD','DADDI','DSUB','DSUBI','AND','ANDI','OR','ORI','ADD.D','ADDD','SUB.D','SUBD','MULD','MUL.D','DIV.D','DIVD','J','BNE','BEQ','HLT']
allowed_integerRegisters = ['R0','R1','R2','R3','R4','R5','R6','R7','R8','R9','R10','R11','R12','R13','R14','R15','R16','R17','R18','R19','R20','R21','R22','R23','R24','R25','R26','R27','R28','R29','R30','R31']
allowed_floatPointRegisters = ['F0','F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12','F13','F14','F15','F16','F17','F18','F19','F20','F21','F22','F23','F24','F25','F26','F27','F28','F29','F30','F31']
load_secondOperand = 0


class instruction:
    def __init__(self, operation, operand1,operand2,operand3,displacement):
        self.operation = operation
        self.operand1 = operand1
        self.operand2 = operand2
        self.operand3 = operand3
        self.displacement = displacement

def isValidOperation(operation):
    if operation.strip(' ') not in allowed_operationTypes:
        return False
    else:
        return True


def hasValidOperands(operation,operands,inst_count):
    global instructions, load_secondOperand
    lengthOfOperands = len(operands)

    if (lengthOfOperands != 1 and operation == 'J'):
        print("Invalid number of operands for the operation J")
        return False
    elif (lengthOfOperands == 2 and (operation not in ('LW','SW','LD','L.D','S.D','SD'))):

        print("Only Load and Store instructions can have two operands")
        return False
    elif ((lengthOfOperands == 3) and (operation not in ('BNE','BEQ','DADD','DADDI','DSUB','DSUBI','AND','ANDI','OR','ORI','ADD.D','ADDD','SUB.D','SUBD','MULD','MUL.D','DIV.D','DIVD'))):
        print("Only Add, Sub, Mult, Div, Or, And, Bne, Beq can have 3 operands")
        return False
    else:
        if (operation == 'LW'):
            load_secondIntegerOperand = (re.search(r"\(([A-Za-z0-9_]+)\)", operands[1])).group(1)
            if ((operands[0].rstrip('\n') not in allowed_integerRegisters) or (load_secondIntegerOperand not in allowed_integerRegisters)):
                print("LW and SW can only have integer registers from R0 to R31")
                return False

        elif(operation in ('LD','L.D')):
            load_secondOperand = (re.search(r"\(([A-Za-z0-9_]+)\)", operands[1])).group(1)
            if ((operands[0].rstrip('\n') not in allowed_floatPointRegisters) or (load_secondOperand not in allowed_integerRegisters)):
                print("LD can only have floating point registers from F0 to F31")
                return False

        elif (operation == 'SW'):
            load_secondIntegerOperand = (re.search(r"\(([A-Za-z0-9_]+)\)", operands[1])).group(1)
            if ((operands[0].rstrip('\n') not in allowed_integerRegisters) or (load_secondIntegerOperand not in allowed_integerRegisters)):
                print("SW can only have integer registers from R0 to R31")
                return False

        elif(operation in ('SD','S.D')):
            load_secondOperand = (re.search(r"\(([A-Za-z0-9_]+)\)", operands[1])).group(1)
            if ((operands[0].rstrip('\n') not in allowed_floatPointRegisters) or (load_secondOperand not in allowed_integerRegisters)):
                print("S.D can only have floating point registers from F0 to F31")
                return False

        elif((operation in ('DADD','DSUB','AND','OR')) and ((operands[0].rstrip('\n') not in allowed_integerRegisters) or (operands[1].rstrip('\n') not in allowed_integerRegisters) or (operands[2].rstrip('\n') not in allowed_integerRegisters))):
            print("Integer Add, Sub, And, Or can only have integer registers")
            return False

        elif ((operation in ('DADDI','DSUBI','ANDI','ORI')) and ((operands[0].rstrip('\n') not in allowed_integerRegisters) or (operands[1].rstrip('\n') not in allowed_integerRegisters) or (not operands[2].rstrip('\n').isdigit()))):
            print("Integer immediate operations -  Add, Sub, And, Or can only have 2 integer registers and a numeric value")
            return False

        elif((operation in ('ADD.D','ADDD','SUB.D','SUBD','MULD','MUL.D','DIV.D','DIVD')) and ((operands[0].rstrip('\n') not in allowed_floatPointRegisters) or (operands[1].rstrip('\n') not in allowed_floatPointRegisters) or (operands[2].rstrip('\n') not in allowed_floatPointRegisters))):
            print("FP Add, Sub, And, Or can only have floating point registers")
            return False

        elif((operation in ('BNE','BEQ')) and (operands[2].rstrip('\n') not in labels)):
            print("The given label not found")
            return False

        if len(operands)==0:
            instructions.append(instruction(operation,None,None,None,None))
        elif len(operands)==1:
            instructions.append(instruction(operation,operands[0].rstrip('\n'),None,None,None))
        elif len(operands)==2:
            global LW_SW_Displacement
            disp = ''
            for i in operands[1]:
                if not i.isnumeric():
                    break
                else:
                    disp = disp + i
            LW_SW_Displacement = int(disp)

            instructions.append(instruction(operation,operands[0].rstrip('\n'),load_secondOperand,None,LW_SW_Displacement))
        else:
            instructions.append(instruction(operation, operands[0].rstrip('\n'), operands[1].rstrip('\n'), operands[2].rstrip('\n'),None))
        return True



def add_Instructions():
    global inst_count
    total_halts = 0

    for line in file_instructions:
        values = []

        line_new = line.strip(' ').upper().rstrip('\n')

        if (line_new.__contains__('HLT')):
            total_halts = total_halts + 1
            if (total_halts == 2):
                continue

        instructions_string.append(line_new)


        if line_new.__contains__(':'):

            interimLabel = line_new.split(':')

            currentLabel = (interimLabel[0]).strip()

            labels.append(currentLabel)
            line_new = interimLabel[1].strip()



        line_new = line_new.rstrip('\n')
        splitLinesBySpace = line_new.split()
        for val in splitLinesBySpace:

            if(val == ','):
                continue
            else:
                values.append(val)



        operation = values[0]
        operands = values[1:]

        for i in range(0,len(operands)):
            operands[i] = operands[i].strip(',')


        isValidOp = isValidOperation(operation)
        if (not isValidOp):
            print("Invalid operation type for instruction ",inst_count," !!!")
            break
        else:
            if(operation == 'HLT'):
                hasValidOpr = hasValidOperands(operation,[],inst_count)
            else:
                hasValidOpr = hasValidOperands(operation,operands,inst_count)
            if (not hasValidOpr):
                break
            else:
                inst_count += 1

    #print("All good")


add_Instructions()


file_instructions.close()
