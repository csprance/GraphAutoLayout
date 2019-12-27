# Substance Designer Graph Auto-Layout
> This is a part of Graph Auto-Layout plugin for Substance Designer
> Copyright (C) 2018 Alex Zotikov (twitter.com/z_fighting)
> Updated for 2019 by Chris Sprance (twitter.com/csprance)
> Published under GPLv2 license

![Example](https://csprance.com/shots/2019-12-27_e24433b4-a471-46ba-b517-49674742212a.gif)
# HELLO!

Nice that you decided to try the plugin.
Graph Auto-Layout plugin will try to transform your creative Substance Designer spaghetti graph
into something aligned and perfect, but at the same moment cold and faceless.
So please, use this tool carefully as a helper to organize your work structure.
I hope, it will save you some time.


# INSTALLATION

Currently supported versions:
* 2018.2
* 2018.3
* 2019

The easiest way to install the plugin is to copy the current folder to 
the default plugins directory:
`C:\Users\%USERNAME%\Documents\Allegorithmic\Substance Designer\python\sduserplugins`

If you already have your custom project in Substance Designer, copy the folder to 
any of your 4P (Project Python Plugin Paths)
Read about project settings here: 
https://support.allegorithmic.com/documentation/sddoc/add-custom-plugins-library-172818881.html


# USAGE

Once installed, plugin will add an Auto-Layout button to all your graph editors.
Also it will register an 'L' shortcut to use by default.
You can either press the button or a keyboard shortcut to run the tool.

There are several ways to use the tool:
* Select the nodes you want to arrange
* Select just one node - will arrange all the downstream (input) nodes
* Don't select anything and just press the button (works only in SBSGraph by now)

Just try it! You always have Ctrl+Z.


# SETTINGS

Settings for the tool (like shortcut or distance between the nodes) can be changed
in the settings.py file.


# CREDITS

This plugin was created by Alex Zotikov.
If you have any questions, issues or suggestions, send me a message in twitter:
https://twitter.com/z_fighting

Updated for Designer 2019 by @csprance
https://twitter.com/csprance
