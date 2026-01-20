import sqlite3
from datetime import date,timedelta
import warnings
warnings.filterwarnings('ignore', 
    message='The default date adapter is deprecated') #IGNORA A MENSAGEM DE AVISO SOBRE A BIBLIOTECA QUE SERÁ REMOVIDA!

caminho = "C:/Users/André Vítor/Downloads/dbExercicio.db"
try:
    conn = sqlite3.connect(caminho)
except:
    print("Erro ao conectar!")

cursor = conn.cursor()
livros_cadastrados = {}
usuarios_cadastrados = {}

def table_usuario(conn):
    conn.execute ('''
                  create table usuario (
                  id_usuario integer primary key autoincrement,
                  nome varchar(40) not null,
                  email varchar(60) not null,
                  telefone varchar(30) not null,
                  status integer not null
                  );
    ''')
    conn.commit()

def table_livros(conn):
    conn.execute ('''
                create table livro (
                  id_livro integer primary key autoincrement,
                  titulo varchar(40) not null,
                  autor varchar(20) not null,
                  categoria varchar(20) not null,
                  ano_publicacao date not null,
                  quantidade_total integer not null,
                  quantidade_disponivel integer not null
                  );
                  ''')
    conn.commit()

def table_emprestimos(conn):
    conn.execute('''
                create table emprestimos(
                 id_emprestimo integer primary key autoincrement,
                 id_livro integer not null,
                 id_usuario integer not null,
                 data_emprestimo date not null,
                 data_devolucao_prevista date not null,
                 data_devolucao_real date,
                 status varchar(10) not null
                 );
                 ''')
    conn.commit()

def gerenciar_livros():
    print('''
          1 - Cadastrar novo livro
          2 - Atualizar dados de um livro
          3 - Consultar livro por ID
          4 - Consultar livros por título
          5 - Listar todos os livros
          6 - Listar livros disponíveis
          7 - Excluir livro
          0 - Voltar ao menu principal
          ''')
    op = int(input("Digite uma opção: "))
    match op:
        case 0:
            main()
        case 1:
            cadastrar_livro(conn)
        case 2:
            atualizar_dados(conn,cursor)
        case 3: 
            consultar_id(cursor)
        case 4:
            consultar_titulo(cursor)
        case 5: 
            listar_todos(cursor)
        case 6:
            listar_disponiveis(cursor)
        case 7:
            excluir_livro(conn,cursor)
        case _:
            print("Opção Inválida!")
            gerenciar_livros()

def cadastrar_livro(conn):
    titulo = input("Digite o título do livro: ")
    autor = input("Digite o autor do livro: ")
    categoria = input("Digite a categoria do livro: ")
    ano_publicacao = input("Digite o ano de publicação(yyyy-mm-dd): ")
    quantidade_total = int(input("Digite a quantidade de livros adquiridos: "))
    quantidade_dis = int(input("Digite a quantidade de livros disponíveis: "))
    while quantidade_dis>quantidade_total:
        quantidade_dis = int(input("Digite a quantidade de livros disponíveis: "))
    livros_cadastrados[titulo] = {"autor":autor,"categoria":categoria,"ano":ano_publicacao,"quantidade_total":quantidade_total,"quantidade_dis":quantidade_dis}
    conn.execute("insert into livro values(?,?,?,?,?,?,?)",
                 (None,titulo,livros_cadastrados[titulo]["autor"],livros_cadastrados[titulo]["categoria"],livros_cadastrados[titulo]["ano"],livros_cadastrados[titulo]["quantidade_total"],livros_cadastrados[titulo]["quantidade_dis"])
                 )
    conn.commit()
    print("Livro cadastrado com sucesso!")

