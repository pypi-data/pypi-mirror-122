# Footnotes2Biblio ![Version Dev](https://img.shields.io/badge/Version-0.0.2a-orange) ![License MIT](https://img.shields.io/github/license/ACour008/footnotes2biblio) ![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-blue)

`Footnotes2Biblio` creates a bibliography page from the footnotes in any `.docx` document. Great for academics who don't want to scroll through hundreds of pages trying to track down every single source.

## Table of Contents
1. [Key features](#key-features)
2. [Download](#download)
3. [How to use](#how-to-use)
4. [Notes and other TODOs & FIXMEs](#todos--fixmes)
5. [Credits](#credits)
6. [Licence](#licence)
7. [Socials](#socials)

## Key features
- Lightweight and relatively easy to use
- Citation-style agnostic. _Should_ work on most style guide.
- Simple syntax structure for marking in your doc what footnotes should be scraped.
(E.g., `{f mono 2}`\[citation\]`{/f}`)
- Saves you hours of scrolling back and forth trying to track down ***every. single. citation.***

## Download
Easiest way to download is to open your Terminal and type in the following: `python3 -m pip install footnotes2biblio`. All necessary files will be installed onto your machine.

## How to use
1. Set up your document to be scraped. Use the following syntax in your footnote sections to mark what should be scraped ('#' indicates the number of authors):
```
(f mono #} ... {/f} for monographs/books.
{f journo #} ... {/f} for journals/articles.
{f online #} ... {/f} for online or other sources.
{f juris} ... {/f} for court cases and other jurisprudence. No number argument required
{f legis} ... {/f} for legislation sources. No number argument required.

Note: it is recommended you make a backup of the document your are scaping. Safety first.
```
2. When you've marked your document, open your terminal again and type in `f2b src dst` where `src` is the path of the document you want scraped and `dst` is the document name of your soon to be bibliography.
(E.g., `f2b /Users/acour008/desktop/thesis.docx /Users/acour008/biblio.docx`)
3. Thats it! Now you get to marvel at the beauty and ease of it.

## TODOs & FIXMEs
Notes:
- This was scripted with McGill Legal Citation (8th ed) in mind, but it is still style agnostic as long as the author names are separated from the title with a comma (,).
- For best results, do not add whitespaces between {f}...{/f} tags.
- Again, make a back up of your work. I am not responsible for any unintended loss of data or written work.

TODOs:
- Add a `type` attribute to the `Footnote` class so instead of 4 different footnote lists and parsers, one parser can find the regex patterns necessary to match the sources and stuff into one list. This will make it easier to sort and print to a new document.

## Credits
This software uses the following:
- [python-docx](https://github.com/python-openxml/python-docx)
- [docx2python](https://github.com/ShayHill/docx2python)

## Licence
MIT

## Socials
- Github: [@ACour008](https://github.com/ACour008)
- Twitter: [@Cour008](https://twitter.com/cour008)