# Baby Registry

Gift registries nearly universally spy on you and sell your information to
advertisers or whatever. I want to make one that won't do that. Also I want
it to be fucking weird. For example, here's a dancing baby gif I found
which will be in my website.

Thanks! Excited to have a kid! See ya.

![A dancing baby GIF](public/images/dancing-baby.gif)

# Installation

1. Clone this repo
2. Download two fonts from fontshare: [supreme](https://www.fontshare.com/fonts/supreme)
   and [chubbo](https://www.fontshare.com/fonts/chubbo). When you download those, put
   the `-Variable.woff2` and `-VariableItalic.woff2` files in `public/fonts/`. I don't include
   these fonts in the repo because doing so would violate the license.
3. Run `npm install`.
4. You can then launch the development server with `npm run dev` or build the site with `npm run build`.

# Importing the items you want

Put a CSV file named `registry-info.csv` in `server/`, then run `registry_parser.py`. `registry-info.csv` should have the
following format:

| "UUID" | "Label for tag" | "Quantity" | "Link for new" | "Description" | "Specifications if buying used" |
| --- | --- | --- | --- | --- | --- |
| An ID for specifically identifying this item. The same item should always use the same UUID. Can just be a number. | The name of the item | How many of the item you want | A link to buy the item new | A description of the item | Things that are important to you for people buying the item used |