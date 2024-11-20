# Breeze Dark Icons — Static Edition

This repository puts together a "static" version of the **Breeze Dark** theme
which fixes some issues:

* [BUG 448169](https://bugs.kde.org/show_bug.cgi?id=448169) - fix the inlay icon in places being white.
   * _White inlays looks odd compared to the original dark inlays. Is it just me?_
   * _This happens because the inlay use the 'text colour', which is white for Breeze Dark._
   * _White inlays are harder to read. It's actually because it's not a compliant foreground/background colour for accessibility._
* [BUG 482648](https://bugs.kde.org/show_bug.cgi?id=482648) - fix symbolic icons not showing where expected, such as sidebars and toolbars.

Plus, some of my personal preferences applied — _design tastes are subjective!_

* Drop `places/96` and `64/folder-git.svg` icons as they look too thin.
* Revert to the older, brighter `folder-black` icon.
* Revert to the older dialog icons.
* Revert to the older `list-remove` icon.
* Revert to the older `application-x-trash` icon.
* Use non-symbolic weather applet icons _(due to a bug in this script)_

This exists because of bugs affecting icons under **Breeze Dark.**
Problems started around 5.87 when the recolouring accent colours were introduced,
and more recently (6.x) with changes to symbolic icons.

This repository fixes the icon (subjectively) for now, by taking a copy of the icons
and making them _static_ in a way that prevents them from being modified by KDE's
icon colouring logic. This theme could be useful for non-KDE environments too.


## Usage

The easiest approach is to clone this repository and install into your local icons folder:

```bash
mkdir -p ~/.local/share/icons
cd ~/.local/share/icons
git clone https://github.com/lah7/breeze-dark-icons-static.git
```

Then, select the icon theme via **System Settings** in KDE.

Later, to update this theme:

```bash
cd ~/.local/share/icons/breeze-dark-icons-static
git pull
```


## KDE vs GNOME Approach

To me, an icon theme has been traditionally static. If you look at GNOME and GTK based
distros _(of which I started my journey with, so it could be bias)_, they
typically have a separate theme per colour, like
[Ubuntu's Yaru](https://github.com/ubuntu/yaru/tree/master/icons) and
[Linux Mint's themes](https://github.com/linuxmint/mint-themes/tree/master/files/usr/share/themes).

KDE, on the other hand, have a single icon theme "Breeze" that is recoloured by code
in `kiconthemes`. It's a more dynamic approach and it has its merits: It is still a
standard SVG using CSS classes to recolour certain elements, meaning the default icon
will work just fine (quite statically) in other desktop environments. It would
save disk space too then duplicating icons in many colours.

When it comes to the dark theme... well... it's a moving part that can (and has) introduced bugs
as it tries to inherit the "Breeze" icon theme.

[This comment](https://bugs.kde.org/show_bug.cgi?id=494399#c3) by Nate Graham (a board member of KDE) highlights:
* There is no standardized way to recolour icons in the icon theme spec.
* Both KDE and GNOME are happy with their current ways and neither wish to change.
* KDE considers GNOME's implementation worse and a hack.

So it's a bit of a _stale-mate situation_. Currently, you can't choose
"Breeze" and use GTK apps, as they will have dark icons on your dark theme.
Yet, if you choose "Breeze Dark", you may encounter some bugs mentioned above
in KDE/Qt apps. It's not a great user experience for dark theme enthusiasts until
the bugs are squashed, or there's a standardised solution.


## License

[LGPL-3.0 license](LICENSE)
