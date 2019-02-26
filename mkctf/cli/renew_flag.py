'''
file: renew_flag.py
date: 2018-03-02
author: koromodako
purpose:

'''
# =============================================================================
#  FUNCTIONS
# =============================================================================
import mkctf.helper.cli as cli
from mkctf.helper.formatting import HSEP, format_text
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def renew_flag(api, args):
    '''[summary]
    '''
    if args.yes or cli.confirm('do you really want to renew flags?'):
        chall_sep = format_text(HSEP, 'blue', ['bold'])
        tags, slug = args.tags, args.slug
        results = []
        for result in api.renew_flag(tags, slug, args.size):
            chall_desc = format_text(f"{result['slug']}[{result['tags']}]", 'blue')
            print(chall_sep)
            print(f"{chall_desc} => {result['flag']}")
    return True
