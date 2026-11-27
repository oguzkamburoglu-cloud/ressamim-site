#!/usr/bin/env python3
"""ressamim.com sayfalarını üretir: arac/metin/<dil>.json → index.html (tr) ve <dil>/index.html.

Çalıştır (depo kökünde): python3 arac/uret.py
Metni değiştirmek için ilgili JSON'u düzenleyip yeniden çalıştırın; HTML'i elle düzenlemeyin.
Videolar: video/<dil>/{ders,atolye,oyun,dergi}.mp4 ve girişte dönen ders-*.mp4 (+ .jpg kapak).
Bir dilin videosu yoksa İngilizcesi (o da yoksa Türkçesi) kullanılır. Ders adları: arac/ders_adlari.json.
Gizlilik sayfası (gizlilik/) bu araçla üretilmez ve adresi değişmemelidir.
"""
import html
import json
import pathlib

KOK = pathlib.Path(__file__).resolve().parent.parent
SITE = 'https://ressamim.com'
# Uygulamadaki sıra (ilk ikisi ana diller).
DILLER = ['tr', 'en', 'zh', 'hi', 'es', 'ar', 'bn', 'fr', 'ru', 'pt', 'ur']
HTML_DIL = {'zh': 'zh-Hans'}

IKON = {
    'ders': '<path d="M3 21l3.8-1 11-11a2.1 2.1 0 0 0-3-3l-11 11L3 21z"/><path d="M13.5 6.5l3 3"/>',
    'atolye': '<path d="M12 3a9 9 0 1 0 0 18c1.1 0 1.8-.9 1.8-1.9 0-.5-.2-.9-.5-1.3-.3-.3-.5-.8-.5-1.3 0-1 .8-1.8 1.8-1.8H17a4 4 0 0 0 4-4C21 6.6 17 3 12 3z"/><circle cx="7.5" cy="11.5" r="1.2"/><circle cx="10.5" cy="7.5" r="1.2"/><circle cx="15" cy="8" r="1.2"/>',
    'oyun': '<circle cx="9" cy="10" r="5"/><circle cx="15" cy="10" r="5"/><circle cx="12" cy="15" r="5"/>',
    'dergi': '<path d="M3 5.5C5 4.5 8 4.3 12 6c4-1.7 7-1.5 9-.5V19c-2-1-5-1.2-9 .5-4-1.7-7-1.5-9-.5V5.5z"/><path d="M12 6v13.5"/>',
    'reklam': '<circle cx="12" cy="12" r="9"/><path d="M5.6 5.6l12.8 12.8"/>',
    'kilit': '<rect x="4.5" y="10.5" width="15" height="10" rx="2.5"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5"/>',
    'saat': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    'grafik': '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    'aile': '<circle cx="8" cy="7" r="3"/><circle cx="17" cy="9" r="2.5"/><path d="M2.5 20c.5-4 2.8-6 5.5-6s5 2 5.5 6M13.5 20c.4-3 1.8-4.6 3.5-4.6S20.1 17 20.5 20"/>',
    'kamera': '<path d="M4 8h3l2-2.5h6L17 8h3a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z"/><circle cx="12" cy="13" r="3.5"/>',
    'ses': '<path d="M4 9.5v5h3.5L12 19V5L7.5 9.5H4z" fill="currentColor" stroke="none"/><path d="M15.5 9a4 4 0 0 1 0 6M18 6.5a7.5 7.5 0 0 1 0 11"/>',
    'dunya': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3z"/>',
    'ok': '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'tik': '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.6 2.6L16 9.7"/>',
    'elma': '<path d="M16.4 12.6c0-2 1.6-3 1.7-3.1-1-1.4-2.4-1.6-2.9-1.6-1.2-.1-2.4.7-3 .7-.6 0-1.6-.7-2.6-.7A3.9 3.9 0 0 0 6.3 10c-1.4 2.4-.4 6 1 8 .7 1 1.5 2 2.5 2s1.4-.6 2.6-.6 1.5.6 2.6.6 1.7-1 2.4-2c.8-1.1 1.1-2.2 1.1-2.3 0 0-2.1-.8-2.1-3.1zM14.5 6.4c.5-.7.9-1.6.8-2.5-.8 0-1.8.5-2.3 1.2-.5.6-1 1.5-.8 2.4.9.1 1.8-.4 2.3-1.1z" fill="currentColor" stroke="none"/>',
    'play': '<path d="M5 3.8l11.2 8.2L5 20.2V3.8z" fill="currentColor" stroke="none"/><path d="M5 3.8l9.2 9.5M5 20.2l9.2-6.9" stroke="#fff" stroke-width="1"/>',
}


def ikon(ad: str) -> str:
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{IKON[ad]}</svg>')


def yol(dil: str) -> str:
    return '' if dil == 'tr' else '../'