def atualizar_dados(conn,cursor):
    livro = input("Digite o nome do livro que dejesa alterar: ")
    cursor.execute("select * from livro where titulo = ?",(livro,))
    resultado = cursor.fetchone()
    #O SELECT RETORNA UMA LISTA COM OS VALORES, PODENDO SER ACESSADO POR ÍNDICE. resultado[3]
    if resultado:
        print("Livro encontrado!")
        print(f"Aqui está o resultado: {resultado}")
    else:
        print("Livro NÃO encontrado!")
        return None
    print('''
          1. Título
          2. Autor
          3. Categoria
          4. Ano de Publicação
          5. Quantidade Total
          6. Quantidade Disponível
          7. Sair
          ''')
    op = int(input("O que deseja alterar: "))
    match op:
        case 1:
            alterar = input("Digite o novo título: ")
            conn.execute('''
                         update livro
                         set titulo = ?
                         where titulo = ?;
                         ''', (alterar,livro))
            conn.commit()
            print("Título alterado com sucesso!")
        case 2:
            alterar = input("Digite o novo autor: ")
            conn.execute('''
                         update livro
                         set autor = ?
                         where titulo = ?; 
                         ''', (alterar,livro))
            conn.commit()
            print("Autor alterado com sucesso!")
        case 3:
            alterar = input("Digite a nova categoria: ")
            conn.execute('''
                         update livro
                         set categoria = ?
                         where titulo = ?; 
                         ''', (alterar,livro))
            conn.commit()
            print("Categoria alterado com sucesso!")
        case 4: 
            alterar = input("Digite a nova data de ppublicação(yyyy-mm-dd): ")
            conn.execute('''
                         update livro
                         set ano_publicacao = ?
                         where titulo = ?; 
                         ''', (alterar,livro))
            conn.commit()
            print("Ano de Publicação alterado com sucesso!")
        case 5:
            alterar = int(input("Digite a nova quantidade total: "))
            conn.execute('''
                         update livro
                         set quantidade_total = ?
                         where titulo = ?; 
                         ''', (alterar,livro))
            conn.commit()
            print("Quantidade Total alterada com sucesso!")
        case 6:
            alterar = int(input("Digite a nova quantidade disponível: "))
            while alterar > resultado[5]:
                print("Quantidade disponível deve ser menor que a Quantidade total!")
                alterar = int(input("Digite a nova quantidade disponível: "))
            conn.execute('''
                         update livro
                         set quantidade_disponivel = ?
                         where titulo = ?; 
                         ''', (alterar,livro))
            conn.commit()
            quant_total = resultado[5]
            conta = quant_total - alterar
            conn.execute('''
                         update livro
                         set quantidade_total = ?
                         where titulo = ?
                         ''',(conta,livro))
            print("Quantidade Disponível alterada com sucesso!")
            conn.commit()
        case 7:
            gerenciar_livros()
        case _:
            print("Opção Inválida!")
            gerenciar_livros()

def consultar_id(cursor):
    id = int(input("Digite o ID do livro que deseja buscar: "))
    cursor.execute("select * from livro where id_livro = ?", (id,))
    resultado = cursor.fetchone()
    if resultado:
        print("Livro encontrado!")
        print(f'''
              Aqui está o resultado:
              ID do livro = {resultado[0]}
              Titulo = {resultado[1]}
              Autor = {resultado[2]}
              Categoria = {resultado[3]}
              Ano de Publicação = {resultado[4]}
              Quantidade Total = {resultado[5]}
              Quantidade Disponível = {resultado[6]}
              ''')
        gerenciar_livros()
    else:
        print("Livro NÃO encontrado!")

def consultar_titulo(cursor):
    titulo = input("Digite o título do livro que deseja buscar: ")
    cursor.execute("select * from livro where titulo = ?", (titulo,))
    resultado = cursor.fetchone()
    if resultado:
        print("Livro encontrado!")
        print(f'''
              Aqui está o resultado:
              ID do livro = {resultado[0]}
              Titulo = {resultado[1]}
              Autor = {resultado[2]}
              Categoria = {resultado[3]}
              Ano de Publicação = {resultado[4]}
              Quantidade Total = {resultado[5]}
              Quantidade Disponível = {resultado[6]}
              ''')
        gerenciar_livros()
    else:
        print("Livro NÃO encontrado!")
    
def listar_todos(cursor):
    cursor.execute("select * from livro")
    resultado = cursor.fetchall()
    if resultado:
        for id,titulo,autor,categoria,publi,total,dis in resultado:
            print(f'''
              ID do livro = {id}
              Titulo = {titulo}
              Autor = {autor}
              Categoria = {categoria}
              Ano de Publicação = {publi}
              Quantidade Total = {total}
              Quantidade Disponível = {dis}
              ''')
    else:
        print("Livro NÃO encontrado!")
            
