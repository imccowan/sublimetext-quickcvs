QuickCVS
=================

[Sublime Text 2](http://www.sublimetext.com/2) CVS plugin that helps... a little bit!...

Runs **cvs** on your console and prints output to Sublime Text 2 console.

---

- [Installation](#installation)
- [Features](#features)
- [Configuration](#configuration)
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
* Open folder in cervisia (linux only)

Usage
-------------
### Via Command Pallette
 * Bring up the Command Palette (`Command+Shift+P` on OS X, `Control+Shift+P` on Linux/Windows).
 * Type `QuickCVS` to select `QuickCVS: status`, `QuickCVS: diff`,...

### Via Tools Menu
 * Tools **>** QuickCVS
 * Click `Status`, `Diff`,...

When using `Diff` you can jump through differences using `F4` / `Shift+F4` .

Development (TODO)
-----------
* Fix `QuickCVS: log` encoding problems. See `"build_variant" :"log"` in [CVS.sublime-build](https://github.com/ePages-rnd/sublimetext-quickcvs/blob/master/CVS.sublime-build).
* Implement `cvs annotate` to render output into file buffer.
* Show CVS status in the editor status bar.
* Open the current cartridge in a graphical CVS tool.
* Open folder in CVS-GUI for windows platform.
* Show a graphical diff. Once you figure out how to render shell output into filebuffer, this is easy, when combind with the [FileDiffs](https://github.com/colinta/SublimeFileDiffs) plugin.
