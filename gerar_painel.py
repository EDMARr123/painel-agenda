r"""
Gera painel.html (+ um painel por supervisor) a partir de dados.json —
páginas únicas, autocontidas (CSS/JS inline), prontas pra publicar como
Artifact ou GitHub Pages. Reaproveita a identidade visual do Painel
Departamentos e as fotos já cadastradas no Painel 4 Pilares.
"""

import base64
import json
import os

PASTA_BASE = os.path.dirname(os.path.abspath(__file__))
CAMINHO_DADOS = os.path.join(PASTA_BASE, "dados.json")
CAMINHO_SAIDA = os.path.join(PASTA_BASE, "painel.html")
PASTA_SUPERVISORES_SAIDA = os.path.join(PASTA_BASE, "supervisores")

# Reaproveita as fotos já cadastradas no painel_pilares — mesmos vendedores,
# não faz sentido duplicar os arquivos aqui.
PASTA_FOTOS_SUPERVISORES = os.path.join(PASTA_BASE, "..", "painel_pilares", "fotos_supervisores")
PASTA_FOTOS_RCAS = os.path.join(PASTA_BASE, "..", "painel_pilares", "fotos_rcas")


def _fotos_json(pasta, com_subpastas):
    fotos = {}
    if not os.path.isdir(pasta):
        return json.dumps(fotos, ensure_ascii=False)
    origens = []
    if com_subpastas:
        for nome_pasta in os.listdir(pasta):
            caminho = os.path.join(pasta, nome_pasta)
            if os.path.isdir(caminho):
                origens.append(caminho)
    else:
        origens.append(pasta)
    for origem in origens:
        for nome_arquivo in os.listdir(origem):
            nome, ext = os.path.splitext(nome_arquivo)
            if ext.lower() not in (".jpg", ".jpeg", ".png"):
                continue
            tipo_mime = "image/png" if ext.lower() == ".png" else "image/jpeg"
            with open(os.path.join(origem, nome_arquivo), "rb") as f:
                b64 = base64.b64encode(f.read()).decode("ascii")
            fotos[nome.upper().strip()] = f"data:{tipo_mime};base64,{b64}"
    return json.dumps(fotos, ensure_ascii=False)


_FOTOS_SUPERVISORES_JSON = _fotos_json(PASTA_FOTOS_SUPERVISORES, com_subpastas=False)
_FOTOS_RCAS_JSON = _fotos_json(PASTA_FOTOS_RCAS, com_subpastas=True)

TEMPLATE = r"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Painel Agenda — Equipe GYN</title>
<style>
:root {
  --bg: #EEF1F4;
  --surface: #FFFFFF;
  --surface-2: #F5F7FA;
  --border: #E1E6EB;
  --ink: #10151C;
  --ink-soft: #5B6472;
  --ink-faint: #6B7684;
  --accent: #0E7C86;
  --accent-deep: #0B5158;
  --good: #1D9A5D;
  --good-soft: #E4F5EC;
  --warn: #B4740A;
  --warn-soft: #FBF0DC;
  --bad: #D33B3B;
  --bad-soft: #FBE7E7;
  --track: #E4E7EC;
  --shadow: 0 1px 2px rgba(16, 21, 28, 0.04), 0 8px 24px -12px rgba(16, 21, 28, 0.18);
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #0B1116; --surface: #131B22; --surface-2: #1A232B; --border: #253039;
    --ink: #EAF0F4; --ink-soft: #93A1AC; --ink-faint: #64707B;
    --accent: #4FD1C8; --accent-deep: #1B6E74;
    --good: #3FC17F; --good-soft: #123625; --warn: #E0A63C; --warn-soft: #3A2C10;
    --bad: #F0645E; --bad-soft: #3A1616; --track: #253039;
    --shadow: 0 1px 2px rgba(0,0,0,0.3), 0 12px 32px -16px rgba(0,0,0,0.6);
  }
}
:root[data-theme="dark"] {
  --bg: #0B1116; --surface: #131B22; --surface-2: #1A232B; --border: #253039;
  --ink: #EAF0F4; --ink-soft: #93A1AC; --ink-faint: #64707B;
  --accent: #4FD1C8; --accent-deep: #1B6E74;
  --good: #3FC17F; --good-soft: #123625; --warn: #E0A63C; --warn-soft: #3A2C10;
  --bad: #F0645E; --bad-soft: #3A1616; --track: #253039;
  --shadow: 0 1px 2px rgba(0,0,0,0.3), 0 12px 32px -16px rgba(0,0,0,0.6);
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink); font-family: ui-sans-serif, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased; }
.wrap { max-width: 1400px; margin: 0 auto; padding: 28px 20px 64px; }

