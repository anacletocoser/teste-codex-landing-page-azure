# Minha landing page: do computador à Azure

Projeto de aprendizado para praticar implementação, Git, GitHub, integração
contínua e, em uma próxima etapa, publicação na Azure.

A página usa HTML e CSS. Você pode editar os arquivos manualmente e abrir
`index.html` diretamente no navegador, sem instalar programas.

## Arquivos do projeto

```text
minha-landing-page/
├── index.html                 # Estrutura e textos da página
├── style.css                  # Aparência e regras para celular
├── LEIA-ME.txt                # Exercícios de edição manual
├── README.md                  # Este guia do projeto
├── .gitignore                 # Arquivos que o Git deve ignorar
├── scripts/
│   └── validar_site.py        # Verificador usado localmente e na CI
└── .github/
    └── workflows/
        └── ci.yml            # Automação do GitHub Actions
```

## Abrir e modificar a página

1. Abra `index.html` no navegador com dois cliques.
2. Abra o mesmo arquivo no Bloco de Notas ou em outro editor de texto.
3. Altere um texto, preserve as marcações HTML e salve com **Ctrl + S**.
4. Atualize o navegador com **F5** para ver a mudança.

Mantenha `index.html`, `style.css` e `LEIA-ME.txt` na mesma pasta.
Consulte o [guia de edição](LEIA-ME.txt) para os primeiros exercícios.

## O fluxo que estamos aprendendo

```text
Editar → verificar → git add → git commit → git push → GitHub Actions
```

- **Git:** registra o histórico dos arquivos no computador.
- **Repositório:** reúne os arquivos e esse histórico.
- **Branch:** uma linha de trabalho; a principal deste projeto se chama `main`.
- **Staging (`git add`):** seleciona as alterações que entrarão no próximo commit.
- **Commit:** registra uma versão local com uma mensagem que explica a mudança.
- **Origin:** apelido do repositório remoto no GitHub.
- **Push:** envia os commits locais para o GitHub.
- **Pull request (PR):** propõe juntar uma branch a outra e permite revisar a mudança.

Comandos para uma alteração nos textos ou no visual, executados nesta pasta:

```powershell
git status
git diff
git add index.html style.css
git diff --cached
git commit -m "Atualiza textos e visual da página"
git push
```

Antes de criar o commit, confira os arquivos selecionados. Esses comandos são
um exemplo para você executar quando desejar; nenhum deles roda ao abrir a página.

## Como funciona a integração contínua (CI)

O arquivo [ci.yml](.github/workflows/ci.yml) descreve uma automação, também chamada
de workflow. Depois de enviado ao GitHub, ele executa em três situações:

1. Um `push` chega à branch `main`.
2. Um pull request propõe uma alteração para `main`.
3. Você solicita uma execução manual na aba **Actions**.

A automação obtém o código, disponibiliza Python 3.13 e executa o verificador.
O job tem limite de cinco minutos e só precisa de permissão de leitura.
Uma nova execução para a mesma referência cancela a anterior ainda em andamento.

No GitHub, abra a aba **Actions**, escolha **CI - Verificar landing page** e abra
a execução. O resultado verde indica sucesso; o vermelho indica falha. Os detalhes
da etapa **Conferir a landing page** mostram a mensagem do verificador.

O verificador confere:

- A existência de `index.html` e `style.css`.
- A leitura dos documentos HTML em UTF-8.
- IDs duplicados, que tornam os destinos internos ambíguos.
- Arquivos locais citados em atributos `href` e `src`.
- Fragmentos como `#sobre`, inclusive quando apontam a outra página HTML.
- Referências a arquivos fora da pasta do site.

Ele usa apenas a biblioteca padrão do Python, sem instalar pacotes ou acessar
a internet. Não confere endereços externos, referências dentro do CSS, aparência
no navegador ou toda a sintaxe de HTML/CSS. Links com `<base href>` são sinalizados
como não suportados nesta versão.

Um resultado vermelho sinaliza um problema. A CI sozinha não bloqueia commits
ou merges: exigir aprovação das verificações depende de regras do repositório.

## Executar a mesma verificação no computador

Se você já tem **Python 3.10 ou superior** disponível, abra um terminal na pasta
do projeto e execute:

```powershell
python -B -X utf8 scripts/validar_site.py
```

`-B` evita criar cache de bytecode e `-X utf8` garante a leitura das mensagens
com acentos. O comando retorna código **0** quando passa e **1** quando encontra
problemas; o GitHub Actions usa esse código para determinar o resultado da etapa.

Se `python` não estiver disponível no seu terminal, você ainda pode usar a página
normalmente e executar a CI no GitHub após o envio dos arquivos. Na preparação
local pelo Codex, pode ser usado o Python já incluído no ambiente do aplicativo;
isso não significa que Python esteja instalado globalmente no seu computador.

## Publicação na Azure: próxima etapa

Por enquanto, esta automação apenas verifica o site. A implantação contínua (CD)
e o recurso Azure Static Web Apps ainda precisam ser configurados.

A proposta é selecionar explicitamente o plano **Free** e usar o endereço padrão
da Azure. Quando conectarmos a publicação à CI, a etapa de deploy deverá depender
do sucesso da verificação para que uma falha impeça aquela publicação automática.

O repositório é público. Executores padrão do GitHub Actions em repositórios
públicos têm execução gratuita. Este workflow usa `ubuntu-latest`, não cria
artefatos para armazenar e não configura serviços pagos.

Na Azure, o plano Free tem cotas. Antes de criar recursos, vamos conferir o plano
selecionado e os limites aplicáveis. As condições e preços dos serviços podem
mudar; ter uma assinatura Azure não torna todos os recursos gratuitos.

## Referências oficiais

- [Sintaxe dos workflows do GitHub Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [Ação checkout](https://github.com/actions/checkout)
- [Ação setup-python](https://github.com/actions/setup-python)
- [Cobrança do GitHub Actions](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
- [Planos do Azure Static Web Apps](https://learn.microsoft.com/en-us/azure/static-web-apps/plans)
- [Cotas do Azure Static Web Apps](https://learn.microsoft.com/en-us/azure/static-web-apps/quotas)
