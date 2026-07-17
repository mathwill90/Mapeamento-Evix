# -*- coding: utf-8 -*-
"""
Conversor de PDF para TXT - Interface Gráfica
Baseado no script original de conversão via docling.

Suporta dois modos:
 - Arquivo(s) individuais: seleciona um ou mais PDFs específicos
 - Pasta: converte todos os PDFs de uma pasta

@author: matheus.willinghoefer
"""

import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class ConversorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de PDF para TXT")
        self.root.geometry("680x560")
        self.root.resizable(True, True)

        self.modo = tk.StringVar(value="arquivos")  # "arquivos" ou "pasta"
        self.itens_selecionados = []  # lista de Path (arquivos ou 1 pasta)
        self.gerar_consolidado = tk.BooleanVar(value=True)
        self.processando = False

        self._montar_interface()

    # ------------------------------------------------------------------
    # Interface
    # ------------------------------------------------------------------
    def _montar_interface(self):
        padding = {"padx": 10, "pady": 6}

        frame_modo = ttk.LabelFrame(self.root, text="O que converter?")
        frame_modo.pack(fill="x", **padding)

        ttk.Radiobutton(
            frame_modo, text="Arquivo(s) PDF individual(is)",
            variable=self.modo, value="arquivos", command=self._limpar_selecao
        ).pack(anchor="w", padx=8, pady=(6, 0))

        ttk.Radiobutton(
            frame_modo, text="Todos os PDFs de uma pasta",
            variable=self.modo, value="pasta", command=self._limpar_selecao
        ).pack(anchor="w", padx=8, pady=(0, 6))

        frame_topo = ttk.Frame(self.root)
        frame_topo.pack(fill="x", **padding)

        ttk.Label(frame_topo, text="Selecionado(s):").pack(anchor="w")

        frame_lista = ttk.Frame(frame_topo)
        frame_lista.pack(fill="x", pady=(4, 0))

        self.entry_selecao = ttk.Entry(frame_lista, state="readonly")
        self.entry_selecao.pack(side="left", fill="x", expand=True)

        ttk.Button(frame_lista, text="Selecionar...", command=self._selecionar).pack(
            side="left", padx=(6, 0)
        )

        ttk.Checkbutton(
            frame_topo,
            text="Gerar também um arquivo consolidado (Documento_Consolidado.txt)",
            variable=self.gerar_consolidado,
        ).pack(anchor="w", pady=(8, 0))

        frame_botoes = ttk.Frame(self.root)
        frame_botoes.pack(fill="x", **padding)

        self.botao_converter = ttk.Button(
            frame_botoes, text="Converter", command=self._iniciar_conversao
        )
        self.botao_converter.pack(side="left")

        self.progress = ttk.Progressbar(frame_botoes, mode="determinate")
        self.progress.pack(side="left", fill="x", expand=True, padx=(10, 0))

        ttk.Label(self.root, text="Log:").pack(anchor="w", padx=10)

        frame_log = ttk.Frame(self.root)
        frame_log.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.texto_log = tk.Text(frame_log, wrap="word", state="disabled")
        scrollbar = ttk.Scrollbar(frame_log, command=self.texto_log.yview)
        self.texto_log.configure(yscrollcommand=scrollbar.set)
        self.texto_log.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        assinatura = ttk.Label(
            self.root,
            text="Desenvolvido por matheus.willinghoefer",
            font=("Segoe UI", 8),
            foreground="#888888",
        )
        assinatura.pack(side="bottom", anchor="e", padx=10, pady=(0, 6))

    # ------------------------------------------------------------------
    # Ações da interface
    # ------------------------------------------------------------------
    def _limpar_selecao(self):
        self.itens_selecionados = []
        self._atualizar_entry_selecao()

    def _atualizar_entry_selecao(self):
        self.entry_selecao.configure(state="normal")
        self.entry_selecao.delete(0, "end")
        if not self.itens_selecionados:
            texto = ""
        elif self.modo.get() == "pasta":
            texto = str(self.itens_selecionados[0])
        else:
            if len(self.itens_selecionados) == 1:
                texto = str(self.itens_selecionados[0])
            else:
                texto = f"{len(self.itens_selecionados)} arquivos selecionados"
        self.entry_selecao.insert(0, texto)
        self.entry_selecao.configure(state="readonly")

    def _selecionar(self):
        if self.modo.get() == "pasta":
            pasta = filedialog.askdirectory(title="Selecione a pasta com os arquivos PDF")
            if pasta:
                self.itens_selecionados = [Path(pasta)]
        else:
            arquivos = filedialog.askopenfilenames(
                title="Selecione um ou mais arquivos PDF",
                filetypes=[("Arquivos PDF", "*.pdf")],
            )
            if arquivos:
                self.itens_selecionados = [Path(a) for a in arquivos]

        self._atualizar_entry_selecao()

    def _log(self, mensagem):
        def atualizar():
            self.texto_log.configure(state="normal")
            self.texto_log.insert("end", mensagem + "\n")
            self.texto_log.see("end")
            self.texto_log.configure(state="disabled")

        self.root.after(0, atualizar)

    def _iniciar_conversao(self):
        if self.processando:
            return

        if not self.itens_selecionados:
            messagebox.showwarning("Atenção", "Selecione arquivo(s) ou uma pasta primeiro.")
            return

        self.processando = True
        self.botao_converter.configure(state="disabled")
        self.texto_log.configure(state="normal")
        self.texto_log.delete("1.0", "end")
        self.texto_log.configure(state="disabled")
        self.progress["value"] = 0

        thread = threading.Thread(target=self._converter, daemon=True)
        thread.start()

    def _finalizar(self, sucesso=True):
        def atualizar():
            self.processando = False
            self.botao_converter.configure(state="normal")
            if sucesso:
                messagebox.showinfo("Concluído", "Conversão finalizada com sucesso!")

        self.root.after(0, atualizar)

    # ------------------------------------------------------------------
    # Lógica de conversão
    # ------------------------------------------------------------------
    def _converter(self):
        try:
            from docling.document_converter import DocumentConverter

            # Monta a lista de arquivos PDF a converter e define pasta(s) de saída
            if self.modo.get() == "pasta":
                pasta_entrada = self.itens_selecionados[0]
                arquivos_pdf = sorted(pasta_entrada.glob("*.pdf"))
                pasta_saida_padrao = pasta_entrada / "txt"
                pasta_saida_padrao.mkdir(exist_ok=True)
                # Todos os arquivos vão para a mesma pasta "txt"
                mapa_saida = {pdf: pasta_saida_padrao for pdf in arquivos_pdf}
                pasta_consolidado = pasta_saida_padrao
            else:
                arquivos_pdf = list(self.itens_selecionados)
                # Cada arquivo salva o .txt na própria pasta onde ele está
                mapa_saida = {pdf: pdf.parent for pdf in arquivos_pdf}
                pasta_consolidado = arquivos_pdf[0].parent if arquivos_pdf else None

            if not arquivos_pdf:
                self._log("Nenhum arquivo PDF encontrado.")
                self._finalizar(sucesso=False)
                return

            self._log(f"Encontrados {len(arquivos_pdf)} arquivo(s) PDF. Iniciando conversão...\n")
            self.root.after(0, lambda: self.progress.configure(maximum=len(arquivos_pdf)))

            converter = DocumentConverter()
            arquivos_txt_gerados = []

            for i, arquivo_pdf in enumerate(arquivos_pdf, start=1):
                try:
                    self._log(f"Convertendo: {arquivo_pdf.name}")
                    resultado = converter.convert(str(arquivo_pdf))
                    texto_convertido = resultado.document.export_to_markdown()

                    pasta_saida = mapa_saida[arquivo_pdf]
                    caminho_saida = pasta_saida / (arquivo_pdf.stem + ".txt")

                    with open(caminho_saida, "w", encoding="utf-8") as f:
                        f.write(texto_convertido)

                    arquivos_txt_gerados.append(caminho_saida)
                    self._log(f"  -> Salvo: {caminho_saida}")
                except Exception as e:
                    self._log(f"  -> ERRO ao processar {arquivo_pdf.name}: {e}")
                finally:
                    self.root.after(0, lambda v=i: self.progress.configure(value=v))

            if self.gerar_consolidado.get() and arquivos_txt_gerados and pasta_consolidado:
                self._log("\nGerando arquivo consolidado...")
                arquivo_geral = pasta_consolidado / "Documento_Consolidado.txt"

                with open(arquivo_geral, "w", encoding="utf-8") as output_file:
                    for arquivo_txt in arquivos_txt_gerados:
                        with open(arquivo_txt, "r", encoding="utf-8") as input_file:
                            output_file.write(f"\n\n=== {arquivo_txt.stem} ===\n\n")
                            output_file.write(input_file.read())
                            output_file.write("\n\n")

                self._log(f"Arquivo consolidado gerado em: {arquivo_geral}")

            self._log("\nProcesso finalizado.")
            self._finalizar(sucesso=True)

        except ImportError:
            self._log(
                "ERRO: a biblioteca 'docling' não foi encontrada. "
                "Instale com: pip install docling"
            )
            self._finalizar(sucesso=False)
        except Exception as e:
            self._log(f"ERRO inesperado: {e}")
            self._finalizar(sucesso=False)


def main():
    root = tk.Tk()
    try:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
        elif "clam" in style.theme_names():
            style.theme_use("clam")
    except Exception:
        pass

    ConversorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
