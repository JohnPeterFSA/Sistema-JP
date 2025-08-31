# JP-GEO Sistema de Gestão Rural

Este projeto é um sistema web simples para gestão rural com cadastro de usuários, controle de marcos geográficos e registro de serviços realizados.

## Funcionalidades

- **Cadastro e Login de Usuários**
- **Gerenciamento de Marcos Geográficos**
- **Registro de Serviços**
- **Dashboard com estatísticas**
- **Exportação de dados (CSV e Relatórios)**

## Tecnologias

- **Backend:** Python 3 + Flask + SQLite
- **Frontend:** HTML, Tailwind CSS, JavaScript

## Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/JohnPeterFSA/Sistema-JP.git
   cd Sistema-JP
   ```

2. **Crie e ative um ambiente virtual (recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o servidor Flask:**
   ```bash
   python app.py
   ```

5. **Acesse o sistema:**
   - Abra [http://127.0.0.1:5000](http://127.0.0.1:5000) no navegador.

## Usuário de Teste

- **Login:** admin
- **Senha:** 123456

## Estrutura do Projeto

```
Sistema-JP/
├── app.py
├── banco.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   ├── index.html
│   ├── cadastro.html
│   ├── dashboard.html
│   ├── usuarios.html
│   ├── marcos.html
│   ├── servicos.html
```

## Observações

- O banco de dados `jpgeo.db` será criado automaticamente no primeiro uso.
- Os arquivos HTML estão na pasta `templates`, conforme padrão Flask.
- Para personalizar estilos ou adicionar imagens, utilize a pasta `static` (crie caso necessário).

## Licença

MIT
