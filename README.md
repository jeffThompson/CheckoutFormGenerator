Checkout Form Generator
=====================

A script that generates checkout forms and hang tags from a master list of students and equipment.

**A FEW CAVEATS:**
* Since the forms result as HTML, you may run into some formatting issues when printing.
* Forms should be printed in landscape format - Chrome seems to respect the CSS @page declaration, so I suggest printing from there.
* The hang tags may be scaled for printing, so you will need to play with the CSS dimensions to get accurate sizes.
* Not everything in the inventory is included on the form - I assume you don't need the value of the item on the checkout form, but it could easily be added if necessary.

**REQUIRES:**
* BeautifulSoup for cleaning up the HTML output - not necessary and could be removed if needed

**THANKS:**
* Writing UTF-8 files:  
http://www.azavea.com/blogs/labs/2014/03/solving-unicode-problems-in-python-2-7