def listar_disponiveis(cursor):
    cursor.execute("select * from livro where quantidade_disponivel > 0")
    resultado = cursor.fetchall()
    if resultado:
        for id,titulo,autor,categoria,publi,total,dis in resultado:
            print(f'''
              ID do livro = {id}
              Titulo = {titulo}
              Autor = {autor}
              Categoria = {categoria}
              Ano de Publicação = {publi}
              Quantidade Total = {total}
              Quantidade Disponível = {dis}
              ''')
    else:
        print("Livro NÃO encontrado!")

def excluir_livro(conn,cursor):
    id = int(input("Digite o ID do livro que deseja excluir: "))
    cursor.execute("select * from livro where id_livro = ?",(id,))
    resultado = cursor.fetchone()
    if resultado:
        print(f'''
              ID do livro = {resultado[0]}
              Titulo = {resultado[1]}
              Autor = {resultado[2]}
              Categoria = {resultado[3]}
              Ano de Publicação = {resultado[4]}
              Quantidade Total = {resultado[5]}
              Quantidade Disponível = {resultado[6]}
              ''')
        op = input("Deseja exlcuir este livro (sim ou não): ").lower()
        if op == "sim":
            conn.execute("delete from livro where id_livro = ?",(id,))
            print("Livro excluído com sucesso!")
            conn.commit()
        else:
            gerenciar_livros()
    else:
        print("Livro NÃO encontrado!")
            
def gerenciar_usuarios():
    print('''
          1 - Cadastrar novo usuário
          2 - Atualizar dados do usuário
          3 - Consultar usuário por ID
          4 - Consultar usuário por nome
          5 - Listar usuários ativos
          6 - Listar todos os usuários
          0 - Voltar ao menu principal
          ''')
    op = int(input("Digite a opção desejada: "))
    match op:
        case 0:
            main()
        case 1:
            cadastrar_usuario(conn,cursor)
        case 2:
            atualizar_dadosusuario(conn,cursor)
        case 3:
            consultar_idusuario(cursor)
        case 4:
            consultar_nome(cursor)
        case 5: 
            listar_usuariosativos(cursor)
        case 6:
            listar_todosusuarios(cursor)
        case _:
            print("Opção Inválida!")
            gerenciar_usuarios()

def cadastrar_usuario(conn,cursor):
    nome = input("Digite o nome do usuário: ")
    email = input("Digite o email do usuário: ")
    while "@" not in email:
        email = input("Digite o email do usuário: ")
    telefone = input("Digite o telefone do usuário(ddd+9 dígitos): ")
    while len(telefone) != 11:
        telefone = input("Digite o telefone do usuário(ddd+9 dígitos): ")
    cursor.execute("select * from usuario where telefone = ?",(telefone,))
    resultado = cursor.fetchone()
    if resultado is not None:
        if telefone in resultado:
            print("Telefone já cadastrado!")
            gerenciar_usuarios()
    else:
        pass
    usuarios_cadastrados[nome] = {"email":email,"telefone":telefone}
    conn.execute('''
                  insert into usuario values (?,?,?,?,?)
                 ''',(None,nome,usuarios_cadastrados[nome]["email"],usuarios_cadastrados[nome]["telefone"],1))
    print("Usuário cadastrado com sucesso!")
    conn.commit()

