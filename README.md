# Novak
Novak is a small static site generator, which I had intended to use to make a site for sharing essays and short stories outside of the traditional blog format.

The default style and layout is very influenced by Matthew Butterick's [Practical Typography](https://practicaltypography.com), as well as Drew McConville's [Better Motherfucking Website](http://bettermotherfuckingwebsite.com), but it supports customization by creating Jinja2 templates and putting them in the `layouts` directory, and including them in your article's metadata.

If you want to use Novak yourself[^1], you need to install [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) and [Markdown2](https://github.com/trentm/python-markdown2), then clone this repo, delete the contents of the `articles` folder, and modify the layouts folders to fit your needs.

[^1]: Don't, I offer no guarantees that it will work for you, and you can get most of what it offers by working with [Zonelets](https://zonelets.net) and the [Zonelets RSS Feed Generator](https://github.com/goofpunk/Zonelets-RSS-Feed-Generator) I made last year.
