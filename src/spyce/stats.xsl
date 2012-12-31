<?xml version="1.0"?>
<!-- 
vim:sw=4 ts=8 smarttab
-->

<xsl:stylesheet
	xmlns="http://www.w3.org/1999/xhtml"
	xmlns:xhtml="http://www.w3.org/1999/xhtml"
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
        xmlns:date="http://exslt.org/dates-and-times"
        extension-element-prefixes="date"
    >
    <xsl:import href="shared.xsl" />

    <xsl:output method="html" indent="yes" version="1.0" encoding="UTF-8" 
            doctype-system="DTD/xhtml1-transitional.dtd"
            doctype-public="-//W3C//DTD XHTML 1.0 Transitional//E" />
    
    <xsl:template match="//players">
	<h3>top <xsl:value-of select="@count"/> 
	    gamestats.loot stats for <xsl:value-of select="@range"/></h3>
	<dl>
	<xsl:for-each select="player">
	    <xsl:if test="preceding-sibling::player[position()=1]/@COUNT != @COUNT or position() = 1">
		<dt><xsl:value-of select="@COUNT"/> - <xsl:value-of select="@RATIO" /></dt>
	    </xsl:if>
	    <dd><a href="character.spy?character_id={@CHARACTER_ID}"><xsl:value-of select="@NAME"/></a></dd>
	</xsl:for-each>
	</dl>
    </xsl:template>

</xsl:stylesheet>
