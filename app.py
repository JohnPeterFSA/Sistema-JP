from flask import Flask, request, jsonify, render_template
from banco import conectar, criar_tabelas
import sqlite3
import hashlib
import os

app = Flask(__name__)

# Garante que as tabelas existam
criar_tabelas()

# Função para hash da senha (segurança básica)
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# --------------------------
# Rotas para servir páginas HTML
# --------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro.html')
def cadastro():
    return render_template('cadastro.html')

@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')

@app.route('/usuarios.html')
def usuarios():
    return render_template('usuarios.html')

@app.route('/marcos.html')
def marcos():
    return render_template('marcos.html')

@app.route('/servicos.html')
def servicos():
    return render_template('servicos.html')

# --------------------------
# Rotas de API para o frontend
# --------------------------

@app.route('/api/cadastrar', methods=['POST'])
def cadastrar_usuario():
    try:
        dados = request.get_json()
        login = dados.get('login')
        senha = dados.get('senha')

        if not login or not senha:
            return jsonify({'message': 'Login e senha são obrigatórios'}), 400

        # Validações básicas
        if len(login) < 3:
            return jsonify({'message': 'Login deve ter pelo menos 3 caracteres'}), 400
        
        if len(senha) < 6:
            return jsonify({'message': 'Senha deve ter pelo menos 6 caracteres'}), 400

        conn = conectar()
        c = conn.cursor()

        # Verifica se o login já existe
        c.execute("SELECT * FROM usuarios WHERE login=?", (login,))
        usuario_existente = c.fetchone()
        
        if usuario_existente:
            conn.close()
            return jsonify({'message': 'Erro: Este login já está em uso.'}), 400

        # Hash da senha para segurança básica
        senha_hash = hash_senha(senha)

        # Insere o novo usuário
        c.execute('''INSERT INTO usuarios (login, nome, estado_civil, profissao, documento, email, endereco, cep, senha)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (dados['login'], dados.get('nome', ''), dados.get('estado_civil', ''), 
                   dados.get('profissao', ''), dados.get('documento', ''), dados.get('email', ''),
                   dados.get('endereco', ''), dados.get('cep', ''), senha_hash))
        
        conn.commit()
        conn.close()
        return jsonify({'message': 'Usuário cadastrado com sucesso!'}), 200

    except sqlite3.IntegrityError:
        return jsonify({'message': 'Erro de integridade do banco de dados.'}), 500
    except Exception as e:
        return jsonify({'message': f'Erro no servidor: {str(e)}'}), 500


@app.route('/api/login', methods=['POST'])
def login_usuario():
    try:
        dados = request.get_json()
        login = dados.get('login')
        senha = dados.get('senha')

        if not login or not senha:
            return jsonify({'message': 'Login e senha são obrigatórios'}), 400

        conn = conectar()
        c = conn.cursor()

        # Hash da senha para comparar
        senha_hash = hash_senha(senha)

        # Verifica se existe usuário com login e senha corretos
        c.execute("SELECT * FROM usuarios WHERE login=? AND senha=?", (login, senha_hash))
        usuario = c.fetchone()
        conn.close()

        if usuario:
            return jsonify({'message': f'Bem-vindo, {login}!'}), 200
        else:
            return jsonify({'message': 'Login ou senha incorretos.'}), 401

    except Exception as e:
        return jsonify({'message': f'Erro no servidor: {str(e)}'}), 500


@app.route('/api/usuarios', methods=['GET'])
def listar_usuarios():
    try:
        conn = conectar()
        c = conn.cursor()
        c.execute("SELECT id, login, nome, email, profissao FROM usuarios")
        usuarios = [
            {"id": u[0], "login": u[1], "nome": u[2], "email": u[3], "profissao": u[4]}
            for u in c.fetchall()
        ]
        conn.close()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao listar usuários: {str(e)}"}), 500


@app.route('/api/usuarios/<int:user_id>', methods=['DELETE'])
def excluir_usuario(user_id):
    try:
        conn = conectar()
        c = conn.cursor()
        c.execute("DELETE FROM usuarios WHERE id=?", (user_id,))
        
        if c.rowcount == 0:
            conn.close()
            return jsonify({"message": "Usuário não encontrado"}), 404
        
        conn.commit()
        conn.close()
        return jsonify({"message": "Usuário excluído com sucesso!"}), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao excluir usuário: {str(e)}"}), 500


@app.route('/api/marcos', methods=['POST'])
def cadastrar_marco():
    try:
        dados = request.get_json()
        
        # Validações básicas
        if not dados.get('fazenda') or not dados.get('proprietario'):
            return jsonify({"message": "Fazenda e proprietário são obrigatórios"}), 400
        
        conn = conectar()
        c = conn.cursor()
        c.execute('''INSERT INTO marcos (tipo, fazenda, municipio, proprietario, numero_inicial, numero_final)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (dados.get('tipo', ''), dados.get('fazenda'), dados.get('municipio', ''),
                   dados.get('proprietario'), dados.get('numero_inicial', 0), dados.get('numero_final', 0)))
        conn.commit()
        conn.close()
        return jsonify({"message": "Marco cadastrado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao cadastrar marco: {str(e)}"}), 500


