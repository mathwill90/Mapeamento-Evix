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
   dist\ConversorPDFparaTXT.exe
   ```

O build pode demorar alguns minutos e o executável final é grande (várias
centenas de MB a alguns GB), pois o `docling` depende de bibliotecas de
IA/OCR (PyTorch, EasyOCR, modelos de layout, etc.).

### Opção 2 — Build automático via GitHub Actions (sem precisar de Python local)

O repositório inclui o workflow
`.github/workflows/build-conversor-pdf-txt.yml`, que compila o `.exe` em um
runner Windows do GitHub.

1. No GitHub, vá em **Actions** → **Build Conversor PDF para TXT (Windows .exe)**.
2. Clique em **Run workflow** (ou apenas dê push de alterações dentro de
   `conversor-pdf-txt/`, o que dispara o build automaticamente).
3. Quando o workflow terminar, baixe o artefato **ConversorPDFparaTXT-windows**
   gerado na execução — ele contém o `ConversorPDFparaTXT.exe`.

## Como usar o programa

1. Abra o `ConversorPDFparaTXT.exe`.
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
- Se antivírus/SmartScreen do Windows alertar sobre o `.exe` (comum em
  executáveis não assinados gerados com PyInstaller), escolha "Executar
  mesmo assim" — o comportamento é esperado para binários sem certificado de
  assinatura de código.
