from django.db import models

# Create your models here.

# CRIAR VARIAVEL DE TOKEN ENTREGUE E DE ATIVO/INATIVO

FUNCOES = [
    ("Médico", "Médico"),
    ("Enfermeiro", "Enfermeiro"),
    ("Técnico de Enfermagem", "Técnico de Enfermagem"),
    ("Fisioterapeuta", "Fisioterapeuta"),
    ("Nutricionista", "Nutricionista"),
    ("Farmacêutico", "Farmacêutico"),
    ("Ortopedista", "Ortopedista"),
    ("Psicólogo", "Psicólogo"),
    ("Assistente Social", "Assistente Social"),
    ("Técnico de Radiologia", "Técnico de Radiologia"),
    ("Técnico de Laboratório", "Técnico de Laboratório"),
    ("Coordenador", "Coordenador"),
    ("Supervisor", "Supervisor"),
    ("Auxiliar Administrativo", "Auxiliar Administrativo"),
]

funcoes = [funcao[0] for funcao in FUNCOES]



# SETORES = [
#     ("Administração", "Administração"),
#     ("Financeiro", "Financeiro"),
#     ("DP", "DP"),
#     ("Produção", "Produção"),
#     ("Compras", "Compras"),
# ]

# setores = [setor[0] for setor in SETORES]

class Token(models.Model):
    nome_responsavel = models.CharField(max_length=125, null=False, blank=False)
    cpf_responsavel = models.CharField(max_length=14, null=True, blank=True)
    funcao_responsavel = models.CharField(max_length=125, choices=FUNCOES, null=True, blank=True)
    # setor_responsavel = models.CharField(max_length=125, choices=SETORES, null=True, blank=True)
    # telefone_responsavel = models.CharField(max_length=15, null=True, blank=True)
    serial = models.CharField(max_length=14, null=True, blank=True)
    data_solicitacao = models.DateField(null=True, blank=True, default=None)
    data_entrega = models.DateField(blank=True, null=True)
    data_modificacao = models.DateField(auto_now=True)
    observacao = models.TextField(null=True, blank=True)
    criador = models.CharField(max_length=125, null=True, blank=True)
    modificador = models.CharField(max_length=125, null=True, blank=True)
    token_entregue = models.BooleanField(default=False)
    token_ativo = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.nome_responsavel}"
    
