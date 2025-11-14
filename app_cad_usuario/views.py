from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .models import Usuario, Estoque, Projeto, Historico
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

def home(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['login']  
        senha = request.POST['senha']

        
        if User.objects.filter(username=email).exists():
            return render(request, 'usuario/home.html', {'error': 'Email já está em uso.'})

        
        usuario = User.objects.create_user(username=email, password=senha, first_name=nome)
        usuario.save()
        return redirect('login')  

    return render(request, 'usuario/home.html')

def usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('login')
        senha = request.POST.get('senha')

        
        user = User.objects.create_user(username=email, email=email, password=senha)
        user.first_name = nome
        user.save()

        
        return redirect('pagina_inicial')

def cadastrar_usuario(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['senha']

        
        if User.objects.filter(username=email).exists():
            return render(request, 'usuario/cadastrar_usuario.html', {'error': 'Email já está em uso.'})

        
        usuario = User.objects.create_user(username=email, password=senha, first_name=nome)
        usuario.save()
        return redirect('login') 

    return render(request, 'usuario/cadastrar_usuario.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['login']
        senha = request.POST['senha']

        
        user = authenticate(request, username=email, password=senha)

        if user is not None:
            login(request, user) 
            return redirect('pagina_inicial')  
        else:
            return render(request, 'usuario/login.html', {'error': 'Login ou senha inválidos.'})

    return render(request, 'usuario/login.html')

def listagem_usuario(request):
    
    usuarios = User.objects.all()

    
    return render(request, 'usuario/usuario.html', {'usuarios': usuarios})

def excluir_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    usuario.delete()  
    return redirect('usuario')  
    
def alterar_email(request):
    if request.method == 'POST':
        novo_email = request.POST.get('email')
        if novo_email: 
            request.user.email = novo_email
            request.user.save() 
            return redirect('pagina_inicial')  
    return render(request, 'usuario/alterar_email.html')

def alterar_senha(request):
    if request.method == 'POST':
        nova_senha = request.POST.get('senha')
        if nova_senha:  
            request.user.set_password(nova_senha)
            request.user.save()  
            update_session_auth_hash(request, request.user) 
            return redirect('pagina_inicial') 
    return render(request, 'usuario/alterar_senha.html')

def logout_view(request):
    logout(request)
    return redirect('login')  

@login_required
def projetos(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        material_id = request.POST['material']
        quantidade = int(request.POST['quantidade'])
        metros_por_unidade = float(request.POST['metros_por_unidade'])

        
        material = Estoque.objects.get(id=material_id, user=request.user)

        
        if material.quantidade_metros < quantidade * metros_por_unidade:
            projetos = Projeto.objects.filter(user=request.user)
            materiais = Estoque.objects.filter(user=request.user)
            return render(request, 'usuario/projetos.html', {
                'projetos': projetos,
                'materiais': materiais,
                'error': 'Quantidade insuficiente no estoque para este projeto.'
            })

        
        Projeto.objects.create(
            user=request.user,
            nome=nome,
            material=material,
            cor=material.cor,
            quantidade=quantidade,
            metros_por_unidade=metros_por_unidade
        )

        
        material.quantidade_metros -= quantidade * metros_por_unidade
        material.save()

        
        if material.quantidade_metros <= 50:
            request.session['estoque_baixo'] = f"O material '{material.material}' ({material.cor}) está com estoque baixo: {material.quantidade_metros} metros."

        return redirect('projetos')

    
    projetos = Projeto.objects.filter(user=request.user)
    materiais = Estoque.objects.filter(user=request.user)
    alerta_estoque = request.session.pop('estoque_baixo', None)  
    return render(request, 'usuario/projetos.html', {
        'projetos': projetos,
        'materiais': materiais,
        'alerta_estoque': alerta_estoque
    })

@login_required
def concluir_projeto(request, id):
    projeto = get_object_or_404(Projeto, id=id, user=request.user)

    print(f"Concluindo projeto: {projeto.nome}")  

    Historico.objects.create(
        user=request.user,
        tabela="Projeto",
        acao="concluido",
        descricao=f"O projeto '{projeto.nome}' foi concluído."
    )

    projeto.delete()

    return redirect('projetos')

def concluir_projeto_remover(request, id):
    projeto = get_object_or_404(Projeto, id=id)

    Historico.objects.create(
        tabela='Projeto',
        acao='concluido',
        descricao=f"Projeto '{projeto.nome}' foi concluído.",
        data_hora=now()
    )

    projeto.concluido = True
    projeto.save()

    return redirect('projetos') 
    return redirect('projetos') 

from django.core.paginator import Paginator  

def historico(request):
    registros = Historico.objects.filter(user=request.user).order_by('-data_hora')  
    paginator = Paginator(registros, 10)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  
    return render(request, 'usuario/historico.html', {'page_obj': page_obj})
    return render(request, 'usuario/historico.html', {'registros': registros})

@login_required
def estoque(request):
    if request.method == 'POST':
        
        material = request.POST.get('material')
        cor = request.POST.get('cor')
        quantidade_metros = request.POST.get('quantidade')

        
        Estoque.objects.create(
            user=request.user,  
            material=material,
            cor=cor,
            quantidade_metros=quantidade_metros
        )
        return redirect('estoque')  

   
    itens = Estoque.objects.filter(user=request.user)
    return render(request, 'usuario/estoque.html', {'itens': itens})

def editar_projeto(request):
    return render(request, 'usuario/editar_projeto.html')

def excluir_item(request, id):
    item = get_object_or_404(Estoque, id=id)
    Historico.objects.create(
        tabela='Estoque',
        acao='excluido',
        descricao=f"Item '{item.material}' excluído do estoque.",
    )
    item.delete()
    return redirect('estoque')

def editar_item(request):
    if request.method == 'POST':
        item = get_object_or_404(Estoque, id=request.POST.get('id'))
        item.material = request.POST.get('material')
        item.cor = request.POST.get('cor')
        item.quantidade_metros = request.POST.get('quantidade')  
        item.save()  
    return redirect('estoque')

@login_required
def adicionar_projeto(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        material_id = request.POST['material']  
        cor = request.POST['cor']
        quantidade = int(request.POST['quantidade'])
        metros_por_unidade = float(request.POST['metros_por_unidade'])

        
        material = get_object_or_404(Estoque, id=material_id, user=request.user)

        
        if material.quantidade_metros < quantidade * metros_por_unidade:
            return render(request, 'usuario/adicionar_projeto.html', {
                'materiais': Estoque.objects.filter(user=request.user),
                'error': 'Quantidade insuficiente no estoque para este projeto.'
            })

        
        Projeto.objects.create(
            user=request.user, 
            nome=nome,
            material=material,
            cor=cor,
            quantidade=quantidade,
            metros_por_unidade=metros_por_unidade
        )

        
        material.quantidade_metros -= quantidade * metros_por_unidade
        material.save()

        return redirect('projetos')

    
    materiais = Estoque.objects.filter(user=request.user)
    return render(request, 'usuario/adicionar_projeto.html', {'materiais': materiais})

@login_required
def alterar_nome(request):
    if request.method == 'POST':
        novo_nome = request.POST.get('novo_nome')
        if novo_nome:
           
            usuario = request.user
            usuario.first_name = novo_nome
            usuario.save()
            return redirect('pagina_inicial')  
    return render(request, 'usuario/alterar_nome.html') 

@login_required
def excluir_projeto(request, id):
   
    projeto = get_object_or_404(Projeto, id=id, user=request.user)

    
    material = projeto.material  
    material.quantidade_metros += projeto.quantidade * projeto.metros_por_unidade
    material.save()

    
    projeto.delete()

    return redirect('projetos') 

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from app_cad_usuario.models import Projeto, Estoque, Historico

@login_required
def pagina_inicial(request):
    projetos_ativos = Projeto.objects.filter(user=request.user).count()
    itens_estoque = Estoque.objects.filter(user=request.user).count()
    registros_total = Historico.objects.filter(user=request.user).count()

    return render(request, 'usuario/pagina_inicial.html', {
        'projetos_ativos': projetos_ativos,
        'itens_estoque': itens_estoque,
        'registros_total': registros_total,
    })

