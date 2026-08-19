---
id: xwiki-XWiki.AttachmentSelector
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781905339000
sync_date: 2026-08-19 20:22:26
tags:
  - xwiki/documentation
  - space/xwiki
---
# Attachments

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781905339000
- **Source:** [Attachments](https://wiki.systemaops.in/bin/view/XWiki/XWiki.AttachmentSelector)

---

{{velocity output="false"}}
#set ($translationPrefix = 'xe.attachmentSelector')

#if ($request.xaction == 'postUpload')
  #set ($targetDocument = $xwiki.getDocument($request.get('docname')))
  #set ($targetAttachDocument = $xwiki.getDocument($request.get('targetdocname')))

  #set ($fieldname = $request.get('fieldname'))
  #set ($comment = $services.localization.render("${translationPrefix}.postUpload.comment", [$fieldname]))
  #set ($docAction = $request.get('docAction'))
  #set ($attachmentList = $targetAttachDocument.getAttachmentList())
  #if ($attachmentList && $attachmentList.size() > 0)
    #set ($sortedAttachments = $collectiontool.sort($attachmentList, 'date:desc'))
    #set ($lastAttachment = $sortedAttachments.get(0))
  #end
  $response.sendRedirect($targetDocument.getURL($docAction, $escapetool.url({
    $fieldname: $lastAttachment.filename,
    'comment': $comment,
    'form_token': $request.form_token
  })))
  #stop
#end
{{/velocity}}

{{velocity output="false"}}
##
## Macros
##
#set ($attachmentPickerDocName = 'XWiki.AttachmentSelector')

$xwiki.ssx.use($attachmentPickerDocName)
$xwiki.jsx.use($attachmentPickerDocName)

#**
 * Displays the attachment gallery as a list of attachment boxes, starting with special boxes for uploading a new attachment and for setting a default value.
 *
 * @param $targetDocument the document to recieve the field value being modified
 * @param $targetAttachDocument the document to list/save attachments to
 * @param $options generic picker options
 *#
#macro (attachmentPicker_displayAttachmentGallery $targetDocument, $targetAttachDocument, $options)
  #set ($currentValue = $targetDocument.getValue($options.property))
  #if ("$!{targetAttachDocument.getAttachment($currentValue)}" == '')
    #set ($currentValue = "$!{options.defaultValue}")
  #end
  (% class="gallery" %)(((
  ## Only display the upload form if they have edit permission on targetAttachDocument
  #attachmentPicker_displayUploadForm($targetDocument, $targetAttachDocument, $options)
  #attachmentPicker_displayAttachmentGalleryEmptyValue($targetDocument, $targetAttachDocument, $options, $currentValue)
  #if ("$!services.temporaryAttachments" != '')
    #set ($unsortedAttachments = $services.temporaryAttachments.listAllAttachments($targetAttachDocument))
    #set ($sortedAttachments = $collectiontool.sort($unsortedAttachments, "${options.sortAttachmentsBy}"))
  #else
    #set ($sortedAttachments = $collectiontool.sort($targetAttachDocument.getAttachmentList(), "${options.sortAttachmentsBy}") )
  #end
  #foreach ($attachment in $sortedAttachments)
    #set ($extension = $attachment.getFilename())
    #set ($extension = $extension.substring($mathtool.add($extension.lastIndexOf('.'), 1)).toLowerCase())
    #if ($options.filter.size() == 0 || $options.filter.contains($extension))
      #attachmentPicker_displayAttachmentBox($attachment $targetDocument $targetAttachDocument, $options $currentValue)
    #end
  #end
  )))
#end

#**
 * Displays an attachment box.
 *
 * @param $attachment the target attachment to display
 * @param $targetDocument the document being modified
 * @param $options generic picker options
 * @param $currentValue the currently selected file, used for determining if the box should be highlighted as the current value
 *#
#macro (attachmentPicker_displayAttachmentBox $attachment $targetDocument $targetAttachDocument, $options $currentValue)
  #set ($hasTemporaryAttachment = "$!services.temporaryAttachments" != '')
  #set ($canEdit = $xwiki.hasAccessLevel('edit', $xcontext.user, ${targetAttachDocument.fullName}))
  #set ($isTemporaryAttachment = false)
  #if(!$hasTemporaryAttachment)
    #set ($canDeleteAttachment = $canEdit)
  #else
    #set ($isTemporaryAttachment = $services.temporaryAttachments.temporaryAttachmentExists($attachment))
    ## TODO: Update once it is made possible to delete temporary attachments (see XWIKI-20225).
    #set ($canDeleteAttachment = !$isTemporaryAttachment && $canEdit)
  #end
  #set ($cssClasses = [])
  #if ($options.displayImage && $attachment.isImage())
    #set ($discard = $cssClasses.add('gallery_image'))
  #end
  #if ($isTemporaryAttachment)
    #set ($discard = $cssClasses.add('temporary_attachment'))
  #end
  #attachmentPicker_displayStartFrame({'value' : $attachment.filename, 'text' : $attachment.filename, 'cssClass' : "${stringtool.join($cssClasses, ' ')}"} $currentValue)
  #attachmentPicker_displayAttachmentDetails($attachment $options)
  #set ($returnURL = $escapetool.url($doc.getURL('view', $request.queryString)))
  #set ($deleteURL = $targetAttachDocument.getAttachmentURL($attachment.filename, 'delattachment', "xredirect=${returnURL}&form_token=$!{services.csrf.getToken()}") )
  #set ($viewURL = $targetAttachDocument.getAttachmentURL($attachment.filename) )##{'name' : 'download', 'url' : $viewURL, 'rel' : '__blank'}
  #set ($selectURL = $targetDocument.getURL(${options.get('docAction')}, $escapetool.url({
    "${options.get('classname')}_${options.get('object')}_${options.get('property')}": ${attachment.filename},
    'form_token': $!{services.csrf.getToken()}
  })))
  ## Delete action is only proposed for users with the edit right on the document.
  ## If the temporary attachment is available, the delete action is only allowed for non-temporary attachments.  
  #set ($attachmentActions = [{'name' : 'select', 'url' : $selectURL}])
  #if($canDeleteAttachment)
    #set ($discard = $attachmentActions.add({'name' : 'delete', 'url' : $deleteURL}))
  #end
  #define($additionalContent)
    #if ($isTemporaryAttachment)
      #set ($titleMessage = $services.localization.render('attachment.attachmentSelector.attachmentBox.temporaryAttachmentTitle'))
      #set ($titleMessage = $services.rendering.escape($titleMessage, 'xwiki/2.1'))
      (% title="$titleMessage" %)$services.icon.render('clock')(%%)
    #end
  #end
  #attachmentPicker_displayEndFrame ($attachmentActions $additionalContent)
