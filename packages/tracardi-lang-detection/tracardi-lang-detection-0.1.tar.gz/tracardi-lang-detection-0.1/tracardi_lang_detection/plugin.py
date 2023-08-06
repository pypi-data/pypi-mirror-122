import asyncio.exceptions

import aiohttp
from aiohttp import ClientConnectorError, FormData
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.domain.result import Result

from tracardi_lang_detection.model.configuration import LangDetectionConfiguration


class LangDetectAction(ActionRunner):

    def __init__(self, **kwargs):
        self.config = LangDetectionConfiguration(**kwargs)

    async def run(self, payload):
        try:

            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:

                params = payload

                async with session.request(
                        method="POST",
                        url=str(self.config.url),
                        data=params
                ) as response:
                    result = {
                        'status': response.status,
                        'body': await response.json()
                    }

                    if response.status in range(200, 204):
                        print(result)
                        return Result(port="response", value=result), Result(port="error", value=None)
                    else:
                        print(response)
                        return Result(port="response", value=None), Result(port="error", value=response)

        except ClientConnectorError as e:
            print(str(e))
            return Result(port="response", value=None), Result(port="error", value=str(e))
        except asyncio.exceptions.TimeoutError:
            Result(port="response", value=None), Result(port="error", value="Lang detection timed out.")


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_lang_detection.plugin',
            className='LangDetectAction',
            inputs=["payload"],
            outputs=['response', 'error'],
            version='0.1',
            license="MIT",
            author="Bartlomiej Komendarczuk",
            init={
                "url": 'https://api.meaningcloud.com/lang-4.0/identification',
                "timeout": 30
            }
        ),
        metadata=MetaData(
            name='tracardi-lang-detection',
            desc='This plugin detects language from given string.',
            type='flowNode',
            width=200,
            height=100,
            icon='icon',
            group=["General"]
        )
    )
