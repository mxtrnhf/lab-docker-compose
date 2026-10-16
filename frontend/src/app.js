const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

async function api(path, opts) {
  const r = await fetch(path, opts);
  const body = r.status === 204 ? null : await r.json();
  if (!r.ok) throw new Error(body?.error || r.statusText);
  return body;
}
const say = t => { $('msg').textContent = t || ''; };

function reqList(g) {
  return `<ul>
    <li>ОЗУ: ${g.min_ram_gb} ГБ</li>
    <li>CPU: ${g.min_cpu_ghz} ГГц</li>
    <li>GPU: ${esc(g.min_gpu)}</li>
    <li>Диск: ${g.min_disk_gb} ГБ</li></ul>`;
}

async function searchCatalog() {
  say();
  const p = new URLSearchParams();
  for (const [k, id] of [['genre','genre'],['q','q'],['ram','ram'],['cpu','cpu'],['disk','disk'],['gpu_tier','gpu']])
    if ($(id).value) p.set(k, $(id).value);
  try {
    const games = await api('/api/catalog?' + p);
    $('title').textContent = `Каталог: найдено ${games.length}`;
    $('result').innerHTML = games.map(g => `
      <div class="card"><h3>${esc(g.title)}</h3><span class="tag">${esc(g.genre)}</span>
      ${reqList(g)}
      <button data-game='${esc(JSON.stringify(g))}'>Добавить в библиотеку</button></div>`).join('');
    document.querySelectorAll('[data-game]').forEach(b => b.onclick = () => addGame(JSON.parse(b.dataset.game)));
  } catch (e) { say('Ошибка: ' + e.message); }
}

async function addGame(g) {
  try {
    await api('/api/library', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(g) });
    say(`«${g.title}» добавлена в библиотеку`);
  } catch (e) { say(e.message); }
}

async function showLibrary() {
  say();
  try {
    const items = await api('/api/library');
    $('title').textContent = `Моя библиотека: ${items.length}`;
    $('result').innerHTML = items.map(g => `
      <div class="card"><h3>${esc(g.title)}</h3><span class="tag">${esc(g.genre)}</span>
      ${reqList(g)}
      <div class="actions">
        <select data-id="${g.id}" class="status">
          ${['planned','playing','completed'].map(s => `<option value="${s}" ${s===g.status?'selected':''}>${{planned:'В планах',playing:'Играю',completed:'Пройдена'}[s]}</option>`).join('')}
        </select>
        <button class="danger" data-del="${g.id}">Удалить</button>
      </div></div>`).join('');
    document.querySelectorAll('.status').forEach(s => s.onchange = async () => {
      await api('/api/library/' + s.dataset.id, { method: 'PUT', headers: {'Content-Type':'application/json'}, body: JSON.stringify({status: s.value}) });
    });
    document.querySelectorAll('[data-del]').forEach(b => b.onclick = async () => {
      await api('/api/library/' + b.dataset.del, { method: 'DELETE' }); showLibrary();
    });
  } catch (e) { say('Ошибка: ' + e.message); }
}

$('btn-catalog').onclick = searchCatalog;
$('btn-library').onclick = showLibrary;
api('/api/genres').then(gs => gs.forEach(g => $('genre').add(new Option(g, g)))).catch(e => say(e.message));
