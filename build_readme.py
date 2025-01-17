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

if __name__ == '__main__':
    readme_path = root / 'README.md'
    readme = readme_path.open().read()

    # Update qoqa_days
    qoqa_days_count = (datetime.date.today() - datetime.date(2021, 6, 1)).days
    years = qoqa_days_count // 365
    months = (qoqa_days_count - years * 365) // 30
    days = (qoqa_days_count - years * 365 - months * 30)
    res_day = f"{years} year {months} month"
    if days > 0:
        res_day += f" and {days} days"
    readme = readme_path.open().read()  # Need to read again with updated entries
    rewritten_qoqa_days = replace_writing(readme, 'qoqa_days', res_day, inline=True)
    readme_path.open('w').write(rewritten_qoqa_days)
