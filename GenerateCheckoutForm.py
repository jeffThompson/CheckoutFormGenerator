
'''
GENERATE CHECKOUT FORM
Jeff Thompson | 2014 | www.jeffreythompson.org

A script that generates checkout forms and hang tags 
from a master list of students and equipment.

A FEW CAVEATS:
+ 	Since the forms result as HTML, you may run into some
	formatting issues when printing.
+ 	Forms should be printed in landscape format - Chrome
	seems to respect the CSS @page declaration, so I suggest
	printing from there.
+	The hang tags may be scaled for printing, so you will need
	to play with the CSS dimensions to get accurate sizes.
+	Not everything in the inventory is included on the form - I
	assume you don't need the value of the item on the checkout
	form, but it could easily be added if necessary.

REQUIRES:
+	BeautifulSoup for cleaning up the HTML output - not necessary
	and could be removed if needed

THANKS:
+	Writing UTF-8 files:
	http://www.azavea.com/blogs/labs/2014/03/solving-unicode-problems-in-python-2-7

'''

import csv, datetime, re, codecs
from bs4 import BeautifulSoup as bs 			# clean up resulting HTML (optional)


# basic variables
semester = 			'Fall 2014'					# for printing cover sheet and filename formatting
first_day = 		'08/25/14'					# for checkout dates - should be in MM/DD/YY format
due_day_of_week = 	'Monday'					# what day does checkout start?
due_time = 			'11am'						# what time is equipment due back?

checkout_weeks =	16							# how many weeks in the semester for checkout?
extra_students =	4							# how many blank lines for late adds?
extra_weeks = 		3							# how many extra checkout weeks to add?

contact_phone = 	'xxx.xxx.xxxx'				# info for hang tags
contact_email = 	'xxxx@xxxxx.edu'

# where can fees be paid?
fees_message = 'Fees can be paid in the CAL office (Peirce 308) or to any VA&T faculty'

# data files
student_list = 		'students.csv'				# file of students to load
equipment_list = 	'inventory.csv'				# file of equipment to load

# headers for student and checkout tables
student_header = 	[ 'NAME', 'ID #', 'CHECKOUT FORM?', 'FEE/PAID', 'FEE/PAID', 'FEE/PAID', 'NO FURTHER CHECKOUT' ]
item_header = 		[ 'WEEK', 'RESERVED FOR', 'CHECKED OUT TO', 'DATE DUE', 'DATED CHECKED IN', '# DAYS OVERDUE' ]


# store students and their details
class Student:
	def __init__(self, details):
		self.first_name = details[0].title()
		self.last_name = re.split('\W+', details[1].title())[1]
		self.id_num = details[2]
		self.checkout_form = False			# these below are not used for anything yet...
		self.has_fees = False
		self.no_further_checkout = False


# store items and their details
class Item:
	def __init__(self, details):
		self.item_id = details[0]
		self.item_name = details[1]
		self.short_desc = details[2]		# not included on the form
		self.should_include = details[3]
		self.manufacturer = details[4]
		self.model_num = details[5]			# not included on the form
		self.serial_num = details[6]
		self.category = details[7]			# not included on the form
		self.value = details[8]				# not included on the form


# load list of students
students = [ ]
with open(student_list) as input:
	all_students = csv.reader(input, quotechar='"')
	for details in all_students:
		students.append(Student(details))


# load list of equipment
equipment = [ ]
with open(equipment_list, 'rU') as input: 
	all_equipment = csv.reader(input, quotechar='"')
	next(all_equipment)	  					# skip header
	for details in all_equipment:
		equipment.append(Item(details))


# basic HTML page setup
first_day_of_semester = datetime.datetime.strptime(first_day, '%m/%d/%y')
output = '''<html>
<head>
	<title>CHECKOUT</title>
	<link href='stylesheet.css' rel='stylesheet' type='text/css'>
</head>

<body>
<div id="wrapper">
'''

# semester divider page
output += '<div id="semesterTitlePage">'
output += '<h1>' + semester.upper() + '</h1>'
output += '</div> <!-- end title page -->'
output += '<div class="pageBreak"></div>'


# generate students list
output += '<h1 class="pageLabel">LATE FEES</h1>'
output += '<span class="pageDetails">'
output += '<p><strong>ALL EQUIPMENT DUE BY ' + due_day_of_week.upper() + ' AT ' + due_time.upper() + '</strong></p>'
output += '''<p>If equipment is late (by even a few minutes), the equipment is considered a day late</p>
<p>''' + fees_message + '''</p></span><div class="clear"></div>'''

