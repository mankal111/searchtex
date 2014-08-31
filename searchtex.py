# Searches a keyword in a given environment in LaTeX files.
#  
# Created by M. Kalafatis, 11 April 2012
#
# The code is released under the MIT License


import os,re


# The "union" procedure from unit 3
def union(a, b):
	for e in b:
		if e not in a:
        		a.append(e)

# A modified version of "MakeIndex" procedure
def MakeIndex(dir,EnvTitle):
	index = {}
	texFileNames=FindtexFiles(dir)	
	while texFileNames:
		texFileName = texFileNames.pop()
		texFile = open(texFileName)
		data = texFile.read()
		texFile.close()
		for content, lpos, rpos in get_blocks(data, EnvTitle):
			add_content_to_index(index, texFileName, content, lpos, rpos)
	return index	

# This procedure finds and returns the content of the environment with title:EnvTitle 
# and its position inside the file.
def get_content_and_positions(data, EnvTitle, rpos):
	newlpos = data.find('\\begin{'+EnvTitle+'}',rpos)
	if newlpos == -1:
		return None, 0, 0
	newrpos = data.find('\\end{'+EnvTitle+'}',newlpos)
	content = data[newlpos+8+len(EnvTitle):newrpos]	
	return content, newlpos, newrpos

# This procedure returns a list with the blocks of code of given data inside the given 
# environment and their positions inside the file.
def get_blocks(data, EnvTitle):				
	blocks = []					
	lpos, rpos = 0, 0				
	while True:					
		content, lpos, rpos = get_content_and_positions(data,EnvTitle,rpos)
		if content:
			blocks.append([content,lpos,rpos])
		else:
			break
	return blocks

# This procedure returns a list with filenames of type '.tex', in a given directory and its subfolders.
def FindtexFiles(dir): 
	texFiles = []
	for x in os.listdir(dir):
		if os.path.isdir(dir + "/" + x):
			union(texFiles,FindtexFiles(dir + "/" + x))
		if x[len(x)-4:] == ".tex":
			texFiles.append(dir + "/" + x)
	return texFiles

# A modified version of add_page_to_index procedure of unit 4:
def add_content_to_index(index, texFileName, content, lpos, rpos):
	words = re.split("\W+",content)				  # 
	for word in words:
		add_to_index(index, word, texFileName, lpos, rpos)

# A modified version of add_to_index procedure of unit 4.
def add_to_index(index, keyword, texFileName, lpos, rpos):	
	if keyword in index:
        	if not [texFileName,lpos,rpos] in index[keyword]:
			index[keyword].append([texFileName,lpos,rpos])
	else:
		index[keyword] = [[texFileName,lpos,rpos]]

# The 'lookup' procedure.
def lookup(index, keyword):
	if keyword in index:
		return index[keyword]
	else:
		return None

# This procedure prints the results.
def PrintResults(Results):
	while Results:						
		Result = Results.pop()
		texFile = open(Result[0])
		data = texFile.read()
		texFile.close()
		print (11+len(Result[0]))*"-"		
		print "In \""+Result[0]+"\" File:"
		print (11+len(Result[0]))*"-"			
		print data[Result[1]:Result[2]+6+len(environment)]

		

environment = raw_input('Please type the title of the environment in which you would like to search:')
Index = MakeIndex('tex files',environment) # Replace 'tex files' with your tex files folder name. 
keyword = raw_input('Please type a keyword to search in \"'+environment+'\" environment:')
Results = lookup(Index, keyword)
PrintResults(Results)

