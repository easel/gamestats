<?xml version="1.0"?>

<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
        xmlns:date="http://exslt.org/dates-and-times"
	    extension-element-prefixes="date"
	    >
	    <xsl:import href="shared.xsl" />
	    <xsl:output method="html" media-type="text/html" version="1.0" 
		encoding="UTF-8" indent="yes"/>

	    <xsl:template match="characters">
	    <ol>
		<xsl:for-each select="character">
		    <li><a href="{@CHARACTER_URL}"><xsl:value-of select="@NAME" /></a></li>
		</xsl:for-each>
	    </ol>
	    </xsl:template>

</xsl:stylesheet>
