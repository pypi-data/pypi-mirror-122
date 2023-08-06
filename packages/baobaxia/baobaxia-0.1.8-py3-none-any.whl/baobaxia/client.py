import os, requests, json, sys
from pathlib import Path
from getpass import getpass
from typing import Optional

from pydantic import BaseModel

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter


class ClientConfig(BaseModel):
    base_url: str
    balaio: Optional[str] = None
    mucua: Optional[str] = None
    username: Optional[str] = None

class BaobaxiaClient():
    
    def __init__(self, config_file=None):
        super().__init__()
        if config_file is None:
            self.config_file = Path.home() / '.baobaxia' / 'client.config'
        else:
            self.config_file = config_file
        if self.config_file.exists():
            self.load_config()
        else:
            url = input('URL: ')
            self.config = ClientConfig(base_url = url)
        self.token = None
        self.last_response = None

    def load_config(self):
        self.config = ClientConfig.parse_file(
            self.config_file)
        
    def save_config(self):
        self.config_file.open('w').write(
            self.config.json())

    def get_headers(self):
        result = {}
        if self.token is not None:
            result['token'] = self.token
        return result
    
    def request(self, method, path,
                data=None,
                files=None,
                as_json=True,
                pretty_print=True
    ):
        method = method.lower()
        if method == 'del':
            method = 'delete'
        self.last_response = getattr(requests, method)(
            self.config.base_url + path,
            data = data,
            files = files,
            headers = self.get_headers())
        if as_json and pretty_print:
            json_str = json.dumps(self.last_response.json(),
                                  sort_keys=True,
                                  indent=2,
                                  separators=(',', ': '))
            return highlight(json_str, JsonLexer(), TerminalFormatter())
        if as_json:
            return self.last_response.json()
        return self.last_response.content
    
    def auth(self):
        password = getpass('Senha: ')
        self.token = self.request('post',
            'auth/' + self.config.balaio + '/' + self.config.mucua,
            data={'username': self.config.username, 'password': password},
            pretty_print=False
            )
        return self.token
    
    def list_balaios(self, pretty_print=True):
        if pretty_print:
            print(self.request('get', 'balaio'))
        else:
            return self.request('get', 'balaio', pretty_print=False)
    
    def post_balaio(self, name, default_mucua):
        return self.request('post', 'balaio',
            data={'name': name, 'default_mucua': default_mucua})
    
    def get_balaio(self, balaio, pretty_print=True):
        if pretty_print:
            print(self.request('get', 'balaio/'+balaio))
        else:
            return self.request('get', 'balaio/'+balaio, pretty_print=False)
    
    def put_balaio(self, balaio, name, default_mucua):
        print(self.request('put', 'balaio/'+balaio,
            data={'name': name, 'default_mucua': default_mucua}))
    
    def del_balaio(self, balaio):
        print(self.request('del', 'balaio/'+balaio))
    
    def list_mucuas(self, pretty_print=True):
        if pretty_print:
            print(self.request('get', 'mucua/'+self.config.balaio))
        else:
            return self.request('get', 'mucua/'+self.config.balaio,
                                pretty_print=False)
    
    def post_mucua(self, name):
        print(self.request('post', 'mucua/'+self.config.balaio,
            data={'name': name}))
    
    def get_mucua(self, mucua, pretty_print=True):
        if pretty_print:
            print(self.request('get', 'mucua/'+self.config.balaio+'/'+mucua))
        else:
            return self.request('get', 'mucua/'+self.config.balaio+'/'+mucua,
                                pretty_print=False)
    
    def put_mucua(self, mucua, name):
        print(self.request('put', 'mucua/'+self.config.balaio+'/'+mucua,
            data={'name': name}))
    
    def del_mucua(self, mucua):
        print(self.request('del', 'mucua/'+self.config.balaio+'/'+mucua))
    
    def list_mocambolas(self, pretty_print=True):
        if pretty_print:
            print(self.request('get',
                               'mocambola/'+self.config.balaio+'/'+self.config.mucua))
        else:
            return self.request('get',
                                'mocambola/'+self.config.balaio+'/'+self.config.mucua,
                                pretty_print=False)
    
    def get_mocambola(self, username, pretty_print=True):
        if pretty_print:
            print(self.request('get', 
            'mocambola/'+self.config.balaio+'/'+self.config.mucua+'/'+username))
        else:
            return self.request('get', 
            'mocambola/'+self.config.balaio+'/'+self.config.mucua+'/'+username,
            pretty_print=False)
    
    def post_mocambola(self, mocambola):
        print(self.request('post',
            'mocambola/'+self.config.balaio+'/'+self.config.mucua,
                            data=json.dumps(mocambola)))
    
    def put_mocambola(self, username, mocambola):
        print(self.request('put',
            'mocambola/'+self.config.balaio+'/'+self.config.mucua+'/'+username,
                            data=json.dumps(mocambola)))
    
    def del_mocambola(self, username):
        print(self.request('del',
            'mocambola/'+self.config.balaio+'/'+self.config.mucua+'/'+username))
    
    def list_midias(self, pretty_print=True):
        if pretty_print:
            print(self.request('get',
            'acervo/midia/'+self.config.balaio+'/'+self.config.mucua))
        else:
            return self.request('get',
                    'acervo/midia/'+self.config.balaio+'/'+self.config.mucua,
                    pretty_print=False)
    
    def get_midia(self, path, pretty_print=True):
        if pretty_print:
            print(self.request('get',
            'acervo/midia/'+self.config.balaio+'/'+self.config.mucua+'/'+str(path)))
        else:
            return self.request('get',
                    'acervo/midia/'+self.config.balaio+'/'+self.config.mucua+'/'+str(path),
                    pretty_print=False)
    
    def post_midia(self, titulo, descricao, tipo, tags):
        print(self.request('post', 
            'acervo/midia/'+self.config.balaio+'/'+self.config.mucua,
            data={
                'titulo': titulo,
                'descricao': descricao,
                'tipo': tipo,
                'tags': tags
            }))
    
    def put_midia(self, path, titulo, descricao, tags):
        print(self.request('put',
            'acervo/midia/'+self.config.balaio+'/'+self.config.mucua+'/'+str(path),
            data={
                'titulo': titulo,
                'descricao': descricao,
                'tags': tags
            }))
    
    def del_midia(self, path):
        print(self.request('del',
            'acervo/midia/'+self.config.balaio+'/'+self.config.mucua+'/'+str(path)))
    
    def upload_midia(self, path, arquivo):
        name = os.path.basename(arquivo)
        with open(arquivo, 'rb') as f:
            print(self.request('post',
                'acervo/upload/'+self.config.balaio+'/'+self.config.mucua+'/'+str(path),
                as_json=False,
                files={'arquivo': (name,f)}))
    
    def download_midia(self, path, arquivo):
        content = self.request('get',
                'acervo/download/'+self.config.balaio+'/'+self.config.mucua+'/'+str(path),
                as_json=False)
        with open(arquivo, 'wb') as f:
            f.write(content)
    
    def publish_midia(self, path):
        return self.request('put',
                'acervo/publish/'+self.config.balaio+'/'+self.config.mucua+'/'+str(path))
    
    def find_midias(self, keywords=None,
                    hashtags=None, tipos=None,
                    ordem_campo=None, ordem_decrescente=None,
                    pag_tamanho=None, pag_atual=None):
        url = 'acervo/find/'+self.config.balaio+'/'+self.config.mucua+'?'
        if keywords is not None:
            url += 'keywords='+keywords+'&'
        if hashtags is not None:
            url += 'hashtags='+hashtags
        if tipos is not None:
            url += 'tipos='+tipos
        if ordem_campo is not None:
            url += 'ordem_campo='+ordem_campo
        if ordem_decrescente is not None:
            url += 'ordem_decrescente='+ordem_decrescente
        if pag_tamanho is not None:
            url += 'pag_tamanho='+pag_tamanho
        if pag_atual is not None:
            url += 'pag_atual='+pag_atual
        return self.request('get', url)
    
    def get_tipos_por_content_type(self):
        return self.request('get', 'acervo/tipos_por_content_type')
