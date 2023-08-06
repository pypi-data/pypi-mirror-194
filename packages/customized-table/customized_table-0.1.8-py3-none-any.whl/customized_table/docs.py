from .customized_table import *


#
# Show documentation about table formatting.
#
def docs_formatting():
    t = CustomizedTable(["Tag", "Description"], width=1110)
    t.column_width(0, 220)
    t.column_style(0, {"font": "bold"})

    t.add_row(["color", ["Sets text color (CSS color or named color):", 
                         tag_text("&nbsp;<#a44 italic>#a44</>"), 
                         tag_text("&nbsp;<#f40bd9 italic>#f40bd9</>"), 
                         tag_text("&nbsp;<red italic>red</>"), 
                         tag_text("&nbsp;<value italic>value</>")
                        ]])
    t.cell_style(1, -1, {"cell-format": "list:\n"})

    t.add_row(["font", [tag_text("List with font style settings <#888>(bold, italic, normal, font size, font family)</>"), 
                         tag_text("For example <bold>'Courier 12px bold'</>"), 
                        ]])
    t.cell_style(1, -1, {"cell-format": "list:\n", "font": "Courier 12px"})


    t.add_row(["background", tag_text("Same as color but sets backgrond color, for example <italic>#eef</>")])
    t.cell_style(1, -1, {"background": "#eef", "row-toggle-background": 0})

    t.add_row(["border", tag_text("List of which borders to show <#888>(top bottom left right)</>")])
    t.cell_style(1, -1, {"border": "top bottom left right"})

    t.add_row(["text-align", tag_text("Sets text alignment (CSS text alignment, for example <italic>center</>)")])
    t.cell_style(1, -1, {"text-align": "center"})

    t.add_row(["row-toggle-background", "Disables alternating shading for a row or cell (set to 0)"])
    t.cell_style(1, -1, {"row-toggle-background": 0})

    t.add_row(["padding", ["Sets padding (space between cell contents and border):", 
                            tag_text("&nbsp;<italic #a44>2px 4px 5px 3px</> sets padding top to <blue>2px</>, right to <blue>4px</>, bottom to <blue>5px</> and left to <blue>3px</>"),
                            tag_text("&nbsp;<italic #a44>2px 5px 3px</> sets padding top to <blue>2px</>, right and left to <blue>5px</>, and bottom to <blue>3px</>"),
                            tag_text("&nbsp;<italic #a44>3px 5px</> sets padding top and bottom to <blue>3px</>, and right and left to <blue>5px</>"),
                            tag_text("&nbsp;<italic #a44>8px</> sets all four paddings to <blue>8px</>"),
                            ]])
    t.cell_style(1, -1, {"cell-format": "list:\n", "padding": "10px 3px 10px"})

    t.add_row(["num-format", ["Number formatting:", 
                              tag_text("&nbsp;<italic #a44>dec-#</> formats values to # decimal digits, for example <value>3.14</> is shown for <value>3.14159</> using <italic #a44>dec-2</>"),
                              tag_text("&nbsp;<italic #a44>pct-#</> formats values to percents with # decimal digits, for example <value>73.1%</> is shown for <value>0.731</> using <italic #a44>pct-1</>"),
                              tag_text("&nbsp;<italic #a44>int</> formats values to integers, for example <value>3</> is shown for <value>3.14159</> using <italic #a44>int</>"),
                              tag_text("&nbsp;<italic #a44>prefix</> formats values to use prefixes, for example <value>2.5M</> is shown for <value>2500000</> using <italic #a44>prefix</>"),
                              tag_text("&nbsp;<italic #a44>prefix-#</> formats values to use prefixes with # decimal digits, for example <value>2.5M</> is shown for <value>2513000</> using <italic #a44>prefix-1</>"),
                             ]])
    t.cell_style(1, -1, {"cell-format": "list:\n"})

    t.add_row(["cell-format", ["Cell contents formatting:", 
                                tag_text("&nbsp;<italic #a44>list</> shows a Python list as a string, for example <value>Batman, Robin</> is shown for <value>['Batman', 'Robin']</> using <italic #a44>list</>"),
                                tag_text("&nbsp;<italic #a44>list:#</> shows a list using custom delimiter, for example <value>Batman & Robin</> is shown for <value>['Batman', 'Robin']</> using <italic #a44>list:&</>"),
                                tag_text("&nbsp;<italic #a44>tag-text</> handles tagged text strings (see <italic #272>tag_text</> function)"),
                             ]])

    t.cell_style(1, -1, {"cell-format": "list:\n"})

    t.display()
    
    
