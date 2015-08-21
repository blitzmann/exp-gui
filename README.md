# exp-gui

This is a simple GUI that I created to browse the expression tree of effects for EVE Online. It helped me put the pieces together, and I've released it as it may help someone else. You can search by effect name (autocomplete available), or if you have a particular expression ID that you want to view, you can enter that as well. There are two buttons that process each. 

The data itself is in two JSON files: `dgmeffects.json` and `dgmexpressions.json`. These files are produced with [Phobos](https://github.com/DarkFenX/Phobos) ([gui available here](https://github.com/blitzmann/phobos-gui)) in case you need to update them.

Due to the simplicity of the program, it is doubtful new features are needed, and so it is provided as-is.

Only Windows builds are available in the Releases section, but it can be run on any platform that supports python3 and has wxPython Pheonix installed ([daily snapshots here](http://wxpython.org/Phoenix/snapshot-builds/))

### Screenshot

![](https://camo.githubusercontent.com/d9c7ba7499284a43784cbef8bad700dad1f37571/687474703a2f2f692e696d6775722e636f6d2f45776e6b6c63782e706e67)
