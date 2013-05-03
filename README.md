QuickCVS
=================

[Sublime Text 2](http://www.sublimetext.com/2) CVS plugin that helps... a little bit!...

Runs **cvs** on your console and prints output to Sublime Text 2 console.

---

- [Installation](#installation)
- [Features](#features)
- [Development](#development)


Installation
------------
Follow [this readme](https://github.com/ePages-rnd/sublimetext-plugins).


Features
--------

* Status
* Diff
* Update
* Get Clean Copy
* Commit
* Open current folder in cervisia (linux only)

Configuration
-------------
* Create or append in file **Packages/User/Context.sublime-menu** to use cervisia feature:

```
[
    {
        "caption": "Open in cervisia",
        "command": "run_build_cvs",
        "args" : {
            "build_system" : "Packages/QuickCVS/CVS.sublime-build",
            "build_variant" :"cervisia"
        }
    }
]
```


Development
-----------
* Show CVS status in the editor status bar.
* Open the current cartridge in a graphical CVS tool.
* Show a graphical diff.
