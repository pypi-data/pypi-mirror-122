Change log
==========

To see earlier changes please see HISTORY.txt.

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


