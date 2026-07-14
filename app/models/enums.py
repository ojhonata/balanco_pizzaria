import enum


class Type(enum.Enum):
    ENTRADA = "entrada"
    SAIDA = "saida"

class Location(enum.Enum):
    FUNDO = "fundo"
    FRENTE = "frente"
    DISPENSA = "dispensa"

class BalanceStatus(enum.Enum):
    ABERTO = "aberto"
    FECHADO = "fechado"

class OrderStatus(enum.Enum):
    PENDENTE = "pendente"
    RECEBIDO = "recebido"
    NAO_ENTREGUE = "nao_entregue"
