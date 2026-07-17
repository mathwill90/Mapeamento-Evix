@echo off
REM Gera o executavel do Conversor de PDF para TXT.
REM Deve ser executado no Windows, dentro desta pasta, com Python instalado.

echo ============================================
echo  Conversor PDF -^> TXT - Build do executavel
echo ============================================

python -m venv venv
call venv\Scripts\activate.bat

echo.
echo Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Gerando executavel (isso pode demorar alguns minutos)...
pyinstaller --noconfirm --onefile --windowed ^
  --name "ConversorPDFparaTXT" ^
  --collect-all docling ^
  --collect-all docling_core ^
  --collect-all docling_parse ^
  --collect-all docling_ibm_models ^
  --collect-all easyocr ^
  --collect-all rapidocr ^
  conversor_pdf_txt.py

echo.
if exist dist\ConversorPDFparaTXT.exe (
    echo Executavel gerado com sucesso em: dist\ConversorPDFparaTXT.exe
) else (
    echo Falha ao gerar o executavel. Verifique as mensagens de erro acima.
)

pause
