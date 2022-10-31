import unittest
import json
from app import app
from flaskr.modelos.modelos import *


def login_user(self, username, password):
        return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            username=username,
            password=password
        )),
        content_type='application/json',
    )

class TestVistaBlackList(unittest.TestCase):
    def setUp(self):        
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        app.config['APP_ENV'] = 'APP_ENV_TESTING'
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        db.create_all()


    

    def test_vista_black_list_get_all_positive(self):
        with self.client:
            token = login_user(self, 'vquiroz', '1234')
            response = self.client.get(
                '/blacklists', 
                headers=dict(
                    Authorization = 'Bearer ' + json.loads(
                        token.data.decode()
                    )['token']
                )
            )            
            self.assertEqual(response.status_code, 200)

    
    def test_vista_black_list_get_all_token_mal_formado(self):
        with self.client:
            token = login_user(self, 'vquiroz', '1234')
            response = self.client.get(
                '/blacklists', 
                headers=dict(
                    Authorization = 'Bearer' + json.loads(
                        token.data.decode()
                    )['token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['msg'] == "Missing 'Bearer' type in 'Authorization' header. Expected 'Authorization: Bearer <JWT>'")
            self.assertEqual(response.status_code, 401)

    def test_vista_blacklist_post_agregar_mail_repetido(self):
        with self.client:
            token = login_user(self, 'vquiroz', '1234')
            new_bloqueado = {
                "email": "correo@uniandes.edu.co",
                "app_uuid": "sdd1234dsfsdf9abcdef",
               "blocked_reason": "Bloqueo de test"
            }
            response = self.client.post(
                '/blacklists', json=new_bloqueado, 
                headers=dict(
                    Authorization = 'Bearer ' + json.loads(
                        token.data.decode()
                    )['token']
                )
            )
            data = json.loads(response.data.decode())              
            code = response.status_code
            self.assertTrue(data['mensaje'] == 'Email ya existe en la lista negra')
            self.assertEqual(code, 400)

    def test_vista_black_list_get_one_positive(self):
        with self.client:
            token = login_user(self, 'vquiroz', '1234')
            response = self.client.get(
                '/blacklists/correo@uniandes.edu.co', 
                headers=dict(
                    Authorization = 'Bearer ' + json.loads(
                        token.data.decode()
                    )['token']
                )
            )
            data = json.loads(response.data.decode())            
            self.assertTrue(data['email'] == 'correo@uniandes.edu.co')
            self.assertEqual(response.status_code, 200)