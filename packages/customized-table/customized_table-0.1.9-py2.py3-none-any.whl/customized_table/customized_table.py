from IPython.display import HTML, display
import sys
from termcolor import colored

#
# Default colors.
#
default_colors = {
    "id": "#666",
    "name": "#b40403",
    "category": "#fb4b04",
    "value": "#3b08d3",
    "percent": "#7a03fc",
    "param-key": "#777",
    "param-value": "#1a07d0",
    "time": "#db6c00",
    "text": "#888",
    "size": "#e2b102",
    "no": "#f00",
    "yes": "#090",
    
    "id-light": "#ccc",
    "name-light": "#fd8f8e",
    "category-light": "#febda3",
    "value-light": "#b198fb",
    "percent-light": "#d0a5fe",
}

#
# Replaces color tag with default colors (if found).
#
def tag_default_color(col):
    if col.lower() in default_colors:
        return default_colors[col.lower()]
    return col

#
# Replaces cell contents with formatted values (if found).
#
def tag_cellformat(cell, p):
    # List
    if "cell-format" in p and (p["cell-format"] == "list" or p["cell-format"].startswith("list:")) and type(cell) == list:
        if "num-format" in p:
            cell = [tag_numformat(x,p) for x in cell]
        cell = [str(x) for x in cell]
        delimiter = ", "
        pv = p["cell-format"]
        if ":" in pv:
            delimiter = pv[pv.find(":")+1:]
            delimiter = delimiter.replace("\n", "<br>")
        return delimiter.join(cell)
    # Tagged text
    if "cell-format" in p and p["cell-format"] == "tag-text" and type(cell) == str:
        cell = tag_text(cell)
    
    return cell

#
# Formats a value with prefix (for example M for million).
#
def tag_prefixformat(cell, fmt):
    if type(cell) not in [int,float]:
        return cell
    
    prefixes = [
        [1e12, "T"],
        [1e9, "G"],
        [1e6, "M"],
        [1e3, "k"],
    ]
    
    # Iterate over prefixes
    for p in prefixes:
        if cell >= p[0]:
            if cell % p[0] == 0:
                return f"{cell/p[0]:.0f}{p[1]}"
            else:
                if fmt.endswith("-2"):
                    return f"{cell/p[0]:.2f}{p[1]}"
                if fmt.endswith("-1"):
                    return f"{cell/p[0]:.1f}{p[1]}"
                return f"{cell/p[0]}{p[1]}"
    
    # No prefix match
    if fmt.endswith("-2"):
        return f"{cell:.2f}"
    if fmt.endswith("-1"):
        return f"{cell:.1f}"
    return f"{cell}"

#
# Replaces numbers with formatted values (if found).
#
def tag_numformat(cell, p):
    if "num-format" in p and (type(cell) == float or type(cell) == int):
        if p["num-format"] == "pct-0":
            return f"{cell*100:.0f}%"
        if p["num-format"] == "pct-1":
            return f"{cell*100:.1f}%"
        if p["num-format"] == "pct-2":
            return f"{cell*100:.2f}%"
        if p["num-format"] == "pct-3":
            return f"{cell*100:.3f}%"
        if p["num-format"] == "pct-4":
            return f"{cell*100:.4f}%"
        if p["num-format"] == "pct-5":
            return f"{cell*100:.5f}%"
        if p["num-format"] == "pct-6":
            return f"{cell*100:.6f}%"
        
        if p["num-format"] == "dec-1":
            return f"{cell:.1f}"
        if p["num-format"] == "dec-2":
            return f"{cell:.2f}"
        if p["num-format"] == "dec-3":
            return f"{cell:.3f}"
        if p["num-format"] == "dec-4":
            return f"{cell:.4f}"
        if p["num-format"] == "dec-5":
            return f"{cell:.5f}"
        if p["num-format"] == "dec-6":
            return f"{cell:.6f}"
        
        if p["num-format"].startswith("prefix"):
            return tag_prefixformat(cell, p["num-format"])
        
        if p["num-format"] == "int" or p["num-format"] == "dec-0":
            return f"{cell:.0f}"
    return cell
    