def atualizar_dadosusuario(conn,cursor):
    id = input("Digite o ID do perfil que deseja alterar: ")
    cursor.execute("select * from usuario where id_usuario = ?",(id,))
    resultado = cursor.fetchone()
    if resultado:
        print(f'''
              ID do Usuário = {resultado[0]}
              Nome = {resultado[1]} 
              Email = {resultado[2]}
              Telefone = {resultado[3]}
              Status = {resultado[4]}
              ''')
    else:
        print("Usuário NÃO encontrado!")
        return None
    print('''
              1. Nome
              2. Email
              3. Telefone
              4. Status
              5. Sair
              ''')
    op = int(input("O que deseja alterar: "))
    match op:
        case 1:
            alterar = input("Digite o novo nome: ") 
            conn.execute('''
                         update usuario
                         set nome = ?
                         where id_usuario = ?
                         ''',(alterar,id))   
            conn.commit()  
        case 2:
            alterar = input("Digite o novo email: ")
            while "@" not in alterar:
                alterar = input("Digite o novo email: ")
            conn.execute('''
                         update usuario
                         set email = ?
                         where id_usuario = ?
                         ''',(alterar,id))
            conn.commit()
        case 3:
            alterar = input("Digite o novo telefone: ")
            while len(alterar) != 11:
                alterar = input("Digite o novo telefone: ")
            conn.execute('''
                         update usuario
                         set telefone = ?
                         where id_usuario = ?
                         ''',(alterar,id))
            conn.commit()
        case 4:
            print(f"Status Atual = {resultado[4]}")
            if resultado[4] == 0:
                alterar = input("Deseja ATIVAR conta (sim ou não): ").lower()
                if alterar == "sim":
                    conn.execute('''
                                 update usuario
                                 set status = 1
                                 where id_usuario = ?
                                 ''',(id,))
                    conn.commit()
                    print("Conta ATIVADA!")
                    gerenciar_usuarios()
                else:
                    print("Status NÃO alterado!")
            elif resultado[4] == 1:
                alterar = input("Deseja DESATIVAR conta (sim ou não): ").lower()
                if alterar == "sim":
                    conn.execute('''
                                 update usuario
                                 set status = 0
                                 where id_usuario = ?
                                 ''',(id,))
                    conn.commit()
                    print("Conta DESATIVADA!")
                    gerenciar_usuarios()
                else:
                    print("Status NÃO alterado!")
        case 5:
            gerenciar_usuarios()
        case _:
            print("Opção Inválida!")
            gerenciar_usuarios()

def consultar_idusuario(cursor):
    id = int(input("Digite o ID que deseja buscar: "))
    cursor.execute("select * from usuario where id_usuario = ?",(id,))
    resultado = cursor.fetchone()
    if resultado:
        print("Usuário encontrado!")
        print(f'''
              ID do Usuário = {resultado[0]}
              Nome = {resultado[1]}
              Email = {resultado[2]}
              Telefone = {resultado[3]}
              Status da Conta = {resultado[4]}
              ''')
        gerenciar_usuarios()
    else:
        print("Usuário não encontrado!")
        gerenciar_usuarios()

def consultar_nome(cursor):
    nome = input("Digite o nome que deve buscar: ")
    cursor.execute("select * from usuario where nome = ?",(nome,))
    resultado = cursor.fetchone()
    if resultado:
        print("Usuário encontrado!")
        print(f'''
              ID do Usuário = {resultado[0]}
              Nome = {resultado[1]}
              Email = {resultado[2]}
              Telefone = {resultado[3]}
              Status da Conta = {resultado[4]}
              ''')
        gerenciar_usuarios()
    else:
        print("Usuário não encontrado!")
        gerenciar_usuarios()

def listar_usuariosativos(cursor):
    cursor.execute("select * from usuario where status = 1")
    resultado = cursor.fetchall()
    for id,nome,email,telefone,status in resultado:
        print(f'''
              ID do Usuário = {id}
              Nome = {nome}
              Email = {email}
              Telefone = {telefone}
              Status da Conta = {status}
              ''')
    if resultado is None:
        print("Nenhuma usuário registrado!")

def listar_todosusuarios(cursor):
    cursor.execute("select * from usuario")
    resultado = cursor.fetchall()
    for id,nome,email,telefone,status in resultado:
        print(f'''
              ID do Usuário = {id}
              Nome = {nome}
              Email = {email}
              Telefone = {telefone}
              Status da Conta = {status}
              ''')
    if resultado is None:
        print("Nenhuma usuário registrado!")

def gerenciar_emprestimos():
    print('''
        1 - Realizar novo empréstimo
        2 - Registrar devolução
        3 - Consultar empréstimo por ID
        4 - Listar empréstimos em aberto
        5 - Listar empréstimos atrasados
        6 - Histórico de empréstimos por usuário
        0 - Voltar ao menu principal
          ''')
    op = int(input("Digite a opção desejada: "))
    match op:
        case 0:
            main()
        case 1:
            realizar_emprestimo(cursor,conn)
        case 2:
            realizar_devolucao(cursor,conn)
        case 3:
            consultar_idemprestimo(cursor)
        case 4:
            emp_abertos(cursor)
        case 5:
            emp_atrasados(cursor)
        case 6:
            historico_emprestimo(cursor)
        case _:
            print("Opção Inválida!")

