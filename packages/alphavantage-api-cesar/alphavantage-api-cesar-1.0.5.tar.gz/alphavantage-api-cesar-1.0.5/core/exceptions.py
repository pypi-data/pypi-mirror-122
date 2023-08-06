class APICallError(Exception):
    pass

class Response404CodeError(APICallError):
    """ Pagina não encontrada"""
    
class Response500CodeError(APICallError):
    """Erro interno do servidor"""

class ResponseGenericCodeError(APICallError):
    """Erro desconhecido"""

class InvalidPayloadError(APICallError):
    """Por favor, verifique os argumentos esperados"""


class InvalidIntervalError(APICallError):
     """Por favor, escolha um valor entre 1, 5, 15 ,30 ou 60 minutos verifique os argumentos esperados"""


