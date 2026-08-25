---
id: xwiki-XWiki.Registration
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781905867000
sync_date: 2026-08-25 21:13:09
tags:
  - xwiki/documentation
  - space/xwiki
---
# Registration

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781905867000
- **Source:** [Registration](https://wiki.systemaops.in/bin/view/XWiki/XWiki.Registration)

---

{{template name="register_macros.vm"/}}

{{velocity}}
## The registration is enabled:
## - on the main wiki
## - on a subwiki if there is no service "$services.wiki.user"
## - on a subwiki where the user scope allows local users
#if($xcontext.isMainWiki() || "$!services.wiki.user" == '' || $services.wiki.user.getUserScope() != "GLOBAL_ONLY")
  ## These are defined in other places around XWiki, changing them here will result in undefined behavior.
  #set($redirectParam = 'xredirect')
  #set($userSpace = 'XWiki.')
  #set($loginPage = 'XWiki.XWikiLogin')
  #set($loginAction = 'loginsubmit')
  ##
  #set($documentName = 'XWiki.Registration')
  ##
  ## Security measure:
  ## If this document is changed such that it must have programming permission in order to run, change this to false.
  #set($sandbox = true)
  ##
  #set ($registrationConfig = $NULL)
  #_loadConfig($registrationConfig)
  ##
  #*
   * You may include this document in other documents using {{include reference="XWiki.Registration"/}}
   * To specify that the user is invited and should be allowed to register even if Guest does not have permission to
   * register, set $invited to true. NOTE: The including script must have programming permission to do this.
   *
   * To specify some code which should run after registration is successfully completed, set
   * $doAfterRegistration to a define block of velocity code like so:
   * #define($doAfterRegistration)
   *   some code
   * #end
   * Output from running this code will not be printed.
   *
   * The fields which will be seen on the registration page are defined here.
   * $fields is an array and each field is a Map. The names shown below are Map keys.
   *
   * Each field must have:
   *   name - this is the name of the field, it will be the value for "name" and "id"
   *
   * Each field may have:
   *   label - this String will be written above the field.
   *
   *   tag - the HTML tag which will be created, default is <input>, may also be a non form tag such as <img>
   *
   *   params - a Map, each key value pair will be in the html tag. eg: {"size" : "30"} becomes <input size=30...
   *
   *   validate a Map describing how to validate the field, validation is done in javascript then redone in velocity
   *   |        for security and because not everyone has javascript.
   *   |
   *   +-mandatory (Optional) - Will fail if the field is not filled in.
   *   | +-failureMessage (Required) - The message to display if the field is not filled in.
   *   | +-noscript (Optional) - will not be checked by javascript
   *   |
   *   +-regex (Optional) - Will validate the field using a regular expression.
   *   | |                  because of character escaping, you must provide a different expression for the
   *   | |                  javascript validation and the server side validation. Both javascript and server side
   *   | |                  validation are optional, but if you provide neither, then your field will not be validated.
   *   | |
   *   | +-failureMessage (Optional) - The message to display if the regex evaluation returns false.
   *   | +-jsFailureMessage (Optional) - The message for Javascript to display if regex fails.
   *   | |                               If jsFailureMessage is not defined Javascript uses failureMessage.
   *   | |                               NOTE: Javascript injects the failure message using createTextNode so &lt; will
   *   | |                                     be displayed as &lt;
   *   | |
   *   | +-pattern (Optional) - The regular expression to test the input at the server side, it's important to use
   *   | |                      this if you need to validate the field for security reasons, also it is good because not
   *   | |                      all browsers use javascript or have it enabled.
   *   | |
   *   | +-jsPattern (Optional) - The regular expression to use for client side, you can use escaped characters to avoid
   *   | |                        them being parsed as HTML or javascript. To get javascript to unescape characters use:
   *   | |                        {"jsPattern" : "'+unescape('%5E%5B%24')+'"}
   *   | |                        NOTE: If no jsPattern is specified, the jsValidator will try to validate
   *   | |                              using the server pattern.
   *   | |
   *   | +-noscript (Optional) - will not be checked by javascript
   *   |
   *   +-mustMatch (Optional) - Will fail if the entry into the field is not the same as the entry in another field.
   *   | |                      Good for password confirmation.
   *   | |
   *   | +-failureMessage (Required) - The message to display if the field doesn't match the named field.
   *   | +-name (Required) - The name of the field which this field must match.
   *   | +-noscript (Optional) - will not be checked by javascript
   *   |
   *   +-programmaticValidation (Optional) - This form of validation executes a piece of code which you give it and
   *   | |                                   if the code returns the word "failed" then it gives the error message.
   *   | |                                   Remember to put the code in singel quotes ('') because you want the value
   *   | |                                   of 'code' to equal the literal code, not the output from running it.
   *   | |
   *   | +-code (Required) - The code which will be executed to test whether the field is filled in correctly.
   *   | +-failureMessage (Required) - The message which will be displayed if evaluating the code returns "false"
   *   |
   *   +-fieldOkayMessage (Optional) - The message which is displayed by LiveValidation when a field is validated as okay.
   *                                   If not specified, will be $defaultFieldOkayMessage
   *
   *   noReturn - If this is specified, the field will not be filled in if there is an error and the user has to fix their
   *              registration information. If you don't want a password to be passed back in html then set this true
   *              for the password fields. Used for the captcha because it makes no sense to pass back a captcha answer.
   *
   *   doAfterRegistration - Some Velocity code which will be executed after a successfull registration.
   *                         This is used in the favorite color example.
   *                         Remember to put the code in singel quotes ('') because you want the 'code' entry to equal the literal
   *                         code, not the output from running it.
   *
   * Each field may not have: (reserved names)
   *   error - This is used to pass back any error message from the server side code.
   *
   * NOTE: This template uses a registration method which requires:
   *        * register_first_name
   *        * register_last_name
   *        * xwikiname
   *        * register_password
   *        * register2_password
   *        * register_email
   *        * template
   *       Removing or renaming any of these fields will result in undefined behavior.
   *
   *###
  #set($mainFields = [])

  ## The first name field.
  #set($field =
    {'name' : 'register_first_name',
      'label' : $services.localization.render('core.register.firstName'),
      'params' : {
        'type' : 'text',
        'size' : '60',
        'autocomplete' : 'given-name'
      }
    })
  #set($discard = $mainFields.add($field))
  ##
  ## The last name field.
  #set($field =
    {'name' : 'register_last_name',
    'label' : $services.localization.render('core.register.lastName'),
    'params' : {
      'type' : 'text',
      'size' : '60',
      'autocomplete' : 'family-name'
      }
    })
  #set($discard = $mainFields.add($field))
  ## The user name field, mandatory and programmatically checked to make sure the username doesn't exist.
  #set($field =
    {'name' : 'xwikiname',
      'label' : $services.localization.render('core.register.username'),
      'params' : {
        'type' : 'text',
        'onfocus' : 'prepareName(document.forms.register);',
        'size' : '60',
        'autocomplete' : 'username'
      },
      'validate' : {
        'mandatory' : {
          'failureMessage' : $services.localization.render('core.validation.required.message')
        },
        'programmaticValidation' : {
          'code' : '#nameAvailable($request.get("xwikiname"))',
          'failureMessage' : $services.localization.render('core.register.userAlreadyExists')
        }
      }
    })
  #set($discard = $mainFields.add($field))
  ## Make sure the chosen user name is not already taken
  ## This macro is called by programmaticValidation for xwikiname (above)
  #macro (nameAvailable, $name)
    #if ($xwiki.exists("$userSpace$name"))
      failed
    #end
  #end
  ##
  ##The password field, mandatory and must be at least 6 characters long.
  ##The confirm password field, mandatory, must match password field, and must also be 6+ characters long.
  #definePasswordFields($mainFields, 'register_password', 'register2_password', $registrationConfig.passwordOptions)
  ##
  ## The email address field, regex checked with an email pattern. Mandatory if registration uses email verification
  #set($field =
    {'name' : 'register_email',
      'label' : $services.localization.render('core.register.email'),
      'params' : {
        'type' : 'text',
        'size' : '60',
        'autocomplete' : 'email'
      },
      'validate' : {
        'regex' : {
          'pattern' : '/^([^@\s]+)@((?:[-a-zA-Z0-9]+\.)+[a-zA-Z]{2,})$/',
          'failureMessage' : $services.localization.render('xe.admin.registration.invalidEmail')
        }
      }
    })
  #if($registrationConfig.useEmailVerification)
    #set($field.validate.mandatory = {'failureMessage' : $services.localization.render('core.validation.required.message')})
  #end
  #set($discard = $mainFields.add($field))
  ##
  #*********
  ## Uncomment this code to see an example of how you can easily add a field to the registration page
  ## NOTE: In order to save the favorite color in the "doAfterRegistration" hook, this page must be
  ## saved by an administrator and can not self sandboxing.
  #set($sandbox = false)
  #set($field =
    {'name' : 'favorite_color',
      'label' : 'What is your favorite color',
      'params' : {
        'type' : 'text',
        'size' : '60'
      },
      'validate' : {
        'mandatory' : {
          'failureMessage' : $services.localization.render('core.validation.required.message')
        },
        'regex' : {
          'pattern' : '/^green$/',
          'failureMessage' : 'You are not cool enough to register here.'
        },
        'fieldOkayMessage' : 'You are awesome.'
      },
      'doAfterRegistration' : '#saveFavoriteColor()'
    })
  #set($discard = $mainFields.add($field))
  ## Save the user's favorite color on their user page.
  #macro(saveFavoriteColor)
    #set($xwikiname = $request.get('xwikiname'))
    #set($userDoc = $xwiki.getDocument("$userSpace$xwikiname"))
    $userDoc.setContent("$userDoc.getContent() ${xwikiname}'s favorite color is $request.get('favorite_color')!")
    ## The user (who is not yet logged in) can't save documents so saveWithProgrammingRights
    ## will save the document as long as the user who last saved this registration page has programming rights.
    $userDoc.saveWithProgrammingRights("Saved favorite color from registration form.")
  #end
  *********###
  ##
  ## To disable the CAPTCHA on this page, comment out the next entry.
  ## The CAPTCHA, not really an input field but still defined the same way.
  #if($services.captcha
      && !$invited
      && $xcontext.getUser() == "XWiki.XWikiGuest"
      && $registrationConfig.requireCaptcha)
    ## The CAPTCHA field, programmatically checked to make sure the CAPTCHA is right.
    ## Not checked by javascript because javascript can't check the CAPTCHA and the Ok message because it passes the
    ## mandatory test is misleading.
    ## Also, not filled back in if there is an error ('noReturn').
    #set($field =
      {'name' : 'captcha_placeholder',
        'label' : $services.localization.render('core.captcha.label'),
        'skipLabelFor' : true,
        'type'  : 'html',
        'html'  : "<span class='xHint'>$escapetool.xml($services.localization.render('core.captcha.instruction'))
          </span> $!{services.captcha.default.display()}",
        'validate' : {
          'programmaticValidation' : {
            'code' : '#if (!$services.captcha.default.isValid())failed#end',
            'failureMessage' : $services.localization.render('core.captcha.captchaAnswerIsWrong')
          }
        },
        'noReturn' : true
      })
    #set($discard = $mainFields.add($field))
  #end
  ## Pass the redirect parameter on so that the login page may redirect to the right place.
  ## Not necessary in Firefox 3.0.10 or Opera 9.64, I don't know about IE or Safari.
  #set($field =
    {'name' : $redirectParam,
      'params' : {
        'type' : 'hidden'
      }
    })
  #set($discard = $mainFields.add($field))
  #set($fields = $mainFields)
  ##
  #######################################################################
  ## The Code.
  #######################################################################
  ##
  ## This application's HTML is dynamically generated and editing in WYSIWYG would not work
  #if($xcontext.getAction() == 'edit')
    $response.sendRedirect("$xwiki.getURL($doc.getFullName(), 'edit')?editor=wiki")
  #end
  ##
  ## If this document has PR and is not included from another document then it's author should be set to Guest
  ## for the duration of it's execution in order to improve security.
  ## Note we compare document ids because
  #if($sandbox
      && $xcontext.hasProgrammingRights()
      && $xcontext.getDoc().getDocumentReference().equals($xwiki.getDocument($documentName).getDocumentReference()))
  ##
    $xcontext.dropPermissions()##
  #end
  ##
  ## Access level to register must be explicitly checked because it is only checked in XWiki.prepareDocuments
  ## and this page is accessible through view action.
  #if(!$xcontext.hasAccessLevel('register', 'XWiki.XWikiPreferences'))
    ## Make an exception if another document with programming permission (Invitation app) has included this
    ## document and set $invited to true.
    #if(!$invited || !$xcontext.hasProgrammingRights())
      $response.sendRedirect("$xwiki.getURL($doc.getFullName(), 'login')")
    #end
  #end
  ##
  ## Display the heading
  $registrationConfig.heading
  ## If the submit button has been pressed, then we test the input and maybe create the user.
  #if($request.getParameter('xwikiname'))
    ## Do server side validation of input fields.
    ## This will output messages if something goes wrong, nothing if everything is alright.
    ## We need to trim the output so that we can keep indentations in the validation script.
    #set ($validationText = $stringtool.trim("#validateFields($fields, $request)"))
    $validationText##
    ## If server side validation was successful, create the user
    #if($allFieldsValid)
      #createUser($fields, $request, $response, $doAfterRegistration)
    #end
  #end
  ## If the registration was not successful or if the user hasn't submitted the info yet
  ## Then we display the registration form.
  #if(!$registrationDone)
    $registrationConfig.welcomeMessage

    {{html clean="false"}}
      <form id="register" action="$xwiki.relativeRequestURL" method="post" class="xform half">
        <div class="hidden">
          #if ($request.xpage == 'registerinline')
            #skinExtensionHooks
          #end
          #set ($userDirectoryReference = $services.model.createDocumentReference('', 'Main', 'UserDirectory'))
          #if ($xwiki.exists($userDirectoryReference))
            <input type="hidden" name="parent" value="$!{services.model.serialize($userDirectoryReference, 'default')}" />
          #end
        </div>
        ## Note that the macro inject the form_token field.
        #generateHtml($mainFields, $request, 'false')
        <input type="hidden" name="form_token" value="$services.csrf.getToken()" />
        #generateJavascript($fields)
        <p class="buttons">
          <span class="buttonwrapper">
            <input type="submit" value="$services.localization.render('core.register.submit')" class="button"/>
          </span>
        </p>
      </form>
    {{/html}}

    ##
    ## Allow permitted users to configure this application.
    #if($xcontext.getUser() != 'XWiki.XWikiGuest' && $xcontext.hasAccessLevel("edit", $documentName))
      [[{{translation key="xe.admin.registration.youCanConfigureRegistrationHere"/}}>>XWiki.XWikiPreferences?section=Registration&editor=globaladmin#HCustomizeXWikiRegistration]]
      {{html}}<a href="$xwiki.getURL($documentName, 'edit', 'editor=wiki')">$services.localization.render('xe.admin.registration.youCanConfigureRegistrationFieldsHere')</a>{{/html}}
    #end
  #end
#else
  ## The registration is not allowed on the subwiki
  ## Redirecting to main wiki's registration page since local user registration is not allowed.
  #set($mainWikiRegisterPageReference = $services.model.createDocumentReference($services.wiki.mainWikiId, 'XWiki', 'Register'))
  #set($temp = $response.sendRedirect($xwiki.getURL($mainWikiRegisterPageReference, 'register', $request.queryString)))
#end
##
#*
 * Create the user.
 * Calls $xwiki.createUser to create a new user.
 *
 * @param $request An XWikiRequest object which made the register request.
 * @param $response The XWikiResponse object to send any redirects to.
 * @param $doAfterRegistration code block to run after registration completes successfully.
 *###
#macro(createUser, $fields, $request, $response, $doAfterRegistration)
  ## CSRF check
  #if(${services.csrf.isTokenValid("$!{request.getParameter('form_token')}")})
    ## See if email verification is required and register the user.
    #if($xwiki.getXWikiPreferenceAsInt('use_email_verification', 0) == 1)
      #set($reg = $xwiki.createUser(true))
    #else
      #set($reg = $xwiki.createUser(false))
    #end
  #else
    $response.sendRedirect("$!{services.csrf.getResubmissionURL()}")
  #end
  ##
  ## Handle output from the registration.
  #if($reg && $reg <= 0)
    {{error}}
    #if($reg == -2)
      {{translation key="core.register.passwordMismatch"/}}
    ## -3 means username taken, -8 means username is superadmin name
    #elseif($reg == -3 || $reg == -8)
      {{translation key="core.register.userAlreadyExists"/}}
    #elseif($reg == -4)
      {{translation key="core.register.invalidUsername"/}}
    #elseif ($reg == -9)
      {{translation key="core.register.invalidCaptcha"/}}
    ## Note that -10 is reserved already (see api.XWiki#createUser)
    #elseif($reg == -11)
      {{translation key="core.register.mailSenderWronglyConfigured"/}}
    #else
      {{translation key="core.register.registerFailed" parameters="$reg"/}}
    #end
    {{/error}}
  #elseif($reg)
  ## Registration was successful
    #set($registrationDone = true)
    ##
    ## If there is any thing to "doAfterRegistration" then do it.
    #foreach($field in $fields)
      #if($field.get('doAfterRegistration'))
        #evaluate($field.get('doAfterRegistration'))
      #end
    #end
    ## If there is a "global" doAfterRegistration, do that as well.
    ## Calling toString() on a #define block will execute it and we discard the result.
    #set($discard = $doAfterRegistration.toString())
    ##
    ## Define some strings which may be used by autoLogin or loginButton
    #set($userName = $!request.get('xwikiname'))
    #set($password = $!request.get('register_password'))
    #set($loginURL = $xwiki.getURL($loginPage, $loginAction))
    #if("$!request.getParameter($redirectParam)" != '')
      #set($redirect = $request.getParameter($redirectParam))
    #else
      #set($redirect = $registrationConfig.defaultRedirect)
    #end
    ## Display a "registration successful" message
    ## Define some strings which may be used by the welcome message
    #set($firstName = $!request.get('register_first_name'))
    #set($lastName = $!request.get('register_last_name'))
    #evaluate($registrationConfig.registrationSuccessMessage)

    ## Empty line prevents message from being forced into a <p> block.

    ## Give the user a login button which posts their username and password to loginsubmit
    #if($registrationConfig.loginButton)

      {{html clean=false wiki=false}}
        <form id="loginForm" action="$loginURL" method="post">
          <div class="centered">
          <input type="hidden" name="form_token" value="$!{services.csrf.getToken()}" />
          <input id="j_username" name="j_username" type="hidden" value="$escapetool.xml($!userName)" />
          <input id="j_password" name="j_password" type="hidden" value="$escapetool.xml($!password)" />
          <input id="$redirectParam" name="$redirectParam" type="hidden" value="$escapetool.xml($redirect)" />
          <span class="buttonwrapper">
            <input type="submit" value="$services.localization.render('login')" class="button"/>
          </span>
          #set ($mainPage = $services.wiki.currentWikiDescriptor.mainPageReference)
          #if ($xwiki.checkAccess($mainPage, 'view'))
            <span class="buttonwrapper">
              <a href="$!xwiki.getURL($mainPage)" rel="home" class="button secondary">
                $services.localization.render('core.register.successful.backtohome')
              </a>
            </span>
          #end
          </div>
        </form>
        ## We don't want autoLogin if we are administrators adding users...
        #if ($registrationConfig.autoLogin && $request.xpage != 'registerinline')
          <script>
            document.observe('xwiki:dom:loaded', function() {
              document.forms['loginForm'].submit();
            });
          </script>
        #end
      {{/html}}

    #end
  #end
  ##
#end## createUser Macro
{{/velocity}}