def realizar_emprestimo(cursor,conn):
    idusuario = int(input("Digite o ID do usuário: "))
    cursor.execute("select * from usuario where id_usuario = ? and status = 1",(idusuario,))
    resultadoid = cursor.fetchone()
    if resultadoid:
        print("Usuário encontrado!")
    else:
        print("Usuário NÃO encontrado ou INDISPONÍVEL!")
        gerenciar_emprestimos()
    cursor.execute("select * from emprestimos where id_usuario = ?",(idusuario,))
    resultadoo = cursor.fetchone()
    if resultadoo:
        if resultadoo[6] == "Atrasado":
            print('''
                Usuiário possui PENDÊNCIAS,
                NÃO será possível realizar novo empréstimo!
                ''')
            gerenciar_emprestimos()
    else:
        pass
    idlivro = int(input("Digite o ID do livro: "))
    cursor.execute("select * from livro where id_livro = ? and quantidade_disponivel > 0",(idlivro,))
    resultado_idlivro = cursor.fetchone()
    if resultado_idlivro:
        print("Livro encontrado!")
    else:
        print("Livro NÃO encontrado ou SEM ESTOQUE!")
        gerenciar_emprestimos()
    data_emprestimo = date.today()
    data_devolucao = data_emprestimo + timedelta(days=7) #ADICIONA 7 DIAS A PARTIR DE HOJE
    usuarios_cadastrados[idusuario] = {"idlivro":idlivro,"emprestimo":data_emprestimo,"devolucao":data_devolucao}
    conn.execute('''
                 insert into emprestimos values(?,?,?,?,?,?,?)
                 ''',(None,usuarios_cadastrados[idusuario]["idlivro"],idusuario,usuarios_cadastrados[idusuario]["emprestimo"],usuarios_cadastrados[idusuario]["devolucao"],None,"Aberto"))
    conn.commit()
    quant_disponivel = resultado_idlivro[6]
    quant_atual = quant_disponivel - 1
    conn.execute('''
                 update livro 
                 set quantidade_disponivel = ?
                 where id_livro = ?
                 ''',(quant_atual,idlivro))
    conn.commit()
    print("Emprestimo realizado com sucesso!")

def realizar_devolucao(cursor,conn):
    print('''
          Busca para devolução:
          1. ID de Empréstimo
          2. ID do Usuário
          ''')
    op = int(input("Digite a opção desejada:"))
    match op:
        case 1:
            id = int(input("Digite o PROTOCOLO/ID de empréstimo: "))
            cursor.execute("select * from emprestimos where id_emprestimo = ?",(id,))
            resultado = cursor.fetchone()
            if resultado:
                print("Empréstimo encontrado!")
            else:
                print("Empréstimo NÃO encontrado!")
                gerenciar_emprestimos()
            data_devolucao = input("Digite a data de devolução (yyyy/mm/dd): ")
            livro = resultado[1]
            # dataformat = date.frimisoformat(data_devolucao)
            conn.execute('''
                         update emprestimos
                         set data_devolucao_real = ?
                         where id_emprestimo = ?
                         ''',(data_devolucao,id))
            conn.execute('''
                         update emprestimos
                         set status = "Devolvido"
                         where id_emprestimo = ?
                         ''',(id,))
            conn.execute('''
                         update livro
                         set quantidade_disponivel = quantidade_disponivel + 1
                         where id_livro = ?
                         ''',(livro,))
            conn.commit()
            print("Devolução realizada com sucesso!")
        case 2:
            id = int(input("Digite o ID do Usuário: "))
            cursor.execute("select * from emprestimos where id_usuario = ? and status = 'Aberto'",(id,))
            resultado = cursor.fetchone()
            if resultado:
                print("Empréstimo encontrado!")
            else:
                print("NENHUM empréstimo encontrado com esse ID!")
                gerenciar_emprestimos()
            data_devolucao = input("Digite a data de devolução (yyyy/mm/dd): ")
            id = resultado[1]
            conn.execute('''
                         update emprestimos
                         set data_devolucao_real = ?
                         where id_emprestimo = ?
                         ''',(data_devolucao,id))
            conn.execute('''
                         update emprestimos
                         set status = "Devolvido"
                         where id_emprestimo = ?
                         ''',(id,))
            conn.execute('''
                         update livro
                         set quantidade_disponivel = quantidade_disponivel + 1
                         where id_livro = ?
                         ''',(livro,))
            conn.commit()
        case _:
            print("Opção Inválida!")
            gerenciar_emprestimos()

