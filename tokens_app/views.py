from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Token, funcoes
import openpyxl as xl
from .atualiza_lista import atualiza_lista_tokens
from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout as logout_django
import logging
import time

logger = logging.getLogger(__name__)

User = get_user_model()

User()

# Funções auxiliares para pegar dados dinâmicos no momento da requisição
def get_assistentes():
    return User.objects.all()

def get_datas_entregas():
    datas = []
    for token in Token.objects.all():
        if token.data_entrega:
            data_str = token.data_entrega.strftime("%d-%m-%Y")
            if data_str not in datas:
                datas.append(data_str)
    datas.sort(key=lambda x: time.strptime(x, "%d-%m-%Y"))
    return datas

def get_datas_solicitacoes():
    datas = []
    for token in Token.objects.all():
        if token.data_solicitacao:
            data_str = token.data_solicitacao.strftime("%d-%m-%Y")
            if data_str not in datas:
                datas.append(data_str)
    datas.sort(key=lambda x: time.strptime(x, "%d-%m-%Y"))
    return datas

def home(request):
    logger.info(f"User {request.user.username} Acessou a página inicial. {time.strftime('%Y-%m-%d %H:%M:%S')}")
    return render(request, 'home.html', {"usuario": request.user})

def lista_tokens(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        logger.info(f"User {request.user.username} Acessou a lista de tokens. {time.strftime('%Y-%m-%d %H:%M:%S')}")
        tokens = Token.objects.all().order_by('nome_responsavel')
        assistentes = get_assistentes()
        data_entregas = get_datas_entregas()
        data_solicitacoes = get_datas_solicitacoes()
        return render(request, 'lista_tokens.html', {
            'tokens': tokens,
            "usuario": request.user,
            "funcoes": funcoes,
            "data_entregas": data_entregas,
            "data_solicitacoes": data_solicitacoes,
            "assistentes": assistentes,
            "user_permissions": request.user.get_all_permissions(),
        })


def lista_tokens_funcao(request, funcao):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        logger.info(f"User {request.user.username} Acessou a lista de tokens da função {funcao}. {time.strftime('%Y-%m-%d %H:%M:%S')}")
        tokens = Token.objects.filter(funcao_responsavel=funcao).order_by('nome_responsavel')
        if not tokens:
            return HttpResponse("Nenhum token encontrado para esta função.")
        assistentes = get_assistentes()
        data_entregas = get_datas_entregas()
        data_solicitacoes = get_datas_solicitacoes()
        return render(request, 'lista_tokens.html', {
            'tokens': tokens,
            "usuario": request.user,
            "funcoes": funcoes,
            "data_entregas": data_entregas,
            "data_solicitacoes": data_solicitacoes,
            "assistentes": assistentes,
            "user_permissions": request.user.get_all_permissions(),
        })

def lista_tokens_assistente_modificador(request, assistente_id):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        try:
            assistente = User.objects.get(id=assistente_id)
            tokens = Token.objects.filter(modificador=assistente.username).order_by('nome_responsavel')
            logger.info(f"User {request.user.username} Acessou a lista de ultimos tokens modificados por: {assistente.username}. {time.strftime('%Y-%m-%d %H:%M:%S')}")
            assistentes = get_assistentes()
            data_entregas = get_datas_entregas()
            data_solicitacoes = get_datas_solicitacoes()
            return render(request, 'lista_tokens.html', {
                'tokens': tokens,
                "usuario": request.user,
                "funcoes": funcoes,
                "data_entregas": data_entregas,
                "data_solicitacoes": data_solicitacoes,
                "assistentes": assistentes,
                "user_permissions": request.user.get_all_permissions(),
            })
        except User.DoesNotExist:
            return HttpResponse("Assistente não encontrado.")

def lista_tokens_assistente_criador(request, assistente_id):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        try:
            assistente = User.objects.get(id=assistente_id)
            tokens = Token.objects.filter(criador=assistente.username).order_by('nome_responsavel')
            logger.info(f"User {request.user.username} Acessou a lista de ultimos tokens criados por: {assistente.username}. {time.strftime('%Y-%m-%d %H:%M:%S')}")
            assistentes = get_assistentes()
            data_entregas = get_datas_entregas()
            data_solicitacoes = get_datas_solicitacoes()
            return render(request, 'lista_tokens.html', {
                'tokens': tokens,
                "usuario": request.user,
                "funcoes": funcoes,
                "data_entregas": data_entregas,
                "data_solicitacoes": data_solicitacoes,
                "assistentes": assistentes
            })
        except User.DoesNotExist:
            return HttpResponse("Assistente não encontrado.")

def lista_tokens_data_solicitacao(request, data_solicitacao):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        try:
            data_solicitacao_parsed = time.strptime(data_solicitacao, "%d-%m-%Y")
            data_solicitacao_formatada = time.strftime("%Y-%m-%d", data_solicitacao_parsed)
            tokens = Token.objects.filter(data_solicitacao=data_solicitacao_formatada).order_by('nome_responsavel')
            if not tokens:
                return HttpResponse("Nenhum token encontrado para esta data de solicitação.")
            logger.info(f"User {request.user.username} Acessou a lista de tokens com data de solicitação: {data_solicitacao_formatada}. {time.strftime('%Y-%m-%d %H:%M:%S')}")
            assistentes = get_assistentes()
            data_entregas = get_datas_entregas()
            data_solicitacoes = get_datas_solicitacoes()
            return render(request, 'lista_tokens.html', {
                'tokens': tokens,
                "usuario": request.user,
                "funcoes": funcoes,
                "data_entregas": data_entregas,
                "data_solicitacoes": data_solicitacoes,
                "assistentes": assistentes
            })
        except Exception as e:
            return HttpResponse(f"Erro ao filtrar tokens por data de solicitação: {str(e)}")

def lista_tokens_data_entrega(request, data_entrega):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        try:
            data_entrega_parsed = time.strptime(data_entrega, "%d-%m-%Y")
            data_entrega_formatada = time.strftime("%Y-%m-%d", data_entrega_parsed)
            tokens = Token.objects.filter(data_entrega=data_entrega_formatada).order_by('nome_responsavel')
            if not tokens:
                return HttpResponse("Nenhum token encontrado para esta data de entrega.")
            logger.info(f"User {request.user.username} Acessou a lista de tokens com data de entrega: {data_entrega_formatada}. {time.strftime('%Y-%m-%d %H:%M:%S')}")
            assistentes = get_assistentes()
            data_entregas = get_datas_entregas()
            data_solicitacoes = get_datas_solicitacoes()
            return render(request, 'lista_tokens.html', {
                'tokens': tokens,
                "usuario": request.user,
                "funcoes": funcoes,
                "data_entregas": data_entregas,
                "data_solicitacoes": data_solicitacoes,
                "assistentes": assistentes,
                "user_permissions": request.user.get_all_permissions(),
            })
        except Exception as e:
            return HttpResponse(f"Erro ao filtrar tokens por data de entrega: {str(e)}")

def lista_tokens_entregue(request, entregue):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if entregue == "True":
            tokens = Token.objects.filter(token_entregue=True).order_by('nome_responsavel')
        elif entregue == "False":
            tokens = Token.objects.filter(token_entregue=False).order_by('nome_responsavel')
        else:
            return HttpResponse("Valor inválido para 'entregue'. Use 'True' ou 'False'.")
        
        if not tokens:
            return HttpResponse("Nenhum token encontrado com o status de entrega especificado.")
        
        logger.info(f"User {request.user.username} Acessou a lista de tokens entregues: {entregue}. {time.strftime('%Y-%m-%d %H:%M:%S')}")
        assistentes = get_assistentes()
        data_entregas = get_datas_entregas()
        data_solicitacoes = get_datas_solicitacoes()
        return render(request, 'lista_tokens.html', {
            'tokens': tokens,
            "usuario": request.user,
            "funcoes": funcoes,
            "data_entregas": data_entregas,
            "data_solicitacoes": data_solicitacoes,
            "assistentes": assistentes,
            "user_permissions": request.user.get_all_permissions(),
        })

def novo_token(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        assistentes = get_assistentes()
        data_entregas = get_datas_entregas()
        data_solicitacoes = get_datas_solicitacoes()

        if request.method == 'POST':
            nome_responsavel = request.POST.get('nome_responsavel')
            cpf_responsavel = request.POST.get('cpf_responsavel')
            funcao_responsavel = request.POST.get('funcao_responsavel')
            serial = request.POST.get('serial')
            data_solicitacao = request.POST.get('data_solicitacao') or None
            data_entrega = request.POST.get('data_entrega') or None
            observacao = request.POST.get('observacao')
            # token_entregue = request.POST.get('token_entregue') == 'on'

            token = Token(
                nome_responsavel=nome_responsavel,
                cpf_responsavel=cpf_responsavel,
                funcao_responsavel=funcao_responsavel,
                serial=serial,
                data_solicitacao=data_solicitacao,
                data_entrega=data_entrega,
                observacao=observacao,
                token_entregue=((request.POST.get('token_entregue') == 'on') or (data_entrega is not None)),
                criador=request.user.username,
                modificador=request.user.username,
            )
            try:
                logger.info(f"User {request.user.username} tentou cadastrar um novo token: {nome_responsavel}, CPF: {cpf_responsavel}, Serial: {serial}. {time.strftime('%Y-%m-%d %H:%M:%S')}")
                if Token.objects.filter(nome_responsavel=nome_responsavel).exists():
                    return HttpResponse("Token já cadastrado com este nome.")
                if serial and Token.objects.filter(serial=serial).exists():
                    return HttpResponse("Token já cadastrado com este serial.")
                if cpf_responsavel and Token.objects.filter(cpf_responsavel=cpf_responsavel).exists():
                    return HttpResponse("Token já cadastrado com este CPF.")
                Token.objects.get(cpf_responsavel=cpf_responsavel)
                return HttpResponse("Token já cadastrado com este nome, CPF ou serial.")
            except Token.MultipleObjectsReturned:
                return HttpResponse("Erro: Múltiplos tokens encontrados com o mesmo nome, CPF ou serial. Verifique os dados.")
            
            except Token.DoesNotExist:
                logger.info(f"User {request.user.username} cadastrou um novo token: {nome_responsavel}, CPF: {cpf_responsavel}, Serial: {serial}. {time.strftime('%Y-%m-%d %H:%M:%S')}")
                token.save()
            return render(request, 'lista_tokens.html', {'tokens': Token.objects.all(), "sucesso": "Token cadastrado com sucesso!", "usuario": request.user, "funcoes": funcoes, "assistentes": assistentes, "data_entregas": data_entregas, "data_solicitacoes": data_solicitacoes, "user_permissions": request.user.get_all_permissions(),})
        logger.info(f"User {request.user.username} acessou a página de cadastro de novo token. {time.strftime('%Y-%m-%d %H:%M:%S')}")
        return render(request, 'novo_token.html', {"funcoes": funcoes, "usuario": request.user, "user_permissions": request.user.get_all_permissions(),})

def atualizar_token(request, token_id):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        token = Token.objects.get(id=token_id)
        try: 
            token.data_entrega = token.data_entrega.strftime("20%y-%m-%d")
            token.data_solicitacao = token.data_solicitacao.strftime("20%y-%m-%d")
        except:
            pass

        logger.info(f"User {request.user.username} acessou a página de atualização do token de: {token.nome_responsavel}. {time.strftime('%Y-%m-%d %H:%M:%S')}")

        if request.method == 'POST':
            token.nome_responsavel = request.POST.get('nome_responsavel')
            token.cpf_responsavel = request.POST.get('cpf_responsavel')
            token.funcao_responsavel = request.POST.get('funcao_responsavel')
            token.serial = request.POST.get('serial')
            if request.POST.get('data_solicitacao'):
                token.data_solicitacao = request.POST.get('data_solicitacao')
            else:
                token.data_solicitacao = None
            if request.POST.get('data_entrega'):
                token.data_entrega = request.POST.get('data_entrega')
            else:
                token.data_entrega = None
            token.observacao = request.POST.get('observacao')
            token.modificador = request.user.username
            token.token_entregue = (request.POST.get('token_entregue') == 'on')
            logger.info(f"User {request.user.username} atualizou o token: {token.nome_responsavel}, CPF: {token.cpf_responsavel}, Serial: {token.serial}. {time.strftime('%Y-%m-%d %H:%M:%S')}")
            token.save()

            assistentes = get_assistentes()
            data_entregas = get_datas_entregas()
            data_solicitacoes = get_datas_solicitacoes()
            return render(request, 'lista_tokens.html', {
                'tokens': Token.objects.all(),
                "sucesso": "Token atualizado com sucesso!",
                "usuario": request.user,
                "funcoes": funcoes,
                "assistentes": assistentes,
                "data_entregas": data_entregas,
                "data_solicitacoes": data_solicitacoes,
                "user_permissions": request.user.get_all_permissions(),
            })
        return render(request, 'token.html', {
            'token': token,
            "funcoes": funcoes,
            "usuario": request.user,
            "assistentes": get_assistentes(),
            "user_permissions": request.user.get_all_permissions(),
        })

def atualizar_lista(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        novos_tokens = atualiza_lista_tokens()
        for token in novos_tokens.values():
            try:
                has_token, created = Token.objects.update_or_create(
                    nome_responsavel=token['nome_responsavel'],
                    defaults={
                        'cpf_responsavel': token['cpf_responsavel'],
                        'funcao_responsavel': token['funcao_responsavel'],
                        'serial': token['serial'],
                        'data_solicitacao': token['data_solicitacao'],
                        'data_entrega': token['data_entrega'],
                        'observacao': token['observacao']
                    }
                )
                if created:
                    print(f"Token {has_token.nome_responsavel} criado com sucesso!")
                else:
                    print(f"Token {has_token.nome_responsavel} já existe. Atualizado!")
            except Token.MultipleObjectsReturned:
                print(f"Erro: Múltiplos tokens encontrados para {token['nome_responsavel']}. Verifique os dados.")
        return redirect('lista_tokens')

def admin(request):
    logger.info(f"User {request.user.username} acessou a área administrativa. {time.strftime('%Y-%m-%d %H:%M:%S')}")
    return redirect('/admin')

def login(request):
    logger.info(f"Usuário acessou a página de login. {time.strftime('%Y-%m-%d %H:%M:%S')}")
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            logger.info(f"Usuário {username} logou com sucesso. {time.strftime('%Y-%m-%d %H:%M:%S')}")
            return redirect('home')
        else:
            logger.warning(f"Tentativa de login falhou para o usuário {username}. {time.strftime('%Y-%m-%d %H:%M:%S')}")
            return render(request, 'login.html', {'error': 'Usuário ou senha inválidos.'})
    return render(request, 'login.html')

def logout(request):
    logger.info(f"Usuário {request.user.username} fez logout. {time.strftime('%Y-%m-%d %H:%M:%S')}")
    logout_django(request)
    return redirect('home')

def exportar_planilha(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="tokens.xlsx"'

        workbook = xl.Workbook()
        sheet = workbook.active
        sheet.title = 'Tokens'

        headers = ['Nome', 'CPF', 'Função', 'Serial', 'Entregue', 'Data de Solicitação', 'Data de Entrega', 'Observação', 'Criador por', 'Ultima Modificação por']
        sheet.append(headers)

        for token in Token.objects.all().order_by('nome_responsavel'):
            row = [
                token.nome_responsavel,
                token.cpf_responsavel,
                token.funcao_responsavel,
                token.serial,
                'Sim' if token.token_entregue else 'Não',
                token.data_solicitacao.strftime('%d/%m/%Y') if token.data_solicitacao else '',
                token.data_entrega.strftime('%d/%m/%Y') if token.data_entrega else '',
                token.observacao,
                token.criador,
                token.modificador
            ]
            sheet.append(row)

        workbook.save(response)
        logger.info(f"Usuário {request.user.username} exportou a lista de tokens para uma planilha Excel. {time.strftime('%Y-%m-%d %H:%M:%S')}")

        return response