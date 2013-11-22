import json
import sys

from itertools import izip
def triple_up(iterable):
    "s -> (s0,s1), (s2,s3), (s4, s5), ..."
    a = iter(iterable)
    return izip(a, a, a)

from BeautifulSoup import BeautifulSoup as bs

if len(sys.argv) != 2:
    print 'Usage:', sys.argv[0], 'html file'
    sys.exit(1)

foo = bs(open(sys.argv[1]).read())
#open('pretty.html', 'w').write(foo.prettify())
#print foo.prettify()

root_table = foo.find('table')
child_tables = root_table.findAll('table')
items = []
all_rows = child_tables[1].findAll('tr')
for main_row, score_row, row3 in triple_up(all_rows):
    cols = main_row.findAll('td')
    item = {}
    item['rank'] = int(cols[0].text[:-1])

    title_obj = cols[2]
    link = title_obj.find('a')
        
    item['title'] = link.text
    item['href'] = link.get('href')

    comhead_obj = title_obj.find('span')
    if comhead_obj:
        item['comhead'] = comhead_obj.text[1:-1]

    score_obj = score_row.findAll('td')[1]
    num_points_obj = score_obj.find('span')
    if num_points_obj:
        item['num_points'] = int(num_points_obj.text.split()[0])
    hrefs = score_obj.findAll('a')
    if hrefs:
        item['username'] = hrefs[0].text
        num_comments = hrefs[1].text
        if num_comments == 'discuss':
            item['num_comments'] = 0
        else:
            item['num_comments'] = int(num_comments.split()[0])
        item['comments_url'] = hrefs[1].get('href')
    items.append(item)

print json.dumps(items)
