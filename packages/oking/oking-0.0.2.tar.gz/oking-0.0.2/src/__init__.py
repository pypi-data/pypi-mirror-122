import configparser
import logging
from logging import config
from src.services import srequest
from src.api import oking
import platform
from os import path

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
config.fileConfig(log_file_path)
conf_prop = configparser.ConfigParser()

logger = logging.getLogger()
logger.debug('====== Inicia Aplicacao __init__ ======')

global client_data, is_connected_oracle_client
global url_api_okvendas, token_api_okvendas

config_path: str = ''
current_os = platform.system()
if current_os == 'Windows':
    config_path = 'c:\\oking\\config.ini'
elif current_os == 'Linux':
    config_path = '/opt/oking/config.ini'
elif current_os == 'Darwin':
    config_path = ''
elif current_os == 'Java':
    config_path = ''

assert config_path != '', 'Nao foi possivel determinar o OS atual'
if path.exists(config_path):
    conf_prop.read(config_path)
    token_oking = conf_prop.get('APIOKING', 'token')

    # Consultar dados da integracao do cliente (modulos, tempo de execucao, dados api okvendas)
    client_data = oking.get(f'https://appbuilder.openk.com.br/api/consulta/integracao_oking/filtros?token={token_oking}', None)

    if client_data is not None:
        assert client_data['integracao_id'] is not None, 'Id da integracao nao informado (Api Oking)'
        assert client_data['db_type'] is not None, 'Tipo do banco de dados nao informado (Api Oking)'
        assert client_data['host'] is not None, 'Host do banco de dados nao informado (Api Oking)'
        assert client_data['database'] is not None, 'Nome do banco de dados nao informado (Api Oking)'
        assert client_data['user'] is not None, 'Usuario do banco de dados nao informado (Api Oking)'
        assert client_data['password'] is not None, 'Senha do banco de dados nao informado (Api Oking)'
        assert client_data['url_api'] is not None, 'Url da api okvendas nao informado (Api Oking)'
        assert client_data['token_api'] is not None, 'Token da api okvendas nao informado (Api Oking)'
        is_connected_oracle_client = False
        url_api_okvendas = client_data['url_api']
        token_api_okvendas = client_data['token_api']

    else:
        logger.warning(f'Cliente nao configurado no painel oking {token_oking}')
else:
    logger.warning('Arquivo de configuração não encontrado config.ini')
