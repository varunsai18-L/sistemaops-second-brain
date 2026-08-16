---
id: xwiki-Menu.MenuTranslations
type: XWiki Page
space: "Menu"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781907353000
sync_date: 2026-08-16 19:45:51
tags:
  - xwiki/documentation
  - space/menu
---
# MenuTranslations

- **Space:** Menu
- **Author:** XWiki.superadmin
- **Last Modified:** 1781907353000
- **Source:** [MenuTranslations](https://wiki.systemaops.in/bin/view/Menu/Menu.MenuTranslations)

---

# Class fields
Menu.MenuClass_content1=Menu Structure

# Live table generic keys
menu.livetable.doc.title=Page title
menu.livetable.doc.name=Page name
menu.livetable.doc.location=Location
menu.livetable.doc.space=Space
menu.livetable.doc.fullname=Page full name
menu.livetable.doc.author=Last Author
menu.livetable.doc.creator=Creator
menu.livetable.doc.date=Update date
menu.livetable.doc.creationDate=Creation date
menu.livetable._avatar=Avatar
menu.livetable._images=Images
menu.livetable._attachments=Attachments
menu.livetable._actions=Actions
menu.livetable._actions.edit=Edit
menu.livetable._actions.delete=Delete
menu.livetable.emptyvalue=-

# Live table specific keys
menu.livetable.content1=Menu Structure

# Administration keys
admin.menu.name=Menus

# UIX keys
menu.uix.extensionPoint.label=Menu Display Location
menu.uix.extensionPoint.hint=Specifies where to display the menu. The menu is displayed either horizontally or vertically, based on the chosen location.
menu.uix.extensionPoint.value.nowhere=Nowhere
menu.uix.extensionPoint.value.template.header.after=After the Page Header
menu.uix.extensionPoint.value.panels.rightPanels=Inside a Right Panel
menu.uix.extensionPoint.value.panels.leftPanels=Inside a Left Panel
menu.uix.content.label=UI Extension Content
menu.uix.content.hint=If you can see this then it probably means you have JavaScript disabled. You should select the same value as for the menu display location.
menu.uix.scope.label=Menu Visibility Scope
menu.uix.scope.hint=Specifies in which context the menu is visible.

# Menu Macro
rendering.macro.menu.name=Menu
rendering.macro.menu.description=Displays a menu created using simple wiki syntax (nested lists and links).
rendering.macro.menu.parameter.id.name=Id
rendering.macro.menu.parameter.id.description=Optional menu identifier that will be set on the HTML element that wraps the menu. You can use this identifier in JavaScript code to access the menu DOM or in functional tests to assert the menu items.
rendering.macro.menu.parameter.label.name=Label
rendering.macro.menu.parameter.label.description=Optional menu label used to describe the content of the menu. Especially important for assistive technologies and accessibility of the menu.
rendering.macro.menu.parameter.type.name=Type
rendering.macro.menu.parameter.type.description=The optional menu type determines the menu appearance and behaviour. The supported values are: horizontal (default value) and vertical.
rendering.macro.menu.content.description=Define the menu structure using wiki syntax. Each menu item should be a list item and should contain the menu item label or link. You can use nested lists for sub-menu items.

# Menu UI
menu.ui.openSubMenu=Open the submenu.
menu.ui.closeSubMenu=Close the submenu.
menu.ui.horizontal.toggler.description=Toggle the horizontal menu.

# Menu WebHome
menu.description=This is a simple application that helps you create navigation menus to be displayed either horizontally as a top bar after the page header or vertically in a side panel.
