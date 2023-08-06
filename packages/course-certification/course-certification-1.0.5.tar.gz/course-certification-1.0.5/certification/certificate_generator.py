
##!/usr/local/bin/python

import gspread
import pystache;
import os;
import getpass;
import sys, argparse;
from datetime import datetime;
import pdfkit
from sys import stdout as out;
from oauth2client.service_account import ServiceAccountCredentials
import json
import imgkit
import pathlib
from tqdm import tqdm


parser = argparse.ArgumentParser()
parser.add_argument('--key', help='Full path of the Google Spreadsheet Json API key file', required=True, type=pathlib.Path)
parser.add_argument('--output', help='Destination folder for the generated certifiates', required=True, type=pathlib.Path)
parser.add_argument('--spreadsheet', help='Name of the Google Spreadsheet', required=True)
parser.add_argument('--worksheet', help='Name of the Worksheet inside Google Spreadsheet', required=True)
parser.add_argument('--resources', help='The directory containing resources required for generation', required=True, type=pathlib.Path)
parser.add_argument('--html', help='Generate HTML file', action='store_true', default=False)
parser.add_argument('--pdf', help='Generate PDF file', action='store_true', default=False)
parser.add_argument('--image', help='Generate Image (JPEG/PNG) file', action='store_true', default=False)
args = parser.parse_args()

if not args.key.exists():
    out.write('Key file: ' + str(args.key) + ' Does not exists \n')
    exit(1)
if not args.output.exists():
    out.write('Output folder: ' + str(args.output) + ' Does not exists \n')
    exit(1)
if not args.resources.exists():
    out.write('Resources folder: ' + str(args.resources) + ' Does not exists \n')
    exit(1)

renderer = pystache.Renderer();


def parse(template, base):
    tqdm.write("Reading Template: " + template)
    base = pathlib.Path(base).expanduser()
    t = open(base.joinpath(template), 'r')
    text = t.read()
    t.close()
    return pystache.parse(text)


def render(myParsed, hash, fullFileName=None, save_as_file=False):
    content = renderer.render(myParsed, hash);
    if save_as_file and fullFileName:
        outputFile = open(fullFileName, "w")
        outputFile.write(content);
        outputFile.close();
    return content


def createDirs(parentFolder, filename):
    fullFileName = parentFolder + filename;
    directory = os.path.dirname(fullFileName);
    if not os.path.exists(directory):
        os.makedirs(directory);
    return fullFileName;


def checkHeader(key, invheader):
    if (key not in invheader):
        tqdm.write("Your sheet does not have a column with name: " + key + ".")
        exit(1);
    if (invheader[key] == ''):
        tqdm.write("Your sheet does not have a value in column: " + key + ".")
        exit(1);

# if (len(sys.argv) != 5) and (len(sys.argv) != 6):
# 	print("Usage: " + sys.argv[0] + " <output folder> <spreadsheet name> <worksheet name> <login> [<password>]")
# 	exit(1);


parentFolder = str(args.output)
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
credentials = ServiceAccountCredentials.from_json_keyfile_name(args.key, scope);


gc = gspread.authorize(credentials)

# Open a worksheet from spreadsheet with one shot
wks = gc.open(args.spreadsheet).worksheet(args.worksheet)

list_of_lists = wks.get_all_values()
header=list_of_lists[0];

outFileNameColIdx = -1;
html_done_status = -1;
pdf_done_status = -1;
jpg_done_status = -1

inv_header = {};


def main():
    # File Name:<Parent Folder>/<Base Folder>/[html|pdf]/ <File Name>.[pdf|html]
    for i in range(len(header)):
        col = header[i];
        inv_header[col] = i;

    checkHeader("outputfilename", inv_header);
    checkHeader("template", inv_header);

    if 'html_done_status' in inv_header:
        html_done_status = inv_header['html_done_status'];

    if 'pdf_done_status' in inv_header:
        pdf_done_status = inv_header['pdf_done_status'];

    if 'jpg_done_status' in inv_header:
        jpg_done_status = inv_header['jpg_done_status'];

    if html_done_status == -1:
        idx = len(header)+1;
        wks.update_cell(1, idx, 'html_done_status');
        html_done_status = idx - 1;

    if pdf_done_status == -1:
        idx = len(header)+2;
        wks.update_cell(1, idx, 'pdf_done_status');
        pdf_done_status = idx - 1;

    if jpg_done_status == -1:
        idx = len(header)+3;
        wks.update_cell(1, idx, 'jpg_done_status');
        jpg_done_status = idx - 1;

    templates = {};
    for i in tqdm(range(1,len(list_of_lists))):
        tqdm.write("=======================================================")
        hash = {};
        row = list_of_lists[i];
        for j in range(len(row)):
            key = header[j];
            hash[key] = row[j];
        html_generated = False;
        tqdm.write('Generating Certificate for Serial: ' + hash['serial'] + '\n')
        tname = hash['template'];
        hash['TEMPLATE_PATH'] = args.resources.resolve()
        parsed = None;
        if tname in templates:
            parsed = templates[tname];
            tqdm.write("Found cached template: " + tname);
        else:
            tqdm.write("Parsing and caching template: " + tname);
            parsed = parse(tname, args.resources);
            templates[tname] = parsed;

        filename = hash['outputfilename'];

        baseFolder = parentFolder;
        if ('folder' in hash) and (hash['folder'] != ''):
            baseFolder = parentFolder + '/' + hash['folder'];

        htmlfile = None;

        if (not args.html):
            tqdm.write("Skipping HTML generation.");
            if hash.get('html_done_status', '') == '':
                hash['html_done_status'] = '-'
                wks.update_cell(i+1, html_done_status+1,  '-');
            htmlfile = hash['html_done_status'];
            html_content = render(parsed, hash, save_as_file=False);

        elif (hash.get('html_done_status', '') == '' ):
            tqdm.write('Generating the HTML: ');
            htmlfile = createDirs(baseFolder + "/html/", filename + ".html");

            html_content = render(parsed, hash, htmlfile, save_as_file=True);
            wks.update_cell(i+1, html_done_status+1,  htmlfile);
            html_generated = True;
            tqdm.write(htmlfile + ' \n')

        if (hash.get('pdf_done_status', '') == ''):
            pdffile = '-'
            if args.pdf:
                tqdm.write('Generating the PDF file \n');

                pdffile = createDirs(baseFolder + "/pdf/", filename + ".pdf");

                html2pdf = pdfkit.from_string(
                    html_content,
                    pdffile,
                    options = {
                        'orientation': 'Landscape',
                        'enable-local-file-access': '',
                        'quiet': '',
                        'page-size': 'A4',
                        'dpi': 400,
                        'margin-bottom': '0',
                        'margin-top': '0',
                        'margin-left': '0',
                        'margin-right': '0',
                        'disable-smart-shrinking': '',
                    }
                );
            wks.update_cell(i+1, pdf_done_status+1,  pdffile);
        else:
            tqdm.write('Skipping PDF Generation.');

        if (hash.get('jpg_done_status', '') == ''):
            jpgfile = '-'
            if args.image:
                tqdm.write('Generating the Image(jpg) file \n');

                jpgfile = createDirs(baseFolder + "/jpg/", filename + ".jpg");
                imgkit.from_string(
                    html_content,
                    jpgfile,
                    options={
                        'enable-local-file-access': '',
                        'quiet': '',
                    }
                )

            wks.update_cell(i+1, jpg_done_status+1,  jpgfile);
        else:
            tqdm.write('Skipping jpg Generation.');