# table header
output += '<table><thead><tr>'
for label in student_header:
	output += '<td>' + label + '</td>'
output += '</tr></thead>'

# students list
for student in students:
	output += '<tr><td>' + student.first_name + ', ' + student.last_name + '</td><td>' + student.id_num + '</td>' + ('<td></td>' * 5) + '</tr>'

# some blanks for late-adds
for i in range(extra_students):
	output += '<tr>' + ('<td>&nbsp;</td>' * 7) + '</tr>'

output += '</table>'


# page break!
output += '''<div class="pageBreak"></div>'''


# load list of equipment
for index, item in enumerate(equipment):
		
		# title and description
		output += '<span class="equipmentDetails">'
		output += '<h1>' + item.item_id + ': ' + item.item_name.upper() + '</h1>'
		output += '<p>Manufacturer: <strong>' + item.manufacturer + '</strong><span class="spacer">|</span>Serial #: <strong>' + item.serial_num + '</strong></p>'

		output += '<h2>SHOULD INCLUDE</h2>'
		output += '<p>' + item.should_include + '</p>'

		# reminders
		output += '<p class="reminder"><strong>CHECK LATE FEES FIRST -- NO CHECKOUT UNTIL FEES ARE PAID!</strong></p>'
		output += '</span>'

		# thumbnail image
		output += '<img src="EquipmentImages/' + item.item_id + '.jpg" class="thumbnail" />'
		output += '<div class="clear"></div>'	

		# checkout table
		output += '<table><thead><tr>'
		for label in item_header:
			output += '<td>' + label + '</td>'
		output += '</tr></thead>'

		# checkout dates
		for i in range(0, checkout_weeks):
			# create each week in the semester, plus due date 1 week from then
			date_out = 'Monday, ' + (first_day_of_semester + datetime.timedelta(days=(i*7))).strftime('%B %-d')
			date_due = 'Monday, ' + (first_day_of_semester + datetime.timedelta(days=((i+1)*7))).strftime('%B %-d')
			output += '<tr><td>' + date_out + '</td><td></td><td></td><td>' + date_due + '</td><td></td><td></td></tr>'

		# add a few blank dates at the end as a buffer (you know, winter break, summer, etc)
		for i in range(0, extra_weeks):
			output += '<tr>' + ('<td>&nbsp;</td>' * 6) + '</tr>'
		output += '</table>'

		# notes form
		output += '<h2>NOTES</h2><p><em>Please note any problems with the equipment, broken or missing pieces, etc</em></p>'

		# page break
		if index < len(equipment)-1:
			output += '<div class="pageBreak"></div>'
			index += 1


# all done, close up HTML tags
output += '''</div>  <!-- end wrapper -->
</body>
</html>'''


# clean up HTML and save to file
soup = bs(output)
prettyHTML = soup.prettify()
semester = semester.replace(' ', '_')			# filename-friendly version
with codecs.open('Checkout-' + semester + '.html', 'w', encoding='utf-8') as html:
	html.write(prettyHTML)


# generate hang tags
output = '''<html>
<head>
	<title>HANG TAGS</title>
	<link href='stylesheet.css' rel='stylesheet' type='text/css'>
</head>

<body>
<div id="wrapper">'''

for item in equipment:

	# front
	output += '<div class="hangTag hangTagEquipmentInfo">'
	output += '<h1>' + item.item_name.upper() + '</h1>'
	output += '<p>ID #: <strong>' + item.item_id + '</strong><span class="spacer">|</span>Manufacturer: <strong>' + item.manufacturer + '</strong></p>'

	if item.should_include != '':
		output += '<p style="margin-top: 40px"><strong>SHOULD INCLUDE</strong></p>'
		output += '<p>' + item.should_include + '</p>'
	output += '</div> <!-- end hangTag front -->'

	# back (fold in half)
	output += '<div class="hangTag hangTagReturnInfo">'
	output += '''<h1>VA&T</h1>
	<h3>STEVENS INSTITUTE OF TECHNOLOGY</h3>
	<p>1 Castle Point on Hudson; Hoboken, New Jersey 07030</p>'''
	output += '<p>If found, please call ' + contact_phone + ' or email ' + contact_email + '.</p></div><!-- end hangTag back -->'

	# clear floating
	output += '<div class="clear"></div>'

output += '''</div>  <!-- end wrapper -->
</body>
</html>'''


# clean up HTML, save to file
soup = bs(output)
prettyHTML = soup.prettify()
with codecs.open('HangTags.html', 'w', encoding='utf-8') as html:
	html.write(prettyHTML)

