"""Confere arquivos e links locais sem modificar o site ou acessar a internet.

Use Python 3.10 ou superior. Não é necessário instalar bibliotecas.
Este é um verificador de referências, não um validador completo de HTML/CSS.
"""

from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit


class DocumentoHTML(HTMLParser):
    """Extrai os identificadores e endereços presentes em um documento HTML."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.ids_duplicados = set()
        self.referencias = []
        self.possui_base = False

    def handle_starttag(self, tag, attrs):
        atributos = dict(attrs)
        identificador = atributos.get("id")
        if identificador is not None:
            if identificador in self.ids:
                self.ids_duplicados.add(identificador)
            self.ids.add(identificador)

        if tag == "base" and atributos.get("href") is not None:
            self.possui_base = True

        for atributo in ("href", "src"):
            endereco = atributos.get(atributo)
            if endereco:
                self.referencias.append((self.getpos()[0], endereco.strip()))


def validar_site(raiz):
    """Retorna uma lista de problemas e a quantidade de páginas examinadas."""
    raiz = raiz.resolve()
    erros = []
    documentos = {}

    # Arquivos mínimos esperados para esta landing page.
    for nome in ("index.html", "style.css"):
        if not (raiz / nome).is_file():
            erros.append(f"Arquivo obrigatório ausente: {nome}")

    # Pastas ocultas de ferramentas, como .git, ficam fora da verificação.
    paginas = sorted(
        caminho for caminho in raiz.rglob("*.html")
        if not any(parte.startswith(".") for parte in caminho.relative_to(raiz).parts)
    )

    def ler_html(caminho):
        if caminho in documentos:
            return documentos[caminho]
        nome = caminho.relative_to(raiz).as_posix()
        try:
            texto = caminho.read_text(encoding="utf-8-sig")
            documento = DocumentoHTML()
            documento.feed(texto)
            documento.close()
        except (OSError, UnicodeError, ValueError, AssertionError) as erro:
            erros.append(f"{nome}: não foi possível ler o HTML: {erro}")
            documentos[caminho] = None
            return None

        for identificador in sorted(documento.ids_duplicados):
            erros.append(f"{nome}: identificador duplicado: {identificador!r}")
        if documento.possui_base:
            erros.append(f"{nome}: links com <base href> ainda não são suportados pelo verificador.")
        documentos[caminho] = documento
        return documento

    for pagina in paginas:
        if not pagina.resolve().is_relative_to(raiz):
            erros.append("Foi encontrada uma página apontando para fora da pasta do site.")
            continue
        documento = ler_html(pagina)
        if documento is None:
            continue
        nome = pagina.relative_to(raiz).as_posix()

        for linha, endereco in documento.referencias:
            try:
                url = urlsplit(endereco)
            except ValueError:
                erros.append(f"{nome}:{linha}: endereço inválido: {endereco!r}")
                continue

            # Links externos, e-mails e outros protocolos não geram requisições.
            if url.scheme or url.netloc:
                continue

            trecho = unquote(url.fragment)
            caminho_url = unquote(url.path)
            if not caminho_url:
                destino = pagina.resolve()
            else:
                base = raiz if caminho_url.startswith("/") else pagina.parent
                destino = (base / caminho_url.lstrip("/")).resolve()

            if not destino.is_relative_to(raiz):
                erros.append(f"{nome}:{linha}: link sai da pasta do site: {endereco!r}")
                continue
            if destino.is_dir():
                destino = destino / "index.html"
            if not destino.is_file():
                erros.append(f"{nome}:{linha}: arquivo não encontrado: {endereco!r}")
                continue

            # Para links como outra-pagina.html#contato, confere o arquivo e o ID.
            if trecho and destino.suffix.lower() == ".html":
                documento_destino = ler_html(destino)
                if documento_destino is not None and trecho not in documento_destino.ids:
                    erros.append(f"{nome}:{linha}: destino #{trecho} não encontrado em {destino.relative_to(raiz).as_posix()}")

    return erros, len(paginas)


def main():
    # A raiz vem do local deste script; o comando funciona de qualquer pasta.
    raiz = Path(__file__).resolve().parent.parent
    erros, quantidade = validar_site(raiz)
    if erros:
        print("FALHA: foram encontrados problemas na página.")
        for erro in erros:
            print(f"- {erro}")
        return 1

    print(f"OK: {quantidade} página(s) HTML verificada(s).")
    print("Arquivos obrigatórios, IDs e referências locais conferidos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
