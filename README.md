# MIPS-Architecture-CPU-Analyzer
The design of an analyzer for a simplified MIPS CPU using Python. The considered MIPS CPU adopts a multi-cycle pipeline processor to dynamically schedule instruction execution and employs caches in order to expedite memory access.
How to run the project
Step1 : Unzip the Simulator folder
Step2: In the extracted folder, makes sure all the files(parser.py, main.py, dataCache.py, instructionCache.py, registers.py and data.py) are present
Step3: Also make sure the txt files(inst.txt, data.txt, reg.txt, config.txt) and script.ksh file are present in the extracted folder.
Step4: Once all the files are present in the folder, open terminal/cmd and run the command : ksh script.ksh
Here, script file will run the command to run the python code. inst.txt, data.txt, reg.txt, config.txt is given as input to the main.py file and the output is printed in result.txt file.
Step5: To verify the results, go to the extracted folder, and open the result.txt. The results consits of the cycle number at 5 stages of processors as IF, ID, EX, ME,WB in the following order, and the hazards if any are present from WAR Hazard, RAW HAzard, WAW Hazard and Structural Hazard in the following order. If any Hazard is present, Y is printed below the same, else N is printed.
