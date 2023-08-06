Change log
==========

To see earlier changes please see HISTORY.txt.


3.0 (2021-10-08)
----------------
- remove support for Zope 2

- add support for Zope 4 on Python 2

- remove support for ``bootstrap.py`` for initializing the buildout

- reorganize package structure to fit with common Zope practices

- add linting and coverage testing with ``tox``

- simplify the ZMI add form and remove all LDAP-specific settings.
  Configuring the LDAPUserFolder inside the plugin should only be done
  on the user folder instance itself.


2.0 (2021-10-07)
----------------
- Major packaging cleanups

- Redo version pins to stay on Zope 2

- Switched documentation to point to the new Git repository

- Refactoring: Moved documentary text files into egg root

- Bug: Demangling user prefix could not deal with non-string user 
  ids, which may appear in certain cases.
  (https://bugs.launchpad.net/bugs/586931)

- Bug: Added GenericSetup magic to fully provide the INode interface
  for the exporter and importer classes, making it easier to nest 
  within other importers.
  (https://bugs.launchpad.net/bugs/586500)

- Bug: enumerateUsers returned undesired results if an exact match
  was required since LDAP searches are not case sensitive.
  (https://bugs.launchpad.net/bugs/585901)
