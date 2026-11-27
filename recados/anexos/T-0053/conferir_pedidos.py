# -*- coding: utf-8 -*-
"""
conferir_pedidos.py - conferencia SO DE LEITURA do Farol de Pedidos (pv_pedidos)

Pedido do Alexandre: "valie o faturado e os pedidos em aberto. valores e qtd".

Rode NA PASTA DE PRODUCAO (onde estao RELATORIOS\\ e os .py do robo):

    python -B conferir_pedidos.py
    (opcoes: --pasta <pasta>  --mes AAAA-MM  --hoje AAAA-MM-DD
             --lote AAAAMMDDTHHMMSS  --pacote <arquivo .json/.json.gz>)

Faz duas contas para o mes (padrao: o mes corrente, fuso de Manaus):
  (a) FAROL  - relatorios_nucleo.montar("pv_pedidos", ...) com os parametros
      do pacote web (bap_automation.params_farol_web) e o recorte por estado
      do pacote web (bap_automation._recortes_do_farol_web =
      recortes_farol_por_uf na tabela "Pedidos", coluna FILIAL);
  (b) FONTE  - direto da aba ftPedidos (a fotografia RELATORIOS\\DADOS que o
      robo usa, ou a TABELA_BAP.xlsx) e da dClientesBap, com as regras
      escritas aqui, sem usar a funcao do farol:
        RN-GER-002 faturado = VND - DEV, pela data da NF (VND: DATA_NF;
                   DEV: D2_EMISSAO, a emissao da nota de devolucao);
        RN-GER-004 CNPJs internos (FRW / BAP AUTOPARTS / PMZ DISTRIBUIDORA)
                   fora, pelo cadastro do codigo e pela razao da linha;
        RN-GER-013 pedido/nota de cliente "NAO LOCALIZADO NA BASE" fora;
        RN-GER-006 estado = filial da nota (do pedido, no em aberto);
        em aberto = a carteira de agora (todas as linhas VEA), por pedido.
      A conta 000040 (vendedor de teste, RN-GER-005) aparece numa linha
      propria: o farol nao a tira; a decisao de tirar e do Alexandre.
  e, se houver, (c) PACOTE - o pacote web gravado no PC (so a simulacao do
      robo grava: %TEMP%\\BAP_PACOTE_WEB\\<lote>\\pv_pedidos.json.gz ou
      %TEMP%\\BAP_PACOTE_WEB\\pacote_web_AAAAMM.json; o envio normal nao
      guarda copia).
  e, informativo, o faturado do Farol de Metas / Painel por estado
      (relatorios_nucleo.por_filial_da_nota).

GARANTIAS
  - nao grava NADA: uma trava no proprio processo recusa toda abertura de
    arquivo para escrita, mkdir, rename, replace, remove (o cache
    _CACHE_RELATORIOS do robo nao e gravado; a conta fica so mais lenta) e
    nao gera __pycache__;
  - sem rede (socket bloqueado);
  - nao le tomtom_config*.json, google_maps_config*.json,
    visitas_config.json, **/auth/**, .env (a trava recusa a leitura);
  - a saida so tem totais e codigos de UF (nenhum nome, CNPJ, telefone ou
    e-mail de cliente ou vendedor).
  Pode rodar com o robo ligado: so le. Se o robo trocar a TABELA_BAP no meio,
  rode de novo.

Saida: 0 = tudo bate; 1 = ha diferenca (lista com o motivo provavel);
       2 = nao deu para conferir.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True          # nada de __pycache__ na pasta

import argparse                          # noqa: E402
import builtins                          # noqa: E402
import csv                               # noqa: E402
import fnmatch                           # noqa: E402
import gzip                              # noqa: E402
import io                                # noqa: E402
import json                              # noqa: E402
import os                                # noqa: E402
import re                                # noqa: E402
import shutil                            # noqa: E402
import socket                            # noqa: E402
import tempfile                          # noqa: E402
import time                              # noqa: E402
import unicodedata                       # noqa: E402
from collections import Counter, defaultdict  # noqa: E402
from datetime import date, datetime, timedelta, timezone  # noqa: E402
from pathlib import Path                 # noqa: E402

try:                                     # console do Windows / redirecionado
    sys.stdout.reconfigure(errors="replace")
except Exception:                        # noqa: BLE001
    pass

# =============================================================================
# 1. A TRAVA: so leitura, sem rede, sem os arquivos proibidos
# =============================================================================
BARRADAS: Counter = Counter()           # o que a trava recusou (so o nome)
_PROIBIDOS = ("tomtom_config*.json", "google_maps_config*.json",
              "visitas_config.json", ".env")


def _proibido(caminho) -> bool:
    try:
        p = Path(os.fsdecode(caminho))
    except Exception:                    # noqa: BLE001
        return False
    nome = p.name.lower()
    if any(fnmatch.fnmatch(nome, pat) for pat in _PROIBIDOS):
        return True
    return "auth" in [x.lower() for x in p.parts[:-1]]


def _barrar(oque, caminho=""):
    try:
        nome = Path(os.fsdecode(caminho)).name if caminho != "" else ""
    except Exception:                    # noqa: BLE001
        nome = "?"
    BARRADAS[f"{oque} {nome}".strip()] += 1
    raise PermissionError(f"conferir_pedidos: so leitura ({oque})")


def instalar_trava():
    # a pasta temporaria sem o teste de escrita do tempfile
    if tempfile.tempdir is None:
        cands = tempfile._candidate_tempdir_list()  # noqa: SLF001
        tempfile.tempdir = cands[0] if cands else "."
    _open = builtins.open

    def open_so_leitura(file, mode="r", *a, **k):
        if not isinstance(file, int):
            if any(c in str(mode) for c in "wax+"):
                _barrar("escrita", file)
            if _proibido(file):
                _barrar("leitura proibida", file)
        return _open(file, mode, *a, **k)
    builtins.open = open_so_leitura
    io.open = open_so_leitura

    _osopen = os.open
    _w = (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC)

    def osopen_so_leitura(path, flags, *a, **k):
        if flags & _w:
            _barrar("escrita", path)
        if _proibido(path):
            _barrar("leitura proibida", path)
        return _osopen(path, flags, *a, **k)
    os.open = osopen_so_leitura

    def nega(nome):
        def f(*a, **k):
            _barrar(nome, a[0] if a else "")
        return f
    for mod, nomes in ((os, ("mkdir", "makedirs", "rename", "renames",
                             "replace", "remove", "unlink", "rmdir",
                             "removedirs", "utime", "chmod", "truncate",
                             "symlink", "link")),
                       (shutil, ("copy", "copy2", "copyfile", "copytree",
                                 "move", "rmtree", "copystat",
                                 "copymode"))):
        for n in nomes:
            if hasattr(mod, n):
                setattr(mod, n, nega(f"{mod.__name__}.{n}"))

    def sem_rede(*a, **k):
        BARRADAS["rede"] += 1
        raise OSError("conferir_pedidos: sem rede")
    socket.socket.connect = sem_rede
    socket.socket.connect_ex = sem_rede
    socket.create_connection = sem_rede
    socket.getaddrinfo = sem_rede


# =============================================================================
# 2. MIUDEZAS (proprias, sem o codigo do robo)
# =============================================================================
FILIAL_UF = {"0101002": "AM", "0101004": "RR", "0101005": "PA",
             "0101007": "PA", "0101006": "MA", "0101003": "AP",
             "0101001": "MT"}                                  # RN-GER-006
ORDEM_UF = ["PA", "MA", "AM", "RR", "AP", "MT"]
MESES = ["", "JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET",
         "OUT", "NOV", "DEZ"]
CONTA_TESTE = "000040"                                         # RN-GER-005
TOL_CARTAO = 1.0       # o cartao do farol mostra R$ sem centavos
TOL_EXATO = 0.01


def sem_acento(s) -> str:
    s = unicodedata.normalize("NFKD", str(s or ""))
    return "".join(c for c in s if not unicodedata.combining(c)).upper().strip()


def txt(v) -> str:
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return str(v).strip()


def num(v) -> float:
    if v is None or v == "":
        return 0.0
    if isinstance(v, bool):
        return float(v)
    if isinstance(v, (int, float)):
        return float(v)
    t = str(v).strip().replace("R$", "").replace(" ", "")
    if "," in t:
        t = t.replace(".", "").replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return 0.0


def dia(v):
    if v in (None, ""):
        return None
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, date):
        return v
    if isinstance(v, (int, float)) and 20000 < v < 80000:     # serial Excel
        return date(1899, 12, 30) + timedelta(days=int(v))
    t = str(v).strip()
    for fmt, n in (("%d-%m-%Y", 10), ("%d/%m/%Y", 10), ("%Y-%m-%d", 10),
                   ("%Y%m%d", 8), ("%d/%m/%y", 8)):
        try:
            return datetime.strptime(t[:n], fmt).date()
        except ValueError:
            continue
    return None


def uf_da_filial(f) -> str:
    d = re.sub(r"\D", "", txt(f))
    return FILIAL_UF.get(d.zfill(7)[-7:], "") if d else ""


def cod_cliente(v) -> str:
    t = txt(v)
    return t.zfill(6) if t.isdigit() else t


def cod_vend(v) -> str:
    t = txt(v)
    return t.zfill(6) if t.isdigit() else t


_RE_INTERNO = re.compile(r"\bFRW\b|BAP\s*AUTO\s*PARTS|PMZ\s+DISTRIBUIDORA")


def interno(*nomes) -> bool:                                   # RN-GER-004
    return bool(_RE_INTERNO.search(sem_acento(" ".join(txt(n) for n in nomes))))


def fora_da_base(razao) -> bool:                               # RN-GER-013
    return sem_acento(razao) == "NAO LOCALIZADO NA BASE"


def brl(v, casas=2) -> str:
    if v is None:
        return "-"
    s = f"{v:,.{casas}f}"
    return s.replace(",", "~").replace(".", ",").replace("~", ".")


def de_brl(s):
    """'R$ 1.234.567' -> 1234567.0; '12' -> 12.0; vazio/traco -> None."""
    if s is None:
        return None
    if isinstance(s, (int, float)):
        return float(s)
    t = str(s).replace("R$", "").replace("\xa0", " ").strip()
    m = re.search(r"-?[\d.]+(?:,\d+)?", t)
    if not m:
        return None
    return float(m.group(0).replace(".", "").replace(",", "."))


# =============================================================================
# 3. A FONTE: ftPedidos e dClientesBap, como o robo deixou
# =============================================================================
def _do_cru(t, cod):
    if cod == "s":
        return t
    if cod == "i":
        return int(t)
    if cod == "f":
        return float(t)
    if cod == "d":
        return datetime.fromisoformat(t)
    if cod == "b":
        return t == "1"
    return t                                  # hora / duracao: nao uso


def _ler_csv_gz(arq: Path, quero):
    """Linhas (dict so das colunas `quero`) de uma aba da fotografia."""
    with gzip.open(arq, "rt", encoding="utf-8", newline="") as f:
        rd = csv.reader(f, delimiter=";")
        cab = next(rd)
        tipos = next(rd)
        ix = {c: cab.index(c) for c in quero if c in cab}
        for campos in rd:
            d = {}
            for c, j in ix.items():
                v = campos[j] if j < len(campos) else ""
                if v == "":
                    d[c] = None
                elif v[0] == "~":
                    cod, _, resto = v[1:].partition(":")
                    d[c] = _do_cru(resto, cod)
                else:
                    d[c] = _do_cru(v, tipos[j])
            yield d


def _ler_xlsx(arq: Path, aba, quero):
    from openpyxl import load_workbook        # noqa: PLC0415
    wb = load_workbook(arq, read_only=True, data_only=True)
    try:
        it = wb[aba].iter_rows(values_only=True)
        cab = [txt(c) for c in next(it)]
        ix = {c: cab.index(c) for c in quero if c in cab}
        for r in it:
            yield {c: (r[j] if j < len(r) else None) for c, j in ix.items()}
    finally:
        wb.close()


def origem_da_fonte(raiz: Path):
    """('fotografia', pasta, estado) se a fotografia RELATORIOS\\DADOS vale
    para a TABELA_BAP (o mesmo criterio do leitor do robo,
    dados_bap.fotografia_para), senao ('xlsx', arquivo, None)."""
    tabela = raiz / "RELATORIOS" / "TABELA_BAP.xlsx"
    if not tabela.exists():
        raise FileNotFoundError("RELATORIOS/TABELA_BAP.xlsx nao existe nesta "
                                "pasta (rode na pasta de producao).")
    try:
        import dados_bap                      # noqa: PLC0415
        est = dados_bap.fotografia_para(tabela)
    except Exception:                         # noqa: BLE001
        est = None
    if est:
        return "fotografia", Path(est.get("_pasta") or
                                  tabela.parent / "DADOS"), est
    return "xlsx", tabela, None


def linhas_da_aba(origem, aba, quero):
    tipo, onde, est = origem
    if tipo == "fotografia":
        arq = Path(onde) / est["abas"][aba]["arquivo"]
        return _ler_csv_gz(arq, quero)
    return _ler_xlsx(onde, aba, quero)


COLS_PED = ("TIPO", "D2_FILIAL", "D2_CLIENTE", "C5_VEND1", "D2_EMISSAO",
            "D2_DOC", "D2_SERIE", "D2_PEDIDO", "NUM_PEDIDO", "DATA_NF",
            "DATA_DEV", "VALOR TOTAL", "RAZÃO_SOCIAL")
COLS_CLI = ("A1_COD", "A1_NOME", "A1_NREDUZ")


def _novo():
    return {"vnd": 0.0, "dev": 0.0, "notas": set(), "peds_fat": set(),
            "abe_val": 0.0, "abe_peds": set()}


def conta_fonte(raiz: Path, ano: int, mes: int, corrente: bool):
    origem = origem_da_fonte(raiz)
    # RN-GER-004: codigo interno = alguma loja do codigo com nome/fantasia
    # do grupo
    lojas = defaultdict(list)
    for r in linhas_da_aba(origem, "dClientesBap", COLS_CLI):
        c = cod_cliente(r.get("A1_COD"))
        if c:
            lojas[c].append(interno(r.get("A1_NOME"), r.get("A1_NREDUZ")))
    cods_internos = {c for c, xs in lojas.items() if any(xs)}
    cods_mistos = {c for c, xs in lojas.items() if any(xs) and not all(xs)}

    def no_mes(d):
        return d is not None and d.year == ano and d.month == mes

    vnd, dev, vea = defaultdict(list), [], defaultdict(list)
    linhas_lidas = Counter()
    max_nf = None
    for r in linhas_da_aba(origem, "ftPedidos", COLS_PED):
        tipo = txt(r.get("TIPO")).upper()
        if tipo not in ("VND", "VEA", "DEV"):
            continue
        linhas_lidas[tipo] += 1
        fil = re.sub(r"\D", "", txt(r.get("D2_FILIAL"))).zfill(7)[-7:]
        it = {"fil": fil, "uf": uf_da_filial(fil),
              "cli": cod_cliente(r.get("D2_CLIENTE")),
              "vend": cod_vend(r.get("C5_VEND1")),
              "razao": r.get("RAZÃO_SOCIAL"),
              "valor": num(r.get("VALOR TOTAL"))}
        it["interno"] = it["cli"] in cods_internos or interno(it["razao"])
        it["misto"] = it["cli"] in cods_mistos
        it["fora"] = fora_da_base(it["razao"])
        if tipo == "VND":
            it["dnf"] = dia(r.get("DATA_NF")) or dia(r.get("D2_EMISSAO"))
            it["demi"] = dia(r.get("D2_EMISSAO"))
            if it["dnf"] and (max_nf is None or it["dnf"] > max_nf):
                max_nf = it["dnf"]
            if no_mes(it["dnf"]):
                it["ped"] = txt(r.get("D2_PEDIDO")) or txt(r.get("NUM_PEDIDO"))
                vnd[(fil, txt(r.get("D2_DOC")), txt(r.get("D2_SERIE")))] \
                    .append(it)
        elif tipo == "DEV":
            it["dnf"] = dia(r.get("D2_EMISSAO")) or dia(r.get("DATA_NF"))
            it["ddev"] = dia(r.get("DATA_DEV"))
            it["doc"] = txt(r.get("D2_DOC"))
            if no_mes(it["dnf"]) or no_mes(it["ddev"]):
                dev.append(it)
        else:                                               # VEA
            ped = txt(r.get("NUM_PEDIDO")) or txt(r.get("D2_DOC"))
            vea[(fil, ped)].append(it)

    res = defaultdict(_novo)
    diag = defaultdict(Counter)          # por escopo: os candidatos a motivo

    def esc(uf):
        return ("TOTAL", uf) if uf else ("TOTAL", "(filial sem UF)")

    pares_venda = defaultdict(set)       # escopo -> {(filial, vendedor)}
    for (fil, nf, serie), itens in vnd.items():
        fora = any(i["fora"] for i in itens)
        intern = [i for i in itens if i["interno"]]
        ok = [i for i in itens if not i["interno"]]
        valor_ok = sum(i["valor"] for i in ok)
        for e in esc(itens[0]["uf"]):
            if intern:
                diag[e]["vnd_internos_R$"] += sum(i["valor"] for i in intern)
            if not ok:
                continue
            if fora:                                         # RN-GER-013
                diag[e]["vnd_fora_base_R$"] += valor_ok
                diag[e]["vnd_fora_base_notas"] += 1
                continue
            x = res[e]
            x["vnd"] += valor_ok
            x["notas"].add((fil, nf, serie))
            ped = ok[0]["ped"]
            x["peds_fat"].add((fil, ped or f"NF:{nf}/{serie}"))
            if not ped:
                diag[e]["notas_sem_pedido"] += 1
            if any(i["vend"] == CONTA_TESTE for i in ok):
                diag[e]["vnd_000040_R$"] += sum(
                    i["valor"] for i in ok if i["vend"] == CONTA_TESTE)
                diag[e]["vnd_000040_notas"] += 1
            if any(i["misto"] for i in ok):
                diag[e]["vnd_cod_misto_R$"] += sum(
                    i["valor"] for i in ok if i["misto"])
            if any(i["demi"] and not no_mes(i["demi"]) for i in ok):
                diag[e]["vnd_emissao_outro_mes_R$"] += sum(
                    i["valor"] for i in ok
                    if i["demi"] and not no_mes(i["demi"]))
            pares_venda[e] |= {(fil, i["vend"]) for i in ok}
    for i in dev:
        v = abs(i["valor"])
        for e in esc(i["uf"]):
            if not no_mes(i["dnf"]):                 # so a DATA_DEV no mes
                if not i["interno"] and not i["fora"]:
                    diag[e]["dev_data_dev_no_mes_emissao_fora_R$"] += v
                continue
            if i["ddev"] and not no_mes(i["ddev"]) and not i["interno"] \
                    and not i["fora"]:
                diag[e]["dev_emissao_no_mes_data_dev_fora_R$"] += v
            if i["interno"]:
                diag[e]["dev_internos_R$"] += v
                continue
            if i["fora"]:
                diag[e]["dev_fora_base_R$"] += v
                continue
            res[e]["dev"] += v
            if i["vend"] == CONTA_TESTE:
                diag[e]["dev_000040_R$"] += v
    notas_sem_par = defaultdict(set)
    for i in dev:                       # devolucao de quem nao vendeu no mes
        if not no_mes(i["dnf"]) or i["interno"] or i["fora"]:
            continue
        for e in esc(i["uf"]):
            if (i["fil"], i["vend"]) not in pares_venda[e]:
                diag[e]["dev_sem_venda_do_par_filial_vendedor_R$"] += \
                    abs(i["valor"])
                notas_sem_par[e].add((i["fil"], i["doc"]))
    for e, ns in notas_sem_par.items():
        diag[e]["dev_sem_venda_do_par_filial_vendedor_notas"] = len(ns)
    if corrente:
        for (fil, ped), itens in vea.items():
            fora = any(i["fora"] for i in itens)
            ok = [i for i in itens if not i["interno"]]
            for e in esc(itens[0]["uf"]):
                if not ok:
                    diag[e]["abe_internos_pedidos"] += 1
                    continue
                v = sum(i["valor"] for i in ok)
                if fora:
                    diag[e]["abe_fora_base_R$"] += v
                    diag[e]["abe_fora_base_pedidos"] += 1
                    continue
                res[e]["abe_val"] += v
                res[e]["abe_peds"].add((fil, ped))
                if any(i["vend"] == CONTA_TESTE for i in ok):
                    diag[e]["abe_000040_R$"] += sum(
                        i["valor"] for i in ok if i["vend"] == CONTA_TESTE)
                    diag[e]["abe_000040_pedidos"] += 1
    saida = {}
    for e, x in res.items():
        saida[e] = {"fat_liq": x["vnd"] - x["dev"], "fat_bruto": x["vnd"],
                    "dev": x["dev"], "fat_notas": len(x["notas"]),
                    "fat_pedidos": len(x["peds_fat"]),
                    "abe_val": x["abe_val"] if corrente else None,
                    "abe_qtd": len(x["abe_peds"]) if corrente else None}
    return {"por": saida, "diag": diag, "origem": origem,
            "lidas": linhas_lidas, "max_nf": max_nf}


# =============================================================================
# 4. O FAROL: as mesmas funcoes do robo (Farol de Pedidos e pacote web)
# =============================================================================
SIT_FAT = ("FATURADO", "ENTREGUE", "DEVOLVIDO", "CANCELADO")


def ler_cartoes(kpis):
    """Os numeros dos cartoes (como a tela mostra)."""
    k = {x.get("rotulo"): x for x in (kpis or []) if isinstance(x, dict)}
    out = {}
    if "Faturado" in k:
        out["fat_liq"] = de_brl(k["Faturado"].get("valor"))
        det = str(k["Faturado"].get("detalhe") or "")
        m = re.search(r"([\d.]+)\s+notas", det)
        out["fat_notas"] = de_brl(m.group(1)) if m else None
        m = re.search(r"devolu\w+\s+(R\$\s*[-\d.,]+)", det)
        out["dev"] = de_brl(m.group(1)) if m else 0.0
    if "Em aberto" in k:
        out["abe_qtd"] = de_brl(k["Em aberto"].get("valor"))
        det = str(k["Em aberto"].get("detalhe") or "")
        out["abe_val"] = de_brl(det) if "R$" in det else None
    elif "R$" in k and "Pedidos" in k:     # cartoes do BI: so em aberto
        out.update(fat_liq=0.0, fat_notas=0.0, dev=0.0,
                   abe_qtd=de_brl(k["Pedidos"].get("valor")),
                   abe_val=de_brl(k["R$"].get("valor")))
    return out


def conta_farol(raiz: Path, ano: int, mes: int, hoje: date):
    import relatorios_nucleo as rn            # noqa: PLC0415
    avisos = []
    try:
        import bap_automation as ba           # noqa: PLC0415
    except Exception as erro:                 # noqa: BLE001
        ba = None
        avisos.append(f"bap_automation nao importou ({type(erro).__name__}); "
                      "recorte por UF pelo relatorios_nucleo")
    params = (ba.params_farol_web("pv_pedidos", ano, mes) if ba
              else {"ANO": str(ano), "MÊS": str(mes)})
    t0 = time.time()
    rel = rn.montar("pv_pedidos", raiz, hoje=hoje, params=dict(params))
    seg = time.time() - t0
    recortes = {}
    if ba is not None and hasattr(ba, "_recortes_do_farol_web"):
        recortes = ba._recortes_do_farol_web("pv_pedidos", rel)  # noqa: SLF001
    elif ba is not None:
        recortes = ba.recortes_farol_por_uf(rel, "Pedidos", "FILIAL")
    cartoes = {"TOTAL": ler_cartoes(rel.get("kpis"))}
    for uf, x in (recortes or {}).items():
        cartoes[uf] = ler_cartoes((x or {}).get("kpis"))
    # a tabela "Pedidos": as linhas que os cartoes contam (o mes, sem fora
    # da base), para o valor exato e a quantidade de pedidos faturados
    tab = next(t for t in rel["tabelas"] if t.get("titulo") == "Pedidos")
    nomes = [c.get("nome") if isinstance(c, dict) else c
             for c in tab["colunas"]]
    ix = {n: nomes.index(n) for n in ("SITUAÇÃO", "MÊS", "FILIAL", "PEDIDO",
                                       "NF", "R$ VENDA", "RAZÃO SOCIAL")}
    rot = f"{MESES[mes]}/{ano % 100:02d}"
    tabela = defaultdict(lambda: {"fat_bruto": 0.0, "notas": 0,
                                  "peds": set(), "abe_val": 0.0, "abe_qtd": 0})
    for ln in tab["linhas"]:
        if str(ln[ix["MÊS"]]) != rot or \
                ln[ix["RAZÃO SOCIAL"]] == rn.NOME_FORA_DA_BASE:
            continue
        uf = rn.uf_do_nome_da_filial(ln[ix["FILIAL"]]) or "(filial sem UF)"
        sit = ln[ix["SITUAÇÃO"]]
        v = float(ln[ix["R$ VENDA"]] or 0)
        for e in ("TOTAL", uf):
            t = tabela[e]
            if sit in SIT_FAT:
                t["fat_bruto"] += v
                t["notas"] += 1
                t["peds"].add((ln[ix["FILIAL"]], ln[ix["PEDIDO"]]
                               or f"NF:{ln[ix['NF']]}"))
            elif sit == "EM ABERTO":
                t["abe_val"] += v
                t["abe_qtd"] += 1
    por = {}
    coerencia = []                 # cartao x tabela do proprio farol
    for e in set(cartoes) | set(tabela):
        c, t = cartoes.get(e, {}), tabela.get(e)
        t = t or {"fat_bruto": 0.0, "notas": 0, "peds": set(),
                  "abe_val": 0.0, "abe_qtd": 0}
        por[e] = {"fat_liq": c.get("fat_liq"), "fat_bruto": t["fat_bruto"],
                  "dev": c.get("dev"), "fat_notas": c.get("fat_notas"),
                  "fat_pedidos": len(t["peds"]), "abe_val": t["abe_val"],
                  "abe_qtd": c.get("abe_qtd")}
        if e not in cartoes:
            coerencia.append(f"{e}: o farol tem linhas, mas o pacote web nao "
                             "tem cartoes para este estado")
            continue
        if c.get("fat_notas") is not None and c["fat_notas"] != t["notas"]:
            coerencia.append(f"{e}: cartao Faturado diz {c['fat_notas']:.0f} "
                             f"notas, a tabela tem {t['notas']}")
        if c.get("abe_qtd") is not None and c["abe_qtd"] != t["abe_qtd"]:
            coerencia.append(f"{e}: cartao Em aberto diz {c['abe_qtd']:.0f}, "
                             f"a tabela tem {t['abe_qtd']}")
        if c.get("abe_val") is not None and \
                abs(c["abe_val"] - t["abe_val"]) > TOL_CARTAO:
            coerencia.append(f"{e}: cartao Em aberto R$ {brl(c['abe_val'], 0)}"
                             f", a tabela R$ {brl(t['abe_val'])}")
        if c.get("fat_liq") is not None and c.get("dev") is not None and \
                abs(t["fat_bruto"] - c["dev"] - c["fat_liq"]) > 2 * TOL_CARTAO:
            coerencia.append(f"{e}: tabela bruto - devolucoes do cartao "
                             "nao da o Faturado do cartao")
    # (informativo) o Farol de Metas / Painel: faturado e notas por estado
    metas = {}
    try:
        ctx = None
        fn = rel.get("detalhe_pedido")
        for cel in (getattr(fn, "__closure__", None) or ()):
            if isinstance(cel.cell_contents, rn.Contexto):
                ctx = cel.cell_contents
        ctx = ctx or rn.Contexto(raiz, hoje, None, dict(params))
        pf = rn.por_filial_da_nota(ctx, f"{ano}-{mes:02d}")
        for uf, v in (pf.get("fat") or {}).items():
            metas[uf] = {"fat_liq": v,
                         "fat_notas": (pf.get("pedidos") or {}).get(uf)}
        metas["TOTAL"] = {
            "fat_liq": sum((pf.get("fat") or {}).values()),
            "fat_notas": sum((pf.get("pedidos") or {}).values())}
    except Exception as erro:                 # noqa: BLE001
        avisos.append(f"Farol de Metas/Painel nao conferido "
                      f"({type(erro).__name__})")
    return {"por": por, "coerencia": coerencia, "avisos": avisos,
            "metas": metas, "segundos": seg,
            "versao_dados": getattr(__import__("bap_dados"), "VERSAO", "?")}


# =============================================================================
# 5. O PACOTE WEB gravado no PC (so a simulacao grava)
# =============================================================================
def achar_pacote(arg_pacote, lote, ano, mes):
    if arg_pacote:
        return Path(arg_pacote)
    base = Path(tempfile.gettempdir()) / "BAP_PACOTE_WEB"
    if lote:
        p = base / lote / "pv_pedidos.json.gz"
        return p if p.exists() else None
    try:
        lotes = sorted((d for d in base.iterdir()
                        if d.is_dir() and (d / "pv_pedidos.json.gz").exists()),
                       key=lambda d: d.name)
    except OSError:
        lotes = []
    if lotes:
        return lotes[-1] / "pv_pedidos.json.gz"
    p = base / f"pacote_web_{ano}{mes:02d}.json"
    return p if p.exists() else None


def conta_pacote(arq: Path):
    bruto = arq.read_bytes()
    if bruto[:2] == b"\x1f\x8b":
        bruto = gzip.decompress(bruto)
    d = json.loads(bruto.decode("utf-8"))
    farol = d
    if isinstance(d, dict) and "relatorios" in d:
        farol = (d.get("relatorios") or {}).get("pv_pedidos") or {}
    por = {"TOTAL": ler_cartoes(farol.get("kpis"))}
    for uf, x in (farol.get("recortes") or {}).items():
        por[uf] = ler_cartoes((x or {}).get("kpis"))
    # o mes do pacote: ano/mes do pacote inteiro, senao o nome do lote
    # (AAAAMMDDTHHMMSS), senao o gerado_em
    mes_pac = None
    if isinstance(d, dict) and d.get("ano") and d.get("mes"):
        mes_pac = (int(d["ano"]), int(d["mes"]))
    else:
        for cand in (arq.parent.name, str(d.get("gerado_em") or "")):
            m = re.match(r"(\d{4})-?(\d{2})", cand)
            if m:
                mes_pac = (int(m.group(1)), int(m.group(2)))
                break
    return {"por": por, "gerado_em": d.get("gerado_em") if isinstance(d, dict)
            else None, "baixado_em": farol.get("baixado_em"),
            "mes": mes_pac}


# =============================================================================
# 6. A COMPARACAO E O RELATORIO
# =============================================================================
INDICADORES = [
    # chave, rotulo, e dinheiro?, tolerancia farol x fonte
    ("fat_liq", "Faturado liquido R$ (VND-DEV)", True, TOL_CARTAO),
    ("fat_bruto", "  faturado bruto R$ (VND)", True, TOL_EXATO),
    ("dev", "  devolucoes R$ (DEV)", True, TOL_CARTAO),
    ("fat_notas", "Faturado qtd notas", False, 0),
    ("fat_pedidos", "Faturado qtd pedidos", False, 0),
    ("abe_val", "Em aberto R$", True, TOL_EXATO),
    ("abe_qtd", "Em aberto qtd pedidos", False, 0),
]


def fmt(v, dinheiro):
    if v is None:
        return "-"
    return brl(v) if dinheiro else brl(v, 0)


def motivos(chave, dif, dg):
    """Candidatos a motivo: o diagnostico da fonte que explica a diferenca
    (farol - fonte)."""
    cand = {
        "fat_liq": [
            (dg["dev_sem_venda_do_par_filial_vendedor_R$"],
             "devolucao de filial+vendedor sem venda no mes nao descontada: "
             "o cartao do farol (devolucoes_da_vista) so desconta a devolucao "
             "de quem vendeu no recorte; RN-GER-002 manda descontar todas "
             "-> defeito do farol"),
            (-dg["dev_fora_base_R$"],
             "o farol desconta devolucao de cliente fora da base "
             "(RN-GER-013 tira so a venda)"),
            (dg["vnd_fora_base_R$"], "nota de cliente fora da base contada "
             "(RN-GER-013)"),
            (dg["dev_emissao_no_mes_data_dev_fora_R$"],
             "devolucao com D2_EMISSAO no mes e DATA_DEV fora (data da NF)"),
            (-dg["dev_data_dev_no_mes_emissao_fora_R$"],
             "devolucao com DATA_DEV no mes e D2_EMISSAO fora (data da NF)"),
            (-dg["vnd_cod_misto_R$"], "codigo com loja interna e externa "
             "(RN-GER-004: a fonte tira; o farol olha a loja de maior "
             "limite) [sinal pode ser o contrario]"),
            (dg["vnd_cod_misto_R$"], "codigo com loja interna e externa "
             "(RN-GER-004)")],
        "dev": [
            (dg["dev_sem_venda_do_par_filial_vendedor_R$"] * -1,
             "devolucao de filial+vendedor sem venda no mes fica fora do "
             "cartao (devolucoes_da_vista) -> defeito do farol "
             "(RN-GER-002)"),
            (dg["dev_fora_base_R$"], "devolucao de cliente fora da base no "
             "cartao do farol")],
        "fat_bruto": [
            (dg["vnd_fora_base_R$"], "nota de cliente fora da base"),
            (dg["vnd_cod_misto_R$"], "codigo com loja interna e externa"),
            (-dg["vnd_cod_misto_R$"], "codigo com loja interna e externa")],
        "fat_notas": [(dg["vnd_fora_base_notas"], "notas fora da base")],
        "fat_pedidos": [(dg["notas_sem_pedido"], "nota sem numero de pedido"),
                        (-dg["notas_sem_pedido"],
                         "nota sem numero de pedido")],
        "abe_val": [(dg["abe_fora_base_R$"], "pedido fora da base")],
        "abe_qtd": [(dg["abe_fora_base_pedidos"], "pedido fora da base"),
                    (dg["abe_internos_pedidos"], "pedido de cliente interno")],
    }.get(chave, [])
    tol = 1.0 if chave in ("fat_liq", "dev", "fat_bruto", "abe_val") else 0.5
    achou = [m for v, m in cand if v and abs(v - dif) <= tol]
    if achou:
        return achou[0]
    soltos = [m for v, m in cand if v]
    return ("sem causa automatica" + (f"; candidatos: {'; '.join(soltos)}"
                                       if soltos else
                                       " (ver a linha no farol x ftPedidos)"))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Confere o Farol de Pedidos "
                                 "(so leitura).")
    ap.add_argument("--pasta", default=".", help="pasta de producao "
                    "(padrao: a atual)")
    ap.add_argument("--mes", help="AAAA-MM (padrao: o mes corrente)")
    ap.add_argument("--hoje", help="AAAA-MM-DD (padrao: hoje em Manaus)")
    ap.add_argument("--lote", help="AAAAMMDDTHHMMSS do pacote simulado")
    ap.add_argument("--pacote", help="arquivo do pacote (.json ou .json.gz)")
    a = ap.parse_args(argv)
    raiz = Path(a.pasta).resolve()
    if not (raiz / "relatorios_nucleo.py").exists():
        print(f"ERRO: {raiz} nao tem o relatorios_nucleo.py (rode na pasta "
              "de producao ou use --pasta).")
        return 2
    instalar_trava()
    sys.path.insert(0, str(raiz))
    os.chdir(raiz)
    hoje = (date.fromisoformat(a.hoje) if a.hoje else
            datetime.now(timezone(timedelta(hours=-4))).date())
    ano, mes = ((int(a.mes[:4]), int(a.mes[5:7])) if a.mes
                else (hoje.year, hoje.month))
    corrente = (ano, mes) == (hoje.year, hoje.month)

    print("=" * 96)
    print("CONFERENCIA DO FAROL DE PEDIDOS (pv_pedidos) - so leitura")
    print(f"pasta: {raiz}")
    print(f"hoje (Manaus): {hoje:%d/%m/%Y}   mes conferido: "
          f"{MESES[mes]}/{ano}   {'(corrente)' if corrente else '(fechado)'}")
    t0 = time.time()
    try:
        fonte = conta_fonte(raiz, ano, mes, corrente)
    except Exception as erro:                 # noqa: BLE001
        print(f"ERRO ao ler a fonte: {type(erro).__name__}: {erro}")
        return 2
    tipo, onde, est = fonte["origem"]
    if tipo == "fotografia":
        desc = (f"fotografia RELATORIOS/DADOS (gerada em "
                f"{est.get('gerada_em')}, rodada {est.get('rodada')})")
    else:
        desc = "RELATORIOS/TABELA_BAP.xlsx (sem fotografia valida)"
    lidas = ", ".join(f"{k} {v}" for k, v in sorted(fonte["lidas"].items()))
    ult = f"{fonte['max_nf']:%d/%m/%Y}" if fonte["max_nf"] else "-"
    print(f"fonte: {desc}")
    print(f"       linhas lidas: {lidas}   ultima DATA_NF: {ult}")
    try:
        farol = conta_farol(raiz, ano, mes, hoje)
    except Exception as erro:                 # noqa: BLE001
        print(f"ERRO ao montar o farol: {type(erro).__name__}: {erro}")
        return 2
    print(f"farol montado em {farol['segundos']:.0f} s "
          f"(bap_dados.VERSAO {farol['versao_dados']})")
    for av in farol["avisos"]:
        print(f"aviso: {av}")
    pacote, arq_pac = None, achar_pacote(a.pacote, a.lote, ano, mes)
    if arq_pac:
        try:
            pacote = conta_pacote(arq_pac)
            print(f"pacote local: {arq_pac} (gerado_em {pacote['gerado_em']},"
                  f" baixado_em {pacote['baixado_em']})")
            if pacote["mes"] and pacote["mes"] != (ano, mes):
                print(f"  o pacote e de {MESES[pacote['mes'][1]]}/"
                      f"{pacote['mes'][0]}, nao do mes conferido: fica fora"
                      " da comparacao.")
                pacote = None
        except Exception as erro:             # noqa: BLE001
            print(f"pacote local ilegivel ({type(erro).__name__}): {arq_pac}")
    else:
        print("pacote local: nao encontrado (o envio normal nao grava copia;"
              " so a simulacao grava em %TEMP%\\BAP_PACOTE_WEB). Use --pacote"
              " para apontar um arquivo.")
    if not corrente:
        print("mes fechado: 'em aberto' e a carteira de AGORA, so no mes "
              "corrente (n/a)")

    escopos = ["TOTAL"] + [u for u in ORDEM_UF if u in ("PA", "MA", "AM",
                                                        "RR")
                           or u in fonte["por"] or u in farol["por"]] + sorted(
        (set(fonte["por"]) | set(farol["por"])) - set(ORDEM_UF) - {"TOTAL"})
    divergencias, dif_pacote, info_metas = [], [], []
    w = (32, 16, 16, 14, 16)
    for e in escopos:
        f_ = farol["por"].get(e, {})
        s_ = fonte["por"].get(e, {})
        p_ = (pacote or {}).get("por", {}).get(e, {}) if pacote else None
        print()
        print(f"-- {e} " + "-" * (90 - len(e)))
        print(f"{'indicador':<{w[0]}}{'farol':>{w[1]}}{'fonte':>{w[2]}}"
              f"{'diferenca':>{w[3]}}" + (f"{'pacote':>{w[4]}}" if pacote
                                          else "") + "  situacao")
        for chave, rotulo, dinheiro, tol in INDICADORES:
            vf, vs = f_.get(chave), s_.get(chave)
            if vs is None and chave in ("abe_val", "abe_qtd") and not corrente:
                continue
            sem_mov = not f_ and not s_      # estado sem nada no mes
            if sem_mov:
                vf = vs = 0.0
            if vs is None and vf is not None:
                vs = 0.0 if chave not in ("abe_val", "abe_qtd") or corrente \
                    else None
            dif = (vf - vs) if (vf is not None and vs is not None) else None
            ok = dif is not None and abs(dif) <= tol
            situ = ("OK (sem movimento no mes)" if sem_mov else "OK" if ok
                    else "sem numero no farol" if vf is None else "DIVERGE")
            if sem_mov:
                vf = None              # o farol nao tem o estado (site: -)
            linha = (f"{rotulo:<{w[0]}}{fmt(vf, dinheiro):>{w[1]}}"
                     f"{fmt(vs, dinheiro):>{w[2]}}"
                     f"{fmt(dif, dinheiro):>{w[3]}}")
            if pacote:
                vp = (p_ or {}).get(chave)
                linha += f"{fmt(vp, dinheiro):>{w[4]}}"
                if vp is not None and vf is not None and chave in (
                        "fat_liq", "fat_notas", "abe_qtd", "dev") and \
                        abs(vp - vf) > tol:
                    dif_pacote.append(f"{e} {rotulo.strip()}: pacote "
                                      f"{fmt(vp, dinheiro)} x farol agora "
                                      f"{fmt(vf, dinheiro)}")
            print(linha + "  " + situ)
            if vf is None and not sem_mov and vs:
                divergencias.append(f"{e} - {rotulo.strip()}: a fonte tem "
                                    f"{fmt(vs, dinheiro)} e o farol nao tem "
                                    "o estado")
            if not ok and vf is not None and dif is not None:
                divergencias.append(
                    f"{e} - {rotulo.strip()}: farol {fmt(vf, dinheiro)} x "
                    f"fonte {fmt(vs, dinheiro)} (dif {fmt(dif, dinheiro)}) -> "
                    + motivos(chave, dif, fonte["diag"].get(e, Counter())))
        m = farol["metas"].get(e)
        if m and s_:
            dm = m["fat_liq"] - s_.get("fat_liq", 0.0)
            print(f"{'(Metas/Painel) fat. liquido R$':<{w[0]}}"
                  f"{fmt(m['fat_liq'], True):>{w[1]}}"
                  f"{fmt(s_.get('fat_liq'), True):>{w[2]}}"
                  f"{fmt(dm, True):>{w[3]}}" + (" " * w[4] if pacote else "")
                  + ("  OK" if abs(dm) <= TOL_EXATO * 100 else "  difere"))
            if abs(dm) > 1:
                dg = fonte["diag"].get(e, Counter())
                expl = dg["vnd_fora_base_R$"] - dg["dev_fora_base_R$"]
                info_metas.append(
                    f"{e}: Farol de Metas/Painel R$ {brl(m['fat_liq'])} x "
                    f"fonte (sem fora da base) R$ {brl(s_.get('fat_liq', 0))}"
                    + (" -> e o fora da base (RN-GER-013 so vale no Farol de "
                       "Pedidos; Metas/Painel conta)" if abs(expl - dm) <= 1
                       else ""))
        dg = fonte["diag"].get(e)
        if dg:
            info = [(k, v) for k, v in sorted(dg.items()) if v]
            if info:
                print("   fonte, fora das contas / candidatos: " + "; ".join(
                    f"{k}={brl(v) if k.endswith('R$') else brl(v, 0)}"
                    for k, v in info))

    print()
    print("=" * 96)
    print("REGRAS: RN-GER-002 (VND-DEV pela data da NF), RN-GER-004 (internos "
          "fora), RN-GER-013 (fora da base fora),")
    print("        RN-GER-006 (UF = filial da nota/pedido), RN-GER-001 (o "
          "Farol de Pedidos nao usa meta: nada de meta RH aqui).")
    print("        Conta 000040: o farol mantem (RN-GER-005 so a tira de "
          "prospeccao/indicacao/pesquisa/e-mails);")
    print("        o peso dela esta nas linhas 'vnd_000040'/'abe_000040' "
          "acima.")
    print("ROTULOS: o cartao 'Faturado' conta NOTAS (nao pedidos); a qtd de "
          "pedidos faturados vem da tabela do farol.")
    soma = []                  # faturamento = soma dos estados (filial)
    for nome, por in (("farol", farol["por"]), ("fonte", fonte["por"])) + (
            (("pacote", pacote["por"]),) if pacote else ()):
        ufs = [u for u in por if u != "TOTAL" and u in FILIAL_UF.values()]
        for chave, rotulo, dinheiro, tol in INDICADORES:
            tot = (por.get("TOTAL") or {}).get(chave)
            vals = [(por[u] or {}).get(chave) for u in ufs]
            if tot is None or any(v is None for v in vals):
                continue
            sm = sum(vals)
            tol_s = max(tol, TOL_CARTAO * len(ufs)) if dinheiro else 0
            if abs(sm - tot) > tol_s:
                soma.append(f"{nome} - {rotulo.strip()}: soma dos estados "
                            f"{fmt(sm, dinheiro)} x total {fmt(tot, dinheiro)}"
                            f" (dif {fmt(sm - tot, dinheiro)})")
    print("SOMA DOS ESTADOS = TOTAL: " + ("OK" if not soma else "NAO"))
    for c in soma:
        print(f"  - {c}")
    if farol["coerencia"]:
        print("COERENCIA cartao x tabela do proprio farol:")
        for c in farol["coerencia"]:
            print(f"  - {c}")
    if dif_pacote:
        print("PACOTE LOCAL x FAROL AGORA (dado pode ter mudado depois do "
              "lote):")
        for c in dif_pacote:
            print(f"  - {c}")
    if info_metas:
        print("OUTROS FAROIS (informativo):")
        for c in info_metas:
            print(f"  - {c}")
    if BARRADAS:
        print("TRAVA (nada foi gravado; tentativas recusadas): " + "; ".join(
            f"{k} x{v}" for k, v in sorted(BARRADAS.items())))
    print(f"tempo total: {time.time() - t0:.0f} s")
    if divergencias or farol["coerencia"] or soma:
        print("RESULTADO: DIVERGE")
        for d in divergencias:
            print(f"  - {d}")
        return 1
    print("RESULTADO: OK (farol = fonte, no total e por UF)"
          + (" - o pacote local difere do farol de agora (acima)"
             if dif_pacote else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
