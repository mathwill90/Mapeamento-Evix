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
REM Modo "pasta" (sem --onefile): abre muito mais rapido, pois nao precisa
REM descompactar tudo em uma pasta temporaria a cada execucao.
pyinstaller --noconfirm --onedir --windowed ^
  --name "ConversorPDFparaTXT" ^
  --collect-all docling ^
  --collect-all docling_core ^
  --collect-all docling_parse ^
  --collect-all docling_ibm_models ^
  --collect-all easyocr ^
  --collect-all rapidocr ^
  conversor_pdf_txt.py

echo.
if not exist dist\ConversorPDFparaTXT\ConversorPDFparaTXT.exe (
    echo Falha ao gerar o executavel. Verifique as mensagens de erro acima.
    pause
    exit /b 1
)

echo Executavel gerado com sucesso em: dist\ConversorPDFparaTXT\ConversorPDFparaTXT.exe
echo (mantenha o .exe dentro dessa pasta - ele depende dos outros arquivos ali)

if exist certificado\ConversorPDFparaTXT.pfx (
    echo.
    echo Assinando o executavel com o certificado local...
    powershell -NoProfile -ExecutionPolicy Bypass -Command ^
      "$securePwd = Get-Content 'certificado\pfx_password.txt' -Raw | ConvertTo-SecureString -AsPlainText -Force; $cert = Get-PfxCertificate -FilePath 'certificado\ConversorPDFparaTXT.pfx' -Password $securePwd; Set-AuthenticodeSignature -FilePath 'dist\ConversorPDFparaTXT\ConversorPDFparaTXT.exe' -Certificate $cert -TimestampServer 'http://timestamp.digicert.com' -HashAlgorithm SHA256 | Format-List"
    copy /y certificado\ConversorPDFparaTXT.cer dist\ConversorPDFparaTXT\ >nul
) else (
    echo.
    echo Certificado local nao encontrado em certificado\ConversorPDFparaTXT.pfx - executavel gerado sem assinatura.
    echo Veja o README.md para gerar/instalar o certificado de assinatura.
)

pause