def consultar_idemprestimo(cursor): #✅
    id = int(input("Digite o ID do empréstimo que deseja buscar: "))
    cursor.execute('''
                   select emprestimos.id_livro,emprestimos.id_usuario,livro.titulo,usuario.nome,emprestimos.data_emprestimo,emprestimos.data_devolucao_prevista,emprestimos.status
                   from emprestimos
                   inner join usuario on usuario.id_usuario = emprestimos.id_usuario
                   inner join livro on livro.id_livro = emprestimos.id_livro
                   where emprestimos.id_emprestimo = ?
                   ''',(id,))
    resultado = cursor.fetchone()
    if resultado:
        print("Empréstimo encontrado!")
    else:
        print("Emprétimo NÃO encontrado!")
        gerenciar_emprestimos()
    print(f'''
          ID do Empréstimo = {id}
          Livro = {resultado[2]}
          Usuário = {resultado[3]}
          Data de Empréstimo = {resultado[4]}
          Data de Devolução Prevista = {resultado[5]}
          Status = {resultado[6]}
          ''')
    gerenciar_emprestimos()

def emp_abertos(cursor): #✅
    cursor.execute('''
                   select emprestimos.id_emprestimo,emprestimos.id_livro,emprestimos.id_usuario,livro.titulo,usuario.nome,emprestimos.data_emprestimo,emprestimos.data_devolucao_prevista,emprestimos.status
                   from emprestimos
                   inner join usuario on usuario.id_usuario = emprestimos.id_usuario
                   inner join livro on livro.id_livro = emprestimos.id_livro
                   where emprestimos.status = 'Aberto'
                   ''')
    resultado = cursor.fetchall()
    if resultado:
        print("Empréstimo encontrado!")
    else:
        print("Emprétimo NÃO encontrado!")
        gerenciar_emprestimos()
    for id1,id2,id3,title,user,emprestimo,prevista,status in resultado:
        print(f'''
          ID do Empréstimo = {id1}
          Livro = {title}
          Usuário = {user}
          Data de Empréstimo = {emprestimo}
          Data de Devolução Prevista = {prevista}
          Status = {status}
          ''')
    gerenciar_emprestimos()

def emp_atrasados(cursor): #✅
    cursor.execute('''
                   select emprestimos.id_emprestimo,emprestimos.id_livro,emprestimos.id_usuario,livro.titulo,usuario.nome,emprestimos.data_emprestimo,emprestimos.data_devolucao_prevista,emprestimos.status
                   from emprestimos
                   inner join livro on livro.id_livro = emprestimos.id_livro
                   inner join usuario on usuario.id_usuario = emprestimos.id_usuario
                   where emprestimos.status = 'Atrasado'
                   ''')
    resultado = cursor.fetchall()
    if resultado:
        print("Empréstimo encontrado!")
    else:
        print("Emprétimo atrasado NÃO encontrado!")
        gerenciar_emprestimos()
    for id1,id2,id3,title,nome,emprestimo,prevista,status in resultado:
        print(f'''
          ID do Empréstimo = {id1}
          Livro = {title}
          Usuário = {nome}
          Data de Empréstimo = {emprestimo}
          Data de Devolução Prevista = {prevista}
          Status = {status}
          ''')

def historico_emprestimo(cursor): #✅
    id = int(input("Digite o ID de usuário desejado: "))
    cursor.execute('''
                   select emprestimos.id_emprestimo,emprestimos.id_livro,emprestimos.id_usuario,livro.titulo,usuario.nome,emprestimos.data_emprestimo,emprestimos.data_devolucao_prevista,emprestimos.status
                   from emprestimos
                   inner join livro on livro.id_livro = emprestimos.id_livro
                   inner join usuario on usuario.id_usuario = emprestimos.id_usuario
                   where emprestimos.id_usuario = ?
                   ''',(id,))
    resultado = cursor.fetchall()
    if resultado:
        print(f"{len(resultado)} resultado(s) encontrado(s)!")
    else:
        print("Emprétimo NÃO encontrado!")
        gerenciar_emprestimos()
    for id1,id2,id3,title,nome,emprestimo,prevista,status in resultado:
        print(f'''
          ID do Empréstimo = {id1}
          Livro = {title}
          Usuário = {nome}
          Data de Empréstimo = {emprestimo}
          Data de Devolução Prevista = {prevista}
          Status = {status}
          ''')

