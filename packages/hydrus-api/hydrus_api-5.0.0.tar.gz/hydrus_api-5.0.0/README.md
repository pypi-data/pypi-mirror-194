# Hydrus API
Python module implementing the Hydrus API.

# Requirements
- Python >= 3.9 (I think; Let me know if you can use this with an older Python version)
- requests library (`pip install requests`)

# Installation
`$ pip install hydrus-api`

If you want to use the package in your own (installable) Python project, specify it in your `setup.py` using:
`install_requires=['hydrus-api']`.

# Contributing
Please feel free to contribute in the form of a pull request when the API changes (keep close to the existing code style
or you'll create more work than help); I've been bad about merging these until now, I'll try to be more conscientious of
them.

Try to avoid checking in your modifications to `.vscode/settings.json` and `.env` please.

I can't guarantee any fixed timespan in which I'll update this module myself when the API changes -- the only reason it
was updated now is because prkc kept bugging me; So if you desperately need this module to be updated, please create a
pull request.

# Description
Read the (latest) official documentation [here](https://hydrusnetwork.github.io/hydrus/help/client_api.html).

When instantiating `hydrus_api.Client` the `acccess_key` is optional, allowing you to initially manually request
permissions using `request_new_permissions()`. Alternatively there is `hydrus_api.utils.request_api_key()` to make this
easier. You can instantiate a new `Client` with the returned access key after that.

If the API version the module is developed against and the API version of the Hydrus client differ, there is a chance
that using this API module might have unintended consequences -- be careful.

If something with the API goes wrong, a subclass of `APIError` (`MissingParameter`, `InsufficientAccess`,
`DatabaseLocked`, `ServerError`) or `APIError` itself will be raised with the
[`requests.Response`](http://docs.python-requests.org/en/master/api/#requests.Response) object that caused the error.
`APIError` will only be raised directly, if the returned status code is unrecognized.

The module provides `Permission`, `URLType`, `ImportStatus`, `TagAction`, `TagStatus`, `PageType`, `PageState`,
`FileSortType`, `ServiceType`, `NoteConflictResolution` and `DuplicateStatus` Enums for your convenience. Due to a
limitation of JSON, all dictionary keys that are returned by the client will be strings, so when using Enum members to
index a dictionary that was returned by the client, make sure to use the string representation of its value. Usually you
would have to do this: `str(Enum.member.value)`, but the listed Enums allow you to just do `str(Enum.member)` instead to
get the string representation of the member's value directly.

The module provides convenience functions in `hydrus_api.utils` that are not strictly part of the API, e.g.
`add_and_tag_files()` and `get_page_list()`; read their docstrings to figure out what they do.

The client methods `add_file()` and `add_and_tag_files()` accept `str`, `pathlib.Path` and objects that implement the
internal `BinaryFileLike` protocol (i.e. all objects that provide a `read()`-method that returns `bytes`).

The function `hydrus_api.utils.parse_hydrus_metadata_file` behaves similarly, except that it accepts objects that
implement the internal `TextFileLike` protocol (i.e. its `read()`-method returns a string).

Check out `examples/` for some example applications. Some of them might be outdated, but they should be good enough to
give you an idea how to use the module.

# Changes with v5.0.0
To avoid confusion, starting with v5.0.0, responses will be returned unmodified from the API, exactly like described in
the official documentation. The previous functionality of automatically indexing a single top-level key has been
removed.
