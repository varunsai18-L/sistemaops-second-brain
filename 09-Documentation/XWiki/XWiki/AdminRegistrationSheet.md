---
id: xwiki-XWiki.AdminRegistrationSheet
type: XWiki Page
space: "XWiki"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781905843000
sync_date: 2026-08-16 19:44:53
tags:
  - xwiki/documentation
  - space/xwiki
---
# AdminRegistrationSheet

- **Space:** XWiki
- **Author:** XWiki.superadmin
- **Last Modified:** 1781905843000
- **Source:** [AdminRegistrationSheet](https://wiki.systemaops.in/bin/view/XWiki/XWiki.AdminRegistrationSheet)

---

{{velocity output="false"}}
### Globally administrate the registration of new users in a wiki.
#set ($params = {
  'registration': ['use_email_verification', 'validation_email_content',
                  'confirmation_email_content', 'invitation_email_content']
})
{{/velocity}}

{{include reference="XWiki.AdminFieldsDisplaySheet" /}}
