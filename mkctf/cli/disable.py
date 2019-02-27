# =============================================================================
#  FUNCTIONS
# =============================================================================
async def disable(api, args):
    '''Enables a challenge
    '''
    status = api.disable(args.slug)
    disabled = status['disabled']
    if disabled:
        print(f"{args.slug}: disabled")
    return disabled

def setup_disable(subparsers):
    parser = subparsers.add_parser('disable', help="disable a challenge.")
    parser.add_argument('slug', help="challenge's slug.")
    parser.set_defaults(func=disable)
