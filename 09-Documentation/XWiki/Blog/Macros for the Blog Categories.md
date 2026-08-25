---
id: xwiki-Blog.CategoriesCode
type: XWiki Page
space: "Blog"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781907492000
sync_date: 2026-08-25 21:14:26
tags:
  - xwiki/documentation
  - space/blog
---
# Macros for the Blog Categories

- **Space:** Blog
- **Author:** XWiki.superadmin
- **Last Modified:** 1781907492000
- **Source:** [Macros for the Blog Categories](https://wiki.systemaops.in/bin/view/Blog/Blog.CategoriesCode)

---

{{include reference="Blog.BlogCode"/}}

{{velocity output="false"}}
##
##
##
#**
 * Retrieves the list of blog entries from a given category. Entries belonging to subcategories
 * are not returned.
 * 
 * @param category The name of the category (XDocument full name, for example 'MyBlog.Fishing').
 * @param entries Return parameter, where the list of entries is placed.
 * @param totalEntries Return parameter, where the total number of entries belonging to this category is
 *        placed. Useful for a paginated view.
 *###
#macro(getEntriesForCategory $category $entries $totalEntries)
  #set ($entries = $NULL)
  #set ($totalEntries = $NULL)
  #if ("$!{blogCategoryEntriesCache.containsKey($!{category})}" == 'true')
    #setVariable ("$entries" $blogCategoryEntriesCache.get($!{category}).get(0))
    #setVariable ("$totalEntries" $blogCategoryEntriesCache.get($!{category}).get(1))
    #preparePagedViewParams ($totalEntries 10)
  #else
    #getCategoriesHierarchy ('' $tree)
    #set ($subcategories = [])
    #getSubcategories ($tree $category $subcategories)
    #set ($categories = [])
    ## check if it a categories space
    #set ($categoryDoc = $xwiki.getDocument($category))
    #if ("$!categoryDoc.getObject($blogCategoryClassname)" != '')
      #set ($discard = $categories.add($category))
    #end
    #set ($discard = $categories.addAll(${subcategories}))
    #getAllBlogPostsQuery($query)
    #set ($query = ", DBStringListProperty as categories join categories.list as category${query} and obj.id = categories.id.id and categories.id.name='category' and category in (:categories)")
    #if ($categories.size() > 0)
      #set ($totalResult = $services.query.hql($query).bindValue('categories', $categories).addFilter("unique").count())
      #preparePagedViewParams ($totalResult 10)
      #set ($result = $services.query.hql("${query} order by publishDate.value desc").setLimit($itemsPerPage).setOffset($startAt).bindValue('categories', $categories).addFilter("unique").execute())
    #else
      #set ($totalResult = 0)
      #set ($result = [])
    #end
    #if ("$!{blogCategoryEntriesCache.containsKey($!{category})}" == '')
      #set ($blogCategoryEntriesCache = {})
    #end
    #set ($discard = $blogCategoryEntriesCache.put("$!{category}", [$result, $totalResult]))
    #setVariable ("$entries" $result)
    #setVariable ("$totalEntries" $totalResult)
  #end
#end
#macro(getSubcategories $tree $category $subcategories)
  #foreach($subcategory in $tree.get($category))
    #set($discard = $subcategories.add($subcategory))
    #getSubcategories($tree $subcategory $subcategories)
  #end
#end
##
##
##
#**
 * Builds a tree of categories, respecting the parent<->subcategory relation. Each node holds the
 * full name of the category's document. The root of the tree is 'Blog.Categories.WebHome' or 'aCategorySpace.WebHome'.
 * 
 * @param space The space where to search for categories. If this parameter is an emptry string or
 *        null, all the categories in the wiki are returned.
 * @param tree Return parameter, HashMap<String, List<String>> structure holding the categories
 *        hierarchy, where the key is the name of a category, and the value contains the names of
 *        all its subcategories. To obtain the full hierarchy, start with the key 'Blog.Categories.WebHome'.
 *###
#macro(getCategoriesHierarchy $space $tree)
  #set ($tree = $NULL)
  #if ("$!{blogCategoriesHierarchyCache.containsKey($!{space})}" == 'true')
    #setVariable ("$tree" $blogCategoriesHierarchyCache.get($!{space}))
  #else
    #set ($result = {})
    #set($query = ', BaseObject obj where ')
    #if("$!space" != '')
      #set($query = "${query}doc.space = :space and ")
    #end
    #set($query = "${query}obj.name = doc.fullName and obj.className = '${blogCategoryClassname}' order by doc.name")
    #set($queryObj = $services.query.hql($query))
    #if("$!space" != '')
      #set($queryObj = $queryObj.bindValue('space', $space))
    #end
    #foreach($category in $queryObj.execute())
      #set($categoryDoc = $xwiki.getDocument($category))
      #set($categoryParent = "$!categoryDoc.parent")
      #if($categoryParent == '')
        #set($categoryParent = $defaultCategoryParent)
      #end
      #set($categoryParent = $services.model.serialize($categoryParent, 'local'))
      #if(!$result.containsKey($categoryParent))
        #set($discard = $result.put($categoryParent, []))
      #end
      #set($discard = $result.get($categoryParent).add($category))
    #end
    #if ("$!{blogCategoriesHierarchyCache.containsKey($!{space})}" == '')
      #set ($blogCategoriesHierarchyCache = {})
    #end
    #set ($discard = $blogCategoriesHierarchyCache.put("$!{space}", $result))
    #setVariable ("$tree" $result)
  #end
#end
##
##
##
#**
 * Displays the category hierarchy held in the <tt>tree</tt> parameter.
 * 
 * @param tree The category hierarchy, a HashMap<String, List<String>> structure, where the key
 *        is the name of a category, and the value contains the names of all its subcategories.
 * @param displayMethod Selects how to display the category tree. Possible values are:
 *        <ul>
 *        <li><em>"simple"</em>: tree with links to the category pages.</li>
 *        <li><em>"selectable"</em>: each category name in the tree is preceded by a checkbox.</li>
 *        <li><em>"option"</em>: wraps each category name in an &lt;option&gt; element, to be used
 *          in a select box.</li>
 *        <li><em>"editable"</em>: displays links to delete and edit each category, if the rights
 *          allow such actions.</li>
 *        </ul>
 *        For any other value, the default ("simple") is considered.
 *###
#macro(displayCategoriesHierarchy $tree $displayMethod)
  #set($processedCategories = [])
  #displayCategoriesHierarchyRecursive($tree $defaultCategoryParent 1 $displayMethod)
#end
##
##
##
#**
 * Displays recursively the category hierarchy held in the <tt>tree</tt> parameter, starting at
 * the node indicated by the <tt>root</tt> parameter, which is on the <tt>level</tt>th level in
 * the tree.
 * 
 * @param tree The category hierarchy HashMap<String, List<String>> structure, where the key
 *        is the name of a category, and the value contains the names of all its subcategories.
 * @param root The full name of the document containing the category that is to be considered the
 *        root of the displayed subtree.
 * @param level The current depth of the tree, used for proper indentation.
 * @param displayMethod Selects how to display the category tree. Possible values are:
 *        <ul>
 *        <li><em>"simple"</em>: tree with links to the category pages.</li>
 *        <li><em>"selectable"</em>: each category name in the tree is preceded by a checkbox.</li>
 *        <li><em>"option"</em>: wraps each category name in an &lt;option&gt; element, to be used
 *          in a select box.</li>
 *        <li><em>"editable"</em>: displays links to delete and edit each category, if the rights
 *          allow such actions.</li>
 *        </ul>
 *        For any other value, the default ("simple") is considered.
 *###
#macro(displayCategoriesHierarchyRecursive $tree $root $level $displayMethod)
  #if(!$processedCategories)
    #set($processedCategories = [])
  #end
  #foreach($item in $tree.get($root))
    #if(!$processedCategories.contains($item))
      #set($discard = $processedCategories.add($item))
      #displayCategory($item $level $displayMethod)
      #displayCategoriesHierarchyRecursive($tree $item $mathtool.add($level, 1) $displayMethod)
    #end
  #end
  #if($displayMethod == "selectable")
    #set ($entryObjNumber = 0)
    #if("$!entryObj.number" != '')
      #set ($entryObjNumber = $entryObj.number)
    #end
    <input type="hidden" name="${blogPostClassname}_$!{entryObjNumber}_category" value="" />
  #end
#end
##
##
##
#**
 * Displays a category as part of a category hierarchy.
 * 
 * @param name The full name of the document containing the category to be displayed.
 * @param level The depth where this category is in the tree, used for proper indentation.
 * @param displayMethod Selects how to display the category tree. Possible values are:
 *        <ul>
 *        <li><em>"simple"</em>: tree with links to the category pages.</li>
 *        <li><em>"selectable"</em>: each category name in the tree is preceded by a checkbox.</li>
 *        <li><em>"option"</em>: wraps each category name in an &lt;option&gt; element, to be used
 *          in a select box.</li>
 *        <li><em>"editable"</em>: displays links to delete and edit each category, if the rights
 *          allow such actions.</li>
 *        </ul>
 *        For any other value, the default ("simple") is considered.
 *###
#macro(displayCategory $name $level $displayMethod)
  #if("$!displayMethod" == "option")
    #displayOptionCategory($name $level)
  #elseif("$!displayMethod" == "selectable")
    #displaySelectableCategory($name $level)
  #elseif("$!displayMethod" == "editable")
    #displayEditableCategory($name $level)
  #else
    #displaySimpleCategory($name $level)
  #end
#end
##
##
##
#**
 * Displays a category as part of a category hierarchy, preceded by a checkbox that allows choosing
 * this category for a blog entry.
 * 
 * @param name The full name of the document containing the category to be displayed.
 * @param level The depth where this category is in the tree, used for proper indentation.
 *###
#macro(displaySelectableCategory $name $level)
  #set($categoryDoc = $xwiki.getDocument($name))
  #set($addCategURL = $doc.getURL('view', $escapetool.url({
    'xaction': 'showAddCategory',
    'parentCategory' : $name
  })))
  #set($addEntryParams = false)
  #if($isBlogPost)
    #set($entry = $xwiki.getDocument($doc.fullName))
    #set($entryObj = $isBlogPost)
    #set($addEntryParams = true)
  #elseif("$!request.entry" != '' && "$!request.entryObjNb" != '')
    #set($entry = $xwiki.getDocument($request.entry))
    #set($entryObj = $entry.getObject($blogPostClassname, $numbertool.toNumber($request.entryObjNb).intValue()))
    #set($addEntryParams = true)
  #end
  #if($isBlogPost || $addEntryParams)
    ## parentCategory must be the last param
    #set($addCategURL = $doc.getURL('view', $escapetool.url({
      'xaction': 'showAddCategory',
      'entry': $entry.fullName,
      'entryObjNb': $entryObj.number,
      'parentCategory': $name
    })))
  #end
  #foreach($i in [1..$level])*#end ##
