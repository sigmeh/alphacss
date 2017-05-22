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
		filepath = sys.argv[1]
	with open(filepath,'r') as f:
		doc = f.read()
	
	el_dict = {}
	els = re.findall('[^{}]*\{[^{}]*\}',doc)
	#print els
	
	for entry in els: 
		el = re.search('.*\w+[^{]*',entry)
		if el in el_dict:
			print 'Warning: Found multiple instances of:',el
			sys.exit()
		el_dict[el.group()] = entry
	
	#print sorted(el_dict, key=lambda x: re.search('\w.*',x.lower() ).group() )
	
	doc = ''.join( [el_dict[y] for y in sorted(el_dict, key=lambda x: re.search('\w+.*',x.lower()).group()) ] )
	
	with open(filepath,'w') as f:
		f.write(doc)
	
	
	pass
if __name__ == '__main__':
	main()