@app.route('/api/marcos', methods=['GET'])
def listar_marcos():
    try:
        conn = conectar()
        c = conn.cursor()
        c.execute("SELECT id, tipo, fazenda, municipio, proprietario, numero_inicial, numero_final FROM marcos")
        marcos = [
            {"id": m[0], "tipo": m[1], "fazenda": m[2], "municipio": m[3],
             "proprietario": m[4], "numero_inicial": m[5], "numero_final": m[6]}
            for m in c.fetchall()
        ]
        conn.close()
        return jsonify(marcos), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao listar marcos: {str(e)}"}), 500


@app.route('/api/marcos/<int:marco_id>', methods=['DELETE'])
def excluir_marco(marco_id):
    try:
        conn = conectar()
        c = conn.cursor()
        c.execute("DELETE FROM marcos WHERE id=?", (marco_id,))
        
        if c.rowcount == 0:
            conn.close()
            return jsonify({"message": "Marco não encontrado"}), 404
        
        conn.commit()
        conn.close()
        return jsonify({"message": "Marco excluído com sucesso!"}), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao excluir marco: {str(e)}"}), 500


@app.route('/api/servicos', methods=['POST'])
def cadastrar_servico():
    try:
        dados = request.get_json()
        
        # Validações básicas
        if not dados.get('fazenda') or not dados.get('cliente') or not dados.get('servico'):
            return jsonify({"message": "Fazenda, cliente e serviço são obrigatórios"}), 400
        
        conn = conectar()
        c = conn.cursor()
        c.execute('''INSERT INTO servicos (fazenda, cliente, servico, valor, pagamento, data)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (dados.get('fazenda'), dados.get('cliente'), dados.get('servico'),
                   dados.get('valor', '0'), dados.get('pagamento', 'Pendente'), dados.get('data', '')))
        conn.commit()
        conn.close()
        return jsonify({"message": "Serviço registrado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao registrar serviço: {str(e)}"}), 500


@app.route('/api/servicos', methods=['GET'])
def listar_servicos():
    try:
        conn = conectar()
        c = conn.cursor()
        c.execute("SELECT id, fazenda, cliente, servico, valor, pagamento, data FROM servicos")
        servicos = [
            {"id": s[0], "fazenda": s[1], "cliente": s[2], "servico": s[3],
             "valor": s[4], "pagamento": s[5], "data": s[6]}
            for s in c.fetchall()
        ]
        conn.close()
        return jsonify(servicos), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao listar serviços: {str(e)}"}), 500


@app.route('/api/servicos/<int:servico_id>', methods=['DELETE'])
def excluir_servico(servico_id):
    try:
        conn = conectar()
        c = conn.cursor()
        c.execute("DELETE FROM servicos WHERE id=?", (servico_id,))
        
        if c.rowcount == 0:
            conn.close()
            return jsonify({"message": "Serviço não encontrado"}), 404
        
        conn.commit()
        conn.close()
        return jsonify({"message": "Serviço excluído com sucesso!"}), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao excluir serviço: {str(e)}"}), 500


# Rota para estatísticas do dashboard
@app.route('/api/stats', methods=['GET'])
def obter_estatisticas():
    try:
        conn = conectar()
        c = conn.cursor()
        
        # Conta usuários
        c.execute("SELECT COUNT(*) FROM usuarios")
        total_usuarios = c.fetchone()[0]
        
        # Conta marcos
        c.execute("SELECT COUNT(*) FROM marcos")
        total_marcos = c.fetchone()[0]
        
        # Conta serviços
        c.execute("SELECT COUNT(*) FROM servicos")
        total_servicos = c.fetchone()[0]
        
        # Soma valores dos serviços
        c.execute("SELECT SUM(CAST(valor AS REAL)) FROM servicos WHERE valor != ''")
        receita_total = c.fetchone()[0] or 0
        
        conn.close()
        
        return jsonify({
            "total_usuarios": total_usuarios,
            "total_marcos": total_marcos,
            "total_servicos": total_servicos,
            "receita_total": f"R$ {receita_total:,.2f}"
        }), 200
        
    except Exception as e:
        return jsonify({"message": f"Erro ao obter estatísticas: {str(e)}"}), 500


# Criar usuário admin padrão se não existir
def criar_usuario_admin():
    try:
        conn = conectar()
        c = conn.cursor()
        
        # Verifica se já existe um admin
        c.execute("SELECT * FROM usuarios WHERE login='admin'")
        if not c.fetchone():
            senha_admin = hash_senha('123456')
            c.execute('''INSERT INTO usuarios (login, nome, senha, email, profissao)
                         VALUES (?, ?, ?, ?, ?)''',
                      ('admin', 'Administrador', senha_admin, 'admin@jpgeo.com', 'Administrador'))
            conn.commit()
            print("✅ Usuário admin criado: admin/123456")
        
        conn.close()
    except Exception as e:
        print(f"Erro ao criar usuário admin: {e}")


if __name__ == '__main__':
    criar_usuario_admin()  # Cria usuário admin na primeira execução
    print("🚀 Servidor JP-GEO iniciado!")
    print("📱 Acesse: http://127.0.0.1:5000")
    print("👤 Login teste: admin / 123456")
    app.run(host='127.0.0.1', port=5000, debug=True)