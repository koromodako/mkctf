# =============================================================================
#  FUNCTIONS
# =============================================================================
async def enable(api, args):
    '''Enables a challenge
    '''
    status = api.enable(args.slug)
    return status['enabled']

def setup_enable(subparsers):
    parser = subparsers.add_parser('enable', help="enable a challenge.")
    parser.add_argument('slug', help="challenge's slug.")
    parser.set_defaults(func=enable)
