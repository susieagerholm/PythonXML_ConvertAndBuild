import csv
from lxml import etree
from lxml.etree import XPath

def convertToNewUniqueIDs(org_csv):
    with open(org_csv, mode='r') as infile:                                     # open input file with curr and new id (key and value)
        reader = csv.reader(infile)                                             # read input file
        mydict = {rows[0]:rows[1] for rows in reader}                           # create dictionary object from file

    for key in mydict:                                                          # check dictionary is created correctly  
        print (key) #("key: %s , value: %s" % (key, mydict[key]))               
        
    
    tree = etree.parse("HentAlleBoligerPaaAfdelinger_utf8.xml")                 # parse XML from file
    root = tree.getroot()                                                       # get root                      
        
    
	namespaces={'x': 'urn:oio:lbf:1.0.0', 'b': 'urn:oio:bbr:1.0.0'}             # define ns   
    bolig = root.xpath('//x:BoligStruktur', namespaces={'x': 'urn:oio:lbf:1.0.0', 'b': 'urn:oio:bbr:1.0.0'})
    
    if bolig:																	# iterate over bolig
        for item in bolig:
            for unique_id in item.findall('.//x:BoligUnikIdentifikator', namespaces):
                unique_id.text = mydict[unique_id.text]
            
            for unique_build in item.findall('.//b:BuildingUnitUniversalIdentifier', namespaces):
                unique_build.text = mydict[unique_build.text]   

            for mode in item.findall('.//x:ObjektStatusKode', namespaces): 
                mode.text = "2"

            for extern_ref in item.findall('.//x:EksternReference', namespaces):
                extern_ref.getparent().remove(extern_ref)           
            
    
    etree.ElementTree(root).write('uuuuuu.xml', pretty_print=True)  # save back to XML file
     
# remember to check if external reference can be reused...if not the case: just remove all external ref!      
