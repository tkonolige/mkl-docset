import os, re, sqlite3
from bs4 import BeautifulSoup, NavigableString, Tag

conn = sqlite3.connect('mkl.docset/Contents/Resources/docSet.dsidx')
cur = conn.cursor()

try: cur.execute('DROP TABLE searchIndex;')
except: pass
cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

docpath = 'mkl.docset/Contents/Resources/Documents'

# find all pages linked in the table of contents
page = open(os.path.join(docpath,'hh_toc.htm')).read()
soup = BeautifulSoup(page)

type_map = { "FunctionRef": "Function", "topic": "Guide"}

for node in soup.select(".treeNode a"):
    url = node["href"]
    node_page = open(os.path.join(docpath, url)).read()
    node_soup = BeautifulSoup(node_page)
    # print node_soup
    ty = node_soup.find("meta", attrs={"name":"DC.Type"})["content"]
    name = node_soup.find("meta", attrs={"name":"DC.Title"})["content"]
    if ty in type_map:
        cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, type_map[ty], url))
        print '%s: %s, path: %s' % (type_map[ty], name, url)
    else:
        print "Unexpected type", ty
    if ty == "FunctionRef":
        for tag in node_soup.select("p.dlsyntaxpara"):
            name = re.search("(\S+)\s*\(", tag.text).group(1)
            # name = tag.contents[1].contents[0].strip()
            cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, 'Function', url))
            print '%s: %s, path: %s' % ('Function', name, url)

conn.commit()
conn.close()
