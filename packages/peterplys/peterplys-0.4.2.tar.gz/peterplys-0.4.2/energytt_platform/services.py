import requests
from abc import abstractmethod
from typing import Any, Optional, Type, Callable, Dict, Tuple

from energytt_platform.serialize import json_serializer


class ConnectionError(Exception):
    """
    Raised when invoking EnergyTypeService results
    in a connection error
    """
    pass


class ServiceError(Exception):
    """
    Raised when invoking EnergyTypeService results
    in a status code != 200
    """
    def __init__(self, msg, status_code=None, response_body=None):
        super(ServiceError, self).__init__(msg)
        self.status_code = status_code
        self.response_body = response_body


# class ServiceUnavailable(Exception):
#     """
#     Raised when requesting energy type which is unavailable
#     for the requested GSRN
#     """
#     pass


class ApiClient(object):
    """
    TODO
    """
    def __init__(self, base_url: str, debug: bool = False):
        """
        :param base_url:
        """
        self.base_url = base_url
        self.debug = debug

    def get_absolute_url(self, path: str):
        """
        :param path:
        :return:
        """
        return f'{self.base_url}{path}'

    @abstractmethod
    def serialize_request(self, request: Any) -> bytes:
        """
        TODO

        :param request:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def deserialize_response(self, response: bytes, schema: Type[Any]) -> Any:
        """
        TODO

        :param response:
        :param schema:
        :return:
        """
        raise NotImplementedError

    def invoke(
            self,
            func: Callable,
            path: str,
            query: Optional[Dict[str, Any]] = None,
            body: Optional[Any] = None,
            response_schema: Optional[Type[Any]] = None,
            allowed_statuses: Tuple[int, ...] = (200,),
    ) -> requests.Response:
        """
        TODO

        :param func:
        :param str path:
        :param query:
        :param body:
        :param response_schema:
        :param allowed_statuses:
        :returns:
        """

        # requests.get()
        #
        # headers = {
        #     'Content-type': 'application/json',
        #     'accept': 'application/json',
        # }

        absolute_url = self.get_absolute_url(path)

        params = {
            'url': absolute_url,
            'verify': not self.debug,
            'headers': {
                'Content-type': 'application/json',
                'accept': 'application/json',
            },
        }

        if query:
            params['params'] = query
        if body:
            params['data'] = self.serialize_request(body)

        try:
            # response = func(
            #     url=absolute_url,
            #     params=query,
            #     verify=not self.debug,
            #     headers=headers,
            # )
            response = func(**params)
        except Exception as e:
            raise ConnectionError(f'Failed to request request service: {e}')

        # if response.status_code != 200:
        if response.status_code not in allowed_statuses:
            raise ServiceError(
                status_code=response.status_code,
                response_body=response.content.decode(),
                msg=(
                    f'Request resulted in status code {response.status_code}: '
                    f'{absolute_url}\n\n{response.content}'
                ),
            )

        return json_serializer.deserialize(
            data=response.content,
            schema=response_schema,
        )

        # try:
        #     response = json_serializer.deserialize(
        #         data=response.content,
        #         schema=response_schema,
        #     )
        #     # response_json = response.json()
        #     # response_model = response_schema().load(response_json)
        # except json.decoder.JSONDecodeError:
        #     raise ServiceError(
        #         f'Failed to parse response JSON: {url}\n\n{response.content}',
        #         status_code=response.status_code,
        #         response_body=str(response.content),
        #     )
        # except marshmallow.ValidationError as e:
        #     raise ServiceError(
        #         f'Failed to validate response JSON: {url}\n\n{response.content}\n\n{str(e)}',
        #         status_code=response.status_code,
        #         response_body=str(response.content),
        #     )
        #
        # return response

    # def invoke(
    #         self,
    #         func: Callable,
    #         path: str,
    #         query: Optional[Dict[str, Any]] = None,
    #         body: Optional[Any] = None,
    #         response_schema: Optional[Type[Any]] = None,
    #         allowed_statuses: Tuple[int, ...] = (200,),
    # ) -> requests.Response:
    #     """
    #     TODO
    #
    #     :param func:
    #     :param str path:
    #     :param query:
    #     :param body:
    #     :param response_schema:
    #     :param allowed_statuses:
    #     :returns:
    #     """
    #
    #     # requests.get()
    #     #
    #     # headers = {
    #     #     'Content-type': 'application/json',
    #     #     'accept': 'application/json',
    #     # }
    #
    #     absolute_url = self.get_absolute_url(path)
    #
    #     params = {
    #         'url': absolute_url,
    #         'verify': not self.debug,
    #         'headers': {
    #             'Content-type': 'application/json',
    #             'accept': 'application/json',
    #         },
    #     }
    #
    #     if query:
    #         params['params'] = query
    #     if body:
    #         params['data'] = self.serialize_request(body)
    #
    #     try:
    #         # response = func(
    #         #     url=absolute_url,
    #         #     params=query,
    #         #     verify=not self.debug,
    #         #     headers=headers,
    #         # )
    #         response = func(**params)
    #     except Exception as e:
    #         raise ConnectionError(f'Failed to request request service: {e}')
    #
    #     # if response.status_code != 200:
    #     if response.status_code not in allowed_statuses:
    #         raise ServiceError(
    #             status_code=response.status_code,
    #             response_body=response.content.decode(),
    #             msg=(
    #                 f'Request resulted in status code {response.status_code}: '
    #                 f'{absolute_url}\n\n{response.content}'
    #             ),
    #         )
    #
    #     return json_serializer.deserialize(
    #         data=response.content,
    #         schema=response_schema,
    #     )
    #
    #     # try:
    #     #     response = json_serializer.deserialize(
    #     #         data=response.content,
    #     #         schema=response_schema,
    #     #     )
    #     #     # response_json = response.json()
    #     #     # response_model = response_schema().load(response_json)
    #     # except json.decoder.JSONDecodeError:
    #     #     raise ServiceError(
    #     #         f'Failed to parse response JSON: {url}\n\n{response.content}',
    #     #         status_code=response.status_code,
    #     #         response_body=str(response.content),
    #     #     )
    #     # except marshmallow.ValidationError as e:
    #     #     raise ServiceError(
    #     #         f'Failed to validate response JSON: {url}\n\n{response.content}\n\n{str(e)}',
    #     #         status_code=response.status_code,
    #     #         response_body=str(response.content),
    #     #     )
    #     #
    #     # return response

    def get(self, *args, **kwargs):
        return self.invoke(requests.get, *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.invoke(requests.post, *args, **kwargs)


class JsonApiClient(ApiClient):
    """
    TODO
    """
    def serialize_request(self, request: Any) -> bytes:
        """
        TODO

        :param request:
        :return:
        """
        return json_serializer.serialize(
            obj=request,
        )

    def deserialize_response(self, response: bytes, schema: Type[Any]) -> Any:
        """
        TODO

        :param response:
        :param schema:
        :return:
        """
        return json_serializer.deserialize(
            data=response,
            schema=schema,
        )
