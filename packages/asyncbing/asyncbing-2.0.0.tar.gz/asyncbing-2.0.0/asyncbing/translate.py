import asyncio
import uuid
import aiohttp
from translateresponse import TranslateResponse

class Translate:
    """The translating part of asyncbing"""
    async def __aenter__(self, auth: str, *, region: str=None, session: aiohttp.ClientSession=None):
        """Takes a `auth` token, as well as an optional aiohttp session.
        example:
        ``
        async with asyncbing.Translate('AUTHTOKEN', region='eastus') as translating:
            await translating.translate...
        ``
        """
        self.auth = auth
        self.bing = 'https://api.cognitive.microsofttranslator.com/translate'
        if not region:
            import warnings
            warnings.warn("You haven't set a region. asyncbing will default to us-central.")
            self.region = 'centralus'
        else:
            self.region = region
        
        if not session:
            async with aiohttp.ClientSession() as session:
                self.session = session
        else:
            self.session = session
    
    async def translate(self, query: str, *, tolang: str='en', fromlang: str=None):
        """|coro|
        Translate the given query with an optional `tolang` language to translate to, as well as an optional `fromlang` language to translate from.
        If `tolang` isn't provided, it will auto translate to english. If `fromlang` isn't provided, it will auto translate from autodetect."""
        if not fromlang:
            params = {'api-version': '3.0', 'to': [tolang]}
        else:
            params = {'api-version': '3.0', 'to': [tolang], 'from': fromlang}
        async with self.session.post(self.bing, params=params, headers={'Ocp-Apim-Subscription-Key': self.auth, 'Ocp-Apim-Subscription-Region': self.region, 'Content-type': 'application/json', 'X-ClientTraceId': str(uuid.uuid4())}, json=[{'text': query}]) as resp:
            return TranslateResponse((await resp.json()))
        
    