#
# Converts a cell text containing tags to correct format.
#
def tag_text(txt):
    # No tags found
    if "<" not in txt:
        return txt

    # Replace tags with HTML/CSS
    s = ""
    while "<" in txt:
        si = txt.find("<")
        ei = txt.find(">", si)
        tags = txt[si+1:ei]

        # Build new string
        s += txt[:si]
        txt = txt[ei+1:]
        if tags == "/":
            s += "</span>"
        else:
            tag = tags.split(" ")
            if "|" in tags:
                tag = tags.split("|")
            style = ""
            for ti in tag:
                if ti == "bold":
                    style += "font-weight:bold;"
                elif ti == "italic":
                    style += "font-style:italic;"
                elif ti == "normal":
                    style += "font-style:normal;"
                else:
                    ti = tag_default_color(ti)
                    style += f"color:{ti};"
            s += f"<span style='{style}'>"

    # Add last part
    s += txt
    
    # Line breaks
    s = s.replace("\n", "<br/>")
    
    return s

#
# Remove tags from text.
#
def remove_tags(txt):
    if type(txt) != str:
        return txt
    
    # No tags found
    if "<" not in txt:
        return txt

    # Remove tags
    s = ""
    while "<" in txt:
        si = txt.find("<")
        ei = txt.find(">", si)
        
        # Build new string
        s += txt[:si]
        txt = txt[ei+1:]

    # Add last part
    s += txt
    return s

#
# Fix colors to Excel style.
#
def fix_excel_color(col):
    if col.startswith("#") and len(col) == 4:
        col = "#" + col[1]*2 + col[2]*2 + col[3]* 2
    return col

#
# Convert css style to Excel style.
#
def to_excel_style(style, workbook):
    style = style.copy()
    update_tags(style)
    
    est = {}
    if "font-family" in style:
        est["font_name"] = style["font-family"]
    if "font-size" in style:
        est["font_size"] = style["font-size"].replace("px","").replace(" ","")
    if "background" in style:
        col = fix_excel_color(style["background"])
        if col not in ["white", "#ffffff"]:
            est["bg_color"] = col
    if "color" in style:
        est["font_color"] = fix_excel_color(style["color"])
    if "font-weight" in style and style["font-weight"] == "bold":
        est["bold"] = True
    if "border-top" in style:
        est["top"] = 1
    if "border-bottom" in style:
        est["bottom"] = 1
    if "border-left" in style:
        est["left"] = 1
    if "border-right" in style:
        est["right"] = 1
    if "num-format" in style:
        if style["num-format"] in ["dec-0", "int"]:
            est["num_format"] = "0"
        if style["num-format"] == "dec-1":
            est["num_format"] = "0.0"
        if style["num-format"] == "dec-2":
            est["num_format"] = "0.00"
        if style["num-format"] == "dec-3":
            est["num_format"] = "0.000"
        if style["num-format"] == "dec-4":
            est["num_format"] = "0.0000"
            
        if style["num-format"] == "pct-1":
            est["num_format"] = "0.0%"
        if style["num-format"] == "pct-2":
            est["num_format"] = "0.00%"
        if style["num-format"] == "pct-3":
            est["num_format"] = "0.000%"
        if style["num-format"] == "pct-4":
            est["num_format"] = "0.0000%"
            
    return workbook.add_format(est)

