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
        
        <xsl:output method="xml" indent="yes" version="1.0" encoding="UTF-8" 
    		doctype-system="DTD/xhtml1-transitional.dtd"
    		doctype-public="-//W3C//DTD XHTML 1.0 Transitional//EN"  />
	    
	    <xsl:template match="attendance">
		<h2>Attendance Statistics</h2>
		<ul>
		<li><a href="?begin=2005-01-01">Jan 2005 -> present (SLOW be patient)</a></li>
		<li><a href="?begin=2006-01-01&amp;end=2007-01-01">All of 2006</a></li>
		<li><a href="?begin=2007-01-01&amp;end=2007-02-01">January 2007</a></li>
		</ul>
		<h3>attendance for <xsl:call-template name="date"><xsl:with-param 
		    name="date"><xsl:value-of select="@begin"/></xsl:with-param></xsl:call-template> to 
		    <xsl:call-template name="date"><xsl:with-param 
		    name="date"><xsl:value-of select="@end"/></xsl:with-param></xsl:call-template>
		</h3>
		<dl>
		<xsl:for-each select="player">
		    <xsl:if test="preceding-sibling::player[position()=1]/@COUNT != @COUNT or position() = 1">
			<dt><xsl:value-of select="@COUNT"/></dt>
		    </xsl:if>
		    <dd><a href="character.spy?character_id={@CHARACTER_ID}"><xsl:value-of 
		    	select="@NAME"/></a></dd>
		</xsl:for-each>
		</dl>
	    </xsl:template>

</xsl:stylesheet>