#set ($entryObjNumber = 0)
#if("$!entryObj.number" != '')
  #set ($entryObjNumber = $entryObj.number)
#end
<span class="blog-category-level"><span class="blog-category">##
<label id='blog_category_${services.rendering.escape(${escapetool.xml($name)}, $xwiki.currentContentSyntaxId)}' title="#getCategoryDescription($categoryDoc)"><input name="${blogPostClassname}_$!{entryObjNumber}_category" value="$services.rendering.escape(${escapetool.xml($name)}, $xwiki.currentContentSyntaxId)" type="checkbox"#if($entryObj.getProperty('category').getValue().contains($name)) checked="checked" #end/> #getCategoryName($categoryDoc)</label>##
</span>##
#if($xwiki.hasAccessLevel('edit', $xcontext.user, $doc.fullName) && ("$!{request.xaction}" != "showAddCategory" || "$!{request.parentCategory}" != $name))
<span class="blog-category-tools">##
<a href="$escapetool.xml($addCategURL)" class="tool add-subcategory">#toolImage('add')</a>##
</span>##
#end
</span>
#end
##
##
##
#**
 * Displays a form for creating a new category. If a parentCategory parameter is present in the 
 * query string, the parent category is set accordingly. Otherwise, the form provides a selection
 * control for choosing the parent category among existing categories.
 *###