#
# Updates style to correct css tag.
#
def update_tags(p):
    # Font shorthand tag
    if "font" in p:
        vals = p["font"].split(" ")
        if "|" in p["font"]:
            vals = p["font"].split("|")
        for v in vals:
            if v == "bold":
                p["font-weight"] = "bold"
            elif v == "italic":
                p["font-style"] = "italic"
            elif v == "normal":
                p["font-style"] = "normal"
            elif v.endswith("px"):
                p["font-size"] = v
            else:
                p["font-family"] = v
        del p["font"]
    
    # Border shorthand tag
    if "border" in p:
        vals = p["border"].split(" ")
        if "|" in p["border"]:
            vals = p["border"].split("|")
        if "top" in vals:
            p["border-top"] = 1
        if "bottom" in vals:
            p["border-bottom"] = 1
        if "left" in vals:
            p["border-left"] = 1
        if "right" in vals:
            p["border-right"] = 1
        del p["border"]
    
    # Re-format to correct CSS borders
    if "border-top" in p and str(p["border-top"]) == "1":
        p["border-top"] = "1px solid #aaa"
    if "border-bottom" in p and str(p["border-bottom"]) == "1":
        p["border-bottom"] = "1px solid #aaa"
    if "border-left" in p and str(p["border-left"]) == "1":
        p["border-left"] = "1px solid #aaa"
    if "border-right" in p and str(p["border-right"]) == "1":
        p["border-right"] = "1px solid #aaa"
        
    # Padding
    if "padding" in p:
        vals = p["padding"].split(" ")
        if "|" in p["padding"]:
            vals = p["padding"].split("|")
        if len(vals) == 4:
            p["padding-top"] = vals[0]
            p["padding-right"] = vals[1]
            p["padding-bottom"] = vals[2]
            p["padding-left"] = vals[3]
        if len(vals) == 3:
            p["padding-top"] = vals[0]
            p["padding-right"] = vals[1]
            p["padding-bottom"] = vals[2]
            p["padding-left"] = vals[1]
        if len(vals) == 2:
            p["padding-top"] = vals[0]
            p["padding-right"] = vals[1]
            p["padding-bottom"] = vals[0]
            p["padding-left"] = vals[1]
        if len(vals) == 1:
            p["padding-top"] = vals[0]
            p["padding-right"] = vals[0]
            p["padding-bottom"] = vals[0]
            p["padding-left"] = vals[0]
        del p["padding"]

    # Re-format default colors
    if "color" in p:
        p["color"] = tag_default_color(p["color"])
    if "background" in p:
        p["background"] = tag_default_color(p["background"])


