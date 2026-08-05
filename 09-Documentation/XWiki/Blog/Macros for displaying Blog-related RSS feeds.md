---
id: xwiki-xwiki:Blog.RssCode
type: XWiki Page
space: "Blog"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781907493000
sync_date: 2026-07-21 11:03:41
tags:
  - xwiki/documentation
  - space/blog
---
# Macros for displaying Blog-related RSS feeds

- **Space:** Blog
- **Author:** XWiki.superadmin
- **Last Modified:** 1781907493000
- **Source:** [Macros for displaying Blog-related RSS feeds](https://wiki.systemaops.in/bin/view/Blog/xwiki:Blog.RssCode)

---

{{include reference="Blog.BlogCode"/}}

{{velocity output="false"}}
##
##
##
#**
 * Display a blog as a RSS feed. The output corresponds to the RSS 1.0 specification, and it makes use of the Dublin
 * Core module to specify metadata.
 * 
 * @param blogDoc The XDocument corresponding to the blog to be syndicated.
 * @param entries The entries to display. Usually, these are the last entries belonging to the blog.
 *###
#macro(displayBlogRss $blogDoc $entries)
  ## Create a Jodatime date formatter that will be used to format dates
  #set($dateFormatter = $xwiki.jodatime.getDateTimeFormatterForPattern("yyyy-MM-dd'T'hh:mm:ssZZ"))
  ## Set the right mimetype
  $!response.setContentType('application/rss+xml')##
  #setBlogRssCacheSettings()
  #printBlogRssHeader()
  #printBlogRssChannelDescription($blogDoc $entries)
  #printBlogRssImage($blogDoc)
  #printBlogRssItems($entries)
  #printBlogRssFooter()
#end
##
##
##
#**
 * Display blog entries from all the wiki as a RSS feed. The output corresponds to the RSS 1.0 specification, and it
 * makes use of the Dublin Core module to specify metadata.
 * 
 * @param entries The entries to display. Usually, these are the last entries belonging to the blog.
 *###
#macro(displayGlobalBlogRss $entries)
  ## Create a Jodatime date formatter that will be used to format dates
  #set($dateFormatter = $xwiki.jodatime.getDateTimeFormatterForPattern("yyyy-MM-dd'T'hh:mm:ssZZ"))
  ## Set the right mimetype
  $!response.setContentType('application/rss+xml')##
  #setBlogRssCacheSettings()
  #printBlogRssHeader()
  #printGlobalBlogRssChannelDescription($entries)
  #printWikiRssImage($blogDoc)
  #printBlogRssItems($entries)
  #printBlogRssFooter()
#end
##
##
##
#**
 * Display blog entries belonging to a target category as a RSS feed. The output corresponds to the RSS 1.0
 * specification, and it makes use of the Dublin Core module to specify metadata.
 * 
 * @param blogDoc The XDocument corresponding to the blog to be syndicated.
 * @param categoryDoc The XDocument corresponding to the blog category to be syndicated.
 * @param entries The entries to display. Usually, these are the last entries belonging to the blog.
 *###
#macro(displayBlogCategoryRss $blogDoc $categoryDoc $entries)
  ## Create a Jodatime date formatter that will be used to format dates
  #set($dateFormatter = $xwiki.jodatime.getDateTimeFormatterForPattern("yyyy-MM-dd'T'hh:mm:ssZZ"))
  ## Set the right mimetype
  $!response.setContentType('application/rss+xml')##
  #setBlogRssCacheSettings()
  #printBlogRssHeader()
  #printBlogCategoryRssChannelDescription($categoryDoc $entries)
  #printBlogRssItems($entries)
  #printBlogRssFooter()
#end
##
##
##
#**
 * Set the proper cache settings, both for the client (HTTP headers) and for the server (rendering cache).
 *###
#macro(setBlogRssCacheSettings)
  ## Internally cache the rendered RSS for 30 minutes, for better performance
  ## TODO: This is disabled for security reasons. Since the cache doesn't take into account the current user, it might
  ## serve hidden/unpublished entries to non-creators.
  ## $!xcontext.setCacheDuration(1800)
  ## Instruct the client to cache the response for 1 hour
  #set($expires = $xwiki.jodatime.getMutableDateTime())##
  $!expires.addHours(1)##
  ## TODO: This has no effect, as the core contains a no-cache setting in com.xpn.xwiki.web.Utils
  $!response.setDateHeader('Expires', $expires.millis)##
  $!response.setHeader('Cache-Control', 'public')##
#end
##
##
##
#**
 * Print the start of the RSS: XML declaration and open root element.
 *###
#macro(printBlogRssHeader)
  <?xml version="1.0" encoding="$xwiki.encoding" ?>
  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns="http://purl.org/rss/1.0/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xwiki="https://xwiki.org">
#end
##
##
##
#**
 * Print the blog channel description: title, link, description, logo, creator, copyright, and the list of entries.
 * 
 * @param blogDoc The XDocument corresponding to the blog to be displayed.
 * @param entries The entries to display. Usually, these are the last entries belonging to the blog.
 *###
#macro(printBlogRssChannelDescription $blogDoc $entries)
  <channel rdf:about="$blogDoc.getURL()">
    #getBlogTitle($blogDoc $title)
    <title>$title</title>
    <link>$blogDoc.getExternalURL()</link>
    ## TODO: Add a Description field in the blog class
    <description>$services.localization.render('blog.code.description.space', [$blogDoc.space])</description>
    #getWikiLogo($logoUrl)
    <image rdf:resource="$logoUrl"/>
    <dc:language>$blogDoc.defaultLocale</dc:language>
    <dc:rights>$escapetool.xml($xwiki.spaceCopyright)</dc:rights>
    ## TODO: Usually this is not something meaningful. Maybe add some Blog object properties for these.
    ## <dc:publisher>$escapetool.xml($xwiki.getUserName($blogDoc.author, false))</dc:publisher>
    ## <dc:creator>$escapetool.xml($xwiki.getUserName($blogDoc.creator, false))</dc:creator>
    <items>
      <rdf:Seq>
      ## This is just a list of blog entries, which are detailed below.
      #foreach ($entryDoc in $entries)
        #if($xwiki.hasAccessLevel('view', ${entryDoc.fullName}))
        <rdf:li rdf:resource="$entryDoc.getExternalURL('view', "language=${entryDoc.realLocale}")" />
        #end
      #end
      </rdf:Seq>
    </items>
  </channel>
#end
##
##
##
#**
 * Print the wiki-wide channel description: title, link, description, logo, creator, copyright, and the list of entries.
 * 
 * @param entries The entries to display. Usually, these are the last entries published in the wiki.
 *###
#macro(printGlobalBlogRssChannelDescription $entries)
  #set ($mainDoc = $xwiki.getDocument($services.model.resolveDocument('', 'default', $doc.documentReference.extractReference('WIKI'))))
  <channel rdf:about="$mainDoc.getExternalURL()">
    <title>$escapetool.xml($mainDoc.plainTitle)</title>
    <link>$mainDoc.getExternalURL()</link>
    ## TODO: Add a Description field in the blog class
    <description>$services.localization.render('blog.code.description.wiki')</description>
    #getWikiLogo($logoUrl)
    <image rdf:resource="$logoUrl"/>
    <dc:rights>$escapetool.xml($xwiki.spaceCopyright)</dc:rights>
    <dc:publisher>XWiki</dc:publisher>
    <items>
      <rdf:Seq>
      ## This is just a list of blog entries, which are detailed below.
      #foreach ($entryDoc in $entries)
        #if($xwiki.hasAccessLevel('view', ${entryDoc.fullName}))
        <rdf:li rdf:resource="$entryDoc.getExternalURL('view', "language=${entryDoc.realLocale}")" />
        #end
      #end
      </rdf:Seq>
    </items>
  </channel>
#end
##
##
##
#**
 * Print the blog channel description: title, link, description, logo, creator, copyright, and the list of entries.
 * 
 * @param blogDoc The XDocument corresponding to the blog to be displayed.
 * @param entries The entries to display. Usually, these are the last entries belonging to the blog.
 *###
#macro(printBlogCategoryRssChannelDescription $categoryDoc $entries)
  <channel rdf:about="$categoryDoc.getURL()">
    #set ($macro.rssFeedTitle = $services.localization.render($categoryDoc.getValue('name')))
    #if ($categoryDoc.getObject('XWiki.DocumentSheetBinding').sheet == $blogCategoriesSheet)## Categories home page
      #set ($macro.rssFeedTitle = $categoryDoc.title)
      #if ("$!macro.rssFeedTitle" == '')
        #set ($macro.rssFeedTitle = $services.localization.render('blog.categories.webhome.title'))
      #end
    #end
    <title>$!macro.rssFeedTitle</title>
    <link>$categoryDoc.getExternalURL()</link>
    ## TODO: Add a Description field in the blog class
    <description>$services.localization.render('blog.code.description.category', [$categoryDoc.display('name')])</description>
    <dc:rights>$escapetool.xml($xwiki.spaceCopyright)</dc:rights>
    <items>
      <rdf:Seq>
      ## This is just a list of blog entries, which are detailed below.
      #foreach ($entryDoc in $entries)
        #if($xwiki.hasAccessLevel('view', ${entryDoc.fullName}))
        <rdf:li rdf:resource="$entryDoc.getExternalURL('view', "language=${entryDoc.realLocale}")" />
        #end
      #end
      </rdf:Seq>
    </items>
  </channel>
#end
##
##
##
#**
 * Print the blog image description. Currently, this is the logo of the wiki.
 * 
 * @param blogDoc The XDocument corresponding to the displayed blog.
 *###
#macro(printBlogRssImage $blogDoc)
  #getWikiLogo($logoUrl)
  <image rdf:about="$logoUrl">
    <title>Wiki Logo</title>
    <url>$logoUrl</url>
    <link>$blogDoc.getExternalURL()</link>
  </image>
#end
##
##
##
#**
 * Print the syndicated blog entries. These are the detailed "item"s, which must be referenced above, in the channel
 * description, as otherwise they are ignored.
 * 
 * @param entries The entries to display. Usually, these are the last entries belonging to the blog.
 *###
#macro(printBlogRssItems $entries)
  ## Print all the entry details
  #foreach ($entryDoc in $entries)
    #if($xwiki.hasAccessLevel('view', ${entryDoc.fullName}))
      #printBlogRssItem($entryDoc)
    #end
  #end
#end
##
##
##
#**
 * Print a blog entry in the RSS feed. besides the mandatory RSS elements (title, link, and description), also print
 * some metadata in the Dublin Core vocabulary (creator, categories, date).
 * 
 * @param entryDoc The XDocument corresponding to the displayed blog entry.
 *###
#macro(printBlogRssItem $entryDoc)
  #set($entryUrl = $entryDoc.getExternalURL('view', "language=${entryDoc.realLocale}"))
  #getEntryObject($entryDoc $entryObj)
  #set($desc = $escapetool.xml($services.blog.renderContentHTML($entryDoc, $entryObj, true, true, true)))
  <item rdf:about="$entryUrl">
    <title>$escapetool.xml($entryDoc.getValue('title'))</title>
    <link>$entryUrl</link>
    <description>$desc</description>
    ## Some metadata, using the Dublin Core extension to RSS.
    ## TODO: Display this in a better way.
    <dc:subject>$escapetool.xml($entryObj.display('category', 'view'))</dc:subject>
    ## Map dc:date to the published date. Note that we don't use the last modified date as otherwise any edit to a blog
    ## post would reorder the post. To voluntarily reorder a post, change the published date instead.
    #set ($dcDate = $entryObj.getValue('publishDate').time)
    #if ("$!dcDate" == '')
      ## Fallback in the unlikely case when there's no publication date
      #set ($dcDate = $entryDoc.date.time)
    #end
    <dc:date>$dateFormatter.print($dcDate)</dc:date>
    <dc:creator>$escapetool.xml($xwiki.getUserName($entryDoc.creator, false))</dc:creator>
    ## Add the image URL if there's an image for the blog post. Since RSS 1.0 and Dublin Core don't seem to support
    ## images for feed items, we use an XWiki specific metadata.
    ## Get the image name from the blog post which always contains the name of an attachment located in the blog post
    ## doc.
    #set ($blogPostImageName = $entryObj.getValue('image'))
    #if ("$!blogPostImageName" != '')
      #set ($blogPostImageURL = $services.blog.getExternalAttachmentURL($entryDoc, $blogPostImageName))
      #set ($blogPostImageAttachment = $entryDoc.getAttachment($blogPostImageName))
      <xwiki:image type="$escapetool.xml($blogPostImageAttachment.mimeType)" length="$escapetool.xml($blogPostImageAttachment.longSize)">$escapetool.xml($blogPostImageURL)</xwiki:image>
    #end
    #if($entryDoc.creator != $entryDoc.author)
      <dc:contributor>
        <rdf:Description link="$xwiki.getURL($entryDoc.author)">
          <rdf:value>$escapetool.xml($xwiki.getUserName($entryDoc.author, false))</rdf:value>
        </rdf:Description>
      </dc:contributor>
    #end
  </item>
#end
##
##
##
#**
 * Print the end of the RSS: close the root element.
 *###
#macro(printBlogRssFooter)
  </rdf:RDF>
#end
##
##
##
#**
 * Normally, this should be a Template eXtension, which would be used to display a blog as a RSS feed. Since TX are not
 * yet implemented, the target blog should be passed in the URL. This macro determines exactly which blog should be
 * syndicated. If the "blog" request parameter is not present, then the default Blog is used.
 * 
 * @param blogDoc The resulting XDocument of the target blog.
 *###
#macro(getTargetBlog $blogDoc)
  #if("$!{request.blog}" != '')
    #set($result = $xwiki.getDocument($request.blog))
  #else
    #getBlogDocument('Blog' $result)
  #end
  #set ($blogDoc = $NULL)
  #setVariable ("$blogDoc" $result)
  ## TODO: Check if the document has a Blog.BlogClass object.
#end
##
##
##
#macro(printFieldContent $entryDoc $entryObj $fieldName)
$escapetool.xml($entryDoc.display($fieldName, 'view', $entryObj))#end
##
##
##
#macro(getWikiLogo $logoUrl)
  #set ($path = $xwiki.getSkinFile($xwiki.getSkinPreference('logo', 'logo.png')))
  #set ($port = '')
  #if (($request.scheme == 'http') && ($request.serverPort != 80))
    #set ($port = ":${request.serverPort}")
  #elseif (($request.scheme == 'https') && ($request.serverPort != 443))
    #set ($port = ":${request.serverPort}")
  #end
  #set ($logoUrl = $NULL)
  #setVariable ("$logoUrl" "${request.scheme}://${request.serverName}${port}${path}")
#end
{{/velocity}}

---
**Knowledge Index:** [[09-Documentation/XWiki/00 - openDesk XWiki Master Index]]
