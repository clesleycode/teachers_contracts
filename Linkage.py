import os, sys
import csv
import zipfile
import textwrap
from collections import defaultdict

 
def unzip(path):
    """ Unzips the files for eventual merging """

    # finds all zipped files in given directory
    listt = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('zip'):
                item = os.path.join(root, name)
                listt.append(item)
                
    # actual process of unzipping al the files
    with zipfile.ZipFile(str(listt[0])) as zf:
        for member in zf.infolist():
            words = member.filename.split('/')
            for word in words[:-1]:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir, ''): continue
                path = os.path.join(path, word)
            zf.extract(member, path)


def build(filename):
    """ Converts education data file to dictionary for matching """
    
    dictionary = {}
    with open(filename) as csvfile:     
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            dictionary[row[0]] = row
    return dictionary
    
    
def split(text):
    """ Outputs a dictionary of districts for each file"""
    
    filename = open(text, 'r')
    lines = {}
    for row in filename:
        item = row.split("\t")
        lines[item[1]] = item
    return lines
    
                  
def adjust(lines):
    for item in lines:
        if len(item) == 0:
            lines[lines.key(item)] = None
    
    
def print_items(dictionary):
    """Prints Matches in Wanted Format"""
    for item in dictionary:
        print(dictionary[item])
        
        
def get_columns(path):
    """Gets columns of each filename"""
    dictionary = {}
    columns = []
    for item in os.walk(path):
        line = item.readline().split("\t")
        dictionary[item] = line
        for item in line: 
            columns.append(item)
    return dictionary, columns
    
 
def most_common(columns):
    """Keeps track of most common column labels"""
    d = defaultdict(int)
    for i in columns:
        d[i] += 1
    result = max(d.iteritems(), key=lambda x: x[1])
    return result    
      
      
def initialize(dictionary, idee):
    """Initializes dictionary entry"""
    dictionary[idee] = {}


def add_data(dictionary, idee, label, data):
    """Adds data to dictionary"""
    dictionary[idee][label] = data
    
    
def output_result(text, widths, out, skip_title=False):
    """ Outputs final result in file format"""
    
    table = open(text, "r")
    title_sep = build(widths, '=') + '\n'
    row_sep = build(widths) + '\n'
    col_count = len(widths)

    out.write(row_sep)
    for table_row_i, row in enumerate(table):
        print table_row_i
        wrapped_columns = []
        wrap_lines_max = 1
        r = 0
        for w, col in zip(widths, row):
            last = r == (col_count - 1)
            r += 1
            wrapped = [adjust(x, w, last) for x in textwrap.wrap(col, w)]
            if len(wrapped) > wrap_lines_max:
                wrap_lines_max = len(wrapped)
            wrapped_columns.append(wrapped)
        
        for i in range(wrap_lines_max):
            out_row = []
            for j in range(col_count):
                try:
                    out_row += [wrapped_columns[j][i]]
                except IndexError:
                    last_pipe = '|' if j == (col_count - 1) else ''
                    out_row += ['|' + ' ' * widths[j] + last_pipe]
             
            out_row += ['\n']
            
            line_str = ''.join(out_row)
            out.write(line_str)

        if not table_row_i and not skip_title:
            out.write(title_sep)
        else:
            out.write(row_sep)
 

    
if __name__ == "__main__":
    
    # Prepares documents for matching
    unzip(sys.argv[1])
    compare = build(sys.argv[2])
    columns = get_columns(sys.argv[1])
    
    # Figures out keyword
    result = most_common(columns)
    
    # Sets up dictionary
    output = {}
    initialize(output, result)
    for item in os.walk(sys.argv[1]):
        split(item)