#
# Generates a table that is styled using css.
#
class CustomizedTable:
    #
    # Init new table with the specified columns (and optional default style).
    #
    def __init__(self, cols, style={}, header_style={}, subheader_style={}, width=None, header=True, tag_warnings=True):
        if not self.valid(cols, [list]): cols = list(cols)
        if not self.valid(style, [dict]): style = {}
        if not self.valid(header, [bool]): header = True
        self.tag_warnings = tag_warnings
        self.valid_style(style)
        self.valid_style(header_style)
        self.valid_style(subheader_style)
        self.style_rules = []
        
        self.width = width
        self.cols = cols # Columns
        self.w = [-1] * len(cols) # Column width
        self.rows = [] # Rows
        self.styles = {} # Css-styles
        self.header = header
        
        # Default style
        self.default_style = {
            "font": "Courier 12px",
            "text-align": "left",
            "background": "white",
            "padding-top": "3px",
            "padding-bottom": "3px",
            "padding-left": "5px",
            "padding-right": "15px",
        }
        for tag,val in style.items():
            self.default_style.update({tag: val})
        
        # Header style
        self.header_style = {
            "font": self.default_style["font"] + " bold",
            "color": "black",
            "background": "#ddd",
            "padding-top": "3px",
            "padding-bottom": "3px",
            "padding-left": "5px",
            "padding-right": "15px",
            "border": "top bottom",
        }
        for tag,val in header_style.items():
            self.header_style.update({tag: val})
        
        # Footer style
        self.subheader_style = {
            "font": self.default_style["font"] + " bold",
            "color": "black",
            "background": "#ddd",
            "border": "top bottom",
            "row-toggle-background": "0",
        }
        for tag,val in subheader_style.items():
            self.subheader_style.update({tag: val})
        
    #
    # Checks if style tag contains valid tags.
    #
    def valid_style(self, style):
        # Check if warnings are enabled
        if not self.tag_warnings:
            return
        # Check if style is optional
        if style is None:
            return
        # Check tags in style
        used_tags = set(["color", "background", "font", "border", "text-align", "row-toggle-background", "num-format", "cell-format", "padding"])
        for tag in style.keys():
            if tag not in used_tags:
                # Get caller function
                w = colored("Warning ", "red", attrs=["bold"]) + colored(f"{sys._getframe().f_back.f_code.co_name}", "blue") + ": "
                print(w + f"tag " + colored(tag, "yellow", attrs=["bold"]) +  " is not valid")
    
    #
    # Checks if a value is valid.
    #
    def valid(self, value, types, min_val=None, max_val=None, length=None):
        # Get caller function
        w = colored("Warning ", "red", attrs=["bold"]) + colored(f"{sys._getframe().f_back.f_code.co_name}", "blue") + ": " 
        
        if value is None:
            print(w + "value is none")
            return False
        if types is not None and type(value) not in types:
            print(w + f"value '{value}' is not a valid type (should be {','.join([x.__name__ for x in types])})")
            return False
        if type(value) == int and min_val is not None and value < min_val:
            print(w + f"value '{value}' is out of bounds (<{min_val})")
            return False
        if type(value) == int and max_val is not None and value > max_val:
            print(w + f"value '{value}' is out of bounds (>{max_val})")
            return False
        if type(value) == list and length is not None and len(value) != length:
            print(w + f"expected list size {length}, got {len(value)}")
            return False
        
        return True
    
    #
    # Returns current number of rows.
    #
    def no_rows(self):
        return len(self.rows)
    
    #
    # Sets column width for the specified column (column name or number). 
    #
    def column_width(self, cols, width):
        if type(cols) in [int,str]: cols = [cols]
        if not self.valid(cols, [list,range]): return
        
        for col in cols:
            if not self.valid(col, [str,int], min_val=0, max_val=len(self.cols)-1): return
            col = self.column_number(col)
            self.w[col] = width
    
    #
    # Returns the column number for a column.
    #
    def column_number(self, col):
        if type(col) == int:
            return col
        if type(col) == str:
            for ci,c in enumerate(self.cols):
                if c == col:
                    return ci
        print(colored("Warning ", "red", attrs=["bold"]) + colored(f"{sys._getframe().f_back.f_code.co_name}", "blue") + f": column '{col}' not found")
        return -1
        
    #
    # Set styles for one or more columns (column names or numbers).
    #
    def column_style(self, cols, style):
        if type(cols) in [int,str]: cols = [cols]
        if not self.valid(cols, [list,range]): return
        if not self.valid(style, [dict]): return
        self.valid_style(style)
        
        for col in cols:
            if not self.valid(col, [str,int], min_val=0, max_val=len(self.cols)-1): return
            col = self.column_number(col)
            key = f"{col}-*"
            self.styles[key] = style
       
    #
    # Set styles for one or more rows (row numbers).
    #
    def row_style(self, rows, style):
        if type(rows) == int: rows = [rows]
        if not self.valid(rows, [list,range]): return
        if not self.valid(style, [dict]): return
        self.valid_style(style)
        
        for row in rows:
            # Set to last row
            if row == -1:
                row = self.no_rows() - 1
            if not self.valid(row, [int], min_val=0): return
            key = f"*-{row}"
            self.styles[key] = style
        
    #
    # Sets style for one or more cells (column names or numbers + row numbers).
    #
    def cell_style(self, cols, rows, style):
        if type(cols) in [int,str]: cols = [cols]
        if type(rows) == int: rows = [rows]
        if not self.valid(cols, [list,range]): return
        if not self.valid(rows, [list,range]): return
        if not self.valid(style, [dict]): return
        self.valid_style(style)
        
        for row in rows:
            # Set to last row
            if row == -1:
                row = self.no_rows() - 1
            if not self.valid(row, [int], min_val=0): return
            
            for col in cols:
                if not self.valid(col, [str,int], min_val=0, max_val=len(self.cols)-1): return
                col = self.column_number(col)
                key = f"{col}-{row}"
                self.styles[key] = style
    
    
    #
    #
    #
    def style_rule(self, col, comp, val, style, cidx=None):
        if not self.valid(col, [int,str]): return
        if not self.valid(val, [int,float,str]): return
        if not self.valid(style, [dict]): return
        if comp not in [">",">=","<","<=","=","=="]: return
        
        col = self.column_number(col)
        if cidx is not None:
            cidx = self.column_number(cidx)
        self.style_rules.append([col, comp, val, style, cidx])
    
    #
    # Adds a row to the table.
    #
    def add_row(self, row, style=None):
        if not self.valid(row, [list], length=len(self.cols)): return
        self.valid_style(style)
        
        self.rows.append(row)
        if style is not None:
            if not self.valid(style, [dict]): return
            
            self.row_style(self.no_rows()-1, style)
            
        
    #
    # Adds a row where cells can span over several columns to the table.
    #
    def add_colspan_row(self, row, style=None):
        if not self.valid(row, [list]): return
        self.valid_style(style)
        
        self.rows.append(row)
        if style is not None:
            if not self.valid(style, [dict]): return
            
            self.row_style(self.no_rows()-1, style)
            
    #
    # Sort the table by column.
    #
    def sort(self, col, reverse=False, lock=None):
        if not self.valid(col, [str,int], min_val=0, max_val=len(self.cols)-1): return
        
        col = self.column_number(col)
        if lock is not None:
            tmp = self.rows[lock:]
            self.rows = self.rows[:lock]
        self.rows = sorted(self.rows, key=lambda x: x[col], reverse=reverse)
        if lock is not None:
            self.rows += tmp
        
    #
    # Adds a footer row to the table.
    #
    def add_subheader(self, row):
        if not self.valid(row, [list]): return
        
        self.rows.append(row)
        self.row_style(len(self.rows)-1, self.subheader_style)
    
    #
    # Updates the value in a cell.
    #
    def update_cell(self, col, row, val):
        if not self.valid(col, [str,int], min_val=0, max_val=len(self.cols)-1): return
        if not self.valid(row, [int], min_val=0, max_val=len(self.rows)-1): return
        if not self.valid(val, None): return
        
        col = self.column_number(col)
        self.rows[row][col] = val
    
    #
    # Returns a css style for for a style dict.
    #
    def style_tag(self, params):
        s = ""
        if params is None:
            params = {}
        for tag,val in params.items():
            s += f"{tag}:{val};"
        for tag,val in self.default_style.items():
            if tag not in params:
                s += f"{tag}:{val};" 
        return s
    
    #
    # Merges a style with another style.
    #
    def merge_style(self, p, tmp):
        for tag,val in tmp.items():
            if tag == "font" and "font" in p:
                p["font"] += f" {val}"
            elif tag == "border" and "border" in p:
                p["border"] += f" {val}"
            else:
                p.update({tag: val})
    
    #
    # Get style for the specified cell (column number + row number).
    #
    def get_style(self, col, row):
        # Lowest prio: default style
        p = self.default_style.copy()
        
        # Column
        key = f"{col}-*"
        if key in self.styles:
            self.merge_style(p, self.styles[key])
        
        # Row
        key = f"*-{row}"
        if key in self.styles:
            self.merge_style(p, self.styles[key])
        
        # Cell
        key = f"{col}-{row}"
        if key in self.styles:
            self.merge_style(p, self.styles[key])
        
        # Update tags
        update_tags(p)
        
        # Add shading to every second row
        if "row-toggle-background" not in p or str(p["row-toggle-background"]) != "0":
            if row % 2 == 1:
                p.update({"filter": "brightness(96%)"})
            else:
                p.update({"filter": "brightness(100%)"})
        
        # Add bottom border to last row
        if row == len(self.rows) - 1:
            p.update({"border-bottom": "1px solid #aaa"})
            
        # Add top border to first row, if header is disabled
        if row == 0 and not self.header:
            p.update({"border-top": "1px solid #aaa"})
        
        return  p
    
    #
    # Generates the table.
    #
    def generate(self):
        t = "<table>"
        if self.width is not None:
            t = f"<table style='width={self.width}px; max-width:{self.width}px; min-width:{self.width}px; table-layout: fixed; word-wrap: break-word;'>"
        
        # Header
        if self.header:
            p = self.header_style.copy()
            update_tags(p)
            t += "<tr>"
            for c,w in zip(self.cols, self.w):
                wt = ""
                if w > 0:
                    wt = f" width={w}"
                t += f"<td style='{self.style_tag(p)}'{wt}>{c}</td>"
            t += "</tr>"
        
        # Rows
        for ri,row in enumerate(self.rows):
            t += "<tr>"
            for ci,cell in enumerate(row):
                # Get style for cell
                p = self.get_style(ci,ri)
                
                for rule in self.style_rules:
                    match = False
                    if rule[1] == ">" and row[rule[0]] > rule[2]:
                        match = True
                    if rule[1] == ">=" and row[rule[0]] >= rule[2]:
                        match = True
                    if rule[1] == "<" and row[rule[0]] < rule[2]:
                        match = True
                    if rule[1] == "<=" and row[rule[0]] <= rule[2]:
                        match = True
                    if rule[1] == "=" and row[rule[0]] == rule[2]:
                        match = True
                    if rule[1] == "==" and row[rule[0]] == rule[2]:
                        match = True
                    
                    if match:
                        if rule[4] is None:
                            p.update(rule[3])
                        elif rule[4] == ci:
                            p.update(rule[3])
                
                # Check number formats or cell formats
                if "num-format" in p:
                    cell = tag_numformat(cell, p)
                if "cell-format" in p:
                    cell = tag_cellformat(cell, p)
                    
                # Build cell
                if type(cell) != list:
                    t += f"<td style='{self.style_tag(p)}'>{cell}</td>"
                else:
                    # Colspan
                    t += f"<td style='{self.style_tag(p)}' colspan={cell[1]}>{cell[0]}</td>"
            t += "</tr>"
            
        # Table done
        t += "</table>"
        
        return t
    
    #
    # Displays the table.
    #
    def display(self):
        display(HTML(self.generate()))
        
    #
    # Stores the table in a csv file.
    #
    def to_csv(self, file):
        try:
            nf = open(file, "wt")
            # Header
            nf.write("\"" + "\",\"".join(self.cols) + "\"\n")
            # Rows
            for row in self.rows:
                r = ""
                for cell in row:
                    if type(cell) == int or type(cell) == float:
                        r += f"{cell},"
                    else:
                        if type(cell) == str:
                            cell = remove_tags(cell)
                        r += f"\"{cell}\","
                nf.write(r[:-1] + "\n")
            nf.close()
        except:
            print(colored("Error: ", "red", attrs=["bold"]) + "unable to create csv file")
    
    #
    # Stores the table in an Excel file.
    #
    def to_excel(self, file):
        try:
            import xlsxwriter
        except ImportError:
            print(colored("Error: ", "red", attrs=["bold"]) + "you need ", end="")
            print(colored("xlsxwriter", "blue"), end="")
            print(" installed to generate Excel files")
            return

        # Create file
        workbook = xlsxwriter.Workbook(file)

        # Add worksheet
        worksheet = workbook.add_worksheet("")

        # Header
        if self.header:
            hst = to_excel_style(self.header_style, workbook)
            for ci in range(0,len(self.cols)):
                worksheet.write(0, ci, self.cols[ci], hst)
                if self.w[ci] > 0:
                    worksheet.set_column_pixels(ci, ci, self.w[ci])

        # Contents
        for ri,row in enumerate(self.rows):
            for ci,cell in enumerate(row):
                # Get style for cell
                p = self.get_style(ci,ri)
                cst = to_excel_style(p, workbook)
                # Handle special num formats
                if "num-format" in p and p["num-format"].startswith("prefix"):
                    cell = tag_prefixformat(cell, p["num-format"])
                if "cell-format" in p and p["cell-format"].startswith("list"):
                    cell = tag_cellformat(cell, p)
                # Write to cell
                if type(cell) == str:
                    cell = remove_tags(cell)
                worksheet.write(ri+1, ci, cell, cst)

        # Close file
        workbook.close()

