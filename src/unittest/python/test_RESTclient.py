
# Copyright (c) 2020 Intel Corporation

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#      http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
from mock import patch
from mock import mock_open
from mock import call
from mock import Mock

from rest3client import RESTclient

import sys
import json
import logging
logger = logging.getLogger(__name__)

consoleHandler = logging.StreamHandler(sys.stdout)
logFormatter = logging.Formatter("%(asctime)s %(threadName)s %(name)s [%(funcName)s] %(levelname)s %(message)s")
consoleHandler.setFormatter(logFormatter)
rootLogger = logging.getLogger()
rootLogger.addHandler(consoleHandler)
rootLogger.setLevel(logging.DEBUG)


class TestRESTclient(unittest.TestCase):

    def setUp(self):
        """
        """
        pass

    def tearDown(self):
        """
        """
        pass

    @patch('rest3client.restclient.os.access', return_value=True)
    def test__init__Should_SetAttributes_When_CabundleExists(self, *patches):
        hostname = 'api.name.com'
        cabundle = 'cabundle'
        client = RESTclient(hostname, cabundle=cabundle)
        self.assertEqual(client.hostname, hostname)
        self.assertEqual(client.cabundle, cabundle)

    @patch('rest3client.restclient.os.access', return_value=False)
    def test__init__Should_SetAttributes_When_CabundleDoesNotExist(self, *patches):
        hostname = 'api.name.com'
        cabundle = 'cabundle'
        client = RESTclient(hostname, cabundle=cabundle)
        self.assertEqual(client.hostname, hostname)
        self.assertFalse(client.cabundle)

    @patch('rest3client.restclient.os.access', return_value=False)
    def test__init__Should_SetAttributes_When_ApiKey(self, *patches):
        hostname = 'api.name.com'
        cabundle = 'cabundle'
        api_key = 'some-api-key'
        client = RESTclient(hostname, api_key=api_key, cabundle=cabundle)
        self.assertEqual(client.api_key, api_key)

    @patch('rest3client.restclient.os.access', return_value=False)
    def test__init__Should_SetAttributes_When_BearerToken(self, *patches):
        hostname = 'api.name.com'
        cabundle = 'cabundle'
        bearer_token = 'token'
        client = RESTclient(hostname, bearer_token=bearer_token, cabundle=cabundle)
        self.assertEqual(client.bearer_token, bearer_token)

    @patch('rest3client.restclient.os.access', return_value=False)
    def test__init__Should_SetAttributes_When_JWT(self, *patches):
        hostname = 'api.name.com'
        cabundle = 'cabundle'
        jwtoken = 'jwtoken'
        client = RESTclient(hostname, jwt=jwtoken, cabundle=cabundle)
        self.assertEqual(client.jwt, jwtoken)

    @patch('rest3client.restclient.os.access', return_value=False)
    @patch('rest3client.restclient.SSLAdapter')
    def test__init__Should_SetAttributes_When_CertfileCertpass(self, ssl_adapter_patch, *patches):
        certfile = '--certfile--'
        certpass = '--certpass--'
        client = RESTclient('api.name.com', certfile=certfile, certpass=certpass)
        self.assertEqual(client.certfile, certfile)
        self.assertEqual(client.certpass, certpass)

    @patch('rest3client.restclient.os.access')
    @patch('rest3client.restclient.SSLAdapter')
    @patch('rest3client.restclient.requests.Session')
    def test__init_Should_InstantiateSslAdapterAndMountSslAdapterToSession_When_CertfileCertpass(self, session_patch, ssl_adapter_patch, *patches):
        session_mock = Mock()
        session_patch.return_value = session_mock
        hostname = 'api.name.com'
        certfile = '--certfile--'
        certpass = '--certpass--'
        client = RESTclient('api.name.com', certfile=certfile, certpass=certpass)
        ssl_adapter_patch.assert_called_once_with(certfile=certfile, certpass=certpass)
        client.session.mount.assert_called_once_with(f'https://{hostname}', ssl_adapter_patch.return_value)

    @patch('rest3client.restclient.os.access', return_value=False)
    @patch('rest3client.RESTclient.decorate_retries')
    def test__init__Should_SetAttributes_When_Retries(self, decorate_retries_patch, *patches):
        hostname = 'api.name.com'
        retries = [{'key1': 'val1'}, {'key1': 'val2'}]
        client = RESTclient(hostname, retries=retries)
        self.assertEqual(client.retries, retries)
        decorate_retries_patch.assert_called_once_with()

    @patch('rest3client.restclient.os.access')
    def test__get_headers_Should_ReturnHeaders_When_Called(self, *patches):
        client = RESTclient('api.name.com')
        result = client.get_headers()
        expected_result = {
            'Content-Type': 'application/json',
        }
        self.assertEqual(result, expected_result)

    @patch('rest3client.restclient.os.access')
    def test__get_headers_Should_ReturnHeaders_When_ApiKey(self, *patches):
        client = RESTclient('api.name.com', api_key='some-api-key')
        result = client.get_headers(headers={'Content-Type': 'application/xml'})
        expected_result = {
            'Content-Type': 'application/xml',
            'x-api-key': 'some-api-key'
        }
        self.assertEqual(result, expected_result)

    @patch('rest3client.restclient.os.access')
    def test__get_headers_Should_ReturnHeaders_When_BearerToken(self, *patches):
        client = RESTclient('api.name.com', bearer_token='token')
        result = client.get_headers()
        expected_result = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer token'
        }
        self.assertEqual(result, expected_result)

    @patch('rest3client.restclient.os.access')
    def test__get_headers_Should_ReturnHeaders_When_Token(self, *patches):
        client = RESTclient('api.name.com', token='token')
        result = client.get_headers()
        expected_result = {
            'Content-Type': 'application/json',
            'Authorization': 'token'
        }
        self.assertEqual(result, expected_result)

    @patch('rest3client.restclient.os.access')
    def test__get_headers_Should_ReturnHeaders_When_JWT(self, *patches):
        client = RESTclient('api.name.com', jwt='jwtoken')
        result = client.get_headers()
        expected_result = {
            'Content-Type': 'application/json',
            'Authorization': 'JWT jwtoken'
        }
        self.assertEqual(result, expected_result)

    @patch('rest3client.restclient.os.access')
    @patch('rest3client.RESTclient.redact')
    @patch('rest3client.restclient.logger')
    def test__log_request_Should_CallLogger_When_JsonNotSerializable(self, logger_patch, redact_patch, *patches):
        redact_patch.return_value = '--redacted-arguments--'
        client = RESTclient('api.name.com', bearer_token='token')
        arguments = {
            'address': '--address--',
            'data': Mock()
        }
        client.log_request('GET', arguments, True)
        debug_call = call('\nGET: --address-- NOOP: True\n"--redacted-arguments--"')
        self.assertTrue(debug_call in logger_patch.debug.mock_calls)

    @patch('rest3client.restclient.os.access')
    @patch('rest3client.RESTclient.redact')
    @patch('rest3client.restclient.logger')
    def test__log_request_Should_CallLogger_When_JsonSerializable(self, logger_patch, redact_patch, *patches):
        arguments = {
            'address': '--address--',
            'data': 'data'
        }
        redact_patch.return_value = arguments
        client = RESTclient('api.name.com', bearer_token='token')

        client.log_request('GET', arguments, True)
        debug_call = call('\nGET: --address-- NOOP: True\n{\n  "address": "--address--",\n  "data": "data"\n}')
        self.assertTrue(debug_call in logger_patch.debug.mock_calls)

    @patch('rest3client.restclient.os.access')
    def test__request_handler_Should_CallFunctionWithArgs_When_Args(self, *patches):
        mock_function = Mock(__name__='mocked method')
        client = RESTclient('api.name.com')
        decorated_function = RESTclient.request_handler(mock_function)
        decorated_function(client, '/rest/endpoint', k1='arg1', k2='arg2')
        expected_args = (client, '/rest/endpoint')
        args, _ = mock_function.call_args_list[0]
        self.assertEqual(args, expected_args)

    @patch('rest3client.restclient.os.access')
    @patch('rest3client.RESTclient.get_headers')
    def test__request_handler_Should_CallFunctionWithKwargs_When_Kwargs(self, get_headers, *patches):
        get_headers.return_value = {'h1': 'v1'}
        mock_function = Mock(__name__='mocked method')
        client = RESTclient('api.name.com')
        decorated_function = RESTclient.request_handler(mock_function)
        object1 = b''
        decorated_function(client, '/rest/endpoint', kwarg1='kwarg1', kwarg2='kwarg2', kwarg3=object1, verify=False)
        expected_kwargs = {
            'headers': {
                'h1': 'v1'
            },
            'verify': False,
            'address': 'https://api.name.com/rest/endpoint',
            'kwarg1': 'kwarg1',
            'kwarg2': 'kwarg2',
            'kwarg3': object1
        }
        _, kwargs = mock_function.call_args_list[0]
        self.assertEqual(kwargs, expected_kwargs)

    @patch('rest3client.restclient.os.access')
    @patch('rest3client.RESTclient.get_response', return_value='result')
    def test__request_handler_Should_CallFunctionAndReturnResult_When_FunctionDoesNotSetNoop(self, *patches):
        mock_function = Mock(__name__='mocked method')
        client = RESTclient('api.name.com')
        decorated_function = RESTclient.request_handler(mock_function)
        result = decorated_function(client, '/rest/endpoint')
        self.assertTrue(mock_function.called)
        self.assertEqual(result, 'result')

    @patch('rest3client.restclient.os.access')
    @patch('rest3client.RESTclient.get_response')
    def test__request_handler_Should_NotCallFunctionAndReturnNone_When_FunctionSetsNoop(self, *patches):
        mock_function = Mock(__name__='mocked method')
        client = RESTclient('api.name.com')
        decorated_function = RESTclient.request_handler(mock_function)
        result = decorated_function(client, '/rest/endpoint', noop=True)
        self.assertIsNone(result)
        self.assertFalse(mock_function.called)

    @patch('rest3client.restclient.os.access')
    @patch('rest3client.RESTclient.get_headers', return_value={'h1': 'v1'})
    def test__get_arguments_Should_SetHeaders_When_NoHeadersSpecified(self, *patches):
        client = RESTclient('api.name.com')
        endpoint = '/endpoint'
        kwargs = {}
        result = client.get_arguments(endpoint, kwargs)
        expected_result = {
            'h1': 'v1'
        }
        self.assertEqual(result['headers'], expected_result)

    @patch('rest3client.restclient.os.access')
    @patch('rest3client.RESTclient.get_headers', return_value={'h1': 'v1'})
    def test__get_arguments_Should_UpdatedHeaders_When_HeadersSpecified(self, *patches):
        client = RESTclient('api.name.com')
        endpoint = '/endpoint'
        kwargs = {
            'headers': {
                'h2': 'v2'
            }
        }
        result = client.get_arguments(endpoint, kwargs)
        expected_result = {
            'h1': 'v1',
            'h2': 'v2'
        }
        self.assertEqual(result['headers'], expected_result)

    @patch('rest3client.restclient.os.access')
    @patch('rest3client.RESTclient.get_headers', return_value={'h1': 'v1'})
    def test__get_arguments_Should_SetVerifyToCabundle_When_VerifyNotSpecified(self, *patches):
        client = RESTclient('api.name.com')
        endpoint = '/endpoint'
        kwargs = {}
        result = client.get_arguments(endpoint, kwargs)
        self.assertEqual(result['verify'], client.cabundle)

    @patch('rest3client.restclient.os.access')
    @patch('rest3client.RESTclient.get_headers', return_value={'h1': 'v1'})
    def test__get_arguments_Should_SetVerifyToCabundle_When_VerifyIsNone(self, *patches):
        client = RESTclient('api.name.com')
        endpoint = '/endpoint'
        kwargs = {
            'verify': None
        }
        result = client.get_arguments(endpoint, kwargs)
        self.assertEqual(result['verify'], client.cabundle)

    @patch('rest3client.restclient.os.access')
    @patch('rest3client.RESTclient.get_headers', return_value={'h1': 'v1'})
    def test__get_arguments_Should_NotSetVerify_When_VerifyIsSet(self, *patches):
        client = RESTclient('api.name.com')
        endpoint = '/endpoint'
        kwargs = {
            'verify': False
        }
        result = client.get_arguments(endpoint, kwargs)
        self.assertFalse(result['verify'])

    @patch('rest3client.restclient.os.access')
    @patch('rest3client.RESTclient.get_headers', return_value={'h1': 'v1'})
    def test__get_arguments_Should_SetAddress_When_Endpoint(self, *patches):
        client = RESTclient('api.name.com')
        endpoint = '/endpoint'
        kwargs = {}
        result = client.get_arguments(endpoint, kwargs)
        expected_result = 'https://api.name.com/endpoint'
        self.assertEqual(result['address'], expected_result)

    @patch('rest3client.restclient.os.access')
    @patch('rest3client.RESTclient.get_headers', return_value={'h1': 'v1'})
    def test__get_arguments_Should_SetAddress_When_HttpAddress(self, *patches):
        client = RESTclient('api.name.com')
        endpoint = 'https://upload.api.com/endpoint'
        kwargs = {}
        result = client.get_arguments(endpoint, kwargs)
        expected_result = 'https://upload.api.com/endpoint'
        self.assertEqual(result['address'], expected_result)

    @patch('rest3client.restclient.os.access')
    def test__get_response_Should_ReturnResponseJson_When_ResponseOk(self, *patches):
        mock_response = Mock(ok=True)
        mock_response.json.return_value = {
            'result': 'result'
        }
        client = RESTclient('api.name.com')
        result = client.get_response(mock_response)
        self.assertEqual(result, mock_response.json.return_value)

    @patch('rest3client.restclient.os.access')
    def test__get_response_Should_CallResponseRaiseForStatus_When_ResponseNotOk(self, *patches):
        mock_response = Mock(ok=False)
        mock_response.json.return_value = {
            'message': 'error message',
            'details': 'error details'}
        mock_response.raise_for_status.side_effect = [
            Exception('exception occurred')
        ]

        client = RESTclient('api.name.com')
        with self.assertRaises(Exception):
            client.get_response(mock_response)

    @patch('rest3client.restclient.os.access')
    def test__get_response_Should_ReturnRawResponse_When_RawResponse(self, *patches):
        mock_response = Mock()
        client = RESTclient('api.name.com')
        result = client.get_response(mock_response, raw_response=True)
        self.assertEqual(result, mock_response)

    @patch('rest3client.restclient.os.access')
    @patch('rest3client.restclient.requests.Session')
    def test__get_Should_CallRequestsGet_When_Called(self, *patches):
        client = RESTclient('api.name.com')
        client.get('/rest/endpoint')
        requests_get_call = call(
            'get',
            'https://api.name.com/rest/endpoint',
            headers={
                'Content-Type': 'application/json'},
            verify=client.cabundle)
        self.assertTrue(requests_get_call in client.session.request.mock_calls)

    @patch('rest3client.restclient.os.access')
    @patch('rest3client.restclient.requests.Session')
    def test__post_Should_CallRequestsPost_When_Called(self, *patches):
        client = RESTclient('api.name.com')
        requests_data = {
            'arg1': 'val1',
            'arg2': 'val2'}
        client.post('/rest/endpoint', json=requests_data)
        requests_post_call = call(
            'post',
            'https://api.name.com/rest/endpoint',
            headers={
                'Content-Type': 'application/json'},
            json={
                'arg1': 'val1',
                'arg2': 'val2'},
            verify=client.cabundle)
        self.assertTrue(requests_post_call in client.session.request.mock_calls)

    @patch('rest3client.restclient.os.access')
    @patch('rest3client.restclient.requests.Session')
    def test__put_Should_CallRequestsPut_When_Called(self, *patches):
        client = RESTclient('api.name.com')
        requests_data = {
            'arg1': 'val1',
            'arg2': 'val2'}
        client.put('/rest/endpoint', json=requests_data)
        requests_put_call = call(
            'put',
            'https://api.name.com/rest/endpoint',
            headers={
                'Content-Type': 'application/json'},
            json={
                'arg1': 'val1',
                'arg2': 'val2'},
            verify=client.cabundle)
        self.assertTrue(requests_put_call in client.session.request.mock_calls)

    @patch('rest3client.restclient.os.access')
    @patch('rest3client.restclient.requests.Session')
    def test__patch_Should_CallRequestsPatch_When_Called(self, *patches):
        client = RESTclient('api.name.com')
        requests_data = {
            'arg1': 'val1',
            'arg2': 'val2'}
        client.patch('/rest/endpoint', json=requests_data)
        requests_patch_call = call(
            'patch',
            'https://api.name.com/rest/endpoint',
            headers={
                'Content-Type': 'application/json'},
            json={
                'arg1': 'val1',
                'arg2': 'val2'},
            verify=client.cabundle)
        self.assertTrue(requests_patch_call in client.session.request.mock_calls)

    @patch('rest3client.restclient.os.access')
    @patch('rest3client.restclient.requests.Session')
    def test__head_Should_CallRequestsHead_When_Called(self, *patches):
        client = RESTclient('api.name.com')
        client.head('/rest/endpoint')
        requests_head_call = call(
            'head',
            'https://api.name.com/rest/endpoint',
            headers={
                'Content-Type': 'application/json'},
            verify=client.cabundle)
        self.assertTrue(requests_head_call in client.session.request.mock_calls)

    @patch('rest3client.restclient.os.access')
    @patch('rest3client.restclient.requests.Session')
    def test__delete_Should_CallRequestsDelete_When_Called(self, *patches):
        client = RESTclient('api.name.com')
        client.delete('/rest/endpoint')
        requests_delete_call = call(
            'delete',
            'https://api.name.com/rest/endpoint',
            headers={
                'Content-Type': 'application/json'},
            verify=client.cabundle)
        self.assertTrue(requests_delete_call in client.session.request.mock_calls)

    @patch('rest3client.restclient.os.access', return_value=False)
    def test__init__Should_SetUsernamePasswordAttributes_When_CalledWithUsernamePassword(self, *patches):
        client = RESTclient('hostname', username='value1', password='value2')
        self.assertEqual(client.username, 'value1')
        self.assertEqual(client.password, 'value2')

    @patch('rest3client.restclient.os.access', return_value=False)
    def test__get_headers_Should_SetAuthorizationHeader_When_UsernamePasswordAttributesExist(self, *patches):
        client = RESTclient('hostname', username='value1', password='value2')
        results = client.get_headers()
        self.assertTrue('Authorization' in results)
        self.assertTrue('Basic' in results['Authorization'])

    @patch('rest3client.restclient.os.access')
    def test__get_response_Should_ReturnResponseText_When_ResponseJsonRaisesValueError(self, *patches):
        mock_response = Mock(ok=True, text='response text')
        mock_response.json.side_effect = [
            ValueError('No JSON')
        ]
        client = RESTclient('api.name.com')
        result = client.get_response(mock_response)
        self.assertEqual(result, 'response text')

    def test__redact_Should_Redact_When_AuthorizationInHeaders(self, *patches):
        headers = {
            'headers': {
                'Content-Type': 'application/json',
                'Authorization': 'Basic abcdefghijklmnopqrstuvwxyz'
            },
            'verify': 'verify'
        }
        result = RESTclient.redact(headers)
        expected_result = {
            'headers': {
                'Content-Type': 'application/json',
                'Authorization': '[REDACTED]'
            },
            'verify': 'verify'
        }
        self.assertEqual(result, expected_result)

    def test__redact_Should_Redact_When_Address(self, *patches):
        headers = {
            'address': 'Address'
        }
        result = RESTclient.redact(headers)
        expected_result = {
        }
        self.assertEqual(result, expected_result)

    def test__redact_Should_Redact_When_AuthInHeaders(self, *patches):
        headers = {
            'headers': {
                'Content-Type': 'application/json',
                'Auth': 'SessionToken'
            },
            'address': 'Address',
            'verify': 'verify'
        }
        result = RESTclient.redact(headers)
        expected_result = {
            'headers': {
                'Content-Type': 'application/json',
                'Auth': '[REDACTED]'
            },
            'verify': 'verify'
        }
        self.assertEqual(result, expected_result)

    def test__redact_Should_Redact_When_XApiKeyInHeaders(self, *patches):
        headers = {
            'headers': {
                'Content-Type': 'application/json',
                'x-api-key': 'some-api-key'
            },
            'address': 'Address',
            'verify': 'verify'
        }
        result = RESTclient.redact(headers)
        expected_result = {
            'headers': {
                'Content-Type': 'application/json',
                'x-api-key': '[REDACTED]'
            },
            'verify': 'verify'
        }
        self.assertEqual(result, expected_result)

    def test__redact_Should_Redact_When_JsonPassword(self, *patches):
        headers = {
            'headers': {
                'Content-Type': 'application/json',
                'Auth': 'SessionToken'
            },
            'address': 'Address',
            'verify': 'verify',
            'json': {
                'userName': 'some user',
                'password': 'some password'
            }
        }
        result = RESTclient.redact(headers)
        expected_result = {
            'headers': {
                'Content-Type': 'application/json',
                'Auth': '[REDACTED]'
            },
            'verify': 'verify',
            'json': {
                'userName': 'some user',
                'password': '[REDACTED]'
            }
        }
        self.assertEqual(result, expected_result)

    def test__redact_Should_Redact_When_JsonPasswordCap(self, *patches):
        headers = {
            'headers': {
                'Content-Type': 'application/json',
                'Auth': 'SessionToken'
            },
            'address': 'Address',
            'verify': 'verify',
            'json': {
                'userName': 'some user',
                'Password': 'some password'
            }
        }
        result = RESTclient.redact(headers)
        expected_result = {
            'headers': {
                'Content-Type': 'application/json',
                'Auth': '[REDACTED]'
            },
            'verify': 'verify',
            'json': {
                'userName': 'some user',
                'Password': '[REDACTED]'
            }
        }
        self.assertEqual(result, expected_result)

    def test__redact_Should_Redact_When_ListOfPasswordsAndTokens(self, *patches):
        headers = {
            'headers': {
                'Content-Type': 'application/json',
                'Auth': 'SessionToken'
            },
            'address': 'Address',
            'verify': 'verify',
            'json': [
                {
                    'userName': 'some user1',
                    'Password': 'some password'
                }, {
                    'userName': 'some user2',
                    'Password': 'some password'
                }, {
                    'User': 'some user3',
                    'Token': 'some token3'
                }, {
                    'User': 'some user4',
                    'token': 'some token4'
                }
            ]
        }
        result = RESTclient.redact(headers)
        expected_result = {
            'headers': {
                'Content-Type': 'application/json',
                'Auth': '[REDACTED]'
            },
            'verify': 'verify',
            'json': [
                {
                    'userName': 'some user1',
                    'Password': '[REDACTED]'
                }, {
                    'userName': 'some user2',
                    'Password': '[REDACTED]'
                }, {
                    'User': 'some user3',
                    'Token': '[REDACTED]'
                }, {
                    'User': 'some user4',
                    'token': '[REDACTED]'
                }
            ]
        }
        self.assertEqual(result, expected_result)

    @patch('rest3client.restclient.os.access')
    def test__get_error_message_Should_ReturnExpected_When_ResponseJson(self, *patches):
        client = RESTclient('api.name.com')
        response_mock = Mock()
        response_mock.json.return_value = 'json value'
        result = client.get_error_message(response_mock)
        self.assertEqual(result, response_mock.json.return_value)

    @patch('rest3client.restclient.os.access')
    def test__get_error_message_ShouldReturnExpected_When_ResponseJsonValueError(self, *patches):
        client = RESTclient('api.name.com')
        response_mock = Mock()
        response_mock.json.side_effect = ValueError()
        response_mock.text = 'text error'
        result = client.get_error_message(response_mock)
        self.assertEqual(result, response_mock.text)

    @patch('rest3client.RESTclient.get_loggable_kwargs')
    @patch('rest3client.restclient.os.access')
    @patch('rest3client.RESTclient.discover_retries')
    @patch('rest3client.restclient.retry')
    def test__decorate_retries_Should_CallExpected_When_Called(self, retry_patch, discover_retries_patch, *patches):
        mock_method = Mock(__name__='retry_type1_error')
        retries = [{'retry_on_exception': mock_method, 'key1': 'val1', 'key2': 'val2'}]
        client = RESTclient('api.name.com', retries=retries)
        discover_retries_patch.assert_called_once_with()
        retry_get_call = call(retry_on_exception=mock_method, key1='val1', key2='val2')(client.get)
        self.assertTrue(retry_get_call, retry_patch.mock_calls)
        retry_post_call = call(retry_on_exception=mock_method, key1='val1', key2='val2')(client.post)
        self.assertTrue(retry_post_call, retry_patch.mock_calls)
        retry_put_call = call(retry_on_exception=mock_method, key1='val1', key2='val2')(client.put)
        self.assertTrue(retry_put_call, retry_patch.mock_calls)
        retry_patch_call = call(retry_on_exception=mock_method, key1='val1', key2='val2')(client.patch)
        self.assertTrue(retry_patch_call, retry_patch.mock_calls)
        retry_delete_call = call(retry_on_exception=mock_method, key1='val1', key2='val2')(client.delete)
        self.assertTrue(retry_delete_call, retry_patch.mock_calls)

    @patch('rest3client.restclient.logger')
    def test__get_loggable_kwargs_Should_CallExpected_When_Called(self, logger_patch, *patches):
        function_mock = Mock(__name__='function1')
        kwargs = {'key1': 'val1', 'function': function_mock}
        result = RESTclient.get_loggable_kwargs(kwargs)
        expected_result = {'key1': 'val1', 'function': 'function1'}
        self.assertEqual(result, json.dumps(expected_result, indent=2))

    @patch('rest3client.RESTclient.retry_type2_error', create=True)
    @patch('rest3client.RESTclient.retry_type1_error', create=True)
    def test__get_retry_methods_Should_ReturnExpected_When_Called(self, *patches):
        client = RESTclient('api.name.com')
        result = client.get_retry_methods()
        expected_result = [
            'retry_type1_error',
            'retry_type2_error'
        ]
        self.assertEqual(result, expected_result)

    def test__get_retry_key_values_Should_ReturnNone_When_NoRetry(self, *patches):
        mock_method = Mock(__name__='retry_type1_error')
        method_help = """ return True if exception is a type1 exception
        """
        result = RESTclient.get_retry_key_values(mock_method, method_help)
        self.assertIsNone(result)

    @patch('rest3client.RESTclient.add_retry_key_values')
    def test__get_retry_key_values_Should_ReturnAndCallExpected_When_RetryMatch(self, add_retry_key_values_patch, *patches):
        mock_method = Mock(__name__='retry_type1_error')
        method_help = """ return True if exception is a type1 exception
            retry:
                wait_random_min:10000
                wait_random_max:20000
                stop_max_attempt_number:6
        """
        result = RESTclient.get_retry_key_values(mock_method, method_help)
        expected_result = {
            'retry_on_exception': mock_method
        }
        self.assertEqual(result, expected_result)
        add_retry_key_values_patch.assert_called_once_with(
            expected_result,
            'wait_random_min:10000\n                wait_random_max:20000\n                stop_max_attempt_number:6')

    @patch('rest3client.RESTclient.retry_type4_error', create=True, __name__='retry_type4_error')
    @patch('rest3client.RESTclient.retry_type3_error', create=True, __name__='retry_type3_error')
    @patch('rest3client.RESTclient.retry_type2_error', create=True, __name__='retry_type2_error', __doc__=None)
    @patch('rest3client.RESTclient.retry_type1_error', create=True, __name__='retry_type1_error')
    @patch('rest3client.RESTclient.decorate_retries')
    @patch('rest3client.RESTclient.get_retry_key_values')
    def test__discover_retries_Should_ReturnExpected_When_Called(self, get_retry_key_values_patch, *patches):
        mock_method0 = Mock(__name__='retry_type0_error')
        mock_method1 = Mock(__name__='retry_type1_error')
        mock_method3 = Mock(__name__='retry_type3_error')
        get_retry_key_values_patch.side_effect = [
            {'retry_on_exception': mock_method1, 'key': 'retry_type1_error_metadata'},
            {'retry_on_exception': mock_method3, 'key': 'retry_type3_error_metadata'},
            None
        ]
        retries = [
            {'retry_on_exception': mock_method0, 'key': 'retry_type0_error_metadata'}
        ]
        client = RESTclient('api.name.com', retries=retries)
        client.discover_retries()
        expected_retries = [
            {'retry_on_exception': mock_method0, 'key': 'retry_type0_error_metadata'},
            {'retry_on_exception': mock_method1, 'key': 'retry_type1_error_metadata'},
            {'retry_on_exception': mock_method3, 'key': 'retry_type3_error_metadata'}
        ]
        self.assertEqual(client.retries, expected_retries)

    def test__add_retry_key_values_Should_ReturnExpected_When_NoEnvEmptyValue(self, *patches):
        method_mock = Mock(__name__='retry_type1_error')
        key_values = {
            'retry_on_exception': method_mock
        }
        retry_text = ''
        RESTclient.add_retry_key_values(key_values, retry_text)
        expected_result = {
            'retry_on_exception': method_mock
        }
        self.assertEqual(key_values, expected_result)

    def test__add_retry_key_values_Should_ReturnExpected_When_NoEnvNoMatchValue(self, *patches):
        method_mock = Mock(__name__='retry_type1_error')
        key_values = {
            'retry_on_exception': method_mock
        }
        retry_text = 'some non-matching text here'
        RESTclient.add_retry_key_values(key_values, retry_text)
        expected_result = {
            'retry_on_exception': method_mock
        }
        self.assertEqual(key_values, expected_result)

    def test__add_retry_key_values_Should_ReturnExpected_When_NoEnvWithValues(self, *patches):
        method_mock = Mock(__name__='retry_type1_error')
        key_values = {
            'retry_on_exception': method_mock
        }
        retry_text = 'wait_fixed:60000\n                stop_max_attempt_number:60'
        RESTclient.add_retry_key_values(key_values, retry_text)
        expected_result = {
            'retry_on_exception': method_mock,
            'wait_fixed': 60000,
            'stop_max_attempt_number': 60
        }
        self.assertEqual(key_values, expected_result)

    def test__add_retry_key_values_Should_RaiseValueError_When_NoEnvNoValue(self, *patches):
        method_mock = Mock(__name__='retry_type1_error')
        key_values = {
            'retry_on_exception': method_mock
        }
        retry_text = 'wait_fixed:\n                stop_max_attempt_number:'
        with self.assertRaises(ValueError):
            RESTclient.add_retry_key_values(key_values, retry_text)

    @patch('rest3client.restclient.os.getenv')
    def test__add_retry_key_values_Should_ReturnExpected_When_EnvWithNoValues(self, getenv_patch, *patches):
        getenv_patch.side_effect = ['60000', '60']
        method_mock = Mock(__name__='retry_type1_error')
        key_values = {
            'retry_on_exception': method_mock
        }
        retry_text = 'wait_fixed:1\n                stop_max_attempt_number:2'
        RESTclient.add_retry_key_values(key_values, retry_text)
        expected_result = {
            'retry_on_exception': method_mock,
            'wait_fixed': 60000,
            'stop_max_attempt_number': 60
        }
        self.assertEqual(key_values, expected_result)
