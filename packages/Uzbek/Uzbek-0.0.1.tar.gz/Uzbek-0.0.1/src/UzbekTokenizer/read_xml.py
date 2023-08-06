import xml.etree.ElementTree as et

tree=et.parse('word.xml')

root=tree.getroot()

#ravish=root.findall('word')

for w in root.findall("./[word='avval']"):
    print(w)