## DO NOT CHANGE INDENTATION
#macro(addCategoryForm) #set($addCategURL = $doc.getURL()) #if("$!request.entry" != '') #set($addCategURL = "${addCategURL}?entry=$escapetool.url($request.entry)&amp;entryObjNb=$escapetool.url($!request.entryObjNb)")#end<form action="${addCategURL}" method="post" class="category-add-form"><div class='create-category'> <input type="hidden" name="form_token" value="$!{services.csrf.getToken()}" /> <input type="hidden" name="xaction" value="create"/> <label>$services.localization.render('blog.categories.new')<br/> <input type="text" name="newCategoryName" class="category-name-input" /></label><br/>#if("$!{request.parentCategory}" == "")<label>#* $services.localization.render('blog.categories.parent')*# $escapetool.xml($services.localization.render('blog.manageCategories.forms.sub_cat_of'))<br/> <select name="newCategoryParent" id="blog_category_selectBox" class="category-add-input"> <option value="${escapetool.xml($defaultCategoryParent)}" selected="selected">$escapetool.xml($services.localization.render('blog.manageCategories.forms.select_none'))</option> $!processedCategories.clear() #displayCategoriesHierarchy($tree 'option') </select> <br/></label>#else<input type="hidden" name="newCategoryParent" value="${escapetool.xml($request.parentCategory)}"/>#end<span class="buttonwrapper"><input class="button" type="submit" value="$escapetool.xml($services.localization.render('blog.manageCategories.forms.add_button_label'))" /></span> <a class="btn btn-default" href="$doc.getURL()">$escapetool.xml($services.localization.render('blog.manageCategories.forms.cancel_button_label'))</a> </div></form> #end
##
##
##
#**
 * Displays a form for renaming a category.
 *###
