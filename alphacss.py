#!/usr/bin/env python
''' Alphabetize css files 

Usage:
	
	$ python alphacss.py filename.css
	

Alternative usage (access script in any working directory using a .bashrc function:
	 
in .bashrc:
	
	acss(){
		python path-to-alphacss.py-file `pwd`/$@
	}

Then:

	$ acss filename.css	 	
	
'''

import sys
import os
import re

def main():
	if len(sys.argv) > 1:
		filepath = sys.argv[1]
	else:
		print 'Supply filename as argument'
		sys.exit()
		
	with open(filepath,'r') as f:
		doc = f.read()
	
	with open(filepath + '_original', 'w') as f:	#save original css file
		f.write(doc)
	
	el_dict = {}
	els = re.findall('[^{}]*\{[^{}]*\}',doc)
	#print els
	
	for entry in els: 
		el = re.search('.*\w+[^{]*',entry)
		if not el: continue
		if el in el_dict:
			print 'Warning: Found multiple instances of:',el
			sys.exit()
			
		el_dict[el.group()] = entry
	
	#print sorted(el_dict, key=lambda x: re.search('\w.*',x.lower() ).group() )
	
	doc = ''.join( [el_dict[y] for y in sorted(el_dict, key=lambda x: re.search('\w+.*',x.lower()).group()) ] )
	
	with open(filepath, 'w') as f:
		f.write(doc)


if __name__ == '__main__':
	main()