<?xml version="1.0"?>

<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
        xmlns:date="http://exslt.org/dates-and-times"
	    extension-element-prefixes="date"
	    >
	    <xsl:import href="shared.xsl" />

	    <xsl:output method="html" media-type="text/html" version="1.0"
                encoding="UTF-8" indent="yes"/>

	    <xsl:template match="items">
	    <form>
	    <table>
	    <tr><th>Item Name</th><th>Trash</th><th>Lucy</th></tr>
		<xsl:for-each select="item">
			<tr>
			<td>
                               <xsl:call-template name="item">
                                    <xsl:with-param name="item_name"><xsl:value-of select="@NAME"/></xsl:with-param>
                                    <xsl:with-param name="item_id"><xsl:value-of select="@ITEM_ID"/></xsl:with-param>
                                    <xsl:with-param name="item_url"><xsl:value-of select="@ITEM_URL"/></xsl:with-param>
                                    <xsl:with-param name="item_type"><xsl:value-of select="@ITEM_TYPE_ID"/></xsl:with-param>
                                </xsl:call-template>
			</td>
			</tr>
		</xsl:for-each>
	    </table>
            </form>
	    </xsl:template>

</xsl:stylesheet>
