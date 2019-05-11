# =============================================================================
#  FUNCTIONS
# =============================================================================
async def init(api, _):
    '''Initializes mkctf repository
    '''
    result = api.init()
    return result['initialized']

def setup_init(subparsers):
    parser = subparsers.add_parser('init', help="initialize mkctf repository.")
    parser.set_defaults(func=init)
