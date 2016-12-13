<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:atom="http://www.w3.org/2005/Atom"
	xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
	xmlns:pncast="http://pncast.ru/static/rss">
<xsl:output method="html" doctype-system="about:legacy-compat" encoding="UTF-8" indent="yes"/>
<xsl:template name="string-replace-all">
	<xsl:param name="text"/>
	<xsl:param name="replace"/>
	<xsl:param name="by"/>
	<xsl:choose>
		<xsl:when test="contains($text,$replace)">
		<xsl:value-of select="substring-before($text,$replace)"/>
		<xsl:value-of select="$by"/>
		<xsl:call-template name="string-replace-all">
			<xsl:with-param name="text" select="substring-after($text,$replace)"/>
			<xsl:with-param name="replace" select="$replace"/>
			<xsl:with-param name="by" select="$by"/>
		</xsl:call-template>
		</xsl:when>
	<xsl:otherwise>
		<xsl:value-of select="$text"/>
	</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<xsl:template match="/">
<html>
<head>
	<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
	<style> @import "/static/style.css" </style>
	<title><xsl:value-of select="rss/channel/title"/></title>
</head>
<body>
<div id="feed-header">
<a><xsl:attribute name="href">
<xsl:variable name="feedlink" select="rss/channel/atom:link/@href" />
<xsl:call-template name="string-replace-all">
	<xsl:with-param name="text" select="$feedlink"/>
	<xsl:with-param name="replace" select="'http'"/>
	<xsl:with-param name="by" select="'pcast'"/>
</xsl:call-template>
</xsl:attribute>
<p>Это поток подкаста, для подписки и прослушивания необходимо импортировать его ссылку в соответствующем приложении.</p></a>
</div>
<div class="content" id="feed-content">
	<div class="container" id="middle">
 		<h1 id="feed-title"><xsl:value-of select="rss/channel/title"/></h1>
		<p id="feed-description"><xsl:value-of select="rss/channel/description"/></p>
		<div id="feed-items">
			<xsl:for-each select="rss/channel/item">
				<div class="feed-item">
                                        <xsl:variable name="postnaukalink" select="link"></xsl:variable>
					<h3><a><xsl:attribute name="href"><xsl:value-of select="$postnaukalink"/></xsl:attribute><xsl:value-of select="title"/></a></h3>
					<ul><xsl:for-each select="pncast:theme">
						<li><a><xsl:attribute name="href">/theme/<xsl:value-of select="@id"/>/rss.xml</xsl:attribute><xsl:value-of select="text()"/></a></li>
					</xsl:for-each></ul>
					<p><xsl:value-of select="itunes:summary"/>.</p>
					<div class="feed-item-attachment">
						<p><a><xsl:attribute name="href"><xsl:value-of select="enclosure/@url"/></xsl:attribute><xsl:value-of select="enclosure/@type"/></a> 
						<span id="item-len"><xsl:value-of select='format-number(enclosure/@length div 1048576, "#.0")'/> МБ</span>
						</p>
					</div>
				</div>
			</xsl:for-each>
		</div>
	</div>
</div>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
