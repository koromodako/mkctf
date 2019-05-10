# =============================================================================
#  FUNCTIONS
# =============================================================================
async def create(api, args):
    '''Creates a challenge
    '''
    result = api.create()
    return result['created']

def setup_create(subparsers):
    parser = subparsers.add_parser('create', help="create a challenge.")
    parser.set_defaults(func=create)
