<?xml version="1.0"?>
<!--
vim: sw=4 ts=8 smarttab
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
    		doctype-public="-//W3C//DTD XHTML 1.0 Transitional//EN" />

	    <xsl:template match="characters">
	    <h2>Character info for <xsl:value-of select="character/@NAME" /> </h2>
	    <p><a href="characters.spy">All Characters</a>&#160;<a href="index.spy">Console</a></p>
	    </xsl:template>

            <xsl:template match="attendance">
            <h3>Recently seen</h3>
            <ol>
		<p>Total attendance score <xsl:value-of select="//attendance_score/attended/@COUNT"/></p>
                <xsl:for-each select="attended">
                    <li><xsl:call-template name="duration">
			<xsl:with-param name="start"><xsl:value-of select="@START_TIME" /></xsl:with-param>
			<xsl:with-param name="end"><xsl:value-of select="@END_TIME" /></xsl:with-param>
		    </xsl:call-template></li>
                </xsl:for-each>
            </ol>
            </xsl:template>

	    <xsl:template match="lootitems">
		<h3>Raid Items</h3>
		<xsl:call-template name="itemlist" />
	    </xsl:template>

	    <xsl:template match="augitems">
		<h3>Raid Augs</h3>
		<xsl:call-template name="itemlist" />
	    </xsl:template>

	    <xsl:template match="questitems">
		<h3>Rare Quest Items</h3>
		<xsl:call-template name="itemlist" />
	    </xsl:template>

	    <xsl:template name="itemlist">
	    <table>
		<tr><th>Date</th><th>Item</th></tr>
		<xsl:for-each select="item">
		    <tr>
			    <td><xsl:value-of select="@SUBMITTER_USER_ID"/>
				&#160;<xsl:call-template name="timestamp"><xsl:with-param name="date"><xsl:value-of
                                select="@EVENT_TIMESTAMP" /></xsl:with-param></xsl:call-template>
                            </td>
                            <td>
                                <xsl:call-template name="item">
                                    <xsl:with-param name="item_name"><xsl:value-of select="@NAME"/></xsl:with-param>
                                    <xsl:with-param name="item_id"><xsl:value-of select="@ITEM_ID"/></xsl:with-param>
                                    <xsl:with-param name="item_url"><xsl:value-of select="@ITEM_URL"/></xsl:with-param>
                                </xsl:call-template>
			    </td>
		    </tr>
		</xsl:for-each>
	    </table>
	    </xsl:template>

</xsl:stylesheet>
