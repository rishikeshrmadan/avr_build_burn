# avr-execute.py

# Authors -  Rishikesh Madan
#           Vishal Indal Gupta

# this program helps to do the following commands
# - Compilation
# - Linking
# - Generating Hex Files 
#   Prerequisite installation:
#		For Linux:
#   	    1.binutils - Tools like the assembler, linker
#   	    2.gcc-avr - The GNU C cross compiler for AVR microcontrollers.
#       	3.avr-libc - Package for the AVR C library, containing many utility functions.
#	    	4."uisp" - Tool for in system programming of AVR microcontrollers.
#   	    5.avrdude - Utility to program AVR microcontroller. It supports the STK500v2 programmer
#			These can be installed with the following commands:
#       		sudo apt update
#       		sudo apt install binutils gcc-avr avr-libc uisp avrdude


# To use this program :
# Inside the folder that contains the C files , execute this script by typing following commands in terminal
# (to store the generated files inside the same folder, rather then on Desktop where the script is originally present)
# $ python /home/vishal/Desktop/avr-CompileBuild.py


import os
import subprocess
import argparse
import platform
import sys

compile_success_flag = 1
parser = argparse.ArgumentParser(description='Build and burn hex files')
parser.add_argument('path', help='Path of the C file', nargs='+', type=str)
parser.add_argument('-b', '--burn', help='Burns the hex file as well if specified', action='store_true')
args = parser.parse_args()

# print(args.path)
c_file_names = []
o_file_names = []
main_addr = args.path[0][0:args.path[0].find(".")]
print(main_addr)
for single_path_arg in args.path:
	addr = single_path_arg[0:single_path_arg.find(".")]
	c_file_names.append(addr+".c")
	o_file_names.append(addr+".o")
hex_file_name = main_addr+".hex"
elf_file_name = main_addr+".elf"
#print(c_file_names,"\n",o_file_names)

try:
	for single_c_file, single_o_file in list(zip(c_file_names, o_file_names)):
		compile_proc = subprocess.Popen(['avr-gcc','-g', '-Os','-mmcu=atmega2560','-c',single_c_file, '-o', single_o_file], stderr = subprocess.PIPE,  stdout = subprocess.PIPE)
		compile_proc.wait()
		(compile_output, compile_error) = compile_proc.communicate()
		if compile_proc.returncode != 0:
			print(compile_error)
			compile_success_flag = 0
			break
		else:
			print("Successfully Compiled Program"+single_c_file	)
	if compile_success_flag == 1:
		link_proc = subprocess.Popen(['avr-gcc','-g', '-mmcu=atmega2560', '-o', elf_file_name]+o_file_names, stderr = subprocess.PIPE,  stdout = subprocess.PIPE)
		link_proc.wait()
		(link_output, link_error) = link_proc.communicate()
		if link_proc.returncode!=0:
			print(link_error)
		else:
			print("Successfully Linked Program!")
			print(link_output)
			hex_create_proc = subprocess.Popen(['avr-objcopy','-j','.text','-j','.data','-O','ihex',elf_file_name,hex_file_name],stderr = subprocess.PIPE,  stdout = subprocess.PIPE)
			hex_create_proc.wait()
			(hex_create_output, hex_create_error) = hex_create_proc.communicate()
			if hex_create_proc.returncode!=0:
				print(hex_create_error)
			else:
				print(hex_create_output)
				print("Successfully Created the Hex file!")
				if args.burn:
					if platform.system() == 'Windows':
						try:
							os.chdir(os.path.expanduser("~\\Desktop\\AVRDude"))
							os.system("avrdude -c stk500v2 -p m2560 -P NEX-USB-ISP -U flash:w:"+hex_file_name+":i")
						except:
							print("Please place AVRDude folder on your Desktop.")
					elif platform.system() == 'Linux':
						os.system("sudo avrdude -c stk500v2 -p m2560 -P /dev/ttyACM0 -U flash:w:"+hex_file_name+":i")
                                        elif platform.system() == 'Darwin':
                                                os.system("avrdude -c stk500v2 -p m2560 -P /dev/tty.usbmodemavrstk5001 -U flash:w:"+hex_file_name+":i")
except KeyboardInterrupt:
	print('You cancelled the operation.')
except IOError:
	print('An error occured trying to read the file.')

