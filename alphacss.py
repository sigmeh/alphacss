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

import re
import os
import sys


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
	
	'''
	  Create list of css elements from target document
	1. Separate out all css elements according to re.findall selector ...{...}
	2. Remove any \n\t, \n, and \t preceded by ';'
	3. Replace any remaining \t with ' '
	4. Replace multiple spaces with single space
	
	5. Separate element selector from properties and remove curly braces
	use properties as dict entry for each el 
	6. Sort entries, ignoring any starting '.' or '#'
	7. 
	'''
	
	els = [re.sub('\ {2,}',' ',re.sub('\n\t|\n|\t(?<=\;)','',x).replace('\t',' ')) for x in re.findall('[^{}]*\{[^{}]*\}',doc)]
	
	for entry in els: 
		el = re.search('.*(?={)',entry).group()
		attrs = re.sub('{|}','',re.search('\{(.*?)\}',entry).group())
		comment = re.search('\/\*[^^]*\*\/',attrs).group() if re.search('\/\*[^^]*\*\/',attrs) else ''
		if comment:
			attrs = re.sub(re.escape(comment),'',attrs)
		print 'comment',comment
		#attrs = {prop.split(':')[0]:prop.split(':')[1] for prop in re.sub('{|}','',re.search('\{(.*?)\}',entry).group()).split(';') if prop.strip() }
		print 'attrs',attrs
		if not el: continue
		if el in el_dict:
			print 'Warning: Found multiple instances of:',el
			sys.exit()
		
		#print el	
		el_dict[el] = attrs
	
	sys.exit()

	el_list = sorted(el_dict, key=lambda x: re.sub('^[\.\#]', '', x.lower()) )
	
	#for el in el_list:
	#	el_form = '%s{\n%s\n}' % ( el, ''.join([x for x in el_dict[el] ) 
	print el_dict
	
	
	
	doc = ''.join( [el_dict[y] for y in sorted(el_dict, key=lambda x: re.search('\w+.*',x.lower()).group()) ] )
	
	with open(filepath, 'w') as f:
		f.write(doc)


if __name__ == '__main__':
	main()