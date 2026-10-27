<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:a="http://www.w3.org/2005/Atom">
  <xsl:output method="html" encoding="UTF-8"/>
  <xsl:template match="/a:feed">
    <html lang="zh-CN">
      <head>
        <meta name="viewport" content="width=device-width,initial-scale=1"/>
        <title>Follow RSI · Atom 订阅</title>
        <style>body{margin:0;background:#f3f3f1;color:#14161c;font:16px/1.8 system-ui,sans-serif}main{max-width:760px;margin:auto;padding:48px 24px}h1{font-size:32px;line-height:1.3}a{color:#2a33d4;overflow-wrap:anywhere}section,article{border-top:1px solid #c9cbd1;margin-top:28px;padding-top:24px}small{color:#656a75}code{overflow-wrap:anywhere;font-size:13px}ul{padding-left:22px}</style>
      </head>
      <body><main>
        <small>Follow RSI · 每天 5 分钟，跟上 RSI 前沿</small>
        <h1>Harness 今日动态 · Atom 订阅</h1>
        <p>把下面的地址添加到 RSS / Atom 阅读器，即可收到经过人工审核的日报。每期日报对应一个订阅条目。</p>
        <p><code><xsl:value-of select="a:link[@rel='self']/@href"/></code></p>
        <p><a href="../daily/">浏览今日动态</a> · <a href="../">阅读证据库</a></p>
        <section>
          <xsl:choose>
            <xsl:when test="a:entry">
              <h2>已发布日报</h2>
              <xsl:for-each select="a:entry"><article>
                <small><xsl:value-of select="a:updated"/></small>
                <h2><a href="{a:link/@href}"><xsl:value-of select="a:title"/></a></h2>
                <p><xsl:value-of select="a:summary"/></p>
              </article></xsl:for-each>
            </xsl:when>
            <xsl:otherwise>
              <h2>首期日报等待人工审核</h2>
              <p>发现的论文还没有正式发布，所以当前没有订阅条目。审核 PR 合并后，日报和此订阅源会自动更新；你可以先保存订阅地址。</p>
              <xsl:if test="a:link[@rel='related']"><p><a href="{a:link[@rel='related']/@href}">查看审核进度 →</a></p></xsl:if>
            </xsl:otherwise>
          </xsl:choose>
        </section>
        <p lang="en"><small>This is an Atom feed of human-reviewed Harness daily editions. An empty feed means the first edition is still awaiting review.</small></p>
      </main></body>
    </html>
  </xsl:template>
</xsl:stylesheet>
