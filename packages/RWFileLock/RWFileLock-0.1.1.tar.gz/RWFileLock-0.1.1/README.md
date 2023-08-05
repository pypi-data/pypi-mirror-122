# Readers / writers file lock Python helper class

This library was created in order to ease the synchronization of several processes
using shared resources, like a caching directory or a SQLite database. All of them
can use the resources, but only one should update them.

The library is being used in several INB projects.
