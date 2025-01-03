# Goodreads to Zotero

Many people asked for a Goodreads to Zotero tool. I was looking for something like that as well, but could not find it.
I created a couple of python scripts that help me accomplish what I need.

You need to be able to run python on your machine to get this up and running.

The solution does two things:

1. import your [goodreads_library_export.csv](https://help.goodreads.com/s/article/How-do-I-import-or-export-my-books-1553870934590) into a sqlite3 database
2. generate a [RIS file](https://en.wikipedia.org/wiki/RIS_(file_format))

- Q: Why the intermediate step of the sqlite database?

You might want to do some selection on the export to create a Collection in Zotero. 
For example, I created a collection `to_read` and `read` based on some small changes in the SQL query.

Not all the fields from the CSV are mapped. I wanted to map the `Add` dates from Goodreads into the `Date Added` fields from Zotero, but this is not directly possible. I now store it in the `Abstract` field which is of course not where it belongs. If you want to spend time on it you could directly interact with the zotero.sqlite database and try to do an update SQL command to change it and update the Date Added with the info from the Abstract field. Do not forget to backup your zotero.sqlite if you do this.

Maybe I will actually write that code when I have more time.

# Getting started

- Have python installed (I used 3.11.2)
- Have pandas installed (I used pandas==2.2.3) 
- note: sqlite comes out of the box in python

1. edit `import_csv.py` to your liking, you can change filename, database name and table name
2. run `python import_csv.py` - this will load all csv data in a sqlite database
3. if you want you can run sqlite3 on your database and investigate the data
4. edit `export_ris.py` change the filename and sql query
5. run `python export_ris.py` this will output a file like 'books.ris'
6. open Zotero, select import and import the file

Some choises I made that are easy to change in this code:
- ratings are added as labels that contain stars
- to_read and read are also labels

Example of what it will look like:

<img width="1640" alt="image" src="https://github.com/user-attachments/assets/32dd33b7-c48e-4768-a374-f76f9715661a" />

# Some info on the export from GoodReads

`sqlite> PRAGMA table_info(books);`

```
cid|name|type|notnull|dflt_value|pk
0|Book Id|INTEGER|0||0
1|Title|TEXT|0||0
2|Author|TEXT|0||0
3|Author l-f|TEXT|0||0
4|Additional Authors|TEXT|0||0
5|ISBN|TEXT|0||0
6|ISBN13|INTEGER|0||0
7|My Rating|INTEGER|0||0
8|Average Rating|REAL|0||0
9|Publisher|TEXT|0||0
10|Binding|TEXT|0||0
11|Number of Pages|INTEGER|0||0
12|Year Published|INTEGER|0||0
13|Original Publication Year|INTEGER|0||0
14|Date Read|TEXT|0||0
15|Date Added|TEXT|0||0
16|Bookshelves|TEXT|0||0
17|Bookshelves with positions|TEXT|0||0
18|Exclusive Shelf|TEXT|0||0
19|My Review|TEXT|0||0
20|Spoiler|INTEGER|0||0
21|Private Notes|REAL|0||0
22|Read Count|INTEGER|0||0
23|Owned Copies|INTEGER|0||0
```