#
# Show documentation about CustomizedTable class.
#
def docs_customizedtable():
    t = CustomizedTable(["Functions (CustomizedTable)", "Description"], width=1110)
    t.column_width(0, 220)
    t.column_style(0, {"font": "bold", "color": "#272"})

    t.add_row(["CustomizedTable (constructor)", ["Creates a new table.", 
                        "Params:", 
                        tag_text("&nbsp;<#a44 italic>cols</> The table column names. <#888>(list of strings)</>"), 
                        tag_text("&nbsp;<#a44 italic>style</> Changes default formatting. <#888>(dict)</>"),
                        tag_text("&nbsp;<#a44 italic>header_style</> Changes default formatting for the header. <#888>(dict)</>"),
                        tag_text("&nbsp;<#a44 italic>subheader_style</> Changes default formatting for subheaders. <#888>(dict)</>"),
                        tag_text("&nbsp;<#a44 italic>width</> Sets table width. If not set, auto size is used. <#888>(int or None)</>"),
                        tag_text("&nbsp;<#a44 italic>header</> Show or hide header, default is show. <#888>(True or False)</>"),
                        ]])
    t.cell_style(1, -1, {"cell-format": "list:\n"})

    t.add_row(["add_row", ["Adds a row to the table.", 
                        "Params:", 
                        tag_text("&nbsp;<#a44 italic>row</> The row to add. <#888>(list of same size as columns)</>"), 
                        tag_text("&nbsp;<#a44 italic>style</> Style for the row (tags + values). <#888>(dict, optional)</>"),
                        ]])
    t.cell_style(1, -1, {"cell-format": "list:\n"})

    t.add_row(["add_colspanrow", ["Adds a row spanning over multiple columns to the table.", 
                        "Params:", 
                        tag_text("&nbsp;<#a44 italic>row</> The row to add. <#888>(list of same size as columns)</>"), 
                        tag_text("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A cell spanning over multiple rows is specified as a list, for example <italic>row</> = <value>[['Span 2 cols',2],'Col 3']</>"), 
                        tag_text("&nbsp;<#a44 italic>style</> Style for the row (tags + values). <#888>(dict, optional)</>"),
                        ]])
    t.cell_style(1, -1, {"cell-format": "list:\n"})

    t.add_row(["no_rows", ["Returns the number of rows in the table."
                        ]])
    t.cell_style(1, -1, {"cell-format": "list:\n"})

    t.add_row(["column_width", ["Sets width for one or more columns.", 
                        "Params:", 
                        tag_text("&nbsp;<#a44 italic>cols</> Columns to set width for. <#888>(column name or index, or list of column names or indexes)</>"), 
                        tag_text("&nbsp;<#a44 italic>width</> Width of columns. <#888>(int)</>"),
                        ]])
    t.cell_style(1, -1, {"cell-format": "list:\n"})

    t.add_row(["column_style", ["Sets style for formatting one or more columns.", 
                        "Params:", 
                        tag_text("&nbsp;<#a44 italic>cols</> Columns to set style for. <#888>(column name or index, or list of column names or indexes)</>"), 
                        tag_text("&nbsp;<#a44 italic>style</> Style (tags + values). <#888>(dict)</>"),
                        ]])
    t.cell_style(1, -1, {"cell-format": "list:\n"})

    t.add_row(["row_style", ["Sets style for formatting one or more rows.", 
                        "Params:", 
                        tag_text("&nbsp;<#a44 italic>rows</> Rows to set style for. <#888>(row number or -1 for last row, or list of row numbers)</>"), 
                        tag_text("&nbsp;<#a44 italic>style</> Style (tags + values). <#888>(dict)</>"),
                        ]])
    t.cell_style(1, -1, {"cell-format": "list:\n"})

    t.add_row(["cell_style", ["Sets style for formatting one or more cells.", 
                        "Params:", 
                        tag_text("&nbsp;<#a44 italic>cols</> Columns to set style for. <#888>(column name or index, or list of column names or indexes)</>"),
                        tag_text("&nbsp;<#a44 italic>rows</> Rows to set style for. <#888>(row number or -1 for last row, or list of row numbers)</>"), 
                        tag_text("&nbsp;<#a44 italic>style</> Style (tags + values). <#888>(dict)</>"),
                        ]])
    t.cell_style(1, -1, {"cell-format": "list:\n"})
    
    t.add_row(["style_rule", ["Sets style to row or cell based on comparisons.", 
                        "Params:", 
                        tag_text("&nbsp;<#a44 italic>col</> Column to compare value for. <#888>(column name or index)</>"),
                        tag_text("&nbsp;<#a44 italic>comp</> Comparison identifier. <#888>('&gt;','&gt;=','&lt;','&lt;=','=')</>"), 
                        tag_text("&nbsp;<#a44 italic>val</> Value to compare with. <#888>(int,float,str)</>"),
                        tag_text("&nbsp;<#a44 italic>style</> Style (tags + values). <#888>(dict)</>"),
                        tag_text("&nbsp;<#a44 italic>cidx</> Cell column index to set style for, or None for whole row. <#888>(column name or index, or None)</>"),
                        ]])
    t.cell_style(1, -1, {"cell-format": "list:\n"})

    t.add_row(["sort", ["Sorts the table on a specified column.", 
                        "Params:", 
                        tag_text("&nbsp;<#a44 italic>col</> Column to to sort on. <#888>(column name or index)</>"),
                        tag_text("&nbsp;<#a44 italic>reverse</> Sort reversed or not (default is not). <#888>(True or False)</>"), 
                        tag_text("&nbsp;<#a44 italic>lock</> Rows from the specified index are locked/not sorted. <#888>(None or index)</>"),
                        
                        ]])
    t.cell_style(1, -1, {"cell-format": "list:\n"})

    t.add_row(["update_cell", ["Updates the content in a cell.", 
                        "Params:", 
                        tag_text("&nbsp;<#a44 italic>col</> Column of the cell. <#888>(column name or index)</>"),
                        tag_text("&nbsp;<#a44 italic>row</> Row of the cell. <#888>(row number or -1 for last row)</>"), 
                        tag_text("&nbsp;<#a44 italic>val</> New cell contents."),
                        ]])
    t.cell_style(1, -1, {"cell-format": "list:\n"})

    t.add_row(["display", ["Displays the table."
                        ]])
    t.cell_style(1, -1, {"cell-format": "list:\n"})

    t.add_row(["to_csv", [tag_text("Saves the table to a <italic>csv</> file."),
                        "Params:", 
                        tag_text("&nbsp;<#a44 italic>file</> File name and path for the file. <#888>(string)</>"),
                        ]])
    t.cell_style(1, -1, {"cell-format": "list:\n"})

    t.add_row(["to_excel", [tag_text("Saves the table to an <italic>Excel</> file."),
                        "Params:", 
                        tag_text("&nbsp;<#a44 italic>file</> File name and path for the file. <#888>(string)</>"),
                        ]])
    t.cell_style(1, -1, {"cell-format": "list:\n"})

    t.display()
    
    
