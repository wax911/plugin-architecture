# plugin-architecture

__Sample plugin architecture for python__

### Fundamental plugin concepts

- Discovery
- Registration
- Application hooks to which plugins attach
- Exposing application capabilities back to plugins

#### Discovery

This is the mechanism by which a running application can find out which plugins it has at its disposal. 
To "discover" a plugin, one has to look in certain places, and also know what to look for.

#### Registration

This is the mechanism by which a plugin tells an application - "I'm here, ready to do work". 
Admittedly, registration usually has a large overlap with discovery.

#### Application hooks

Hooks are also called "mount points" or "extension points". 
These are the places where the plugin can "attach" itself to the application, 
signaling that it wants to know about certain events and participate in the flow. 
The exact nature of hooks is very much dependent on the application. 

#### Exposing application API to plugins

To make plugins truly powerful and versatile, the application needs to give them access to itself, 
by means of exposing an API the plugins can use.

Inspired by: **[fundamental-concepts-of-plugin-infrastructures](https://eli.thegreenplace.net/2012/08/07/fundamental-concepts-of-plugin-infrastructures)**