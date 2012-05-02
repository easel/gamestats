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
		<h3>Item history</h3>
		<h4>
		    <a href="?item_type_id=5">Rare Quest Items</a> |
		    <a href="?item_type_id=6">Raid Loot</a> |
		    <a href="?item_type_id=7">Augs</a> |
		    <a href="?item_type_id=10">Spell Items</a> 
		</h4>
		<dl>
		<xsl:for-each select="item">
		    <xsl:if test="preceding-sibling::item[position()=1]/@ITEM_COUNT != @ITEM_COUNT or position() = 1">
                        <dt><xsl:value-of select="@ITEM_COUNT"/></dt>
                    </xsl:if>
		    <dd>
		    <a href="item.spy?item_id={@ITEM_ID}">
		    <xsl:value-of select="@ITEM_NAME" />
		    </a>
		    </dd>
		</xsl:for-each>
		</dl>
	    </xsl:template>

</xsl:stylesheet>
