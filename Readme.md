📦 Sistema de Gestão de Patrimônio
Este repositório contém um sistema completo de gestão de patrimônio desenvolvido em Django, uma estrutura web Python poderosa e escalável. O sistema foi projetado para gerenciar bens, categorias, departamentos, fornecedores, instituições e movimentações de forma eficiente e intuitiva.

✨ Funcionalidades Principais
📝 Cadastro de Bens:

Registro de bens com detalhes como nome, descrição, categoria, departamento, fornecedor, instituição, data de aquisição, valor de aquisição, RFID e status.

🗂️ Gestão de Categorias, Departamentos e Fornecedores:

CRUD (Create, Read, Update, Delete) para categorias, departamentos e fornecedores.

🏛️ Controle de Instituições:

Cadastro e gerenciamento de instituições associadas aos bens.

🚚 Movimentações:

Registro de movimentações de bens entre departamentos ou instituições.

📊 Dashboard Interativo:

Visualização de métricas importantes, como total de ativos, valor total do patrimônio e ativos em manutenção.

Gráficos dinâmicos para análise de dados (ativos por categoria, departamento, instituição e status).

🔐 Autenticação e Autorização:

Sistema de login e registro de usuários.

Controle de acesso para garantir que apenas usuários autenticados possam acessar as funcionalidades do sistema.

📡 Integração com RFID:

Leitura de tags RFID para cadastro rápido de bens.

🛠️ Tecnologias Utilizadas
Backend:

🐍 Django (Python)
🗃️ Django ORM (Banco de Dados)
📋 Django Forms (Validação de Dados)
🔄 Django REST Framework (API, se necessário)

Frontend:

🌐 HTML5, CSS3, JavaScript
🎨 Bootstrap (Design Responsivo)
📈 Chart.js (Gráficos Interativos)

Banco de Dados:

💾 SQLite (Desenvolvimento)

Outras Ferramentas:

🔌 PySerial (Integração com RFID)