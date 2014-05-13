#!/user/bin/python
# coding: utf-8

from Tkinter import *
import tkMessageBox
from tkFileDialog import askopenfilename, asksaveasfilename

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

import codecs

import ttk

# create a window
main_window = Tk()
main_window.wm_title("PDF to Web")
main_window.geometry('400x250')

# the original text files


# functions for buttons
def open_file():
	global file_list

	file_list = askopenfilename(multiple=1)

	# add the file names to the list
	for i, file_name in enumerate(file_list):
		file_listbox.insert(i, file_name)

def do_nothing():
   pass

def convert_pdf_to_txt(path):
	rsrcmgr = PDFResourceManager()
	retstr = StringIO()
	codec = 'utf-8'
	laparams = LAParams()
	device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
	file_pointer = file(path, 'rb')
	interpreter = PDFPageInterpreter(rsrcmgr, device)
	password = ""
	maxpages = 0
	caching = True
	pagenos=set()
	for page in PDFPage.get_pages(file_pointer, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
		interpreter.process_page(page)
	file_pointer.close()
	device.close()
	str = retstr.getvalue()
	retstr.close()
	return str

def create_websites():
	global file_list
	filename = asksaveasfilename()
	print(filename)
	n = 1
	if filename:
		for pdf_file_path in file_list:
			web_content = convert_pdf_to_txt(pdf_file_path)
			web_content = web_content.replace("\n\n", "<br><br>")
			web_content = web_content.replace(u"´ı", u"i")
			web_content = web_content.replace(u"ï¬", u"fi")
			web_content = web_content.replace(u"ï¬‚", u"fl")
			save_file_fp = codecs.open(filename+str(n)+".html", "w", encoding='utf8')
			save_file_fp.write("<!DOCTYPE HTML>\n<html><header></header><body><div style='max-width: 800px; margin: 0 auto;'>\n")
			save_file_fp.write(web_content)
			save_file_fp.write("</div></body>\n</html>")
			save_file_fp.close()
			n += 1

def keyPress_Delete(key_pressed):
	if key_pressed.char == '':
		file_listbox.delete(ACTIVE)

# open button
open_btn = Button(main_window, text="Open PDF files", command=open_file)
open_btn.pack(fill=X)

# list the selected files
file_listbox = Listbox(main_window)
file_listbox.pack(fill="both", expand=True)
file_listbox.bind('<Key>', keyPress_Delete)

# create button
create_btn = Button(main_window, text="Create Websites", command=create_websites)
create_btn.pack(fill=X)

main_window.mainloop()