## DO NOT CHANGE INDENTATION
#macro(renameCategoryForm)##
<form action="$doc.getURL()" method="post" class="category-rename-form"><div class='rename-category'>##
<input type="hidden" name="form_token" value="$!{services.csrf.getToken()}" />
<input type="hidden" name="xaction" value="rename"/>##
<input type="hidden" name="category" value="${escapetool.xml($request.category)}"/>##
<label>$services.localization.render('blog.categories.newName')<br/> <input type="text" name="newCategoryName" class="category-name-input" /></label><br/>##
<span class="buttonwrapper"><input class="button" type="submit" value="$escapetool.xml($services.localization.render('blog.manageCategories.forms.rename_button_label'))" /></span> ##
<a class="btn btn-default" href="$doc.getURL()">$escapetool.xml($services.localization.render('blog.manageCategories.forms.cancel_button_label'))</a>##
</div></form>##
#end
##
##
##
#**
 * Displays a category as part of a category hierarchy, followed by links for editing and deleting
 * this category, if the current user has the rights to perform these actions.
 * 
 * @param name The full name of the document containing the category to be displayed.
 * @param level The depth where this category is in the tree, used for proper indentation.
 *###
## DO NOT CHANGE INDENTATION
#macro(displayEditableCategory $name $level)
  #getEntriesForCategory($name $discard $totalEntries)
  #set($nameUrl = $escapetool.url($name))
  #foreach($i in [1..$level])*#end ##
