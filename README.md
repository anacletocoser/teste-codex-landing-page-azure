# Minha landing page: do computador à Azure

Projeto de aprendizado para praticar implementação, Git, GitHub, integração
contínua (CI) e publicação automática na Azure (CD).

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
        └── ci.yml            # Verificação e publicação pelo GitHub Actions
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
Editar → verificar → git add → git commit → git push → CI → publicação na Azure
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
O job de verificação tem limite de cinco minutos e só precisa de permissão de
leitura do repositório. Em pull requests, uma nova execução cancela a anterior
da mesma referência. Em `main`, uma publicação em andamento não é cancelada
automaticamente por uma nova execução.

No GitHub, abra a aba **Actions**, escolha **CI/CD - Verificar e publicar landing page** e abra
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

## Publicação na Azure (CD)

O recurso foi criado pelo portal da Azure com esta configuração:

| Campo | Valor |
| --- | --- |
| Serviço | Azure Static Web Apps |
| Nome | `swa-codex-landing-page` |
| Grupo de recursos | `rg-codex-landing-page` |
| Região | `centralus` |
| Plano | **Free** |
| Origem da implantação | **Other / Outro**: workflow configurado manualmente |

Endereço público: <https://witty-meadow-028eb4510.2.azurestaticapps.net>.
A página ficará disponível nesse endereço depois da primeira publicação
bem-sucedida. Criar o recurso e configurar o segredo, por si só, não envia o site.

O workflow contém dois jobs:

```text
verificar-site → publicar-site
```

`needs: verificar-site` faz a publicação esperar pelo sucesso da verificação.
Se a CI falhar, o job de publicação é ignorado. Ele também é ignorado em pull
requests: a publicação em produção roda somente em `push` para `main` ou em uma
execução manual que selecione `main`.

O job de publicação:

1. Obtém os arquivos da mesma versão que passou na verificação.
2. Confere se o segredo de publicação foi configurado, sem mostrar seu valor.
3. Cria uma pasta temporária `site-publicado` dentro do executor do GitHub.
4. Copia para ela somente `index.html`, `style.css` e `LEIA-ME.txt`.
5. Usa a ação oficial `Azure/static-web-apps-deploy@v1` para enviar essa pasta.

A pasta temporária é criada no GitHub Actions, não na sua pasta local. README,
scripts, configuração de workflow e histórico Git ficam fora do conteúdo enviado
à hospedagem. Ao adicionar imagens ou outros arquivos ao site no futuro, atualize
também a lista de arquivos copiados no workflow.

Como os arquivos estão prontos para servir, `skip_app_build: true` dispensa uma
etapa de compilação. Não há API neste projeto: `api_location` fica vazio. O job
tem um limite de dez minutos e usa o recurso Azure já existente, sem criar
outros recursos ou alterar seu plano.

### Segredo de publicação

O token da Azure foi cadastrado manualmente em **Settings → Secrets and variables
→ Actions → New repository secret**, com o nome:

```text
AZURE_STATIC_WEB_APPS_API_TOKEN
```

O YAML contém somente a referência `${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}`.
O valor do token deve ficar no segredo do GitHub. Se ele for redefinido na Azure,
atualize esse segredo antes da próxima publicação.

### Como acompanhar e manter o site

1. Edite a página e confira o resultado localmente no navegador.
2. Execute o verificador, se tiver Python disponível.
3. Revise as alterações, faça o commit e envie com `git push`.
4. Na aba **Actions**, acompanhe primeiro **Verificar arquivos e links** e depois
   **Publicar na Azure**. Abra uma etapa para ler suas mensagens.
5. Depois do sucesso da publicação, abra o endereço público e confira a mudança.
   Se a página parecer antiga, tente **Ctrl + F5** para atualizar sem usar o cache.

Para publicar novamente a versão de `main` sem criar um commit, abra **Actions →
CI/CD - Verificar e publicar landing page → Run workflow**, selecione `main`
e confirme. Isso executa a verificação e, se ela passar, publica novamente.

Se algo falhar, abra o job vermelho e leia a primeira mensagem de erro. Uma
falha de CI deve ser corrigida no código; segredo ausente ou inválido deve ser
corrigido nas configurações do GitHub. Não substitua o segredo por um token
escrito no código.

## Custos e limites

O repositório é público. Executores padrão do GitHub Actions em repositórios
públicos têm execução gratuita. Este workflow usa `ubuntu-latest`, não configura
upload de artefatos nem cache de dependências e não provisiona serviços pagos.

Na Azure, o plano Free tem cotas. Confira periodicamente o plano de hospedagem,
o uso do recurso e os custos associados a este grupo de recursos no portal.
As condições e preços dos serviços podem mudar; ter uma assinatura Azure não
torna todos os recursos gratuitos. Um alerta de orçamento da Azure avisa sobre
gastos, mas não é um bloqueio automático de cobranças.

## Referências oficiais

- [Sintaxe dos workflows do GitHub Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [Ação checkout](https://github.com/actions/checkout)
- [Ação setup-python](https://github.com/actions/setup-python)
- [Ação de publicação na Azure](https://github.com/Azure/static-web-apps-deploy)
- [Configuração de publicação](https://learn.microsoft.com/en-us/azure/static-web-apps/build-configuration)
- [Gerenciar o token de publicação](https://learn.microsoft.com/en-us/azure/static-web-apps/deployment-token-management)
- [Cobrança do GitHub Actions](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
- [Planos do Azure Static Web Apps](https://learn.microsoft.com/en-us/azure/static-web-apps/plans)
- [Cotas do Azure Static Web Apps](https://learn.microsoft.com/en-us/azure/static-web-apps/quotas)
