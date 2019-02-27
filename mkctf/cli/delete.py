# =============================================================================
#  FUNCTIONS
# =============================================================================
async def delete(api, args):
    '''Deletes a challenge
    '''
    result = api.delete(args.slug)
    return result['deleted']

def setup_delete(subparsers):
    parser = subparsers.add_parser('delete', help="delete a challenge.")
    parser.add_argument('slug', help="challenge's slug.")
    parser.set_defaults(func=delete)