def atualizar_status(cursor,conn):
    atual = date.today()
    cursor.execute("select * from emprestimos where status = 'Aberto'")
    resultado = cursor.fetchall()
    if resultado:
        for id, livro, usuario, emprestimo, prevista, real, status in resultado:
            emprestado = date.fromisoformat(emprestimo) 
            diferenca = (atual - emprestado).days
            if diferenca > 7:
                print("Warning: Atualize o Sistema!")
                conn.execute('''
                             update emprestimos
                             set status = 'Atrasado'
                             where id_emprestimo = ?
                             ''',(id,))
                conn.commit()
            else:
                pass
    else:
        pass

def consultas():
    print('''
          1 - Listar livros por categoria
          2 - Listar livros mais emprestados
          3 - Contar livros indisponíveis
          4 - Contar usuários cadastrados
          5 - Relatório geral de empréstimos
          0 - Voltar ao menu principal
          ''')
    op = int(input("Digite a opção desejada: "))
    match op:
        case 0:
            main()
        case 1:
            listar_categoria(cursor)
        case 2:
            listar_maisemprestados(cursor)
        case 3:
            count_indisponiveis(cursor)
        case 4:
            count_usuarios(cursor)
        case 5:
            relat(cursor)
        case _:
            print("Opção Inválida!")

def listar_categoria(cursor):
    cursor.execute('''
                   select distinct categoria
                   from livro
                   ''') #DISTINCT TIRA LINHAS DUPLICADAS
    resultado = cursor.fetchall()
    if resultado:
        print("""
              Categorias encontradas!
              CATEGORIAS:""")
        for x, in resultado:
            print(x)
    else:
        print("NENHUMA categoria encontrada!")
        consultas()
    op = input("Digite a opção desejada: ")
    cursor.execute("select * from livro where categoria = ?",(op,))
    livro = cursor.fetchall()
    if not livro:
        print("Categoria não encontrada!")
        return
    for id,titulo,autor,categoria,publicacao,total,disponivel in livro:
        print(f'''
                ID do Livro = {id}
                Titulo = {titulo}
                Autor = {autor}
                Categoria = {categoria}
                Ano de publicação = {publicacao}
                Quantidade Total = {total}
                Quantidade Disponivel = {disponivel}
                ''')

def listar_maisemprestados(cursor):
    # cursor.execute('''
    #                select id_livro, count(*) 
    #                from emprestimos
    #                group by id_livro
    #                order by count(*) desc
    #                limit 3
    #                ''') 
    #SELECIONA A COLUNA id_livro E CONTA, AGRUPA TODAS AS LINHAS QUE O ID SE REPETE, ORDENA A CONTAGEM EM DESC (MAIOR PRO MENOR) E LIMITA ATÉ 3
    cursor.execute('''
                   select count(emprestimos.id_livro),emprestimos.id_livro,livro.titulo,livro.autor,livro.categoria,livro.ano_publicacao
                   from emprestimos
                   inner join livro on livro.id_livro = emprestimos.id_livro
                   group by emprestimos.id_livro
                   order by count(*) desc
                   limit 3
                   ''')
    #INVÉS DE FAZER OUTRO SELECT, ELE UNE O JOIN COM AS OUTRAS FUNÇÕES
    resultado = cursor.fetchall()
    print(resultado)
    if resultado:
        pass
    else:
        print("NENHUM livro cadastrado!")
        consultas()
    print("LIVROS MAIS EMPRESTADOS:")
    for rep,id,title,autor,categoria,ano in resultado:
        print(f'''
                ID do Livro: {id}
                Título: {title}
                Autor: {autor}
                Categoria: {categoria}
                Ano de publicação: {ano}
                ''')
    
