# mkdocs-revealjs

## :warning: Warning :warning:

* **THIS MKDOCS EXTENSION IS ON DEV/ALPHA MODE : IT IS NOT OPERATIONAL YET**
* **NEVERTHELESS, THIS MDKOCS DOCUMENTATION is a Work in Progress Mode**

## What is mkdocs-revealjs ?

**mkdocs-revealjs** is a configurable **Python Markdown extension for Mkdocs**, that directly renders Revealjs presentation in your mkdocs markdown pages.

## Prerequisites

Note that the npm package **reveal-md must be installed on the server** (and/or locally for debugging) for this extension to work with **mkdocs**, and hence allow Revealjs presentations.  

Install `reveal-md`, on Manjaro/Archlinux with :

`$ npm install -g reveal-md`

# mkdocs-revealjs is part of mkhack3rs

**mkdocs-revealjs** is one of several other one-line-install additional functionnalities for mkdocs.  
Please have a look at *mkhack3rs* site if interested :

*  [https://eskool.gitlab.io/mkhack3rs/](https://eskool.gitlab.io/mkhack3rs/)

# Installation

## Via PIP

**mkdocs-revealjs** is a Python package, to be installed via pip :

`$ pip install mkdocs-revealjs`

or upgrade via pip (if already installed)

`$ pip install --upgrade mkdocs-revealjs`

Project's page in PyPI is: [https://pypi.org/project/mkdocs-revealjs/](https://pypi.org/project/mkdocs-revealjs/)

## Via Conda or Mamba

Please have a look at [this github page](https://github.com/conda-forge/mkdocs-revealjs-feedstock) if you want get more precise instructions to install `mkdocs-revealjs` with **conda** or **mamba**, via the **conda-forge** github channel :

[https://github.com/conda-forge/mkdocs-revealjs-feedstock](https://github.com/conda-forge/mkdocs-revealjs-feedstock)

# Configuration

## Activation

Activate the `mkdocs_revealjs` extension. For example, with **Mkdocs**, you add a
stanza to `mkdocs.yml`:

```yaml
markdown_extensions:
    - mkdocs_revealjs
```

## Options

**Optionnally**, use any (or a combination) of the following options with all colors being written as:

* a **standard HTML Color Name** as in [this W3C page](https://www.w3schools.com/tags/ref_colornames.asp) (All Caps Allowed)
* an **HTML HEXADECIMAL COLOR, but WITHOUT THE # SIGN**

```yaml
markdown_extensions:
  - mkdocs_revealjs:
      vartable:                     # Specific Configs for Variations Tables
        light:                      # Light Theme Configs
          color: 044389                 # Any HTML Color Name, or, any HTML Hexadecimal color code WITHOUT the `#` sign
          bglabel: darksalmon           # Any HTML Color Name, or, any HTML Hexadecimal color code WITHOUT the `#` sign
          bgvi: FFFFFF                  # Any HTML Color Name, or, any HTML Hexadecimal color code WITHOUT the `#` sign
        dark:                       # Dark Theme Configs
          color: lavenderblush          # Any HTML Color Name, or, any HTML Hexadecimal color code WITHOUT the `#` sign
          bglabel: 7F0385               # Any HTML Color Name, or, any HTML Hexadecimal color code WITHOUT the `#` sign
          bgvi: red                     # Any HTML Color Name, or, any HTML Hexadecimal color code WITHOUT the `#` sign
        priority: 75                 # The priority for this Markdown Extension (DEFAULT : 75)
```

Where:

* `vartable` refers to configs which are specific to Maths Variation Tables
* `light` is the keyword for configs relative to **Light Theme** in Mkdocs
* `dark` is the keyword for configs relative to **Dark Theme** in Mkdocs
* `color` is a color option that modifies **The Color** of **ALL** the following caracteristics in Variation Tables :
    * both Borders and Arrows
    * All Texts (Labels, and non Labels)
    * **Defaults** for the `color` config param are :
        * `black` for Light Theme, and 
        * `white` for Dark Theme
* `bglabel` sets the Bakcground Color the the **Labels** (texts upon arrows mainly). 
    * **Defaults** for the `bgLabel` config param are:
        * `white` for Light Theme, and 
        * `2E303E` for Dark Theme = Default Mkdocs Material Dark Background for Slate
* `bgvi` sets the Background Color for **Valeurs Interdites (VI)** / **Forbidden Values (FV)** (the background inside the double vertical bars)
    * **Defaults** for the `bgvi` config param are :
        * `white` for Light Theme, and 
        * `2E303E` for Dark Theme = Default Mkdocs Material Dark Background for Slate
* `priority` (default `75`) sets the priority for this Markdown Extension

## Color Codes

Color Codes can be :

* a **standard HTML Color Name** as in [this W3C page](https://www.w3schools.com/tags/ref_colornames.asp) (All Caps Allowed)
* an **HTML HEXADECIMAL COLOR, WITHOUT THE # SIGN**

## Mixing & Conflicting Options

* No known conflicts with the **tkz-tab** syntax (may be with the `bglabel` config param? Please feel free to feedback any issue)
* **tkz-tab** colouring is compatible with **mkdocs-revealjs**

# Usage

To use it in your Markdown doc, 

(TO BE DONE)

# Examples

Other examples in these pages:

* Installation & Configs : [https://eskool.gitlab.io/mkhack3rs/maths/tables/](https://eskool.gitlab.io/mkhack3rs/maths/tables/)
* Examples : [https://eskool.gitlab.io/mkhack3rs/maths/tables/examples/](https://eskool.gitlab.io/mkhack3rs/maths/tables/examples/)

# CSS / JS Classes

* Each `vartable` svg img is preceded by a span tag with the two classes : `revealjs` and `vartable.

# Credits

* Rodrigo Schwencke for all credits : [rod2ik/mkdocs-revealjs](https://gitlab.com/rod2ik/mkdocs-revealjs)

# License

* All parts are from [Rodrigo Schwencke / rod2ik](https://gitlab.com/rod2ik) are [GPLv3+](https://opensource.org/licenses/GPL-3.0)
