# plugin-architecture

## Fundamental plugin concepts

- Discovery
- Registration
- Application hooks to which plugins attach (aka. "mount points")
- Exposing application capabilities back to plugins (aka. extension API)

#### Discovery

This is the mechanism by which a running application can find out which plugins it has at its disposal. 
To "discover" a plugin, one has to look in certain places, and also know what to look for. In our example, 
the discover_plugins function implements this - plugins are Python classes that inherit from a known base class, 
contained in modules located in known places.

#### Registration

This is the mechanism by which a plugin tells an application - "I'm here, ready to do work". 
Admittedly, registration usually has a large overlap with discovery, 
but I still want to keep the two concepts separate since it makes things more explicit 
(not in all languages registration is as automatic as our example demonstrates).

#### Application hooks

Hooks are also called "mount points" or "extension points". 
These are the places where the plugin can "attach" itself to the application, 
signaling that it wants to know about certain events and participate in the flow. 
The exact nature of hooks is very much dependent on the application. 
In our example, hooks allow plugins to intervene in the text-to-HTML transformation process performed by the application. 
The example also demonstrates both coarse grained hooks (processing the whole contents) and fine grained hooks 
(processing only certain marked-up chunks).

#### Exposing application API to plugins

To make plugins truly powerful and versatile, the application needs to give them access to itself, 
by means of exposing an API the plugins can use. 
In our example the API is relatively simple - the application simply passes some of its own internal objects to the plugins. 
APIs tend to get much more complex when multiple languages are involved. I hope to show some interesting examples in future articles.

**[Read full blog here](https://eli.thegreenplace.net/2012/08/07/fundamental-concepts-of-plugin-infrastructures)**