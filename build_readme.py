import feedparser
import pathlib
import re
import datetime
from dateutil import parser

root = pathlib.Path(__file__).parent.resolve()


def replace_writing(content, marker, chunk, inline=False):
    r = re.compile(
        r'<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->'.format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = '\n{}\n'.format(chunk)
    chunk = '<!-- {} starts -->{}<!-- {} ends -->'.format(marker, chunk, marker)
    return r.sub(chunk, content)


def fetch_writing():
    entries = feedparser.parse('https://fatalement.com/feed.xml')['entries']
    top5_entries = entries[:5]

    return [
               {
                   'title': entry['title'],
                   'url': entry['link'].split('#')[0],
                   'published': parser.parse(entry['published']).strftime("%A %d %B %Y")
               }
               for entry in top5_entries
           ]


if __name__ == '__main__':
    readme_path = root / 'README.md'
    readme = readme_path.open().read()
    entries = fetch_writing()
    print(f'Recent 5: {entries}')
    entries_md = '\n'.join(
        ['* [{title}]({url}) - {published}'.format(**entry) for entry in entries]
    )

    # Update entries
    rewritten_entries = replace_writing(readme, 'writing', entries_md)
    readme_path.open('w').write(rewritten_entries)

    # Update qoqa_days
    qoqa_days_count = (datetime.date.today() - datetime.date(2021, 6, 1)).days
    readme = readme_path.open().read()  # Need to read again with updated entries
    rewritten_qoqa_days = replace_writing(readme, 'qoqa_days', qoqa_days_count, inline=True)
    readme_path.open('w').write(rewritten_qoqa_days)