#
# Creates a table from a csv file.
#
def from_csv(file):
    # Check if value is int
    def to_int(v):
        try:
            int(v)
            return int(v)
        except:
            return None

    # Check if value is float
    def to_float(v):
        try:
            float(v)
            return float(v)
        except:
            return None
    
    try:
        # Read and format data
        nf = open(file, "rt")
        data = nf.readlines()
        for r in range(0,len(data)):
            data[r] = data[r].split(",")
            data[r] = [x.replace("\"", "").replace("'", "").replace("\n", "") for x in data[r]]
            for c in range(0,len(data[r])):
                # Value conversion
                fv = to_int(data[r][c])
                if fv is None:
                    fv = to_float(data[r][c])
                if fv is None:
                    fv = data[r][c]
                # Update value
                data[r][c] = fv

        # Create table
        t = CustomizedTable(data[0])
        for i in range(1,len(data)):
            t.add_row(data[i])
        nf.close()
        return t
    except:
        print(colored("Error: ", "red", attrs=["bold"]) + "unable to create table from csv file")
        return CustomizedTable([""])


#
# Generates a counts table from a list or dict.
#
def generate_counts(data, cidx=0, labels=None, sort=None, footer=["total"], group=None, style=None):
    if type(data) not in [dict, list]:
        print(colored("Warning", "red", attrs=["bold"]) + ": data must dict or list")
        return
    
    # Convert from list to dict
    if type(data) == list:
        cnt = {}
        for r in data:
            v = r
            if type(r) == list:
                v = r[cidx]
            if v not in cnt:
                cnt.update({v: 0})
            cnt[v] += 1
    if type(data) == dict:
        cnt = data
    
    # Generate table from dict
    title = ""
    if labels is not None and "title" in labels:
        title = labels["title"]
    cnlbl = "No"
    if labels is not None and "no" in labels:
        cnlbl = labels["no"]
    cplbl = "Part"
    if labels is not None and "part" in labels:
        cplbl = labels["part"]
        
    if style is None:
        t = CustomizedTable([title, cnlbl, cplbl])
    else:
        t = CustomizedTable([title, cnlbl, cplbl], style=style)
    t.column_style(1, {"color": "value"})
    t.column_style(2, {"color": "percent", "num-format": "pct-2"})
    tot = sum(list(cnt.values()))
    for key,n in cnt.items():
        t.add_row([key,n,n/tot])
    
    # Sort table
    if sort in ["key", 0]:
        t.sort(0)
    if sort in ["asc", "ascending", 1]:
        t.sort(1)
    if sort in ["desc", "descending", 2]:
        t.sort(1, reverse=True)
    
    # Group after sort
    ngrp = 0
    if group is not None:
        ngrp = sum([x[1] for x in t.rows[group:]])
        t.rows = t.rows[:group]
    
    # Grouped row
    if ngrp > 0:
        olbl = "Other:"
        if labels is not None and "other" in labels:
            olbl = labels["other"]
        t.add_row([olbl,ngrp,ngrp/tot])
        t.cell_style(0,-1,{"color": "#811"})
        t.cell_style(1,-1,{"color": "#933"})
        t.cell_style(2,-1,{"color": "#944"})

    # Bottom border
    t.row_style(-1, {"border": "bottom"})
    
    # Add total and/or mean row
    if footer is not None:
        if "total" in footer:
            tlbl = "Total:"
            if labels is not None and "total" in labels:
                tlbl = labels["total"]
            t.add_row([tlbl, tot, ""], style={"background": "#eee", "row-toggle-background": 0})
        if "mean" in footer:
            mlbl = "Mean:"
            if labels is not None and "mean" in labels:
                mlbl = labels["mean"]
            t.add_row([mlbl, tot/len(cnt), ""], style={"background": "#eee", "row-toggle-background": 0})
            t.cell_style(1,-1,{"num-format": "dec-2"})
    
    return t

