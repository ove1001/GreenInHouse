""" BackendService class module.
"""

from typing import Optional
import requests
from dms2223common.data import Role
from dms2223common.data.Comentario import Comentario
from dms2223common.data.Pregunta import Pregunta
from dms2223common.data.Respuesta import Respuesta
from dms2223common.data.rest import ResponseData
from dms2223common.data.Reporte import Reporte


class BackendService():
    """ REST client to connect to the backend service.
    """

    def __init__(self,
        host: str, port: int,
        api_base_path: str = '/api/v1',
        apikey_header: str = 'X-ApiKey-Backend',
        apikey_secret: str = 'This is another frontend API key'
        ):
        """ Constructor method.

        Initializes the client.

        Args:
            - host (str): The backend service host string.
            - port (int): The backend service port number.
            - api_base_path (str): The base path that is prepended to every request's path.
            - apikey_header (str): Name of the header with the API key that identifies this client.
            - apikey_secret (str): The API key that identifies this client.
        """
        self.__host: str = host
        self.__port: int = port
        self.__api_base_path: str = api_base_path
        self.__apikey_header: str = apikey_header
        self.__apikey_secret: str = apikey_secret

    def __base_url(self) -> str:
        return f'http://{self.__host}:{self.__port}{self.__api_base_path}'

    def list_questions(self,token: Optional[str]):
        """ Requests a list of registered users.

        Args:
            token (Optional[str]): The user session token.

        Returns:
            - ResponseData: If successful, the contents hold a list of user data dictionaries.
              Otherwise, the contents will be an empty list.
        """
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + '/questions',
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
            response_data.set_content([])
        return response_data

    def create_question(self, token: Optional[str], pregunta: Pregunta):
        """ Requests a user creation.

        Args:
            - token (Optional[str]): The user session token.
            - username (str): The new user's name.
            - password (str): The new user's password.

        Returns:
            - ResponseData: If successful, the contents hold the new user's data.
        """
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.post(
            self.__base_url() + '/questions',
            json=pregunta.to_json(True),
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def get_question(self,token: Optional[str],id:int):

        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + f"/questions/{id}/answers",
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data
    
    def get_answer(self,token: Optional[str],id:int):

        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + f"/answers/{id}",
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def get_comment(self,token: Optional[str],id:int):

        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + f"/comments/{id}",
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def post_answer(self,token: Optional[str],id:int,answer: Respuesta):
        
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.post(
            self.__base_url() + f"/questions/{id}/answers",
            json=answer.to_json(True),
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def question_report(self,token: Optional[str],id:int,reporte: Reporte):
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.post(
            self.__base_url() + f"/questions/{id}/reports",
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            json=reporte.to_json(True),
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def list_reports(self,token: Optional[str]):

        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + '/reports',
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
            response_data.set_content([])
        return response_data

    def change_report(self,token: Optional[str],report: Reporte):

        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.post(
            self.__base_url() + f"/reports",
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            json={"status":report.getEstado().name, "id":report.getId(), "tipo":report.getTipoElemento()},
            timeout=60
        )
        response_data.set_successful(response.ok)
        if not response_data.is_successful():
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def upvote_answer(self,token: Optional[str],id:int,usuario:str):
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.post(
            self.__base_url() + f"/answers/{id}/votes",
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            json=usuario,
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def post_comment(self,token: Optional[str],id:int,comment: Comentario):
        
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.post(
            self.__base_url() + f"/answers/{id}/comments",
            json=comment.to_json(True),
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def report_answer(self,token: Optional[str],id:int,reporte:Reporte):

        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.post(
            self.__base_url() + f"/answers/{id}/reports",
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            json=reporte.to_json(True),
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def upvote_comments(self,token: Optional[str],id:int,usuario:str):

        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.post(
            self.__base_url() + f"/comments/{id}/votes",
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            json=usuario,
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def report_comments(self,token: Optional[str],id:int,reporte:Reporte):

        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.post(
            self.__base_url() + f"/comments/{id}/reports",
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            json=reporte.to_json(True),
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data