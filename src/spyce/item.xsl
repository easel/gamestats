<?xml version="1.0"?>

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


    <xsl:template match="//item">
	<h2>Item details for <xsl:value-of select="@NAME" /></h2>
	<p>
	<a target="lucy" href="http://lucy.allakhazam.com/itemlist.html?searchtext={@NAME}">Lucy</a>
	&#160;
	<a href="items.spy">Back to all items</a>
	</p>
    </xsl:template>

    <xsl:template match="//looters">
	<h3>Loot history</h3>
	<ol>
	<xsl:for-each select="looter">
		<li><xsl:call-template name="date"><xsl:with-param name="date"><xsl:value-of 
		    select="@LOOT_TIMESTAMP" /></xsl:with-param></xsl:call-template>
		&#160;<a href="{@PLAYER_URL}"><xsl:value-of select="@PLAYER_NAME" /></a>
		</li>
	</xsl:for-each>
	</ol>
    </xsl:template>

</xsl:stylesheet>