<span class="blog-category-level"><span class="blog-category">##
<a href="$services.rendering.escape($xwiki.getURL('Blog.CategoryRss', 'view', "xpage=plain&amp;category=$nameUrl"), $doc.syntax)" title="RSS">#toolImage('rss')</a>&nbsp;##
<span class="wikilink"><a href="$services.rendering.escape($xwiki.getURL($name), $doc.syntax)">#getCategoryName($xwiki.getDocument($name)) <span class="itemCount">($totalEntries)</span></a></span></span>##
<span class="blog-category-tools">##
#if($xwiki.hasAccessLevel('delete', $xcontext.user, $name) && ("$!{request.xaction}" != 'showRenameCategory' || "$!{request.category}" != $name))<a href="$services.rendering.escape($xwiki.getURL('Blog.ManageCategories', 'view', "xaction=showRenameCategory&amp;category=$nameUrl"), $doc.syntax)" class="tool rename">#toolImage('pencil')</a>#end##
#if($xwiki.hasAccessLevel('edit', $xcontext.user, $doc.fullName) && ("$!{request.xaction}" != "showAddCategory" || "$!{request.parentCategory}" != $name))<a href="$services.rendering.escape($xwiki.getURL('Blog.ManageCategories', 'view', "xaction=showAddCategory&amp;parentCategory=$nameUrl"), $doc.syntax)" class="tool add-subcategory">#toolImage('add')</a>#end##
#if($xwiki.hasAccessLevel('delete', $xcontext.user, $name)) <a href="$services.rendering.escape($xwiki.getURL('Blog.ManageCategories', 'view', "xaction=delete&amp;category=$nameUrl&amp;form_token=$!{services.csrf.getToken()}"), $doc.syntax)" class="tool delete">#toolImage('cross')</a>#end##
</span>##
#if($xwiki.hasAccessLevel('edit', $xcontext.user, $doc.fullName) && "$!{request.xaction}" == "showRenameCategory" && "$!{request.category}" == $name) #renameCategoryForm() #end##
#if($xwiki.hasAccessLevel('edit', $xcontext.user, $doc.fullName) && "$!{request.xaction}" == "showAddCategory" && "$!{request.parentCategory}" == $name) #addCategoryForm() #end##
</span>
#end
##
##
##
#**
 * Displays a category as part of a category hierarchy, wrapped in an &lt;option&gt; element, to
 *          be used in a select box.
 * 
 * @param name The full name of the document containing the category to be displayed.
 * @param level The depth where this category is in the tree, used for proper indentation.
 *###
#macro(displayOptionCategory $name $level)
  <option id="blog_category_${services.rendering.escape(${escapetool.xml($name)}, $doc.syntax)}_option" value="$services.rendering.escape(${escapetool.xml($name)}, $doc.syntax)">#if($level > 1)#foreach($i in [2..$level])&nbsp;&nbsp;#end#end#getCategoryName($xwiki.getDocument($name))</option>
#end
##
##
##
#**
 * Displays a category as part of a category hierarchy, wrapped in a link.
 * 
 * @param name The full name of the document containing the category to be displayed.
 * @param level The depth where this category is in the tree, used for proper indentation.
 *###
#macro(displaySimpleCategory $name $level)
  #getEntriesForCategory($name $discard $totalEntries)
  #set($nameUrl = $escapetool.url($name))
  #foreach($i in [1..$level])*#end (% class="blog-category-level" %)((( [[#toolImage('rss')>>$services.rendering.escape($name, $xwiki.getCurrentContentSyntaxId())||queryString="xpage=plain&sheet=Blog.CategoryRss" title="RSS"]] <span class="wikilink"><a href="$services.rendering.escape($xwiki.getURL($name), $xwiki.getCurrentContentSyntaxId())">#getCategoryName($xwiki.getDocument($name)) <span class="itemCount">($totalEntries)</span></a></span>)))
#end
##
##
##
#**
 * Prints the name of a category, indicated by its document.
 * The result is XML-escaped and Wiki syntax escaped.
 * 
 * @param categoryDoc The document containing the category to be displayed.
 *###
#macro(getCategoryName $categoryDoc)
## Don't indent!
#set($result = "$!categoryDoc.getObject(${blogCategoryClassname}).getProperty('name').value.trim()")##
#if($result == '')
#set($result = $categoryDoc.name)
#end
## Escape wiki syntax, if any.
#set ($result = "$services.rendering.escape($result, $xwiki.currentContentSyntaxId)")
## Escape HTML, if any.
$escapetool.xml($result)##
#end
##
##
##
#**
 * Prints the description of a category, indicated by its document.
 * The result is XML-escaped
 * 
 * @param categoryDoc The document containing the category to be displayed.
 *###