#end

#**
 * Writes the wiki code used at the start of an attachment box. Outputs the attachment title bar, and opens the inner frame div.
 *
 * @param $boxOptions a map of parameters/options for the current attachment, holding, for example, the attachment name (boxOptions.value),
 *        the title to display (boxOptions.text), optional extra CSS classnames to put on the box (boxOptions.cssClass)
 * @param $currentValue the currently selected file, used for determining if this attachment should be highlighted as the current value
 *#
#macro (attachmentPicker_displayStartFrame $boxOptions $currentValue)
  (% class="gallery_attachmentbox $!{boxOptions.cssClass} #if ("$!{boxOptions.value}" == $currentValue) current#{end}" %)(((
    (% class="gallery_attachmenttitle" title="$services.rendering.escape($!{boxOptions.value}, 'xwiki/2.1')" %)(((
      $services.rendering.escape($boxOptions.text, 'xwiki/2.1')
    )))
    (% class="gallery_attachmentframe" %)(((
#end

#**
 * Displays details about an attachment inside the attachment box. If the attachment is an image and the "displayImage" option is on,
 * then the image is displayed. Otherwise, some basic information is displayed: the version, the size, the date and the author.
 *
 * @param $attachment the target attachment to display
 * @param $options generic picker options
 *#
#macro (attachmentPicker_displayAttachmentDetails $attachment $options)
  #if ($attachment)
    ## Compute the attachment reference because there's no getter.
    #set ($attachmentReference = $services.model.createAttachmentReference($attachment.document.documentReference,
      $attachment.filename))
    #set ($attachmentStringReference = $services.rendering.escape($services.model.serialize($attachmentReference, 'default'), 'xwiki/2.1'))
    #if ($attachment.isImage() && $options.displayImage)
      ## We add the version to the query string in order to invalidate the cache when an image attachment is replaced.
      #set ($queryString = $escapetool.url({'version': $attachment.version}))
      [[[[image:${attachmentStringReference}||width=180 queryString="$queryString"]]>>attach:$attachmentStringReference]]
    #else
      * (% class="mime" %){{html wiki=false clean=false}}#mimetypeimg($attachment.getMimeType().toLowerCase() $attachment.getFilename().toLowerCase()){{/html}}(%%) (% class="filename" %)$services.rendering.escape($attachment.getFilename(), 'xwiki/2.1')(% %)
      * v$attachment.getVersion() (#dynamicsize($attachment.longSize))
      * $services.localization.render('core.viewers.attachments.author', [$!{xwiki.getUserName($attachment.author, false)}]) $services.localization.render('core.viewers.attachments.date', [$!{xwiki.formatDate($attachment.date, 'dd/MM/yyyy hh:mm')}])
      * (% class="buttonwrapper" %)[[${services.localization.render("${translationPrefix}.actions.download")}>>attach:${attachmentStringReference}||title="$services.localization.render("${translationPrefix}.actions.download")" rel="__blank" class="button"]](%%)
    #end
  #end
#end

#**
 * Writes the wiki code used at the end of an attachment box. Closes the inner frame div, and outputs the attachment actions.
 *
 * @param $actions a list of maps defining action buttons, where each entry contains a subset of the following:
 *        <dl>
 *          <dt>name</dt>
 *          <dd>identifies the action; the name is used as a CSS classname, and in the translation key for the display text, as "xe.attachmentSelector.actions.<name>"</dd>
 *          <dt>url</dt>
 *          <dd>the destination of the button</dd>
 *          <dt>rel</dt>
 *          <dd>an optional parameter to be used in the "rel" HTML attribute; for example "__blank" can be used to open the link in a new tab/window</dd>
 *        </dl>
 * @param $additionalContent optional additional content that does not follow the structure of the actions 
 *#
#macro (attachmentPicker_displayEndFrame $actions $additionalContent)
    )))## attachmentframe
    (% class="gallery_actions" %)(((
      #foreach ($action in $actions)
        #set( $actionname = $services.localization.render("${translationPrefix}.actions.${action.name}") )
        [[${actionname}>>path:${action.url}||class="tool ${action.name}" title="${actionname}" #if($action.rel) rel="${action.rel}"#end]]##
      #end
      $!additionalContent
    )))## actions
  )))## attachmentbox
#end

#**
 * Displays the upload box used for adding and selecting a new attachment.
 *
 * @param $targetDocument the document with the property being modified
 * @param $targetAttachDocument the document to upload the attachment to
 * @param $options generic picker options
 *#
#macro (attachmentPicker_displayUploadForm $targetDocument, $targetAttachDocument, $options)
#attachmentPicker_displayStartFrame({
   'value' : $services.localization.render("${translationPrefix}.upload.title"),
   'text' : $services.localization.render("${translationPrefix}.upload.title"),
   'cssClass' : 'gallery_upload'
  } $NULL)
{{html clean="false"}}
<form action="$targetAttachDocument.getURL('upload')" enctype="multipart/form-data" method="post" id="uploadAttachment" class="uploadAttachment xform">
  <div class="gallery_upload_input">
    #if (${options.rawfilter} != '')
      <span class="xHint">$escapetool.xml($services.localization.render("${translationPrefix}.upload.hint", [${options.rawfilter}]))</span>
    #end
    <input type="file" name="filepath" id="attachfile" class="noitems" title="$!{escapetool.xml($options.rawfilter)}"/>
    <input type="hidden" name="xredirect" value="$xwiki.getDocument($attachmentPickerDocName).getURL('get', "xaction=postUpload&amp;docAction=$!{escapetool.url($options.get('docAction'))}&amp;targetdocname=$!{escapetool.url($targetAttachDocument.fullName)}&amp;docname=$!{escapetool.url($targetDocument.fullName)}&amp;fieldname=$!{escapetool.url($options.get('classname'))}_$!{escapetool.url($options.get('object'))}_$!{escapetool.url($options.get('property'))}&amp;form_token=$!{services.csrf.getToken()}")" />
    <input type="hidden" name="docname" value="$!{escapetool.xml($targetDocument.fullName)}" />
    <input type="hidden" name="classname" value="$!{escapetool.xml($options.get('classname'))}" />
    <input type="hidden" name="object" value="$!{escapetool.xml($options.get('object'))}" />
    <input type="hidden" name="property" value="$!{escapetool.xml($options.get('property'))}" />
    <input type="hidden" name="form_token" value="$!{services.csrf.getToken()}" />
  </div>
  #if ("$!currentValue" != '' && $currentValue != $options.defaultValue)
    <div>
      <label>
        <input type="checkbox" name="filename" value="$!escapetool.xml($currentValue)"
          />$services.localization.render('attachmentSelector.replace',
          ["<strong>$!escapetool.xml($currentValue)</strong>"])
      </label>
      <span class="xHint">$escapetool.xml($services.localization.render('attachmentSelector.replace.hint'))</span>
    </div>
  #end
  #if ($xwiki.hasEditComment() && $options.versionSummary)
    <div>
    #if ($xwiki.isEditCommentFieldHidden())
      <input type="hidden" name="comment" value="$!escapetool.xml($request.comment)" />
    #else
      <label for="commentinput">$services.localization.render('core.comment')</label>
      <input type="text" name="comment" id="commentinput" value="$!escapetool.xml($request.comment)"
        title="$services.localization.render('core.comment.tooltip')" />
    #end
    </div>
  #end
  <div class="buttons">
    <span class="buttonwrapper">
    <input type="submit" name="action_upload" class="button " value='$services.localization.render("${translationPrefix}.upload.submit")'  title='$services.localization.render("${translationPrefix}.upload.submit")'/>
    </span>
  </div>
