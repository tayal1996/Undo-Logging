import sys

def get_variable_between_brackets(transaction):
	var = transaction[transaction.find("(")+1:transaction.find(")")]
	if var.find(',') == -1:
		return var.strip()
	var1,var2 = var.split(',')
	return var1.strip(),var2.strip()

def print_dict(mydict):
	s = ''
	for key,value in mydict.items():
		if value != None:
			s = s + key + ' ' + str(value) + ' '
	return s[0:-1]

def is_empty(mydict):
	for key,value in mydict.items():
		if value != []:
			return False
	return True

def execute_x_lines(lines,main_memory,disk,extra_var,key):
	temp_output = []
	for transaction in lines:
		if transaction.find('READ') != -1:
			var1,var2 = get_variable_between_brackets(transaction)
			if var1 not in disk:
				print("Not found: ",var1)
				exit(0)
			if main_memory[var1] == None:
				main_memory[var1] = disk[var1]
			extra_var[var2] = main_memory[var1]
		elif transaction.find('WRITE') != -1:
			var1,var2 = get_variable_between_brackets(transaction)
			if var1 not in disk:
				print("Not found: ",var1)
				exit(0)
			temp_output.append('<'+key+', '+var1+', '+str(main_memory[var1])+'>')
			main_memory[var1] = extra_var[var2]
			temp_output.append(print_dict(main_memory))
			temp_output.append(print_dict(disk))
		elif transaction.find('OUTPUT') != -1:
			var1 = get_variable_between_brackets(transaction)
			disk[var1] = main_memory[var1]
		elif transaction.find('=') != -1:
			var1 = transaction[0:transaction.find(":")].strip()
			if transaction.find('+') != -1:
				op = '+'
			elif transaction.find('-') != -1:
				op = '-'
			elif transaction.find('*') != -1:
				op = '*'
			elif transaction.find('/') != -1:
				op = '/'
			else:
				print("Invalid operator")
				exit(0)
			var2 = transaction[transaction.find("=")+1:transaction.find(op)].strip()
			var3 = transaction[transaction.find(op)+1:].strip()
			if var2 in extra_var:
				var2 = extra_var[var2]
			else:
				var2 = int(var2)
			if var3 in extra_var:
				var3 = extra_var[var3]
			else:
				var3 = int(var3)
			if op == '+':
				extra_var[var1] = var2 + var3
			elif op == '-':
				extra_var[var1] = var2 - var3
			elif op == '*':
				extra_var[var1] = var2 * var3
			elif op == '/':
				extra_var[var1] = var2 / var3
		else:
			print("Invalid Transactions Input")
			exit(0)

	return temp_output

#run python3 undo_log.py input.txt 3
def main():
	filename = sys.argv[1]
	x = int(sys.argv[2])
	
	file = open(filename,'r').read().splitlines()
	disk = {}
	main_memory = {}
	initial_val = file[0].split()
	for i in range(0,len(initial_val),2):
		disk[initial_val[i]] = int(initial_val[i+1])
		main_memory[initial_val[i]] = None
	
	transactions = {}
	flag_start = {}
	i = 1
	while i < len(file):
		if file[i] !=  '':
			trans_name,no_of_lines = file[i].split()
			flag_start[trans_name] = False
			transactions[trans_name] = file[i+1:i+int(no_of_lines)+1]
			i = i+int(no_of_lines)+1
		i += 1

	final_output = []
	extra_var = {}
	while is_empty(transactions) == False:
		for key,value in transactions.items():
			if flag_start[key] == False:
				final_output.append('<START '+key+'>')
				final_output.append(print_dict(main_memory))
				final_output.append(print_dict(disk))
				flag_start[key] = True
			if len(value) <= x:
				final_output.extend(execute_x_lines(value[0:],main_memory,disk,extra_var,key))
				final_output.append('<COMMIT '+key+'>')
				final_output.append(print_dict(main_memory))
				final_output.append(print_dict(disk))
				transactions[key] = []
			else:
				final_output.extend(execute_x_lines(value[0:x],main_memory,disk,extra_var,key))
				value = value[x:]
				transactions[key] = value

	file = open("undo_log.txt",'w')
	for x in final_output:
		# print(x)
		file.write(x+'\n')
		
	file.close()

if __name__ == "__main__":
	main()