#macro(getCategoryDescription $categoryDoc)
## Don't indent!
$escapetool.xml($!categoryDoc.getObject(${blogCategoryClassname}).getProperty('description').value.trim())##
#end
##
##
##
#**
 * Generates a form for creating a new category. The form allows to enter the name of the new
 * category, and select a parent category from the existing ones.
 * 
 * @param tree The category hierarchy, a HashMap<String, List<String>> structure, where the key
 *        is the name of a category, and the value contains the names of all its subcategories.
 * @todo When javascript is disabled, a link to "Manage categories" should be displayed instead.
 *       This "form" should be created from javascript.
 *###
#macro(showCreateCategoryBoxWithForm $tree)
  <form action="$doc.getURL()" method="post">
  #showCreateCategoryBox($tree)
  </form>
#end
#**
 * Generates a box for creating a new category. This allows to enter the name of the new
 * category, and select a parent category from the existing ones. Note that this does not create
 * a HTML form element, but requires one to be defined already as its ancestor.
 * 
 * @param tree The category hierarchy HashMap<String, List<String>> structure, where the key
 *        is the name of a category, and the value contains the names of all its subcategories.
 * @todo When javascript is disabled, a link to "Manage categories" should be displayed instead.
 *       This "form" should be created from javascript.
 *###
#macro(showCreateCategoryBox $tree)
  <div class='create-category'>
    <input type="hidden" name="form_token" value="$!{services.csrf.getToken()}" />
    <input type="hidden" name="xaction" value="create"/>
    <label>$services.localization.render('blog.categories.new') <input type="text" name="newCategoryName" /></label>
    <label>$services.localization.render('blog.categories.parent')
      <select name="newCategoryParent" id="blog_category_selectBox">
        <option value="${defaultCategoryParent}" selected="selected">None</option>
        $!processedCategories.clear()##
        #displayCategoriesHierarchy($tree 'option')
      </select>
    </label>
    <span class="buttonwrapper"><input class="button" type="button" value="Add" id="blog_AddCategoryButton" /></span>
  </div>
#end
##
##
##
#macro(displayCategoryManagementTree $space $displayType)
  <div class="blog-categories-list">
    #getCategoriesHierarchy($space $tree)
    #if ("$!space" != $defaultBlogSpace)
      #set ($defaultCategoryParent = "${space}.WebHome")
    #end
    #set ($categoriesDocFullName = $defaultCategoryParent)
    #displayCategoriesHierarchy($tree $displayType)
    #if ($xwiki.hasAccessLevel('edit', $xcontext.user, $categoriesDocFullName))
      #set ($queryString = {
        'xaction' : 'showAddCategory',
        'parentCategory' : '',
        'categoriesSpace': $space
      })
      #if ($isBlogPost || ("$!request.entry" != '' && "$!request.entryObjNb" != ''))
        #set ($entryParam = $doc.fullName)
        #set ($entryObjNbParam = $entryObj.number)
        #if (!$isBlogPost)
          #set ($entryParam = $request.entry)
          #set ($entryObjNbParam = $request.entryObjNb)
        #end
        #set ($discard = $queryString.put('entry', $entryParam))
        #set ($discard = $queryString.put('entryObjNb', $entryObjNbParam))
      #end
      #set ($addCategURL = $doc.getURL('view', $escapetool.url($queryString)))
      * <span class="blog-add-category-label">$services.icon.renderHTML('add')&nbsp;<a href="$escapetool.xml($addCategURL)">$services.localization.render('blog.categories.addcategory')</a></span>
       #if ("$!request.xaction" == 'showAddCategory' && "$!request.parentCategory" == '')
         #addCategoryForm()
       #end
    #end
  </div>
#end
##
##
##
#**
 * Deletes a category, moving all the subcategories to its parent and removing this category from
 * all existing blog entries.
 * 
 * @param category The full name of the document containing the category to be deleted.
 *###