header.top { display: flex; flex-wrap: wrap; align-items: flex-end; justify-content: space-between; gap: 20px; margin-bottom: 22px; }
.title-block h1 { margin: 0 0 4px; font-size: 26px; font-weight: 800; letter-spacing: -0.01em; }
.title-block p { margin: 0; color: var(--ink-soft); font-size: 14px; }

.summary-strip { display: flex; gap: 10px; flex-wrap: wrap; }
.stat-pill { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 10px 16px; min-width: 108px; box-shadow: var(--shadow); }
.stat-pill .n { font-size: 20px; font-weight: 800; font-variant-numeric: tabular-nums; line-height: 1.1; }
.stat-pill .l { font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--ink-faint); margin-top: 2px; }

.tabs { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 22px; border-bottom: 1px solid var(--border); padding-bottom: 14px; }
.tab { appearance: none; border: 1px solid var(--border); background: var(--surface); color: var(--ink-soft); font: inherit; font-size: 13px; font-weight: 600; padding: 7px 14px; border-radius: 999px; cursor: pointer; }
.tab:hover { border-color: var(--accent); color: var(--accent); }
.tab.active { background: var(--accent-deep); border-color: var(--accent-deep); color: #fff; }
.tab .count { opacity: 0.7; font-weight: 500; margin-left: 4px; }

.resumo-time { max-width: 460px; margin-bottom: 22px; }
.resumo-time .card { border-width: 2px; border-color: var(--accent); }

.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 18px; }

