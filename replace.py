import sys

def execute_codes(__code_line__, value, line_number):
	exec __code_line__
	return value

def execute_lines(__code_line__, line, line_number, data):
	exec __code_line__
	return data

def main():
	srep_data = file(sys.argv[1], "r").readlines()
	
	template = ""
	output_file = ""
	input_data = []
	line_code = []
	codes = {}
	current_code = ""
	section = ""
	
	for line in srep_data:
		line = line.strip()
		
		if line == "[data]":
			section = "data"
			
		elif line == "[line]":
			section = "line"
			
		elif line == "[process]":
			section = "process"
		
		elif line != "":
			if section == "data":
				if line.find("input") == 0:
					input_data = file(line[6:], "r").readlines()
				
				elif line.find("output") == 0:
					output_file = line[6:].strip()
				
				elif line.find("template") == 0:
					template = file(line[9:], "r").read()
			
			elif section == "line":
				line_code.append(line)
			
			elif section == "process":
				if line[0] == "$":
					codes.setdefault(line)
					codes[line] = []
					current_code = line
				
				elif current_code != "":
					codes[current_code].append(line)
	
	data_processed = []
	
	n = 1
	for line in input_data:
		line = line.strip()
		data = []
		
		for le in line_code:
			data = execute_lines(le, line, n, data)
		
		i = 1
		for p in data:
			indx = "$%i" %i
			if codes.has_key(indx):
				value = p
				for le in codes[indx]:
					value = execute_codes(le, value, n)
				
				data[i - 1] = value
				
			i += 1
		
		n += 1
		data_processed.append(data)
	
	out = ""
	for data in data_processed:
		i = 1
		tmp = template
		for arg in data:
			tmp = tmp.replace("$%i" %i, data[i - 1])
			i += 1
		
		out += tmp + "\n"
	
	f = open(output_file, "w+")
	f.write(out)
	f.close()
	
	print "sucess"

main()