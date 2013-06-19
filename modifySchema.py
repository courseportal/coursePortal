#!/usr/bin/env python
import os
import sys


from xml.dom.minidom import parse
dom = parse('solr-4.3.0/example/solr/collection1/conf/schema.xml')
x = dom.createElement("field")
x.setAttribute("type","long")
x.setAttribute("name","_version_")
x.setAttribute("indexed","true")
x.setAttribute("stored","true")
y = dom.getElementsByTagName("fields")
y[0].appendChild(x)
f = open ('solr-4.3.0/example/solr/collection1/conf/schema.xml','w')
dom.writexml(f)

