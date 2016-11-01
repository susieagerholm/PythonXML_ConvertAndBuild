from lxml import etree
from lxml.etree import ElementTree
from lxml.etree import XSLT
import sys

class FileResolver(etree.Resolver):
    def resolve(self, url, pubid, context):
        return self.resolve_filename(url, context)


def buildXMLDocumentFromDatabase(my_xml, my_xslt):
    my_parser = etree.XMLParser()
    my_parser.resolvers.add( FileResolver() )
    with open(my_xml, 'rt') as f:
        tree = etree.parse(f, my_parser)
    
    
    
    xslt_tree = etree.XML('''\
        <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
        <xsl:template match="/">
	        <BoligListe xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="urn:oio:lbf:1.0.0">
                <xsl:apply-templates select="dataroot/BOLIG_XML"/>
            </BoligListe>  
        </xsl:template>
        
        <xsl:template match="dataroot/BOLIG_XML">
            <BoligStruktur>
                <xsl:apply-templates select="BK_Enhed_id"/>
                <xsl:apply-templates select="dbo_Byggeafsnit.Nummer"/> 
                <xsl:apply-templates select="Kladde"/>  
                <ObjektStatusKode>2</ObjektStatusKode>
                <xsl:apply-templates select="Lejertype"/>
                <xsl:apply-templates select="Opvarmningsform"/>
                <xsl:apply-templates select="KoekkenKunForLejer"/> 
                <xsl:apply-templates select="Garage"/> 
                <xsl:apply-templates select="Carport"/> 
                <xsl:apply-templates select="IndvendigVedligeholdelseLejer"/> 
                <xsl:apply-templates select="UdvendigVedligeholdelseLejer"/> 
                <xsl:apply-templates select="URL"/>         
                <xsl:apply-templates select="BevaegelseshaemmetEgnet"/>         
                <xsl:apply-templates select="HandicappedeHarFortrinsret"/>
                <xsl:apply-templates select="IkkeAktivUdloebNotifikation"/>
                <xsl:apply-templates select="Kollegievaerelse"/>         
                <xsl:apply-templates select="Boligtype"/>         
                <xsl:apply-templates select="LukketForOpskrivning"/> 
                <xsl:apply-templates select="AktueltIndskud"/>         
                <xsl:apply-templates select="AktueltDepositum"/> 
                <xsl:apply-templates select="document('boligudgift.xml')/Boligudgifter/Boligudgift"/>       
                <!-- <xsl:apply-templates select="document('lejekontrakt.xml')/Lejekontrakter/Lejekontrakt"/> -->
                
            </BoligStruktur>
        </xsl:template>
        
        <xsl:template match="BK_Enhed_id">
            <BoligIdentifikationStruktur>
                <BoligUnikIdentifikator><xsl:value-of select="current()"/></BoligUnikIdentifikator>
                <BuildingUnitUniversalIdentifier xmlns="urn:oio:bbr:1.0.0"><xsl:value-of select="current()"/></BuildingUnitUniversalIdentifier>
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
        
        <xsl:template match="Lejertype">
            <BoligLejertypeKode><xsl:value-of select="current()"/></BoligLejertypeKode>   
        </xsl:template>
        
        <xsl:template match="Opvarmningsform">
            <BoligOpvarmningsformKode><xsl:value-of select="current()"/></BoligOpvarmningsformKode>   
        </xsl:template>
        
        <xsl:template match="KoekkenKunForLejer">
            <BoligKoekkenKunForLejerIndikator><xsl:value-of select="current()"/></BoligKoekkenKunForLejerIndikator>  
        </xsl:template>
        
        <xsl:template match="Garage">
            <BoligGarageKode><xsl:value-of select="current()"/></BoligGarageKode>   
        </xsl:template>
        
        <xsl:template match="Carport">
            <BoligCarportKode><xsl:value-of select="current()"/></BoligCarportKode>   
        </xsl:template>
        
        <xsl:template match="IndvendigVedligeholdelseLejer">
            <BoligIndvendigVedligeholdelseLejerKode><xsl:value-of select="current()"/></BoligIndvendigVedligeholdelseLejerKode>   
        </xsl:template>
        
        <xsl:template match="UdvendigVedligeholdelseLejer">
            <BoligUdvendigVedligeholdelseLejerKode><xsl:value-of select="current()"/></BoligUdvendigVedligeholdelseLejerKode>   
        </xsl:template>
        
        <xsl:template match="URL">
            <BoligURLTekst><xsl:value-of select="current()"/></BoligURLTekst>   
        </xsl:template>
        
        <xsl:template match="BevaegelseshaemmetEgnet">
            <BoligBevaegelseshaemmetEgnetIndikator><xsl:value-of select="current()"/></BoligBevaegelseshaemmetEgnetIndikator>   
        </xsl:template>
        
        <xsl:template match="HandicappedeHarFortrinsret">
            <BoligHandicappedeHarFortrinsretIndikator><xsl:value-of select="current()"/></BoligHandicappedeHarFortrinsretIndikator>   
        </xsl:template>
        
        <xsl:template match="IkkeAktivUdloebNotifikation">
            <BoligIkkeAktivUdloebNotifikationIndikator><xsl:value-of select="current()"/></BoligIkkeAktivUdloebNotifikationIndikator>   
        </xsl:template>
        
        <xsl:template match="Kollegievaerelse">
            <BoligKollegievaerelseIndikator><xsl:value-of select="current()"/></BoligKollegievaerelseIndikator>   
        </xsl:template>
        
        <xsl:template match="Boligtype">
            <BoligTypeKode><xsl:value-of select="current()"/></BoligTypeKode>   
        </xsl:template>
        
        <xsl:template match="LukketForOpskrivning">
            <BoligLukketForOpskrivningIndikator><xsl:value-of select="current()"/></BoligLukketForOpskrivningIndikator>   
        </xsl:template>
        
        <xsl:template match="AktueltIndskud">
            <BoligAktueltIndskudBeloeb><xsl:value-of select="current()"/></BoligAktueltIndskudBeloeb>   
        </xsl:template>
        
        <xsl:template match="AktueltDepositum">
            <BoligAktueltDepositumBeloeb><xsl:value-of select="current()"/></BoligAktueltDepositumBeloeb>   
        </xsl:template>
        
        <xsl:template match="Boligudgift">
            <xsl:apply-templates select="BK_Enhed_id"/>  <!--OPRETTE VARIABEL TIL AT HOLDE ENHEDSID?? -->
            <xsl:apply-templates select="Kladde"/>  
            <ObjektStatusKode>2</ObjektStatusKode>
            <xsl:apply-templates select="Start"/>
            <xsl:apply-templates select="Slut"/>
            <xsl:apply-templates select="Beloeb"/>
        </xsl:template>
        
        <xsl:template match="Start">
            <BoligudgiftStartDato><xsl:value-of select="current()"/></BoligudgiftStartDato>   
        </xsl:template>
        
        <xsl:template match="Slut">
            <BoligudgiftSlutDato><xsl:value-of select="current()"/></BoligudgiftSlutDato>   
        </xsl:template>
        
        <xsl:template match="Beloeb">
            <BoligudgiftBeloeb><xsl:value-of select="current()"/></BoligudgiftBeloeb>   
        </xsl:template>
        
        <xsl:template match="Modtager">
            <BoligudgiftModtagerTypeKode><xsl:value-of select="current()"/></BoligudgiftModtagerTypeKode>   
        </xsl:template>
        
        <xsl:template match="IndeholdtHusleje">
            <BoligudgiftIndeholdtIHuslejeIndikator><xsl:value-of select="current()"/></BoligudgiftIndeholdtIHuslejeIndikator>   
        </xsl:template>
        
        <xsl:template match="Beskrivelse">
            <BoligudgiftBeskrivelseTekst><xsl:value-of select="current()"/></BoligudgiftBeskrivelseTekst>   
        </xsl:template>
        
        <xsl:template match="Type">
            <BoligudgiftstypeKode><xsl:value-of select="current()"/></BoligudgiftstypeKode>   
        </xsl:template>
        
        </xsl:stylesheet>'''
    , my_parser)

	
    transform = etree.XSLT(xslt_tree)
    doc_root = tree.getroot()     

    result = transform(doc_root)
    
    print(type(result))
    print(etree.tostring(result, pretty_print = True))
    
buildXMLDocumentFromDatabase("BOLIG_XML_0045_003.xml", "transformer.xls")

