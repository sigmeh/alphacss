#!/usr/bin/env python
''' Alphabetize css files 

Usage:
	
	$ python alphacss.py filename
	
'''
import sys
import os
import re

def main():
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		print 'Supply filename as argument'
		sys.exit()
		
	with open(filename,'r') as f:
		doc = f.read()
	
	with open(filename + '_original', 'w') as f:	#save original css file
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
	
	with open(filename, 'w') as f:
		f.write(doc)


if __name__ == '__main__':
	main()