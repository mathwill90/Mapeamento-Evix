# Conversor de PDF para TXT

Interface gráfica simples (Tkinter) para converter arquivos PDF em TXT usando a
biblioteca [`docling`](https://github.com/docling-project/docling). Permite
converter arquivos individuais ou todos os PDFs de uma pasta, com opção de
gerar um arquivo `.txt` consolidado com todos os documentos.

## Como gerar o executável (.exe)

O executável precisa ser gerado no **Windows** (o PyInstaller empacota para o
mesmo sistema operacional em que é executado). Há duas formas:

### Opção 1 — Build local no Windows

Pré-requisitos: Python 3.10+ instalado no Windows.

1. Copie a pasta `conversor-pdf-txt` para o seu computador (ou clone o repositório).
2. Dê duplo clique em `build.bat`, ou rode pelo `cmd`/PowerShell dentro da pasta:
   ```bat
   build.bat
   ```
3. O script cria um ambiente virtual, instala as dependências e roda o
   PyInstaller. Ao final, o executável fica em:
   ```
   dist\ConversorPDFparaTXT\ConversorPDFparaTXT.exe
   ```

O build pode demorar alguns minutos e a pasta final é grande (várias
centenas de MB a alguns GB), pois o `docling` depende de bibliotecas de
IA/OCR (PyTorch, EasyOCR, modelos de layout, etc.).

O programa é gerado em modo "pasta" (não é um único arquivo `.exe`) de
propósito: assim ele abre rápido, sem precisar descompactar tudo a cada
execução. **Mantenha o `.exe` dentro da pasta `ConversorPDFparaTXT`** — os
outros arquivos ali são necessários para ele funcionar. Para o dia a dia,
crie um atalho para o `.exe` na área de trabalho.

### Opção 2 — Build automático via GitHub Actions (sem precisar de Python local)

O repositório inclui o workflow
`.github/workflows/build-conversor-pdf-txt.yml`, que compila o `.exe` em um
runner Windows do GitHub.

1. No GitHub, vá em **Actions** → **Build Conversor PDF para TXT (Windows .exe)**.
2. Clique em **Run workflow** (ou apenas dê push de alterações dentro de
   `conversor-pdf-txt/`, o que dispara o build automaticamente).
3. Quando o workflow terminar, baixe o artefato **ConversorPDFparaTXT-windows**
   gerado na execução — é um `.zip` com a pasta `ConversorPDFparaTXT`
   completa (o `.exe` e o `.cer` do certificado já vêm juntos).

## Como usar o programa

1. Extraia o `.zip` (se baixou pelo GitHub Actions) e abra o
   `ConversorPDFparaTXT.exe` que fica dentro da pasta `ConversorPDFparaTXT`.
2. Escolha o modo: **arquivo(s) individuais** ou **todos os PDFs de uma pasta**.
3. Clique em **Selecionar...** e escolha os PDFs (ou a pasta).
4. Marque ou desmarque a opção de gerar o arquivo consolidado
   (`Documento_Consolidado.txt`).
5. Clique em **Converter** e acompanhe o progresso no log.
   - No modo "arquivos individuais", cada `.txt` é salvo na mesma pasta do
     PDF de origem.
   - No modo "pasta", os `.txt` são salvos em uma subpasta `txt` dentro da
     pasta selecionada.

## Rodando direto do código-fonte (sem gerar .exe)

```bash
pip install -r requirements.txt
python conversor_pdf_txt.py
```

## Observações

- A primeira conversão pode demorar mais, pois o `docling` baixa modelos de
  IA na primeira execução (é necessário acesso à internet nesse momento).

## Assinatura digital do executável (aviso do SmartScreen)

O `.exe` é assinado com um **certificado autoassinado** (não emitido por uma
Autoridade Certificadora reconhecida). Isso deixa o executável com uma
assinatura válida e identificável (autor + integridade do arquivo), mas o
Windows SmartScreen só para de avisar "editor desconhecido" nas máquinas em
que esse certificado for instalado como confiável.

### Confiar no certificado em uma máquina (fazer uma vez por PC)

O arquivo público do certificado está em
`certificado/ConversorPDFparaTXT.cer` (sem a chave privada — seguro para
distribuir).

1. Copie `ConversorPDFparaTXT.cer` para o PC de destino.
2. Rode no PowerShell **como Administrador**:
   ```powershell
   Import-Certificate -FilePath ".\ConversorPDFparaTXT.cer" -CertStoreLocation Cert:\LocalMachine\TrustedPublisher
   Import-Certificate -FilePath ".\ConversorPDFparaTXT.cer" -CertStoreLocation Cert:\LocalMachine\Root
   ```
   (ou, pela interface: duplo clique no `.cer` → **Instalar Certificado** →
   **Máquina Local** → **Colocar todos os certificados no repositório
   seguinte** → escolha **Editores Confiáveis** e depois repita escolhendo
   **Autoridades de Certificação Raiz Confiáveis**.)
3. Depois disso, o `ConversorPDFparaTXT.exe` assinado com esse certificado
   roda nessa máquina sem o aviso do SmartScreen.

Em máquinas onde o certificado não foi instalado, o aviso continua
aparecendo (é o comportamento esperado de um certificado autoassinado) — aí
basta escolher **"Mais informações" → "Executar assim mesmo"**.

### Habilitar a assinatura automática no build do GitHub Actions

O workflow só assina o `.exe` se os secrets abaixo estiverem configurados no
repositório (**Settings → Secrets and variables → Actions → New repository
secret**). Sem eles, o build funciona normalmente, só que sem assinatura.

- `CODE_SIGNING_PFX_BASE64`: certificado + chave privada (`.pfx`) em base64.
- `CODE_SIGNING_PFX_PASSWORD`: senha do `.pfx`.

O certificado (chave privada) não fica no repositório — é sensível e só deve
existir nos secrets do GitHub e, opcionalmente, na sua máquina para builds
locais.

### Assinatura no build local (`build.bat`)

Para o `build.bat` assinar o `.exe` automaticamente, coloque nesta pasta
(esses arquivos **não são versionados**, veja `.gitignore`):

- `certificado\ConversorPDFparaTXT.pfx` — o certificado com a chave privada.
- `certificado\pfx_password.txt` — um arquivo texto só com a senha do `.pfx`.

Se esses arquivos não existirem, o `build.bat` gera o `.exe` normalmente,
apenas sem assinatura.