#
# Show documentation about general functions.
#
def docs_general():
    t = CustomizedTable(["Functions (general)", "Description"], width=1110)
    t.column_width(0, 220)
    t.column_style(0, {"font": "bold", "color": "#272"})

    t.add_row(["tag_text", [tag_text("Handles tagged text strings. Tagged text strings can contain tags for text color and style."),
                        "Params:", 
                        tag_text("&nbsp;<#a44 italic>txt</> Tagged text string. <#888>(string)</>"),
                        "Examples:",
                        tag_text("&nbsp;<#a44>&lt;bold&gt;bold&lt;/&gt;</> shows a <bold>bold</> text."),
                        tag_text("&nbsp;<#a44>&lt;italic&gt;titalic&lt;/&gt;</> shows an <italic>italic</> text."),
                        tag_text("&nbsp;<#a44>&lt;blue&gt;blue&lt;/&gt;</> shows a <blue>blue</> text."),
                        tag_text("&nbsp;<#a44>&lt;blue bold&gt;blue and bold&lt;/&gt;</> shows a <blue bold>blue and bold</> text."),
                        tag_text("&nbsp;<#a44>&lt;red italic&gt;red and italic&lt;/&gt;</> shows a <red italic>red and italic</> text."),
                        tag_text("&nbsp;<#a44>&lt;#f708b1&gt;pink&lt;/&gt;</> shows a <#f708b1>pink</> text."),
                        ]])
    t.cell_style(1, -1, {"cell-format": "list:\n"})

    t.add_row(["from_csv", [tag_text("Creates a table from a <italic>csv</> file."),
                        "Params:", 
                        tag_text("&nbsp;<#a44 italic>file</> File name and path for the file. <#888>(string)</>"),
                        ]])
    t.cell_style(1, -1, {"cell-format": "list:\n"})
    
    t.add_row(["generate_counts", [tag_text("Generates a counts table (number of occurences for each item) from a list or dict."),
                        "Params:", 
                        tag_text("&nbsp;<#a44 italic>data</> Data to generate counts from. <#888>(list or dict)</>"),
                        tag_text("&nbsp;<#a44 italic>cidx</> Column to generate counts from, if data is list of lists. <#888>(column index, optional)</>"),
                        tag_text("&nbsp;<#a44 italic>title</> Title of the table. <#888>(string, optional)</>"),
                        tag_text("&nbsp;<#a44 italic>sort</> How to sort the counts table. <#888>(None for no sorting, or 'key', 'asc', 'desc')</>"),
                        tag_text("&nbsp;<#a44 italic>footer</> What to show in the footer. <#888>(list ('total','mean') or None)</>"),
                        tag_text("&nbsp;<#a44 italic>group</> Group all entries after the specified row to make the table more compact. <#888>(row index, optional)</>"),
                        tag_text("&nbsp;<#a44 italic>style</> Changes default formatting. <#888>(dict, optional)</>"),
                        
                        ]])
    t.cell_style(1, -1, {"cell-format": "list:\n"})

    t.display()
