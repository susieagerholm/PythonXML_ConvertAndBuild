from lxml import etree
from lxml.etree import ElementTree
from lxml.etree import XSLT
import sys
import datetime

class FileResolver(etree.Resolver):
    def resolve(self, url, pubid, context):
        return self.resolve_filename(url, context)


def buildXMLDocumentFromDatabase(my_xml, write_to_filename):
    my_parser = etree.XMLParser()
    my_parser.resolvers.add( FileResolver() )
    with open(my_xml, 'rt') as f:
        tree = etree.parse(f, my_parser)
    
     
    xslt_tree = etree.XML('''\
        <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
        <xsl:template match="/">
	        <BoligListe xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="urn:oio:lbf:1.0.0">
                <xsl:apply-templates select="dataroot/XML_BOLIGUDGIFT"/>
            </BoligListe>  
        </xsl:template>
        
        <xsl:template match="dataroot/XML_BOLIGUDGIFT">
            <Boligstruktur>
                <xsl:apply-templates select="BK_Enhed_id"/>
                <xsl:apply-templates select="dbo_Byggeafsnit.Nummer"/>
                <BoligudgiftStruktur>
                    <xsl:apply-templates select="Udgift_id"/>
                    <xsl:apply-templates select="Kladde"/>  
                    <ObjektStatusKode>3</ObjektStatusKode>
                    <xsl:apply-templates select="StartDato"/>
                    <xsl:apply-templates select="SlutDato"/>
                    <xsl:apply-templates select="Beloeb"/>
                    <xsl:apply-templates select="ModtagerType"/>
                    <xsl:apply-templates select="IndeholdtIHusleje"/>
                    <xsl:apply-templates select="Beskrivelse"/>
                    <xsl:apply-templates select="Boligudgiftstype"/>
                </BoligudgiftStruktur>
            </Boligstruktur>              
        </xsl:template> 
        
        <xsl:template match="StartDato">
            <BoligudgiftStartDato><xsl:value-of select="substring(current(), 1, 10)"/></BoligudgiftStartDato>   
        </xsl:template>
        
        <xsl:template match="SlutDato">
            <BoligudgiftSlutDato><xsl:value-of select="substring(current(), 1, 10)"/></BoligudgiftSlutDato>   
        </xsl:template>
        
        <xsl:template match="Beloeb">
            <BoligudgiftBeloeb><xsl:value-of select="current()"/></BoligudgiftBeloeb>   
        </xsl:template>
        
        <xsl:template match="ModtagerType">
            <BoligudgiftModtagerTypeKode><xsl:value-of select="current()"/></BoligudgiftModtagerTypeKode>   
        </xsl:template>
       
        <xsl:template match="IndeholdtIHusleje">
            <BoligudgiftIndeholdtIHuslejeIndikator><xsl:value-of select="current()"/></BoligudgiftIndeholdtIHuslejeIndikator>   
        </xsl:template>
        
        <xsl:template match="Beskrivelse">
            <BoligudgiftBeskrivelseTekst><xsl:value-of select="current()"/></BoligudgiftBeskrivelseTekst>   
        </xsl:template>
        
        <xsl:template match="Boligudgiftstype">
            <BoligudgiftstypeKode><xsl:value-of select="current()"/></BoligudgiftstypeKode>   
        </xsl:template>
        
        <xsl:template match="BK_Enhed_id">
            <BoligIdentifikationStruktur>
                <BoligUnikIdentifikator><xsl:value-of select="substring(current(),2,36)"/></BoligUnikIdentifikator>
                <BuildingUnitUniversalIdentifier xmlns="urn:oio:bbr:1.0.0"><xsl:value-of select="substring(current(),2,36)"/></BuildingUnitUniversalIdentifier>
            </BoligIdentifikationStruktur> 
        </xsl:template>
        
        <xsl:template match="dbo_Byggeafsnit.Nummer">
            <ByggeafsnitIdentifikationStruktur>
                <ByggeafsnitUnikIdentifikator>MISSING_INFO</ByggeafsnitUnikIdentifikator>
                <AfdelingIdentifikationStruktur>
                    <AfdelingUnikIdentifikator>MISSING_INFO</AfdelingUnikIdentifikator>
                    <BoligorganisationIdentifikationStruktur>
                        <BoligorganisationUnikIdentifikator>MISSING_INFO</BoligorganisationUnikIdentifikator>
                        <BoligorganisationIdentifikator><xsl:value-of select="preceding-sibling::*[2]"/></BoligorganisationIdentifikator>
                    </BoligorganisationIdentifikationStruktur>
                    <AfdelingIdentifikator><xsl:value-of select="preceding-sibling::*[1]"/></AfdelingIdentifikator>
                </AfdelingIdentifikationStruktur>
                <ByggeafsnitIdentifikator><xsl:value-of select="current()"/></ByggeafsnitIdentifikator>
            </ByggeafsnitIdentifikationStruktur>
        </xsl:template>
        
        <xsl:template match="Udgift_id">
            <BoligudgiftIdentifikationStruktur>
                <BoligudgiftUnikIdentifikator>current()</BoligudgiftUnikIdentifikator>
                <EksternReference>TEST</EksternReference>
            </BoligudgiftIdentifikationStruktur>
        </xsl:template>
        
        <xsl:template match="Kladde">
            <xsl:choose>
                <xsl:when test="current() = 0">
                    <Kladde>false</Kladde>
                </xsl:when>
                <xsl:otherwise>
                    <Kladde>true</Kladde>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:template>
        
                
        </xsl:stylesheet>'''
    , my_parser)

	
    transform = etree.XSLT(xslt_tree)
    doc_root = tree.getroot()     

    result = transform(doc_root)
    
    print(etree.tostring(result, pretty_print = True))
    
    et = etree.ElementTree(result.getroot())
    et.write(write_to_filename, pretty_print=True)
    
    
buildXMLDocumentFromDatabase("boligudgift.xml", "final_result.xml")

