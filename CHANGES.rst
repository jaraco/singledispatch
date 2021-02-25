v3.6.1
======

Fixed DeprecationWarnings referring to members from
``collections.abc`` referenced from ``collections``.

v3.6.0
======

#1: Added support for annotations as found on Python 3.7.

v3.5.0
======

Adopt semver for versioning.

Adopt jaraco/skeleton for packaging.

Declare support through 3.9.

#2: Tests now pass under pytest and when typing is present.

3.4.0.4
=======

Hosting moved to Github.

Now maintained by jaraco. Thanks to Łukasz Langa for the original
backport and maintenance.

Last version before switch to semver for versioning.

3.4.0.3
=======

Should now install flawlessly on PyPy as well. Thanks to Ryan Petrello
for finding and fixing the ``setup.py`` issue.

3.4.0.2
=======

Updated to the reference implementation as of 02-July-2013.

* more predictable dispatch order when abstract base classes are in use:
  abstract base classes are now inserted into the MRO of the argument's
  class where their functionality is introduced, i.e. issubclass(cls,
  abc) returns True for the class itself but returns False for all its
  direct base classes. Implicit ABCs for a given class (either
  registered or inferred from the presence of a special method like
  __len__) are inserted directly after the last ABC explicitly listed in
  the MRO of said class. This also means there are less "ambiguous
  dispatch" exceptions raised.

* better test coverage and improved docstrings

3.4.0.1
=======

Updated to the reference implementation as of 31-May-2013.

* better performance

* fixed a corner case with PEP 435 enums

* calls to `dispatch()` also cached

* dispatching algorithm now now a module-level routine called `_find_impl()`
  with a simplified implementation and proper documentation

* `dispatch()` now handles all caching-related activities

* terminology more consistent: "overload" -> "implementation"

3.4.0.0
=======

* the first public release compatible with 3.4.0
