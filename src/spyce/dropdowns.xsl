<?xml version="1.0"?>
<!--
vim: sw=4 ts=8 expandtab
-->

<xsl:stylesheet
	xmlns="http://www.w3.org/1999/xhtml"
	xmlns:xhtml="http://www.w3.org/1999/xhtml"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
    xmlns:date="http://exslt.org/dates-and-times"
    extension-element-prefixes="date"
    >


<xsl:template name="item_type">
<xsl:param name="field_name"></xsl:param>
<xsl:param name="field_id"></xsl:param>
<xsl:param name="item_id"></xsl:param>
<xsl:param name="selected"></xsl:param>
<select name="{$field_name}" id="{$field_id}" onchange="Javascript:setItemType({$item_id}, '{$field_id}')">
<option value=""/>
<xsl:if test="not($selected=1)"><option value="1">Vendor Trash</option></xsl:if>
<xsl:if test="$selected=1"><option selected="selected" value="1">Vendor Trash</option></xsl:if>
<xsl:if test="not($selected=2)"><option value="2">Tradeskill Item</option></xsl:if>
<xsl:if test="$selected=2"><option selected="selected" value="2">Tradeskill Item</option></xsl:if>
<xsl:if test="not($selected=3)"><option value="3">Rare Tradeskill Item</option></xsl:if>
<xsl:if test="$selected=3"><option selected="selected" value="3">Rare Tradeskill Item</option></xsl:if>
<xsl:if test="not($selected=4)"><option value="4">Quest Item</option></xsl:if>
<xsl:if test="$selected=4"><option selected="selected" value="4">Quest Item</option></xsl:if>
<xsl:if test="not($selected=5)"><option value="5">Rare Quest Item</option></xsl:if>
<xsl:if test="$selected=5"><option selected="selected" value="5">Rare Quest Item</option></xsl:if>
<xsl:if test="not($selected=6)"><option value="6">Raid Loot</option></xsl:if>
<xsl:if test="$selected=6"><option selected="selected" value="6">Raid Loot</option></xsl:if>
<xsl:if test="not($selected=7)"><option value="7">Raid Aug</option></xsl:if>
<xsl:if test="$selected=7"><option selected="selected" value="7">Raid Aug</option></xsl:if>
<xsl:if test="not($selected=8)"><option value="8">Trash Loot</option></xsl:if>
<xsl:if test="$selected=8"><option selected="selected" value="8">Trash Loot</option></xsl:if>
<xsl:if test="not($selected=9)"><option value="9">Bazaar Loot</option></xsl:if>
<xsl:if test="$selected=9"><option selected="selected" value="9">Bazaar Loot</option></xsl:if>
<xsl:if test="not($selected=10)"><option value="10">Spell Item</option></xsl:if>
<xsl:if test="$selected=10"><option selected="selected" value="10">Spell Item</option></xsl:if>
</select>
</xsl:template>
</xsl:stylesheet>
