import sqlite3
import pandas as pd

"""
cid  name                        type     notnull  dflt_value  pk
---  --------------------------  -------  -------  ----------  --
0    Book Id                     INTEGER  0                    0
1    Title                       TEXT     0                    0
2    Author                      TEXT     0                    0
3    Author l-f                  TEXT     0                    0
4    Additional Authors          TEXT     0                    0
5    ISBN                        TEXT     0                    0
6    ISBN13                      INTEGER  0                    0
7    My Rating                   INTEGER  0                    0
8    Average Rating              REAL     0                    0
9    Publisher                   TEXT     0                    0
10   Binding                     TEXT     0                    0
11   Number of Pages             REAL     0                    0
12   Year Published              REAL     0                    0
13   Original Publication Year   REAL     0                    0
14   Date Read                   TEXT     0                    0
15   Date Added                  TEXT     0                    0
16   Bookshelves                 TEXT     0                    0
17   Bookshelves with positions  TEXT     0                    0
18   Exclusive Shelf             TEXT     0                    0
19   My Review                   TEXT     0                    0
20   Spoiler                     INTEGER  0                    0
21   Private Notes               REAL     0                    0
22   Read Count                  INTEGER  0                    0
23   Owned Copies                INTEGER  0                    0
"""

"""
 'A1': 'first_authors',
 'A2': 'secondary_authors',
 'A3': 'tertiary_authors',
 'A4': 'subsidiary_authors',
 'AB': 'abstract',
 'AD': 'author_address',
 'AN': 'accession_number',
 'AU': 'authors',
 'C1': 'custom1',
 'C2': 'custom2',
 'C3': 'custom3',
 'C4': 'custom4',
 'C5': 'custom5',
 'C6': 'custom6',
 'C7': 'custom7',
 'C8': 'custom8',
 'CA': 'caption',
 'CN': 'call_number',
 'CY': 'place_published',
 'DA': 'date',
 'DB': 'name_of_database',
 'DO': 'doi',
 'DP': 'database_provider',
 'EP': 'end_page',
 'ER': 'end_of_reference',
 'ET': 'edition',
 'ID': 'id',
 'IS': 'number',
 'J2': 'alternate_title1',
 'JA': 'alternate_title2',
 'JF': 'alternate_title3',
 'JO': 'journal_name',
 'KW': 'keywords',
 'L1': 'file_attachments1',
 'L2': 'file_attachments2',
 'L4': 'figure',
 'LA': 'language',
 'LB': 'label',
 'M1': 'note',
 'M3': 'type_of_work',
 'N1': 'notes',
 'N2': 'notes_abstract',
 'NV': 'number_of_volumes',
 'OP': 'original_publication',
 'PB': 'publisher',
 'PY': 'year',
 'RI': 'reviewed_item',
 'RN': 'research_notes',
 'RP': 'reprint_edition',
 'SE': 'section',
 'SN': 'issn',
 'SP': 'start_page',
 'ST': 'short_title',
 'T1': 'primary_title',
 'T2': 'secondary_title',
 'T3': 'tertiary_title',
 'TA': 'translated_author',
 'TI': 'title',
 'TT': 'translated_title',
 'TY': 'type_of_reference',
 'UK': 'unknown_tag',
 'UR': 'urls',
 'VL': 'volume',
 'Y1': 'publication_year',
 'Y2': 'access_date'
"""

"""
TY  - BOOK
TI  - Ill fares the land: a treatise on our present discontents
AU  - Judt, Tony
CY  - London
DA  - 2010///
PY  - 2010
DP  - BnF ISBN
SP  - 300
LA  - eng
PB  - Allen Lane
SN  - 978-1-84614-359-5
ST  - Ill fares the land
N1  - <div data-schema-version="9"><p>anopther note</p>
</div>
N1  - <div data-schema-version="9"><p>Awesome book</p>
</div>
KW  - Economic forecasting
KW  - Prediction theory
ER  - 

TY  - BOOK
TI  - The Years of Rice and Salt
AU  - Robinson, Kim Stanley
CY  - Westminster
DA  - 2003///
PY  - 2003
DP  - K10plus ISBN
SP  - 1
LA  - eng
PB  - Random House Publishing Group
SN  - 978-0-553-58007-5 978-0-553-89760-9
N1  - Description based on publisher supplied metadata and other sources
ER  - 

"""

# Connect to the SQLite database
conn = sqlite3.connect('goodreads.db')
cursor = conn.cursor()

# Run your query and set the filename
cursor.execute('SELECT * FROM books where "Exclusive Shelf" = "read"')
filename = 'read.ris'
rows = cursor.fetchall()

conn.close()

# Create RIS file from the database
# Define the RIS fields
# Reference: https://en.wikipedia.org/wiki/RIS_(file_format)

entries = []
for row in rows:
    # Set ISBN to ISBN10 if 13 is not available
    if row[6] == '0':
        isbn = row[5]
    else:
        isbn = row[6]
    # Build 1 RIS entry
    entry = f"""TY - BOOK
ID - {row[0]}
T1 - {row[1]}
AU - {row[3]}
A2 - {row[4]}
SN - {isbn}
PB - {row[9]}
PY - {row[12]}
DA - {row[12]}
"""
    # DA - {row[14]} (in the zotero code PY and DA are the same)
    # see https://github.com/zotero/translators/blob/4cadb3e1455e6438b0b7c530d509cddca5f3e1c6/RIS.js

    # Number of pages
    if row[11]:
        entry += f"SP - {row[11]}\n"
    # Review
    if row[19]:
        entry += f"N1 - {row[19]}\n"

    # Keywords/Tags
    if row[16]:
        keywords = row[16].split(',')
        for keyword in keywords:
            entry += f"KW  - {keyword.strip()}\n"  # Strip whitespace
    # Exclusive shelf as a tag (in case of double with above it will be deduplicated by Zotero)
    if row[18]:
        entry += f"KW  - {row[18]}\n"
    # Binding (Hardcover etc) as a tag
    if row[10]:
        entry += f"KW  - {row[10]}\n"
    # Access date / read date 
    if row[14]:
        entry += f"Y2  - {row[14]}\n"
    # Date Added stored in Abstract Note
    if row[15]:
        entry += f"N2  - {row[15]}\n"
    # Process rating to a tag
    if (row[7] == 0) or (row[7] is None):
        entry += f"KW  - ☆☆☆☆☆\n"
    elif row[7] == 1:
        entry += f"KW  - ★☆☆☆☆\n"
    elif row[7] == 2:
        entry += f"KW  - ★★☆☆☆\n"
    elif row[7] == 3:
        entry += f"KW  - ★★★☆☆\n"
    elif row[7] == 4:
        entry += f"KW  - ★★★★☆\n"
    elif row[7] == 5:
        entry += f"KW  - ★★★★★\n"

    entry += "ER  - \n"  # End of Reference marker which closes one RIS entry
    entries.append(entry)

# Write all RIS entries to file
with open(filename, 'w') as risfile:
    risfile.write("\n".join(entries))

print(f"RIS file '{filename}' created successfully, you can view it and import in Zotero.")
