#===============================================================================
# IMPORTS
#===============================================================================
from aiohttp import web
#===============================================================================
# CLASSES
#===============================================================================
class MKCTFWebHandler:
    '''[summary]
    '''
    def __init__(self, api):
        '''[summary]
        '''
        self._api = api

    async def enum_challenges(self, request):
        slugs = [challenge['slug'] for challenge in self._api.enum()]
        return web.json_response({'challenges': slugs})

    async def challenge_status(self, request):
        result = await self._api.status(slug=request.match_info['slug'])
        if result:
            return web.json_response(result)
        raise web.HTTPNotFound()

    async def check_challenge_flag(self, request):
        if not request.has_body:
            raise web.HTTPBadRequest(reason="JSON body is missing.")
        try:
            body = await request.json()
        except:
            raise web.HTTPBadRequest(reason="JSON body cannot be parsed.")
        flag = body.get('flag')
        if not flag:
            raise web.HTTPBadRequest(reason="JSON body does not contain 'flag' key as expected.")
        challenge = self._api.find(request.match_info['slug'])
        if challenge:
            valid = (challenge['conf'].get('flag') == flag)
        return web.json_response({'valid': valid})