#macro(deleteCategory $category)
  #set($categoryDoc = $xwiki.getDocument($category))
  #set($categoryParent = "$!categoryDoc.parent")
  #if($categoryParent == '')
    #set($categoryParent = "{$defaultCategoryParent}")
  #end
  #set($query = ', BaseObject obj where ')
  #if($space != '')
    #set($query = "${query}doc.space = '${space}' and ")
  #end
  ## Get the subcategories of the deleted category.
  #set($query = "${query}obj.name = doc.fullName and obj.className = '${blogCategoryClassname}' and doc.fullName <> 'Blog.CategoryTemplate' and doc.parent = :category order by doc.name")

  #foreach($item in $services.query.hql($query).bindValue('category', $category).execute())
    #if($xwiki.hasAccessLevel('edit', $xcontext.user, $item) && $!{services.csrf.isTokenValid("$!{request.getParameter('form_token')}")})
      #set($subcategoryDoc = $xwiki.getDocument($item))
      $subcategoryDoc.setParent($categoryParent)
      $subcategoryDoc.save($services.localization.render('blog.manageCategories.comment.updatedParent'), true)
    #end
  #end
  #set($query = ', BaseObject obj, DBStringListProperty categories join categories.list as category where ')
  #if($space != '')
    #set($query = "${query}doc.space = '${space}' and ")
  #end
  ## Get the blog posts of the deleted category.
  #set($query = "${query}obj.name = doc.fullName and obj.className = '${blogPostClassname}' and doc.fullName <> 'Blog.BlogPostTemplate' and categories.id.id = obj.id and categories.id.name = 'category' and category = :category order by doc.name")

  #foreach($item in $services.query.hql($query).bindValue('category', $category).execute())
    #if($xwiki.hasAccessLevel('edit', $xcontext.user, $item) && $!{services.csrf.isTokenValid("$!{request.getParameter('form_token')}")})
      #set($blogEntryDoc = $xwiki.getDocument($item))
      #set($discard = $blogEntryDoc.getObject(${blogPostClassname}).getProperty('category').value.remove($category))
      $blogEntryDoc.save($services.localization.render('blog.manageCategories.comment.removedDeletedCategory'), true)
    #end
  #end
  $categoryDoc.delete()
#end
##
##
##
#**
 * Renames a category, updating all the subcategories and all existing blog entries.
 * 
 * @param category The full name of the document containing the category to be renamed.
 * @param newCategoryName The new name of the category.
 *###
#macro(renameCategory $category $newCategoryName)
  #set($categoryDoc = $xwiki.getDocument($category))
  #set ($newCategoryFullName = $newCategoryName)
  #if ($category.space != $defaultBlogSpace)
    #set ($newCategoryFullName = "${categoryDoc.space}.${newCategoryName}")
  #end
  #set($newCategoryDoc = $xwiki.getDocument($newCategoryFullName))
  #set($query = ', BaseObject obj where ')
  ## Get the subcategories of the renamed category.
  #set($query = "${query}obj.name = doc.fullName and obj.className = '${blogCategoryClassname}' and doc.fullName <> 'Blog.CategoryTemplate' and doc.parent = :category order by doc.name")
  #foreach($item in $services.query.hql($query).bindValue('category', $category).execute())
    #if($xwiki.hasAccessLevel('edit', $xcontext.user, $item) && $!{services.csrf.isTokenValid("$!{request.getParameter('form_token')}")})
      #set($subcategoryDoc = $xwiki.getDocument($item))
      $subcategoryDoc.setParent($newCategoryDoc.fullName)
      $subcategoryDoc.save($services.localization.render('blog.manageCategories.comment.updatedParent'), true)
    #end
  #end
  #set($query = ', BaseObject obj, DBStringListProperty categories join categories.list as category where ')
  ## Get the blog posts of the renamed category.
  #set($query = "${query}obj.name = doc.fullName and obj.className = '${blogPostClassname}' and doc.fullName <> 'Blog.BlogPostTemplate' and categories.id.id = obj.id and categories.id.name = 'category' and category = :category order by doc.name")
  #foreach($item in $services.query.hql($query).bindValue('category', $category).execute())
    #if($xwiki.hasAccessLevel('edit', $xcontext.user, $item) && $!{services.csrf.isTokenValid("$!{request.getParameter('form_token')}")})
      #set($blogEntryDoc = $xwiki.getDocument($item))
      #set($discard = $blogEntryDoc.getObject(${blogPostClassname}).getProperty('category').value.remove($category))
      #set($discard = $blogEntryDoc.getObject(${blogPostClassname}).getProperty('category').value.add($newCategoryDoc.fullName))
      $blogEntryDoc.save($services.localization.render('blog.manageCategories.comment.updatedRenamedCategory'), true)
    #end
  #end
  #if ($!{services.csrf.isTokenValid("$!{request.getParameter('form_token')}")})
    $categoryDoc.getObject('Blog.CategoryClass').set('name', $newCategoryName)
    $categoryDoc.save($services.localization.render('blog.manageCategories.comment.updatedCategory'), true)
    $categoryDoc.rename($newCategoryFullName)
  #end