</form>
{{/html}}
#attachmentPicker_displayEndFrame ([])
#end

#**
 * Displays the "empty value" box, used for unsetting the field value.
 *
 * @param $targetDocument the document being modified
 * @param $targetAttachDocument the document that the attachments will the loaded from/saved to
 * @param $options generic picker options
 * @param $currentValue the currently selected file, used for determining if the empty box should be highlighted as the current value
 *#
#macro (attachmentPicker_displayAttachmentGalleryEmptyValue $targetDocument, $targetAttachDocument, $options, $currentValue)
  #if ("$!{options.get('defaultValue')}" != '')
    #set ($reference = ${options.get('defaultValue')})
    #set ($docNameLimit = $reference.indexOf('@'))
    #if ($docNameLimit > 0)
      #set ($docName = $reference.substring(0, $docNameLimit))
    #else
      #set ($docName = $targetAttachDocument.fullName)
    #end
    #set ($attachmentName = $reference.substring($mathtool.add($docNameLimit, 1)))
    #set ($defaultAttachment = $xwiki.getDocument($docName).getAttachment($attachmentName))
    #if ($defaultAttachment.isImage())
      #set($dcssClass = 'gallery_image')
    #end
  #end
  #attachmentPicker_displayStartFrame({'cssClass' : "gallery_emptyChoice $!{dcssClass}", 'text' : $services.localization.render("${translationPrefix}.default"), 'value' : "${options.defaultValue}"} $currentValue)
  #attachmentPicker_displayAttachmentDetails($defaultAttachment $options)
  #set ($returnURL = $escapetool.url($doc.getURL('view', $request.queryString)))
  #set ($selectURL = $targetDocument.getURL(${options.get('docAction')}, "${options.get('classname')}_${options.get('object')}_${options.get('property')}=&form_token=$!{services.csrf.getToken()}"))
  #attachmentPicker_displayEndFrame ([{'name' : 'select', 'url' : $selectURL}])
