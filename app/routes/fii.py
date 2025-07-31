from flask import Blueprint, request, jsonify, render_template, send_file, current_app
import pandas as pd
import os
import zipfile
import io

fii_bp = Blueprint("fii", __name__)

@fii_bp.route("/dados", methods=["GET"])
def dados_dinamicos():
    nome_arquivo = request.args.get("arquivo")

    if not nome_arquivo:
        arquivos = os.listdir("output/dados_projeto")
        arquivos = [a.replace(".csv", "") for a in arquivos if a.endswith(".csv")]
        return jsonify({"arquivos_disponiveis": arquivos})

    caminho = f"output/dados_projeto/{nome_arquivo}.csv"
    if not os.path.exists(caminho):
        return jsonify({"erro": f"Arquivo '{nome_arquivo}' não encontrado"}), 404

    df = pd.read_csv(caminho, sep="\t", encoding="latin1", engine="python", on_bad_lines='skip')
    return jsonify(df.to_dict(orient="records"))


# Rota HTML para listar todos os arquivos disponíveis
@fii_bp.route("/ver-dados")
def ver_dados():
    try:
        arquivos = [f.replace(".csv", "") for f in os.listdir("output/dados_projeto") if f.endswith(".csv")]
    except FileNotFoundError:
        arquivos = []
    return render_template("visualizar.html", arquivos=arquivos)

@fii_bp.route("/download/<nome_arquivo>")
def download_arquivo(nome_arquivo):
    pasta = current_app.config.get('PASTA_DADOS', 'output/dados_projeto')
    nome_completo = f"{nome_arquivo}.csv"
    caminho_arquivo = os.path.join(pasta, nome_completo)

    if not os.path.exists(caminho_arquivo):
        return jsonify({"erro": "Arquivo não encontrado"}), 404

    return send_file(caminho_arquivo, as_attachment=True)

@fii_bp.route("/download-todos")
def download_todos_csvs():
    pasta = "output/dados_projeto"
    arquivos_csv = [f for f in os.listdir(pasta) if f.endswith(".csv")]

    if not arquivos_csv:
        return jsonify({"erro": "Nenhum arquivo CSV encontrado"}), 404

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for nome in arquivos_csv:
            caminho_completo = os.path.join(pasta, nome)
            zip_file.write(caminho_completo, arcname=nome)

    zip_buffer.seek(0)

    return send_file(
        zip_buffer,
        mimetype="application/zip",
        as_attachment=True,
        download_name="todos_arquivos.zip"
    )

@fii_bp.route("/ver-dados/<nome_arquivo>")
def ver_arquivo(nome_arquivo):
    caminho = f"output/dados_projeto/{nome_arquivo}.csv"
    if not os.path.exists(caminho):
        return f"Arquivo '{nome_arquivo}' não encontrado", 404

    df = pd.read_csv(caminho, sep="\t", encoding="latin1", engine="python", on_bad_lines='skip')
    
    # Retorna uma página com a tabela HTML + botão para JSON
    return render_template("ver_arquivo.html", nome_arquivo=nome_arquivo, tabela=df.to_html(index=False))
