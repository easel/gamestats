"""
vim: sw=4 ts=8 expandtab
"""

import os 
import libxml2
import libxslt
import StringIO
from elementtree.SimpleXMLWriter import XMLWriter


def printXSLPI(filename):
    print '<?xml-stylesheet href="%s%s" type="text/xml"?>' \
	%('http://vpc-ubuntu-a.quonic.net/~erik/eqlogdb/', filename)
#	%('file:///home/erik/public_html/eqlogdb/', filename)

def setContentType(request, response):
    #os.chdir('/home/erik/public_html/eqlogdb')
    if request['output'] == 'xml':
	response.setContentType('text/xml')
    elif request['output'] == 'text':
	response.setContentType('text/plain')
    else:
	response.setContentType('text/html')
 
def renderXslt(xml, xsltFile):
    styledoc = libxml2.parseFile(xsltFile)
    style = libxslt.parseStylesheetDoc(styledoc)
    doc = libxml2.parseDoc(xml)
    result = style.applyStylesheet(doc, None)
    retval = result.serialize()
    style.freeStylesheet()
    doc.freeDoc()
    result.freeDoc()
    return retval

def getWriter():
    global buf
    buf = StringIO.StringIO()
    w = XMLWriter(buf)
    return w

def renderContent(request, response, xsltFile):
    global buf
    xml = buf.getvalue()
    if request['output'] == 'xml':
	return xml
    elif request['output'] == 'text':
	return renderXslt(xml, xsltFile)
    else:
	return renderXslt(xml, xsltFile)
	
