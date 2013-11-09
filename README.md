QuickCVS
=================

[Sublime Text 3](http://www.sublimetext.com/3) CVS plugin that helps! A little bit! That's a bold claim, I know, but you can take it to the bank.

Runs **cvs** on your console and prints output to Sublime Text 3 console.

---

- [Installation](#installation)
- [Features](#features)
- [Usage](#usage)
- [Development](#development-todo)


Installation
------------
Clone this repo into your Sublime Text 3/Packages directory. Rename it to "QuickCVS".


Features
--------

* Status
* Diff
* Update
* Get Clean Copy
* Commit

Usage
-------------
### Via Command Palette
 * Bring up the Command Palette (`Command+Shift+P` on OS X, `Control+Shift+P` on Linux/Windows).
 * Type `QuickCVS` to select `QuickCVS: status`, `QuickCVS: diff`,...

### Via Tools Menu
 * Tools **>** QuickCVS
 * Click `Status`, `Diff`, etc.

When using `Diff` you can jump through differences using `F4` / `Shift+F4` .

Development (TODO)
-----------
* Fix `QuickCVS: log` encoding problems. See `"build_variant" :"log"` in [CVS.sublime-build](https://github.com/ePages-rnd/sublimetext-quickcvs/blob/master/CVS.sublime-build).
* Implement `cvs annotate` to render output into file buffer.
* Show a graphical diff. Once you figure out how to render shell output into filebuffer, this is easy when combined with the [FileDiffs](https://github.com/colinta/SublimeFileDiffs) plugin.
