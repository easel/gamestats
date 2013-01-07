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
	    <xsl:import href="dropdowns.xsl"/>

	    <xsl:template match="page">
		<html><head>
		    <script src="YAHOO.js" type="text/javascript" /><script 
		    src="connection.js" type="text/javascript" /><script src="shared.js" 
		    type="text/javascript" />
		    <title><xsl:value-of select="@title"/></title></head>
		<body>
		<p>
		<xsl:if test="@SKIP and @COUNT">
		<xsl:if test="@SKIP > 0">
		<a href="?skip={@SKIP-50}&amp;count={@COUNT}">Previous</a>
		</xsl:if>
		&#160;<a href="?skip={@SKIP+50}&amp;count={@COUNT}">Next</a>
		</xsl:if>
		</p>
		<xsl:call-template name="body_top"/>
		<xsl:apply-templates />
		<xsl:if test="@SKIP and @COUNT">
		<xsl:if test="@SKIP > 0">
		<a href="?skip={@SKIP-50}&amp;count={@COUNT}">Previous</a>
		</xsl:if>
		<p>
		&#160;<a href="?skip={@SKIP+50}&amp;count={@COUNT}">Next</a>
		</p>
		</xsl:if>
		</body>
		</html>
	    </xsl:template>

         <xsl:template name="body_top">
         <h1>Undivided Faith Database</h1>
         <h2>Tools / Reports</h2>
         <ul>
			<li><a href="eqlogdb.msi">Download</a> the parser.</li>
			<li><a href="index.spy">Recent Loots</a></li>
			<li><a href="stats.spy">90 Day Loot Statistics</a></li>
			<li><a href="stats.spy?days=180">180 Day Loot Statistics</a></li>
			<li><a href="stats.spy?days=270">270 Day Loot Statistics</a></li>
			<li><a href="attendance.spy">Attendance Statistics</a></li>
			<li><a href="item_freq.spy">Item Statistics</a></li>
		 </ul>

         <h2>Search</h2>
         <form method="get" action="characters.spy">
         <p>
         <input type="text" name="playerQuery" />
         <input type="submit" value="Search" />
         </p>
         </form>
         <h3>Players</h3>
         <p><a href="characters.spy?character_type=1">View All</a></p>
         <h3>Items</h3>
         <form method="get" action="items.spy"> 
         <p>
         <input type="text" name="itemQuery" />
         <input type="submit" value="Search" />
         </p>
         </form>
         <p><a href="items.spy">View All</a></p>
         </xsl:template>

         <xsl:template match="item">
                <a target="lucy" href="http://lucy.allakhazam.com/itemlist.html?searchtext={@NAME}">Lucy</a>
         </xsl:template>

	    <xsl:template name="item">
	    <xsl:param name="item_key"/>
		<xsl:param name="item_name"/>
		<xsl:param name="item_id"/>
		<xsl:param name="item_url"/>
		<xsl:param name="item_type">None</xsl:param>
		<xsl:if test="$item_type != 'None'">
		    <xsl:call-template name="item_type">
			<xsl:with-param name="field_id">item_<xsl:value-of select="$item_key"/></xsl:with-param>
			<xsl:with-param name="item_id"><xsl:value-of select="$item_id"/></xsl:with-param>
			<xsl:with-param name="selected"><xsl:value-of select="$item_type"/></xsl:with-param>
		    </xsl:call-template>
		</xsl:if>
		<a href="{$item_url}"><xsl:value-of select="$item_name"/></a>&#160;--&#160;<a target="lucy" 
		    href="http://lucy.allakhazam.com/itemlist.html?searchtext={$item_name}">Lucy</a>
	   
	    </xsl:template>

           <xsl:template match="loots">
		<table>
		<tr><th>Time</th><th>Item</th><th>Player</th></tr>
                <xsl:for-each select="gamestats.loot">
                        <tr>
			    <td><xsl:call-template name="date"><xsl:with-param name="date"><xsl:value-of 
				select="@EVENT_TIMESTAMP" /></xsl:with-param></xsl:call-template>
			    </td>
			    
			    <td>
				<xsl:call-template name="item">
					<xsl:with-param name="item_key"><xsl:value-of select="@LOOT_ID"/></xsl:with-param>
				    <xsl:with-param name="item_name"><xsl:value-of select="@ITEM_NAME"/></xsl:with-param>
				    <xsl:with-param name="item_id"><xsl:value-of select="@ITEM_ID"/></xsl:with-param>
				    <xsl:with-param name="item_url"><xsl:value-of select="@ITEM_URL"/></xsl:with-param>
				    <xsl:with-param name="item_type"><xsl:value-of select="@ITEM_TYPE_ID"/></xsl:with-param>
				</xsl:call-template>
			    </td>
			    
			    <td><a href="{@PLAYER_URL}"><xsl:value-of select="@PLAYER_NAME" /></a></td>
			</tr>
                </xsl:for-each>
		</table>
            </xsl:template>

	<xsl:template name="date">
	    <xsl:param name="date"/>
	    <!--<xsl:value-of select="date:day-abbreviation($date)"/>,&#160; -->
	    <!--	<xsl:value-of select="date:month-abbreviation($date)"/>-->
	    <xsl:value-of select="date:month-in-year($date)"/>/<xsl:value-of 
	    select="date:day-in-month($date)"/>/<xsl:value-of select="date:year($date)"/>
	</xsl:template>

	<xsl:template name="timestamp">
	    <xsl:param name="date"/>
	    <!--<xsl:value-of select="date:day-abbreviation($date)"/>,&#160; -->
	    <!--	<xsl:value-of select="date:month-abbreviation($date)"/>-->
	    <xsl:value-of select="date:month-in-year($date)"/>/<xsl:value-of 
	    select="date:day-in-month($date)"/>/<xsl:value-of select="date:year($date)"/>
	    &#160;<xsl:value-of select="date:hour-in-day($date)"/>:<xsl:value-of 
select="date:minute-in-hour($date)"/> EST
	</xsl:template>


	<xsl:template name="duration">
	    <xsl:param name="start"/>
	    <xsl:param name="end"/>
	    <xsl:value-of select="date:date($start)"/>&#160;<xsl:value-of 
		select="date:time($start)"/> for
	    <xsl:call-template name="duration2"><xsl:with-param name="duration"><xsl:value-of 
		select="date:difference($start, $end)"/></xsl:with-param></xsl:call-template>
	</xsl:template>

	<xsl:template name="duration2">
	<xsl:param name="duration"></xsl:param> <!-- duration string -->
	<!-- hours -->
	<xsl:if test="date:seconds($duration) div 3600 > 1">
	    <xsl:value-of select="floor(date:seconds($duration) div 3600)"/> hrs
	</xsl:if>
	<!-- minutes -->
	<xsl:if test="date:seconds($duration) div 60 > 1">
	    <xsl:value-of select="floor(date:seconds($duration) mod 3600 div 60)"/> mins
	</xsl:if>
	<!-- seconds -->
	<xsl:value-of select="date:seconds($duration) mod 60"/> secs<xsl:text/>
	</xsl:template>





</xsl:stylesheet>
