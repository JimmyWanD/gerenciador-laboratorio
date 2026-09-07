# Gerenciador de Laboratório

Aplicativo para gerenciamento de laboratório de análises clínicas.

## Funcionalidades

- **Incidentes (Colaboradores)**: Registre incidentes envolvendo colaboradores
- **Incidentes (Amostra)**: Registre incidentes com amostras
- **Temperaturas**: Controle e registro de temperaturas de equipamentos
- **Manutenção dos Equipamentos**: Gerencie manutenções de controle e calibração
- **Gerenciamento de Riscos**: Identifique e gerencie riscos no laboratório
- **Troca de Almotolias**: Controle a troca de almotolias com bancada, lote e datas
- **Análise de Pendências**: Acompanhe pendências com prioridades e status
- **Exportação para Excel**: Exporte todos os dados para arquivos Excel

## Estrutura do Projeto

```
app_laboratorio/
├── main.py           # Aplicação principal (Tkinter)
├── database.py       # Gerenciamento do banco SQLite
├── exporter.py       # Exportação para Excel
├── build_exe.py      # Script para criar o .exe
├── laboratorio.db    # Banco de dados SQLite
└── requirements.txt  # Dependências
```

## Como Executar

### Opção 1: Executar como script Python

```bash
cd app_laboratorio
pip install -r requirements.txt
python main.py
```

### Opção 2: Criar arquivo .exe (Windows)

1. Instale o PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Execute o script de build:
   ```bash
   python build_exe.py
   ```

3. O arquivo executável será criado em `dist/GerenciadorLaboratorio.exe`

4. Copie o arquivo `.exe` e o `laboratorio.db` para o pen drive

## Campos de Cada Categoria

### Incidentes (Colaboradores)
- Colaborador (obrigatório)
- Tipo de Incidente (obrigatório)
- Descrição
- Data/Hora (automático)

### Incidentes (Amostra)
- ID da Amostra (obrigatório)
- Tipo de Problema (obrigatório)
- Responsável
- Descrição
- Data/Hora (automático)

### Temperaturas
- Equipamento (obrigatório)
- Temperatura (obrigatório)
- Limite Aceitável Mínimo
- Limite Aceitável Máximo
- Data/Hora (automático)

### Manutenção dos Equipamentos
- Equipamento (obrigatório)
- Tipo: Controle ou Calibração (obrigatório)
- Responsável
- Descrição
- Data da Manutenção (obrigatório)
- Próxima Manutenção

### Gerenciamento de Riscos
- Descrição (obrigatório)
- Nível: Baixo, Médio, Alto
- Ações
- Data de Identificação (automático)
- Data de Revisão

### Troca de Almotolias
- Bancada (obrigatório)
- Data da Troca (obrigatório)
- Lote do Reagente (obrigatório)
- Próxima Troca (obrigatório)

### Análise de Pendências
- Descrição (obrigatório)
- Prioridade: Baixa, Média, Alta
- Data Limite (obrigatório)
- Status: Pendente, Em Andamento, Concluído
- Data de Criação (automático)

## Exportação para Excel

- **Exportar Tudo**: Cria um arquivo Excel com todas as categorias em abas separadas
- **Exportar por Categoria**: Cria um arquivo Excel com apenas a categoria atual

## Requisitos

- Python 3.6+
- Tkinter (geralmente já incluso com Python)
- pandas
- openpyxl
- PyInstaller (apenas para criar o .exe)

## Notas

- O banco de dados SQLite é criado automaticamente na primeira execução
- Todos os dados são salvos localmente no arquivo `laboratorio.db`
- O aplicativo pode ser executado diretamente de um pen drive
- Não é necessário instalação ou cadastro de usuários
