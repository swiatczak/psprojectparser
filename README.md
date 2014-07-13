Simple PeopleSoft Project File Parser (coroutine based)
===============

This program reads exported PeopleSoft project file (XML) and splits it into sections each in a separate folder.
Selected types of sections (at the moment: peoplecode and sql) can be processed further to save their content 
without surrounding XML.

![Peoplecode Section with Application Package subfolder](/content/ExtractedSections.png?raw=true "Peoplecode Section with Application Package")

In order to add more sections edit psconstants.py
+ add section type to the EXTENSIONS dictionary. 'flds' key includes a list of tags that contain the data to be extracted.
  
+ INSTANCE_START_TAG, INSTANCE_END_TAG define section's starting and ending markers 
   
+ NAME_MAP contains mapping of known sections and names of tags containing key fields. These are used to determine section id and a path.
  
+ SQL_TYPES includes various types of SQL objects used by PeopleSoft.
  
+ CLASSES contains mapping of the value of OBJECTTYPE to the name of the type.

Note:
----
* Coroutines and Generators - tutorials and presentations by David Beazley @ http://www.dabeaz.com
* Dealing with reading PeopleSoft generated XML file and possible encoding issues - I used the answer(s) in http://stackoverflow.com/questions/491921/unicode-utf8-reading-and-writing-to-files-in-python
