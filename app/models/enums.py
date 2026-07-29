import enum


class TypeMovement(enum.Enum):
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
    SOLICITADO = "solicitado"
    PEDIDO_REALIZADO = "pedido_realizado"
    RECEBIDO = "recebido"
    NAO_ENTREGUE = "nao_entregue"

class Roles(enum.Enum):
    PIZZARIA = "pizzaria"
    BAR = "bar"
    COZINHA = "cozinha"
    ADMIN = "admin"
