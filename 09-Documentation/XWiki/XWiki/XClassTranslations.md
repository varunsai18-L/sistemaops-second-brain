---
id: xwiki-XWiki.XClassTranslations
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906689000
sync_date: 2026-08-19 20:22:57
tags:
  - xwiki/documentation
  - space/xwiki
---
# XClassTranslations

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906689000
- **Source:** [XClassTranslations](https://wiki.systemaops.in/bin/view/XWiki/XWiki.XClassTranslations)

---

#
# Default Class Sheet
#

platform.xclass.defaultClassSheet.title=Default Class Sheet
platform.xclass.defaultClassSheet.description=You can edit this page to change the default presentation of classes, or you can copy it to create a customized view just for one or several classes.

platform.xclass.defaultClassSheet.properties.heading=Class Properties
platform.xclass.defaultClassSheet.properties.empty=This class does not have any properties yet. You can use the {0}class editor{1} to define them.
platform.xclass.defaultClassSheet.properties.edit=You can use the {0}class editor{1} to add or modify the class properties.

platform.xclass.defaultClassSheet.createPage.heading=Create a new page
platform.xclass.defaultClassSheet.createPage.pageAlreadyExists=The target page already exists. Please choose a different name or {0}view{1} the existing page.
platform.xclass.defaultClassSheet.createPage.denied=You don't have permission to create that page
platform.xclass.defaultClassSheet.createPage.label=Create this page

platform.xclass.defaultClassSheet.pages.heading=Existing Pages
platform.xclass.defaultClassSheet.pages.description=The following pages have objects described by this class.

platform.xclass.defaultClassSheet.sheets.heading=Class Sheets
platform.xclass.defaultClassSheet.sheets.missing=Before using this class you must first create a sheet and a template for it. Follow the instructions below to do this.
platform.xclass.defaultClassSheet.sheets.description=The {0}sheet{1} allows you to control the presentation of pages of this type. You can use the default presentation, which enumerates all the available fields, or you can design your own presentation. You can also choose different presentations for the viewing and for the editing modes.
platform.xclass.defaultClassSheet.sheets.create=Create the sheet
platform.xclass.defaultClassSheet.sheets.notBound=The sheet is not bound to the class so it won't be applied automatically when a page that has an object of this class is displayed.
platform.xclass.defaultClassSheet.sheets.bind=Bind the sheet to the class
platform.xclass.defaultClassSheet.sheets.view=View the sheet page ({0})
platform.xclass.defaultClassSheet.sheets.list=The following class sheets are bound to this class:

platform.xclass.defaultClassSheet.template.heading=Class Template
platform.xclass.defaultClassSheet.template.description=The {0}template{1} is the page used as the model when creating a new page of this type. It contains an instance of your {0}class{1}.
platform.xclass.defaultClassSheet.template.create=Create the template
platform.xclass.defaultClassSheet.template.missingObject=The template does not contain an object of type {0}.
platform.xclass.defaultClassSheet.template.addObject=Add a {0} object to the template
platform.xclass.defaultClassSheet.template.view=View the template page ({0})

platform.xclass.defaultClassSheet.templateProvider.heading=Class Template Provider
platform.xclass.defaultClassSheet.templateProvider.description=The {0}template provider{0} allows to create wiki pages using an existing template. A template will be displayed in the {0}Create{0} menu.
platform.xclass.defaultClassSheet.templateProvider.create=Create the template provider
platform.xclass.defaultClassSheet.templateProvider.view=View the template provider page ({0})
platform.xclass.templateProvider.defaultDescription=Add a new {0} entry.

#
# Default Object Sheet
#

xclass.defaultObjectSheet.noProperties=No properties

#
# Classes
#

platform.xclass.classes.title=Data types
platform.xclass.classes.description=This tool allows to define structured data types (classes) in your wiki. Please consult the {0}developer''s guide{1} to get familiar with the XWiki data model and the public APIs.

platform.xclass.classes.templates.heading=Templates for new data types
platform.xclass.classes.templates.description=Here are the templates and sheets for creating new classes:
platform.xclass.classes.templates.classSheet=Default code for displaying a class
platform.xclass.classes.templates.classTemplate=Page template for new classes
platform.xclass.classes.templates.objectSheet=Default code for displaying class instances (objects)

platform.xclass.classes.createClass.heading=Create a new data type
platform.xclass.classes.createClass.description=Choose a simple title, such as {0}Article{1}, {0}Book{1}, {0}Employee{1}. ''{0}Class{1}'' will be appended at the end automatically.
platform.xclass.classes.createClass.denied=You don't have permission to create that class
platform.xclass.classes.createClass.title.hint=Title of the new class
platform.xclass.classes.createClass.title.placeholder=New Class
platform.xclass.classes.createClass.location.hint=Location in the page hierarchy where this new class will be created
platform.xclass.classes.createClass.parent.hint=Parent of the new class
platform.xclass.classes.createClass.parent.placeholder=Path.To.Class
platform.xclass.classes.createClass.name.hint=Name of the new class
platform.xclass.classes.createClass.label=Create this Class

platform.xclass.classes.livetable.heading=Data types defined in this wiki
platform.xclass.classes.livetable.doc.title=Class
platform.xclass.classes.livetable.doc.location=Location
platform.xclass.classes.livetable.doc.date=Date
platform.xclass.classes.livetable.doc.author=Last Author
platform.xclass.classes.livetable.pageCount=Page Count
platform.xclass.classes.livetable._actions=Actions
