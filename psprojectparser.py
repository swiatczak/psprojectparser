__author__="Janusz Swiatczak"
__date__ ="13/07/2014"
import re
import codecs
import os
import os.path
import xml.etree.ElementTree as ET
import psconstants as ppsc

#
# Reference: David Beazley @ http://www.dabeaz.com
#
def coroutine(func):
    """
        Turn function object into a coroutine.
        use as a decoration:
        @coroutine
        def myCoroutineFunc():
    """
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.next()
        return cr
    return start

def sections(fileobject, targets):
    """
    generate section element stream and pass onto any interested listeners(targets)
    use fileobject to read the data .
    """
    idFunc = lambda x: x
    section = None
    for line in fileobject:
        # section is set only when the section start marker is found (below)
        if section:
            secType = section['type']
            # found? section end marker  
            # determine path
            # construct section content (          
            # generate section id
            if re.search( ppsc.INSTANCE_END_TAG, line):
                section['ftr'] = line
                section['content'] = '<?xml version="1.0" ?>\n' + section['hdr'] + ''.join(section['body']) + section['ftr'].strip()
                if secType in ppsc.NAME_MAP:
                    idFieldNames = ppsc.NAME_MAP[secType]
                    # TODO: optimise to do only once per section type 
                    idFields = [re.compile('<{}>(.*)</'.format(fldName)) for fldName in idFieldNames]
                    # TODO: Rewrite to make it less obscure :( 
                    section['id'] = dict(zip(idFieldNames,[g.search(l).groups()[0] for g in idFields for l in section['body'] if g.search(l) and g.search(l).groups()]))
                    sectionId = section['id']
                    pathRule = ppsc.PATH_KEYS.get(secType) if secType in ppsc.PATH_KEYS else [(p, idFunc) for p in ppsc.NAME_MAP.get(secType)]
                    section['path'] = os.path.join(secType, ''.join([ func(sectionId[pid]) for pid, func in pathRule if func(sectionId[pid]) not in ['NONE', '']]))

                #send to targets even if section is of an unknown type     
                if targets:
                    for target in targets:
                        target.send(section)
                # reset section 
                section = None
            else: # if not - simply add line to section's body
                section['body'].append(line)
        else:
            # initialise section 
            ttt = re.search( ppsc.INSTANCE_START_TAG, line)
            if ttt and ttt.groups():
                section = {'hdr': line, 'type': ttt.groups()[0], 'id': {}, 'body': [], 'ftr': ' '}

@coroutine
def contentExtractor(sectionType, targets):  
    """
    extract content of the specified type and send to any interested target.
    Content type is defined through sectiontype for which the criteria is 
    obtained from the constants.
    """  
    contentFlds = ppsc.EXTENSIONS.get(sectionType)
    if contentFlds:
        while True:
            section = (yield)
            if section['type'] == sectionType:
                sectionXMLData = section['content']
                root = ET.fromstring(sectionXMLData)                
                section['content'] = ''
                for contFld in contentFlds['flds']:
                    nodes = root.findall(".//{}".format(contFld))
                    section['content'] += ''.join([node.text for node in nodes ] ) if nodes else ''

                if targets:
                    for target in targets:
                        target.send(section)

@coroutine
def saveSection(wrkFolder, ext):
    """
    Save section to a file. The path is obtained from the section's 'path' key.
    Create any required directories 
    """
    while True:
        section = (yield)
        if section:
            filename = os.path.join(wrkFolder, '{}.{}'.format(section['path'], ext))
            dirname = os.path.dirname(filename)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            with open(filename, "w") as output:
                output.write(section['content'])

# test
if __name__ == "__main__":
    EXTRACTS = os.path.join(os.getcwd(), 'EXTRACTS')

    pplcdExtractor = contentExtractor('PCM', [saveSection(EXTRACTS, 'peoplecode')])
    sqlExtractor = contentExtractor('SRM', [saveSection(EXTRACTS, 'sql')])
    sections(codecs.open("PROJECT/PROJECT.XML", 'r', "utf-8"), [saveSection(EXTRACTS, 'xml'), pplcdExtractor, sqlExtractor] )