.card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; box-shadow: var(--shadow); padding: 18px; display: flex; flex-direction: column; gap: 12px; }
.card-head { display: flex; align-items: flex-start; gap: 12px; }
.avatar { width: 44px; height: 44px; border-radius: 50%; flex: none; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 15px; color: #fff; letter-spacing: -0.02em; }
.card-head .who { flex: 1; min-width: 0; }
.card-head h2 { margin: 0; font-size: 15.5px; font-weight: 800; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.card-head .meta { margin: 1px 0 0; font-size: 12px; color: var(--ink-faint); text-transform: uppercase; letter-spacing: 0.03em; }
.head-actions { display: flex; align-items: center; gap: 6px; flex: none; }
.badge-status { font-size: 11.5px; font-weight: 800; padding: 4px 9px; border-radius: 999px; white-space: nowrap; font-variant-numeric: tabular-nums; }
.icon-btn { width: 28px; height: 28px; border-radius: 8px; border: 1px solid var(--border); background: var(--surface-2); color: var(--ink-soft); display: flex; align-items: center; justify-content: center; cursor: pointer; flex: none; }
.icon-btn:hover { border-color: var(--accent); color: var(--accent); }
.icon-btn svg { width: 14px; height: 14px; }

.horarios { display: flex; gap: 8px; }
.horarios .box { flex: 1; background: var(--surface-2); border-radius: 10px; padding: 8px 10px; text-align: center; }
.horarios .box .l { font-size: 9.5px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.04em; color: var(--ink-faint); }
.horarios .box .v { font-size: 14px; font-weight: 800; font-variant-numeric: tabular-nums; margin-top: 2px; }

.metric-row { display: flex; flex-direction: column; gap: 4px; }
.metric-row .top { display: flex; justify-content: space-between; align-items: baseline; font-size: 12.5px; }
.metric-row .top .l { font-weight: 700; color: var(--ink-soft); }
.metric-row .top .v { font-weight: 800; font-variant-numeric: tabular-nums; }
.bar { height: 7px; border-radius: 999px; background: var(--track); overflow: hidden; }
.bar > div { height: 100%; border-radius: 999px; }

.pedidos-row { display: flex; gap: 8px; }
.pedidos-row .box { flex: 1; background: var(--surface-2); border-radius: 10px; padding: 9px 10px; text-align: center; }
.pedidos-row .box .l { font-size: 9.5px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.03em; color: var(--ink-faint); }
.pedidos-row .box .v { font-size: 15px; font-weight: 800; font-variant-numeric: tabular-nums; margin-top: 2px; }

.empty-state { text-align: center; color: var(--ink-faint); padding: 60px 0; font-size: 14px; }
footer.foot { margin-top: 40px; text-align: center; font-size: 11.5px; color: var(--ink-faint); }
</style>
</head>
<body>

<div class="wrap">
  <header class="top">
    <div class="title-block">
      <h1>Painel Agenda</h1>
      <p>Visitas, agenda cumprida e pedidos do dia __DIA__ — atualizado em __DATA_EXTRACAO__</p>
    </div>
    <div class="summary-strip" id="summary"></div>
  </header>

  <nav class="tabs" id="tabs"></nav>
  <section class="resumo-time" id="resumoTime"></section>
  <main class="grid" id="grid"></main>
  <div class="empty-state" id="empty" style="display:none;">Nenhum RCA encontrado pra esse filtro.</div>

  <footer class="foot">Dados extraídos de AGENDA.xlsx (RESUMO DO DIA) · gerado automaticamente</footer>
</div>

<script>
const DADOS = __DADOS_JSON__;
const FOTOS_SUPERVISORES = __FOTOS_SUPERVISORES_JSON__;
const FOTOS_RCAS = __FOTOS_RCAS_JSON__;

function normalizarNomeFoto(nome) {
  return nome.replace(/\s*-\s*$/, "").trim().toUpperCase();
}

function fmtPct(v) { return (v * 100).toLocaleString("pt-BR", { maximumFractionDigits: 0 }) + "%"; }

function corPct(v, boa, media) {
  if (v >= boa) return "good";
  if (v >= media) return "warn";
  return "bad";
}

function iniciais(nome) {
  return nome.split(/\s+/).filter(Boolean).slice(0, 2).map(p => p[0]).join("").toUpperCase();
}

const PALETA_AVATAR = ["#0E7C86", "#7A5CC7", "#C0672B", "#3D6FB4", "#1D9A5D", "#B4740A", "#B4406B"];
function corAvatar(nome) {
  let h = 0;
  for (const c of nome) h = (h * 31 + c.charCodeAt(0)) >>> 0;
  return PALETA_AVATAR[h % PALETA_AVATAR.length];
}

function linhaMetric(label, valor, meta, pct, thresholds) {
  const [boa, media] = thresholds || [0.9, 0.6];
  const cor = corPct(pct, boa, media);
  return `
    <div class="metric-row">
      <div class="top">
        <span class="l">${label}</span>
        <span class="v" style="color:var(--${cor})">${valor} / ${meta} · ${fmtPct(pct)}</span>
      </div>
      <div class="bar"><div style="width:${Math.min(pct * 100, 100)}%;background:var(--${cor})"></div></div>
    </div>`;
}

function card(rca) {
  const av = corAvatar(rca.nome);
  const foto = rca.codigo === "EQUIPE" ? FOTOS_SUPERVISORES[rca.nome] : FOTOS_RCAS[normalizarNomeFoto(rca.nome)];
  const avatarHtml = foto
    ? `<div class="avatar" style="padding:0;overflow:hidden"><img src="${foto}" alt="${rca.nome}" style="width:100%;height:100%;object-fit:cover;border-radius:50%"></div>`
    : `<div class="avatar" style="background:${av}">${iniciais(rca.nome)}</div>`;

  const corStatus = corPct(rca.pct_agenda, 1, 0.9);
  const bateu = rca.pct_agenda >= 1;

  const textoWhats = encodeURIComponent(
    `*${rca.nome}* (RCA ${rca.codigo} · ${rca.rota})\n` +
    `Agenda: ${rca.visitado}/${rca.meta_agenda} (${fmtPct(rca.pct_agenda)})\n` +
    `Dentro da agenda: ${rca.dentro_agenda} (${fmtPct(rca.pct_dentro_agenda)})\n` +
    `Pedidos na agenda: ${rca.ped_agenda} · Conversão: ${fmtPct(rca.conversao)}\n` +
    `Total de pedidos: ${rca.total_pedidos}`
  );

  return `
  <article class="card" id="card-${rca.codigo}" data-supervisor="${rca.supervisor}">
    <div class="card-head">
      ${avatarHtml}
      <div class="who">
        <h2>${rca.nome}</h2>
        <p class="meta">RCA ${rca.codigo} · ${rca.rota || rca.supervisor}</p>
      </div>
      <div class="head-actions">
        ${rca.codigo === "EQUIPE"
          ? ""
          : `<span class="badge-status" style="background:var(--${corStatus}-soft);color:var(--${corStatus})">${bateu ? "BATEU !" : "NÃO BATEU !"}</span>`}
        <button class="icon-btn" title="Imprimir" onclick="window.print()">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
        </button>
        <a class="icon-btn" title="Enviar no WhatsApp" href="https://wa.me/?text=${textoWhats}" target="_blank" rel="noopener">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12.04 2c-5.52 0-10 4.48-10 10 0 1.77.46 3.45 1.27 4.9L2 22l5.25-1.38a9.96 9.96 0 0 0 4.79 1.22h.01c5.52 0 10-4.48 10-10s-4.48-10-10-10Zm0 18.15h-.01a8.2 8.2 0 0 1-4.17-1.14l-.3-.18-3.11.82.83-3.04-.2-.31a8.19 8.19 0 0 1-1.26-4.35c0-4.52 3.68-8.2 8.22-8.2 2.2 0 4.26.86 5.81 2.41a8.15 8.15 0 0 1 2.4 5.8c0 4.52-3.68 8.2-8.21 8.2Zm4.5-6.15c-.25-.12-1.46-.72-1.68-.8-.23-.08-.39-.12-.56.13-.16.24-.64.8-.78.96-.14.16-.29.18-.53.06-.25-.12-1.04-.38-1.98-1.22-.73-.65-1.23-1.46-1.37-1.7-.14-.25-.02-.38.11-.5.11-.11.25-.29.37-.43.12-.14.16-.24.24-.4.08-.16.04-.31-.02-.43-.06-.12-.56-1.35-.77-1.85-.2-.48-.41-.42-.56-.42-.14 0-.31-.02-.47-.02-.16 0-.43.06-.66.31-.22.24-.86.85-.86 2.08 0 1.22.89 2.4 1.01 2.57.12.16 1.75 2.67 4.24 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.46-.6 1.66-1.17.21-.58.21-1.08.14-1.18-.06-.1-.22-.16-.47-.28Z"></path></svg>
        </a>
      </div>
    </div>

    ${rca.codigo === "EQUIPE" ? "" : `
    <div class="horarios">
      <div class="box"><div class="l">1º Cliente</div><div class="v">${rca.primeiro_cliente || "—"}</div></div>
      <div class="box"><div class="l">Último</div><div class="v">${rca.ultimo_cliente || "—"}</div></div>
      <div class="box"><div class="l">T.M.A.</div><div class="v">${rca.tma || "—"}</div></div>
    </div>`}

    ${linhaMetric("Agenda cumprida", rca.visitado, rca.meta_agenda, rca.pct_agenda, [1, 0.9])}
    ${linhaMetric("Dentro da agenda", rca.dentro_agenda, rca.visitado, rca.pct_dentro_agenda)}

    <div class="pedidos-row">
      <div class="box"><div class="l">Pedidos na agenda</div><div class="v">${rca.ped_agenda}</div></div>
      <div class="box"><div class="l">Conversão</div><div class="v">${fmtPct(rca.conversao)}</div></div>
      <div class="box"><div class="l">Total pedidos</div><div class="v">${rca.total_pedidos}</div></div>
    </div>
  </article>`;
}

function montarResumo(dados) {
  const total = dados.length;
  const bateram = dados.filter(r => r.pct_agenda >= 1).length;
  const mediaAgenda = dados.reduce((s, r) => s + r.pct_agenda, 0) / (total || 1);
  const supervisores = new Set(dados.map(r => r.supervisor)).size;
  document.getElementById("summary").innerHTML = `
    <div class="stat-pill"><div class="n">${total}</div><div class="l">RCAs</div></div>
    <div class="stat-pill"><div class="n">${supervisores}</div><div class="l">Supervisores</div></div>
    <div class="stat-pill"><div class="n">${bateram}</div><div class="l">Bateram agenda</div></div>
    <div class="stat-pill"><div class="n">${fmtPct(mediaAgenda)}</div><div class="l">Média agenda</div></div>
  `;
}

function agregarTime(dados, nomeSupervisor) {
  const soma = campo => dados.reduce((s, r) => s + r[campo], 0);
  const metaAgenda = soma("meta_agenda");
  const visitado = soma("visitado");
  const dentroAgenda = soma("dentro_agenda");
  const pedAgenda = soma("ped_agenda");
  const totalPedidos = soma("total_pedidos");
  return {
    codigo: "EQUIPE",
    nome: nomeSupervisor,
    rota: `${dados.length} RCA${dados.length > 1 ? "s" : ""}`,
    supervisor: nomeSupervisor,
    meta_agenda: metaAgenda,
    visitado,
    pct_agenda: metaAgenda ? visitado / metaAgenda : 0,
    dentro_agenda: dentroAgenda,
    pct_dentro_agenda: visitado ? dentroAgenda / visitado : 0,
    ped_agenda: pedAgenda,
    conversao: visitado ? pedAgenda / visitado : 0,
    total_pedidos: totalPedidos,
  };
}

function montarResumoTime(dados, nomeSupervisor) {
  const el = document.getElementById("resumoTime");
  if (!dados.length) { el.innerHTML = ""; return; }
  el.innerHTML = card(agregarTime(dados, nomeSupervisor));
}

function montarTabs(dados) {
  const supervisores = [...new Set(dados.map(r => r.supervisor))].sort();
  const contagem = s => dados.filter(r => r.supervisor === s).length;
  const tabsEl = document.getElementById("tabs");
  tabsEl.innerHTML =
    `<button class="tab active" data-sup="__todos__">Todos <span class="count">${dados.length}</span></button>` +
    supervisores.map(s => `<button class="tab" data-sup="${s}">${s} <span class="count">${contagem(s)}</span></button>`).join("");

  tabsEl.addEventListener("click", (e) => {
    const btn = e.target.closest(".tab");
    if (!btn) return;
    tabsEl.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    btn.classList.add("active");
    filtrar(btn.dataset.sup);
  });
}

function filtrar(sup) {
  const cards = document.querySelectorAll(".card");
  let visiveis = 0;
  cards.forEach(c => {
    const mostra = sup === "__todos__" || c.dataset.supervisor === sup;
    c.style.display = mostra ? "" : "none";
    if (mostra) visiveis++;
  });
  document.getElementById("empty").style.display = visiveis === 0 ? "block" : "none";

  const filtrados = sup === "__todos__" ? DADOS : DADOS.filter(r => r.supervisor === sup);
  montarResumoTime(filtrados, sup === "__todos__" ? "EQUIPE TODA" : sup);
}

function montar() {
  montarResumo(DADOS);
  const supervisorUnico = new Set(DADOS.map(r => r.supervisor)).size === 1 ? DADOS[0].supervisor : "EQUIPE TODA";
  montarResumoTime(DADOS, supervisorUnico);
  montarTabs(DADOS);
  document.getElementById("grid").innerHTML = DADOS
    .slice()
    .sort((a, b) => b.pct_agenda - a.pct_agenda || a.nome.localeCompare(b.nome))
    .map(card)
    .join("");
}

montar();
</script>
</body>
</html>
"""


def gerar_html(dados, dia, titulo="Painel Agenda — Equipe GYN"):
    import datetime

    data_extracao = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    html = TEMPLATE.replace("__DADOS_JSON__", json.dumps(dados, ensure_ascii=False))
    html = html.replace("__FOTOS_SUPERVISORES_JSON__", _FOTOS_SUPERVISORES_JSON)
    html = html.replace("__FOTOS_RCAS_JSON__", _FOTOS_RCAS_JSON)
    html = html.replace("__DATA_EXTRACAO__", data_extracao)
    html = html.replace("__DIA__", str(dia))
    html = html.replace("<title>Painel Agenda — Equipe GYN</title>", f"<title>{titulo}</title>")
    return html


if __name__ == "__main__":
    with open(CAMINHO_DADOS, "r", encoding="utf-8") as f:
        saida = json.load(f)
    dados = saida["rcas"]
    dia = saida["dia"]

    with open(CAMINHO_SAIDA, "w", encoding="utf-8") as f:
        f.write(gerar_html(dados, dia))
    print(f"Painel gerado em: {CAMINHO_SAIDA}")

    os.makedirs(PASTA_SUPERVISORES_SAIDA, exist_ok=True)
    supervisores = sorted({r["supervisor"] for r in dados})
    for sup in supervisores:
        dados_sup = [r for r in dados if r["supervisor"] == sup]
        caminho = os.path.join(PASTA_SUPERVISORES_SAIDA, f"painel_{sup}.html")
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(gerar_html(dados_sup, dia, titulo=f"Painel Agenda — {sup}"))
        print(f"  -> Painel de {sup} gerado em: {caminho}")