#end
##
##
##
#**
 * Dipslay posts of a given category or a categories space.
 * This macro is used in Blog.CategorySheet and Blog.CategoriesSheet pages
 * 
 * @param catDoc The document containing the category or the WebHome page of a categories space.
 * @param catObj The Blog.CategoryClass object attached to the category document, this parameter is null in case of categories space WebHome.
 *###
#macro(displayCategoryPosts $catDoc $catObj)
  #getEntriesForCategory($catDoc.fullName $discard $totalEntries)

  #if ($totalEntries == 0)

    {{info}}{{translation key="blog.categories.noentries"/}}{{/info}}
  #else
    #set ($macro.isCategoriesSpace = $catDoc.getObject('XWiki.DocumentSheetBinding').sheet == 'Blog.CategoriesSheet')
    #if ($catObj || $macro.isCategoriesSpace)

    (% class="cat-posts-count" %)
    ==== [[#toolImage('feed')>>Blog.CategoryRss||queryString="xpage=plain&category=$escapetool.url($catDoc.fullName)" title="RSS"]] $services.localization.render('blog.category.posts.count', [$totalEntries]) ====
    #end
    ## Keep testing the inline action for backward compatibility with older categories.
    #if ($xcontext.action != 'edit' && $xcontext.action != 'inline')
      #getCategoriesHierarchy($catDoc.space $tree)
      #if ("$!tree.get($catDoc.fullName)" != '')
        (% class="blog-categories-list subcategories cat-count" %)
        (((
          (((
            **&nbsp;**
          )))
          (((
            #displayCategoriesHierarchyRecursive($tree $catDoc.fullName 1 'simple')
          )))
        )))
      #end
      (% class="clearfloats" %)((()))

      #set ($macro.layoutParams = 'displayTitle=true|useSummary=true')
      #getBlogDocumentForCategoriesSpace($catDoc.space $blogDoc)
      #getBlogPostsLayout($blogDoc $postsLayout)
      #set ($category = $catDoc.fullName)
      #if ($macro.isCategoriesSpace)
        #set ($category = $catDoc.space)
      #end
      (% class="hfeed category" %)((({{blogpostlist category="$category.replaceAll('~', '~~').replaceAll('"', '~"')" paginated="yes" layout="$postsLayout.replaceAll('~', '~~').replaceAll('"', '~"')" layoutParams="$!macro.layoutParams.replaceAll('~', '~~').replaceAll('"', '~"')" /}})))
    #end
  #end
#end
##
##
##
#*
  Provide a modal box to notify the user when the category is not set on a blog post creation/update.
*#
#macro(checkCategorySelectionModal)
  <div class="modal fade" id="checkCategorySelection" tabindex="-1" role="dialog">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal">&times;</button>
          <h4 class="modal-title">$services.localization.render('blog.modal.checkCategorySelection.header')</h4>
        </div>
        <div class="modal-body">
          <div>
            $services.localization.render('blog.modal.checkCategorySelection.body')
          </div>
        </div>
        <div class="modal-footer">
          <input id="continueCategorySelection" type="button" class="btn btn-default" data-dismiss="modal"
            value="$escapetool.xml($services.localization.render('yesno_1'))">
          <input type="button" class="btn btn-danger" data-dismiss="modal"
            value="$escapetool.xml($services.localization.render('blog.modal.checkCategorySelection.footer.no'))">
        </div>
      </div>
    </div>
  </div>
#end
{{/velocity}}
