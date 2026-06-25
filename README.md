# 📱 Authenticator CONSIGA

Um aplicativo desktop para Windows que **emula o comportamento de dispositivos móveis**, permitindo que você abra, visualize e assinale documentos ou acesse links restritos para celular diretamente pelo seu computador.

Este projeto foi desenhado especificamente para contornar a limitação de links de autorização do banco/promotora **CONSIGA** (como URLs do *Trustic* / *assinar.io*), que exigem o uso em um smartphone.

---

## 🚀 Como funciona?

O aplicativo utiliza o motor do navegador Chromium subjacente (via [Playwright](https://playwright.dev/)) para disfarçar a sua sessão. Ele oculta propriedades de automação e define corretamente as coordenadas de GPS, permissões de câmera/microfone fake, User-Agent e dimensões de tela para que o servidor de destino acredite que você está utilizando um celular real.

Tudo isso encapsulado em uma interface gráfica amigável de fácil uso (construída com `pywebview`).

---

## 💻 Passo a Passo para Instalar e Usar

Existem duas formas de preparar e rodar o aplicativo, dependendo de como você obteve os arquivos:

### Cenário A: Você recebeu o pacote pronto (`dist.zip`) *(Operador / Usuário Final)*

Se você recebeu apenas a pasta final compilada (ou baixou da aba *Releases*):

1. **Extraia a pasta** em qualquer local do computador.
2. Execute o arquivo **`instalar.bat`**. 
   *(Ele copiará os arquivos para sua AppData e criará os atalhos na Área de Trabalho e no Menu Iniciar)*.
3. Abra o atalho **Assinar Documento** na sua Área de Trabalho.
4. Na janela do aplicativo:
   - O campo de link já virá preenchido com `https://www.google.com` por padrão para testes. Substitua colando o link que você recebeu por SMS ou e-mail.
   - Selecione qual modelo de celular deseja simular (ex: *iPhone 15 Pro*).
   - Clique em **Abrir para Assinar**.
5. Uma janela idêntica a uma tela de celular se abrirá. Faça o processo de autorização ou assinatura normalmente.

Ao fechar a janela do celular, o processo é encerrado de forma limpa.

---

### Cenário B: Você baixou o Código-Fonte (GitHub / Git) *(Desenvolvedor)*

Se você clonou o repositório completo e ainda não tem o executável `.exe` gerado:

1. Certifique-se de ter o **Python 3.8+** instalado no Windows.
2. Dê um duplo clique no arquivo **`build.bat`**.
   *(O script irá baixar automaticamente as bibliotecas do Python, o motor do Chromium e criará uma pasta chamada **`dist`** com o programa compilado)*.
3. Quando a compilação finalizar, execute o **`instalar.bat`**. 
   *(Nota: O instalador possui inteligência automática; você pode executá-lo diretamente na pasta raiz ou dentro da pasta `dist/`, e ele configurará os atalhos corretamente!)*.

---

## 📦 Como distribuir para outros computadores

- **Para colegas de trabalho / operadores:** Compile o projeto rodando `build.bat`. Pegue a pasta **`dist/`** gerada, compacte em um arquivo `.zip` e envie para eles. No PC deles, basta extrair e rodar `instalar.bat`. Eles **não precisam** instalar Python ou Git!
- **Para outros programadores:** Compartilhe o link do repositório no GitHub. Eles deverão clonar o código e executar `build.bat` na máquina deles.

---

## 🛠️ Estrutura do Projeto

- **`interface.py`**: Coração visual do app. Gera a janela amigável (HTML/CSS) e engatilha o Playwright mobile.
- **`assinar.py`**: Versão via Linha de Comando (CLI) para testes diretos e rápidos via terminal.
- **`build.bat`**: Script de compilação automática. Usa `python -m` para instalar dependências e rodar o PyInstaller contornando erros de PATH do Windows.
- **`copy_chromium.py`**: Script auxiliar invocado pelo build para isolar e copiar o Chromium offline de forma segura.
- **`instalar.bat`**: Instalador inteligente para o usuário final com detecção de contexto e criação de atalhos PowerShell.

---

## ⚠️ Isenção de Responsabilidade
Esta ferramenta tem o objetivo de facilitar a rotina de operadores que precisam verificar links e dependem do computador no dia a dia. A responsabilidade por autorizar transações usando esse método e garantir as políticas de uso com a Consiga é puramente de quem realiza as requisições. O aplicativo não salva ou intercepta dados sensíveis transitados dentro da janela do Chromium.
