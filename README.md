# Recipe Scraper

> recipe-scraper helps you transform recipes from cooking websites
> into machine-readable files

supported websites:

* www.marmiton.org
* www.atelierdeschefs.fr
* www.chefkoch.de

As a fallback for unknown websites, recipe-scraper looks for JSON-LD
content and tries to parse it. Since JSON-LD seems to be used by many
recipe websites that might give you usable results without having to
write a new importer.

supported export formats:

* Meal-Master (.mmf)
* Gourmet (.grmt)

You can run recipe-scraper by simply giving it a URL to a recipe.
It will then print out the recipe in meal master format.

```
recipe-scraper.py $URL_TO_RECIPE
```

## License

This program is licensed under the GPL version 3 or (at your option)
any later version.

The text of the GPL version 3 can be found in the file LICENSE.