def count_indisponiveis(cursor):
    cursor.execute("select * from livro where quantidade_disponivel = 0")
    resultado = cursor.fetchall()
    # print(resultado)
    if not resultado:
        print("TODOS os livros estão disponíveis")
        print(f"Há {len(resultado)} livro(s) indisponível")
        consultas()
    else:
        print(f"{len(resultado)} encontrado(s)!")
    for q,w,e,r,t,y,u in resultado:
        print(f'''
                  ID do Livro: {q}
                  Título: {w}
                  Autor: {e}
                  Categoria: {r}
                  Ano de publicação: {t}
                  Quantidade Disponivel: {u}
                  ''')

def count_usuarios(cursor):
    cursor.execute("select * from usuario")
    resultado = cursor.fetchall()
    if resultado:
        print(f"Há {len(resultado)} usuários cadastrado(s)")
    else:
        print("NENHUM usuário cadastrado!")
        consultas()
    print("CONTAS ATIVAS:")
    # cursor.execute("select * from usuario where status = 1")
    # ativos = cursor.fetchall()
    for id,nome,email,telefone,status in resultado:
        if status == 1:
            condicao = "ATIVA"
            print(f'''
              ID do Usuário: {id}
              Nome: {nome}
              Email: {email}
              Telefone: {telefone}
              Status: {condicao}
              ''')
        else:
            pass
    print("CONTAS DESATIVADAS")
    for id,nome,email,telefone,status in resultado:
        if status == 0:
            condicao = "DESATIVADA"
            print(f'''
                ID do Usuário: {id}
                Nome: {nome}
                Email: {email}
                Telefone: {telefone}
                Status: {condicao}
                ''')
        else:
            pass

def relat(cursor):
    indice = 0
    cursor.execute('''
                   select emprestimos.id_emprestimo,emprestimos.id_livro,emprestimos.id_usuario,livro.titulo,usuario.nome,emprestimos.data_emprestimo,emprestimos.data_devolucao_prevista,emprestimos.data_devolucao_real,emprestimos.status
                   from emprestimos
                   inner join livro on livro.id_livro = emprestimos.id_livro
                   inner join usuario on usuario.id_usuario = emprestimos.id_usuario
                   ''')
    resultado = cursor.fetchall()
    total = len(resultado)
    if resultado:
        print(f"{total} encontrado(s)!")
    else:
        print("NENHUM resultado encontrado!")
        consultas()
    print("EMPRÉSTIMOS ATRASADOS:")
    for id1,id2,id3,title,nome,emprestimo,prev,real,status in resultado:
        if status == "Atrasado":
            print(f'''
                  ID do Empréstimo = {id1}
                  Livro = {title}
                  Usuário = {nome}
                  Data de empréstimo = {emprestimo}
                  Data de devolução prevista = {prev}
                  ''')
    print("EMPRÉSTIMOS DEVOLVIDOS:")
    for id1,id2,id3,title,nome,emprestimo,prev,real,status in resultado:  
        if status == "Devolvido":
            indice += 1
            print(f'''
                  ID do Empréstimo = {id1}
                  Livro = {title}
                  Usuário = {nome}
                  Data de empréstimo = {emprestimo}
                  Data de devolução prevista = {prev}
                  Data de devolução real = {real}
                  ''')
    print("EMPRÉSTIMOS EM ABERTO:")
    for id1,id2,id3,title,nome,emprestimo,prev,real,status in resultado: 
        if status == "Aberto":
            indice += 1
            print(f'''
                  ID do Empréstimo = {id1}
                  Livro = {title}
                  Usuário = {nome}
                  Data de empréstimo = {emprestimo}
                  Data de devolução prevista = {prev}
                  ''')
    print(f"TAXA DE ATRASOS: {(total-indice)*10}%")

def main(conn):
    while True:
        print('''
          !Bem - Vindo ao Sistema Bibliotech!
          1. Gerenciar Livros ✅
          2. Gerenciar Usuarios ✅
          3. Empréstimos ✅ 
          4. Consultas e Relatórios ✅
          0. Sair
          ''')
        op = int(input("Digite uma opção: "))
        match op:
            case 0:
                conn.close()
                break
            case 1:
                gerenciar_livros()
            case 2:
                gerenciar_usuarios()
            case 3:
                gerenciar_emprestimos()
            case 4:
                consultas()
            case _:
                print("Opção Inválida!")

# atualizar_status(cursor,conn)
main(conn)
# conn.close()
# print("Programa Encerrado!")
