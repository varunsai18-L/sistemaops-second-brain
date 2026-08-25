---
id: xwiki-AppWithinMinutes.DynamicMessageTool
type: XWiki Page
space: "AppWithinMinutes"
author: "XWiki.superadmin"
version: "1.1"
last_modified: 1781906827000
sync_date: 2026-08-25 21:13:57
tags:
  - xwiki/documentation
  - space/appwithinminutes
---
# DynamicMessageTool

- **Space:** AppWithinMinutes
- **Author:** XWiki.superadmin
- **Last Modified:** 1781906827000
- **Source:** [DynamicMessageTool](https://wiki.systemaops.in/bin/view/AppWithinMinutes/AppWithinMinutes.DynamicMessageTool)

---

{{groovy}}
import com.xpn.xwiki.doc.XWikiDocument;
import com.xpn.xwiki.web.Utils;
import com.xpn.xwiki.web.XWikiMessageTool;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.xwiki.script.service.ScriptService;
import org.xwiki.component.descriptor.DefaultComponentDescriptor;

/**
 * Extends the default message tool with the ability to add/overwrite translation keys dynamically.
 * @deprecated since 4.5M1 the AppWithinMinutes wizard generates a translation bundle for each application so there's
 *             no need to use this hack any more. We keep it just to not break existing applications. It's enough to
 *             edit and save an existing application to migrate it to the new translation engine.
 */
public class XWikiDynamicMessageTool extends XWikiMessageTool
{
  private XWikiMessageTool msg;

  private Map<String, String> overwrites = new HashMap<String, String>();

  public XWikiDynamicMessageTool(XWikiMessageTool msg)
  {
    super(msg.bundle, msg.context);
    this.msg = msg;
  }

  // @Override
  public List<XWikiDocument> getDocumentBundles()
  {
    return this.msg.getDocumentBundles();
  }

  // @Override
  public String get(String key)
  {
    String result = super.get(key);
    return result == key ? this.msg.get(key) : result;
  }

  // @Override
  public String get(String key, Object... params)
  {
    String result = super.get(key, params);
    return result == key ? this.msg.get(key, params) : result;
  }

  // @Override
  protected String getTranslation(String key)
  {
    return this.overwrites.get(key);
  }

  public String put(String key, String value)
  {
    return this.overwrites.put(key, value);
  }
}

public class XWikiDynamicMessageToolFactory implements ScriptService
{
  public XWikiDynamicMessageTool createDynamicMessageTool(XWikiMessageTool msg, Map<?, ?> overwrites)
  {
    XWikiDynamicMessageTool dynamicMessageTool = new XWikiDynamicMessageTool(msg);
    for(Map.Entry<?,?> entry : overwrites.entrySet()) {
      dynamicMessageTool.put(entry.getKey(), entry.getValue());
    }
    return dynamicMessageTool;
  }
}

if (!services.component.componentManager.hasComponent(ScriptService.class, 'dynamicMessageToolFactory')) {
  def descriptor = new DefaultComponentDescriptor(implementation: XWikiDynamicMessageToolFactory.class, role: ScriptService.class, roleHint: 'dynamicMessageToolFactory');
  services.component.getComponentManager("wiki:${xcontext.database}").registerComponent(descriptor);
}
{{/groovy}}
