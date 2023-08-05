===============
Getting started
===============

Once the package is installed, this will by default enforce that a user will only have *one* logged in session. This will *not* proactively logout existing sessions: only if the user
logs in with another browser or device, the old session(s) will be closed.

You can disable the single session behavior by specifying the `SINGLE_USER_SESSION` setting in `settings.py` and thus setting this value to `False` (or any other value with truthiness `False`).

You can customise this behaviour by making the `SINGLE_USER_SESSION` setting be a string representing the name of a function which takes a user
object as an argument. If this function returns `True` then the user will be logged out. If it returns `False` then the user will not be logged out.

The tool will also clean up *all* sessions of a user in case that user logs out. This thus means that if a user logs out on one browser/device, they will log out on all other browsers/devices as well. This functionality is still enabled if `SINGLE_USER_SESSION` is set to `False`. You can disable this by setting the `LOGOUT_ALL_SESSIONS` setting in `settings.py` to `False` (or any other value with truthiness `False`).