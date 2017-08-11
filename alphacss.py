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
			7a. Merge property:value lists for identical css selectors (and overwrite any previous val for
				identical elements with multiple identical property assignments
					e.g., 
						#box{
							color:red;
						}
						#box{
							color:black;
						}
					results in:
						#box{
							color:black;
						}
	8.  Add 'comments' property to el_dict[el], as list of /* ... */ comments
	9.  Sort elements alphabetically as el_list, ignoring any starting '.' or '#'
	10. Create new css doc formatted for viewing as standard css file	
	
'''

import re
import os
import sys


def main():

	print '----====  alphacss.py  ====----'
	
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
	els 	= [ re.sub('\ {2,}',' ',re.sub('\n\t|\n|\t(?<=\;)','',x).strip().replace('\t',' ')) for x in re.findall('[^{}]*\{[^{}]*\}',doc) ]
	
	for entry in els: 
		
		el = re.search('.*(?={)',entry).group()
		attrs = re.sub('{|}','',re.search('\{(.*?)\}',entry).group())
		
		comment_blocks = re.findall('\/\*[^^]*\*\/',attrs)
		comments = []
		
		for i,c in enumerate(comment_blocks):			# remove comments from attrs list for each element
			attrs = re.sub(re.escape(c),'',attrs)			
			comments = [ tuple(x.split(':')) for x in re.sub('\/\*|\*\/','',c).split(';') if x]

		prop_pair_keys = []			# Transferring to list usage to avoid overwriting dictionary entries for duplicate/conflicting property assignments (both are retained)
		prop_pair_vals = []
		
		for line in attrs.split(';'):
			if not line: continue
			prop_pair = line.split(':')
			if prop_pair[0] in prop_pair_keys:
				print 'Warning: multiple identical property assignments to "%s":\n\t"%s:%s"\n\t"%s:%s"' % (el, prop_pair[0], prop_pair_vals[prop_pair_keys.index(prop_pair[0])], prop_pair[0], prop_pair[1])
				
			prop_pair_keys.append(prop_pair[0])
			prop_pair_vals.append(prop_pair[1])

		if not el_dict.get(el):		
			# add new element to el_dict			
			el_dict[el] = {
				'keys'		: prop_pair_keys,
				'vals'		: prop_pair_vals,
				'props'		: [(prop_pair_keys[i],prop_pair_vals[i]) for i in range(len(prop_pair_keys))],
				'comments'	: comments	
			}

		else:		
			# merge data from identical elements				
			for i in range(len(prop_pair_keys)):
				if prop_pair_keys[i] in el_dict[el][keys]:
					print 'Warning: multiple identical property assignments to "%s":\n\t"%s : %s"\n\t"%s : %s"' % ( el, prop_pair_keys[i], el_dict[el][vals][el_dict[el][keys].index(prop_pair_keys[i])], prop_pair_keys[i], prop_pair_vals[i] )
				el_dict[el][keys].append(prop_pair_keys[i])
				el_dict[el].append(prop_pair_vals[i])
	
	
	# Remake the document
	
	doc = ''
	el_list = sorted(el_dict, key=lambda x: re.sub('^[\.\#]', '', x.lower()) )	# alphabetical element list (ignore # .)		
	for el in el_list:
		doc += '%s{\n' % el
	
		for k,v in sorted(el_dict[el]['props'], key = lambda x: x[0]):			
			doc += '\t%s:%s;\n' % ( k,v )
			# restricting sort to property name only keeps duplicate element property assignments in their original order 

		if not el_dict[el]['comments']: continue
		
		doc += '\t/*\n'
		for c in sorted(el_dict[el]['comments'], key = lambda x: x[0]):
			doc += '\t%s:%s;\n' % ( c[0], c[1] )
		doc += '\t*/\n'
		
	doc += '}\n'

	print doc
	sys.exit()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	with open(filepath, 'w') as f:
		f.write(doc)


if __name__ == '__main__':
	main()