#!/usr/bin/env python
''' Alphabetize css files 

Usage:
	
	$ python alphacss.py filepath/filename.css
	

Alternative usage (access script in any working directory using a .bashrc function:
	 
in .bashrc:
	
	acss(){
		python path-to-alphacss.py-file `pwd`/$@
	}

Then:

	$ acss filename.css	 	



  Steps:
	1.  Separate out all css elements according to re.findall selector ...{...}
	2.  Remove any \n\t, \n, and \t preceded by ';'
	3.  Replace any remaining \t with ' '
	4.  Replace multiple spaces with single space
	
	5.  Separate element selector from attributes and remove curly braces
	6.  Extract comments from attrs string
	7.  Create dict obj for each css element, composed of css { property1: value1, prop2: val2, ... } pairs
	8.  Add 'comments' property to el_dict[el], as list of /* ... */ comments
	9.  Sort elements alphabetically as el_list, ignoring any starting '.' or '#'
	10. Create new css doc formatted for viewing as standard css file	
	
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
	
	els = [re.sub('\ {2,}',' ',re.sub('\n\t|\n|\t(?<=\;)','',x).replace('\t',' ')) for x in re.findall('[^{}]*\{[^{}]*\}',doc)]
	
	for entry in els: 
		el = re.search('.*(?={)',entry).group()
		attrs = re.sub('{|}','',re.search('\{(.*?)\}',entry).group())
		comments = re.findall('\/\*[^^]*?\*\/',attrs)
		for c in comments:
			attrs = re.sub(re.escape(c),'',attrs)
			
		el_dict[el] = {x.split(':')[0].strip():x.split(':')[1].strip() for x in [y for y in attrs.split(';') if y.strip()] if x.strip()} 
		el_dict[el]['comments'] = comments


	el_list = sorted(el_dict, key=lambda x: re.sub('^[\.\#]', '', x.lower()) )
	

	#gratuitous one-liner for new css doc generation
	doc = '\n'.join( '%s{%s\n}' % (el, '\n\t'.join(sorted( '%s:%s;' % (prop, el_dict[el][prop]) if prop != 'comments' else   (  '\n\t'.join([c if (c and len(el_dict[el][prop])) > 1 else '\n\t'+el_dict[el][prop][0] for c in el_dict[el][prop]  ]) ) for prop in el_dict[el]  ) ) ) for el in el_list )

	with open(filepath, 'w') as f:
		f.write(doc)


if __name__ == '__main__':
	main()