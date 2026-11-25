# Avaliação semestral — Flask

Aplicação web Flask com visual inspirado nas imagens de referência, cadastro de professores e persistência em SQLite.

## Rotas implementadas
- `/` — página inicial com aluno, prontuário e data/hora local.
- `/professores` — formulário de cadastro e relação de professores.

Os outros itens da navegação exibem **“Não disponível”** no navegador sem criar rotas adicionais.

## Executar localmente
Recomendado Python 3.10 ou 3.11:
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python app.py
```
Acesse http://127.0.0.1:5000.

O banco `avaliacao.db` é criado automaticamente na primeira execução. A tabela recebe dados de demonstração somente quando está vazia. Novos cadastros ficam salvos no SQLite.

## Publicar no PythonAnywhere
1. Crie uma conta em https://www.pythonanywhere.com/ e abra **Dashboard > Files**.
2. Envie este ZIP e extraia-o em `/home/SEU_USUARIO/avaliacao_semestral_flask`.
3. Abra **Consoles > Bash** e execute:
   ```bash
   cd ~/avaliacao_semestral_flask
   python3.10 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
   Se sua conta usar outra versão de Python, selecione a mesma versão na aba **Web** e use-a para criar o ambiente.
4. Em **Web**, crie uma aplicação Flask manual, escolhendo a mesma versão Python.
5. Em **Virtualenv**, informe:
   `/home/SEU_USUARIO/avaliacao_semestral_flask/venv`
6. Edite o arquivo WSGI indicado na aba **Web** e substitua o conteúdo por:
   ```python
   import sys
   project_home = '/home/SEU_USUARIO/avaliacao_semestral_flask'
   if project_home not in sys.path:
       sys.path.insert(0, project_home)

   from app import app as application
   ```
   Troque `SEU_USUARIO` pelo seu usuário real do PythonAnywhere.
7. Clique em **Reload** na aba **Web** e acesse o endereço `.pythonanywhere.com`.

## Observações
- O `SECRET_KEY` padrão serve para teste. Configure uma chave própria antes de usar publicamente.
- Para mudar os dados exibidos na página inicial, edite os valores padrão em `app.py`.
- Para reiniciar o banco de demonstração, pare a aplicação, apague `avaliacao.db` e inicie novamente.