#end
{{/velocity}}

{{velocity}}
#if ($request.docname)
  #set ($targetDocument = $xwiki.getDocument($request.docname))
  #if ($request.targetdocname)
    ## Use the target document if it exists.
    #set ($targetAttachDocument = $xwiki.getDocument($request.targetdocname))
  #else
    ## Otherwise, just use the current document as the target to save/load attachments
    #set ($targetAttachDocument = $targetDocument)
  #end
  #if ("$!{request.savemode}" == 'direct')
    #set($docAction = 'save')
  #else
    #set($docAction = $targetAttachDocument.getDefaultEditMode())
  #end
  #set ($filter = [])
  #set ($rawfilter = '')
  #if ("$!{request.filter}" != '')
    #foreach ($value in $request.filter.trim().split('\s*+[,|; ]\s*+'))
      #if ("$!value" != '')
        #set ($discard = $filter.add($value.toLowerCase()))
        #set ($rawfilter = "${rawfilter}, ${value}")
      #end
    #end
    #if ($rawfilter != '')
      #set ($rawfilter = $rawfilter.substring(2))
    #end
  #end
  #if ("$!{request.displayImage}" == 'true')
    #set ($displayImage = true)
  #else
    #set ($displayImage = false)
  #end
  ### Determine attachment sorting
  #set($sortAttachmentsBy = "$!{request.sortAttachmentsBy}")
  #set ($validAttachmentProperties = ['filename', 'date', 'filesize', 'author', 'version', 'mimeType'])
  #if($sortAttachmentsBy == '' || $validAttachmentProperties.indexOf($sortAttachmentsBy) == -1)
    ### Default to sorting by filename, sort not requested.
    #set($sortAttachmentsBy = "filename")
  #end
  ### Set attachment sorting direction
  #if($sortAttachmentsBy == 'date')
    ### Sort the date descending
    #set($sortAttachmentsBy = "date:desc")
  #else
    ### Sort everything else ascending
    #set($sortAttachmentsBy = "${sortAttachmentsBy}:asc")
  #end
  #set ($options = {
    'classname' : ${request.get('classname')},
    'object' : $!{numbertool.toNumber($request.object).intValue()},
    'property' : ${request.property},
    'displayImage' : ${displayImage},
    'docAction' : ${docAction},
    'defaultValue' : "$!{request.defaultValue}",
    'rawfilter': "$!{rawfilter}",
    'filter': ${filter},
    'sortAttachmentsBy': ${sortAttachmentsBy},
    'versionSummary': $request.versionSummary.equals('true')
  })
  $!targetDocument.use($targetDocument.getObject($options.classname, $options.object))##
  #attachmentPicker_displayAttachmentGallery($targetDocument, $targetAttachDocument, $options)

  #set ($cancelLinkName = $services.rendering.escape($services.rendering.escape($services.localization.render("${translationPrefix}.cancel"), 'xwiki/2.1'), 'xwiki/2.1'))
  #set ($cancelLinkTarget = $services.rendering.escape($services.model.serialize($targetDocument), 'xwiki/2.1'))
  (% class="gallery_buttons buttons" %)(((
  (% class="buttonwrapper secondary" %)[[$cancelLinkName>>$cancelLinkTarget||class="button secondary" id="attachment-picker-close"]]
  )))
#end
{{/velocity}}