def adres(dil: str) -> str:
    return f'{SITE}/' if dil == 'tr' else f'{SITE}/{dil}/'


def video(dil: str, sahne: str) -> str:
    for d in (dil, 'en', 'tr'):
        if (KOK / 'video' / d / f'{sahne}.mp4').exists():
            return d
    raise FileNotFoundError(f'video/{dil}/{sahne}.mp4')


# Girişteki telefonda sırayla dönen ders videoları: (sahne, uygulamadaki ders adı anahtarı).
HERO_DERSLER = [('ders', 'd_gunes'), ('ders-balonlar', 'd_ana'), ('ders-gokkusagi', 'd_firca'),
                ('ders-elma', 'd_elma'), ('ders-kedi', 'd_kedi')]
DERS_ADLARI = json.loads((KOK / 'arac' / 'ders_adlari.json').read_text(encoding='utf-8'))


def sayfa(dil: str, m: dict, adlar: dict) -> str:
    e = html.escape
    r = yol(dil)
    hd = HTML_DIL.get(dil, dil)
    gizlilik = f'{r}gizlilik/{m["gizlilik_capa"]}'
    # Veliler için yazdırılabilir plan sayfası yalnızca Türkçe; bağlantı da yalnızca Türkçe ana sayfada çıkar.
    plan = ('\n      <p style="text-align:center;margin-top:28px"><a href="veliler/7-gunde-7-cizim/">'
            'Veliler için yazdırılabilir plan: 7 günde 7 çizim</a></p>') if dil == 'tr' else ''
    alternatifler = '\n'.join(f'<link rel="alternate" hreflang="{HTML_DIL.get(d, d)}" href="{adres(d)}">' for d in DILLER)
    dil_menu = '\n'.join(
        f'        <li><a href="{r}{"" if d == "tr" else d + "/"}" hreflang="{HTML_DIL.get(d, d)}" lang="{HTML_DIL.get(d, d)}"'
        f'{" aria-current=\"page\"" if d == dil else ""}>{e(adlar[d])}<small>{d.upper()}</small></a></li>' for d in DILLER)
    alt_diller = ' '.join(
        f'<a href="{r}{"" if d == "tr" else d + "/"}" lang="{HTML_DIL.get(d, d)}"{" aria-current=\"page\"" if d == dil else ""}>{e(adlar[d])}</a>'
        for d in DILLER)

    def vid(sahne, kimlik, gizli=False, oto=True):
        v = video(dil, sahne)
        return (f'<video id="{kimlik}"{" data-oto" if oto else ""} loop muted playsinline preload="{"none" if gizli else "metadata"}"'
                f'{" hidden" if gizli else ""} poster="{r}video/{v}/{sahne}.jpg" aria-label="{e(m["video_" + sahne])}">'
                f'<source src="{r}video/{v}/{sahne}.mp4" type="video/mp4"></video>')

    renk = {'ders': 'var(--sulu)', 'atolye': 'var(--gul)', 'oyun': 'var(--okr)', 'dergi': 'var(--sogut)'}
    sekmeler = []
    for i, s in enumerate(['ders', 'atolye', 'oyun', 'dergi']):
        lis = ''.join(f'<li>{x}</li>' for x in m[f'{s}_li'])
        sekmeler.append(f'''        <div class="sekme-kutu{" secili" if i == 0 else ""}" style="--r: {renk[s]}">
          <button class="sekme" type="button" role="tab" id="s-{s}" aria-controls="v-{s}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">
            <span class="simge">{ikon(s)}</span>
            <span class="ad">{e(m[s + "_h"])} <small>{e(m["ucretsiz_etiket"])}</small></span>
            <span class="ozet">{e(m[s + "_ozet"])}</span>
          </button>
          <div class="ayrinti"><ul>{lis}</ul><p class="kilit">{ikon("kilit")}<span>{e(m[s + "_kilit"])}</span></p></div>
        </div>''')
    sekmeler = '\n'.join(sekmeler)
    vitrin_videolar = '\n          '.join(vid(s, f'v-{s}', gizli=(s != 'ders')) for s in ['ders', 'atolye', 'oyun', 'dergi'])

    v0 = video(dil, 'ders')
    hero_video = (f'<video id="v-hero" data-oto data-liste muted playsinline preload="metadata" poster="{r}video/{v0}/ders.jpg" '
                  f'aria-label="{e(m["video_ders"])}"><source src="{r}video/{v0}/ders.mp4" type="video/mp4"></video>')
    hero_noktalar = ''.join(
        f'<button type="button" class="nokta" data-src="{r}video/{video(dil, s)}/{s}.mp4" data-poster="{r}video/{video(dil, s)}/{s}.jpg" '
        f'data-ad="{e(DERS_ADLARI[a][dil])}" aria-label="{e(DERS_ADLARI[a][dil])}"{" aria-current=\"true\"" if i == 0 else ""}></button>'
        for i, (s, a) in enumerate(HERO_DERSLER))

    adimlar = '\n'.join(f'        <li style="--r: {c}"><h3>{e(m[f"adim{i}_h"])}</h3><p>{e(m[f"adim{i}_p"])}</p></li>'
                        for i, c in [(1, 'var(--sulu)'), (2, 'var(--okr)'), (3, 'var(--gul)')])
    ebeveyn = '\n'.join(f'''        <article class="belir" style="--r: {c}"><span class="simge">{ikon(ik)}</span><h3>{e(m[f"e{i}_h"])}</h3><p>{e(m[f"e{i}_p"])}</p></article>'''
                        for i, ik, c in [(1, 'reklam', '#E58A93'), (2, 'kilit', '#6E9BC5'), (3, 'saat', '#E9B44C'),
                                         (4, 'grafik', '#8BBF85'), (5, 'aile', '#8E6CB8'), (6, 'kamera', '#C8553D')])
    sss = '\n'.join(f'        <details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in m['sss'])
    magaza = (f'<span class="yakinda">{e(m["yakinda"])}: <b>{ikon("elma")}App Store</b> <b>{ikon("play")}Google Play</b></span>')

    return f'''<!doctype html>
<html lang="{hd}" dir="{m["yon"]}" class="js-yok">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(m["baslik"])}</title>
<meta name="description" content="{e(m["aciklama"])}">
<meta name="theme-color" content="#FAF6EE">
<link rel="icon" href="{r}simge.png">
<link rel="apple-touch-icon" href="{r}simge.png">
<link rel="canonical" href="{adres(dil)}">
{alternatifler}
<link rel="alternate" hreflang="x-default" href="{adres("en")}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Ressamım">
<meta property="og:title" content="{e(m["baslik"])}">
<meta property="og:description" content="{e(m["og_aciklama"])}">
<meta property="og:image" content="{SITE}/video/{video(dil, "ders")}/ders.jpg">
<meta property="og:url" content="{adres(dil)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="{r}stil.css">
</head>
<body>
<header class="cubuk">
  <div class="kap">
    <a class="marka" href="{r}{"" if dil == "tr" else dil + "/"}"><img src="{r}simge.png" alt="" width="38" height="38">Ressamım</a>
    <nav class="menu">
      <a href="#ucretsiz">{e(m["menu_ucretsiz"])}</a><a href="#nasil">{e(m["menu_nasil"])}</a><a href="#uyelik">{e(m["menu_uyelik"])}</a><a href="#ebeveyn">{e(m["menu_ebeveyn"])}</a><a href="#sss">{e(m["menu_sss"])}</a>
    </nav>
    <details class="dil">
      <summary aria-label="{e(m["dil_etiket"])}">{ikon("dunya")}{dil.upper()}</summary>
      <ul>
{dil_menu}
      </ul>
    </details>
  </div>
</header>

<main>
  <section class="hero">
    <div class="kap">
      <div>
        <h1>{m["hero_h1"]}</h1>
        <p class="giris-metni">{e(m["hero_metin"])}</p>
        <ul class="rozetler">
          <li style="--r: var(--sulu)"><i></i>{e(m["rozet_yas"])}</li><li style="--r: var(--okr)"><i></i>{e(m["rozet_dil"])}</li><li style="--r: var(--gul)"><i></i>{e(m["rozet_reklam"])}</li><li style="--r: var(--sogut)"><i></i>{e(m["rozet_veri"])}</li>
        </ul>
        <div class="eylemler">
          <a class="dugme ana" href="#ucretsiz">{e(m["dugme_izle"])}<span class="ok">{ikon("ok")}</span></a>
          <a class="dugme ikinci" href="#nasil">{e(m["dugme_nasil"])}</a>
        </div>
        {magaza}
      </div>
      <div class="sahne">
        <i class="leke l1"></i><i class="leke l2"></i>
        <div class="telefon">{hero_video}</div>
        <div class="hero-liste">
          <p class="hero-ad" aria-live="polite">{e(DERS_ADLARI[HERO_DERSLER[0][1]][dil])}</p>
          <div class="noktalar">{hero_noktalar}</div>
        </div>
        <span class="ogretmen"><img src="{r}gorsel/ogretmen.webp" alt="" width="200" height="200"></span>
        <button class="ses" type="button" data-ses="v-hero" data-acik="{e(m["ses_ac"])}" data-kapali="{e(m["ses_kapat"])}" aria-pressed="false"><span class="halka">{ikon("ses")}</span><span class="yazi">{e(m["ses_ac"])}</span></button>
      </div>
    </div>
  </section>

  <div class="rakamlar">
    <ul class="kap">
      <li><b>4–12</b><span>{e(m["rakam_yas"])}</span></li><li><b>11</b><span>{e(m["rakam_dil"])}</span></li><li><b>200</b><span>{e(m["rakam_ders"])}</span></li><li><b>0</b><span>{e(m["rakam_reklam"])}</span></li>
    </ul>
  </div>

  <section id="nasil">
    <div class="kap">
      <div class="bolum-basi orta belir">
        <span class="ust-baslik">{e(m["nasil_ust"])}</span>
        <h2>{e(m["nasil_h2"])}</h2>
        <p>{e(m["nasil_metin"])}</p>
      </div>
      <ol class="adimlar belir">
{adimlar}
      </ol>
    </div>
  </section>

  <section class="ucretsiz" id="ucretsiz">
    <div class="kap">
      <div class="bolum-basi belir">
        <span class="ust-baslik">{e(m["ucretsiz_ust"])}</span>
        <h2>{e(m["ucretsiz_h2"])}</h2>
        <p>{e(m["ucretsiz_metin"])}</p>
      </div>
      <div class="vitrin">
        <div class="sekmeler" role="tablist" aria-label="{e(m["ucretsiz_h2"])}">
{sekmeler}
          <p class="not">{ikon("tik")}<span>{e(m["ucretsiz_not"])}</span></p>
        </div>
        <div class="sahne">
          <div class="telefon">
          {vitrin_videolar}
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="uyelik" id="uyelik">
    <div class="kap">
      <div class="kart belir">
        <div>
          <span class="ust-baslik">{e(m["uyelik_ust"])}</span>
          <h2>{e(m["uyelik_h2"])}</h2>
          <p>{e(m["uyelik_metin"])}</p>
          <p class="kucuk">{e(m["uyelik_kucuk"])}</p>
        </div>
        <ul>
          <li><b>200</b><span>{e(m["uyelik_ders"])}</span></li>
          <li><b>9</b><span>{e(m["uyelik_oyun"])}</span></li>
          <li><b>50</b><span>{e(m["uyelik_dergi"])}</span></li>
          <li><b>50</b><span>{e(m["uyelik_boyama"])}</span></li>
        </ul>
      </div>
    </div>
  </section>

  <section id="ebeveyn">
    <div class="kap">
      <div class="bolum-basi orta belir">
        <span class="ust-baslik">{e(m["ebeveyn_ust"])}</span>
        <h2>{e(m["ebeveyn_h2"])}</h2>
      </div>
      <div class="izgara">
{ebeveyn}
      </div>{plan}
    </div>
  </section>

  <section class="sss" id="sss">
    <div class="kap">
      <div class="bolum-basi">
        <span class="ust-baslik">{e(m["sss_ust"])}</span>
        <h2>{e(m["sss_h2"])}</h2>
        <p>{e(m["sss_metin"])} <a href="mailto:destek@ressamim.com">destek@ressamim.com</a></p>
      </div>
      <div>
{sss}
      </div>
    </div>
  </section>

  <section class="kapanis" id="destek">
    <div class="kap">
      <div class="kart belir">
        <img src="{r}gorsel/ogretmen.webp" alt="" width="200" height="200">
        <h2>{e(m["son_h2"])}</h2>
        <p>{e(m["son_metin"])}</p>
        <div class="eylemler">
          <a class="dugme ana" href="mailto:destek@ressamim.com">{e(m["son_yaz"])}</a>
        </div>
      </div>
    </div>
  </section>
</main>

<footer>
  <div class="kap">
    <div class="ust">
      <span>© 2026 Ressamım</span>
      <nav><a href="{gizlilik}">{e(m["alt_gizlilik"])}</a><a href="mailto:destek@ressamim.com">{e(m["alt_destek"])}: destek@ressamim.com</a></nav>
    </div>
    <nav class="diller" aria-label="{e(m["dil_etiket"])}">{alt_diller}</nav>
  </div>
</footer>
<script src="{r}site.js" defer></script>
</body>
</html>
'''


def main() -> None:
    metinler = {d: json.loads((KOK / 'arac' / 'metin' / f'{d}.json').read_text(encoding='utf-8'))
                for d in DILLER if (KOK / 'arac' / 'metin' / f'{d}.json').exists()}
    adlar = {d: metinler[d]['ad'] if d in metinler else d for d in DILLER}
    anahtarlar = set(metinler['tr'])
    for d, m in metinler.items():
        eksik = anahtarlar - set(m)
        if eksik:
            raise SystemExit(f'{d}.json eksik anahtarlar: {sorted(eksik)}')
        hedef = KOK / ('index.html' if d == 'tr' else f'{d}/index.html')
        hedef.parent.mkdir(exist_ok=True)
        hedef.write_text(sayfa(d, m, adlar), encoding='utf-8')
        print(hedef.relative_to(KOK))


if __name__ == '__main__':
    main()
