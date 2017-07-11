<h4>alphacss</h4>

<h5>Alphabetize css files</h5>


Usage:
	
	$ python alphacss.py filename.css
	

Alternative usage (access script in any working directory using a .bashrc function:
	 
in .bashrc:
	
	acss(){
		python path-to-alphacss.py-file `pwd`/$@
	}

Then:

	$ acss filename.css	 


By placing in .bashrc, alphacss.py can be run from any working directory. 

The file (filename is a required argument) is parsed using regular expressions and the style selectors are ordered alphabetically. 

A copy of the original css file is also saved. 
