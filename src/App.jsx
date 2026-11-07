import { useState } from 'react';
import { games } from './games';

const genresOf = (game) => game.genre.split(',').map((genre) => genre.trim());
const genres = [...new Set(games.flatMap(genresOf))];
const inGenre = (game, genre) => genresOf(game).includes(genre);
const number = (value) => new Intl.NumberFormat('fa-IR').format(value);

function Brand({ onClick }) {
  return <button className="brand" onClick={onClick} aria-label="GameTrail، صفحه اصلی"><span className="brand-mark" aria-hidden="true">G<span>·</span></span><span className="brand-text"><strong>GAME<span>TRAIL</span></strong><small>دنیای بازی‌ها</small></span></button>;
}

function GameCards({ list, onSelect }) {
  return <div className="grid">{list.map((game) => (
    <button key={game.id} className="card" onClick={() => onSelect(game)}>
      <div className="thumb"><img src={encodeURI(game.cover)} alt="" loading="lazy" />{game.rating > 0 && <span className="badge"><span>★</span> {game.rating}</span>}</div>
      <div className="card-info"><h3 dir="auto">{game.title}</h3><p><span>{game.genre}</span><span>{game.year}</span></p></div>
    </button>
  ))}</div>;
}

function SectionHeading({ eyebrow, title, count, action, onAction }) {
  return <div className="section-heading"><div className="heading-title"><span className="heading-accent" /><div><span className="eyebrow">{eyebrow}</span><h2>{title} {count !== undefined && <span className="count">{number(count)} بازی</span>}</h2></div></div>{action && <button className="view-all" onClick={onAction}>{action} <span aria-hidden="true">←</span></button>}</div>;
}

function GenreHome({ onPick, onSelect }) {
  return <>
    <div className="genre-jump"><span>گشت‌وگذار در ژانرها</span><div>{genres.map((genre) => <button key={genre} onClick={() => onPick(genre)}>{genre}<span>↖</span></button>)}</div></div>
    <div className="genre-sections">{genres.map((genre, index) => {
      const list = games.filter((game) => inGenre(game, genre));
      return <section className="genre-section" key={genre}><SectionHeading eyebrow={`دسته‌بندی ${number(index + 1)}`} title={`بازی‌های ${genre}`} count={list.length} action="مشاهده همه" onAction={() => onPick(genre)} /><GameCards list={list} onSelect={onSelect} /></section>;
    })}</div>
  </>;
}

function GenreList({ genre, onBack, onSelect }) {
  const list = games.filter((game) => inGenre(game, genre));
  return <section className="content-section"><button className="back" onClick={onBack}>→ بازگشت به همه ژانرها</button><SectionHeading eyebrow="دسته‌بندی بازی‌ها" title={`بازی‌های ${genre}`} count={list.length} /><GameCards list={list} onSelect={onSelect} /></section>;
}

function GameDetail({ game, onBack, onSelect }) {
  const similar = games.filter((g) => g.id !== game.id && genresOf(g).some((x) => genresOf(game).includes(x))).slice(0, 4);
  return <div className="detail"><button className="back" onClick={onBack}>→ بازگشت</button><div className="detail-heading"><span className="eyebrow">معرفی بازی</span><h1 dir="auto">{game.title}</h1><p>{game.genre} <span>·</span> {game.year} <span>·</span> امتیاز {game.rating}/5</p></div>
    <h2>درباره بازی</h2><div className="desc">{game.description.split('\n').map((p, i) => <p key={i}>{p}</p>)}</div>
    <h2>تریلر بازی</h2><div className="video"><video src={encodeURI(game.trailer)} poster={encodeURI(game.cover)} controls preload="metadata" /></div>
    <h2>سیستم مورد نیاز</h2><div className="table-wrap"><table><thead><tr><th>مشخصه</th><th>حداقل</th><th>پیشنهادی</th></tr></thead><tbody>{Object.keys(game.requirements.minimum).map((key) => <tr key={key}><td>{key}</td><td>{game.requirements.minimum[key]}</td><td>{game.requirements.recommended[key]}</td></tr>)}</tbody></table></div>
    {similar.length > 0 && <div className="similar"><SectionHeading eyebrow="بیشتر کشف کنید" title="بازی‌های مشابه" /><GameCards list={similar} onSelect={onSelect} /></div>}
  </div>;
}

export default function App() {
  const [selected, setSelected] = useState(null);
  const [genre, setGenre] = useState(null);
  const [q, setQ] = useState('');
  const goHome = () => { setQ(''); setSelected(null); setGenre(null); window.scrollTo(0, 0); };
  const goGenre = (value) => { setQ(''); setSelected(null); setGenre(value); window.scrollTo(0, 0); };
  const selectGame = (game) => { setQ(''); setSelected(game); window.scrollTo(0, 0); };
  const found = q.trim() ? games.filter((game) => game.title.toLowerCase().includes(q.trim().toLowerCase())) : null;
  let content;
  if (found) content = <section className="content-section"><SectionHeading eyebrow="جستجو در بازی‌ها" title="نتایج جستجو" count={found.length} />{found.length ? <GameCards list={found} onSelect={selectGame} /> : <p className="empty">بازی‌ای با این نام پیدا نشد. عبارت دیگری را امتحان کنید.</p>}</section>;
  else if (selected) content = <GameDetail key={selected.id} game={selected} onSelect={selectGame} onBack={() => setSelected(null)} />;
  else if (genre) content = <GenreList genre={genre} onBack={goHome} onSelect={selectGame} />;
  else content = <GenreHome onPick={goGenre} onSelect={selectGame} />;

  return <div className="page" id="top"><header className="topbar"><div className="topbar-inner"><Brand onClick={goHome} /><label className="search-box"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.8" cy="10.8" r="6.5" /><path d="m16 16 4.2 4.2" /></svg><input type="search" placeholder="نام بازی را جستجو کنید" aria-label="جستجوی نام بازی" value={q} onChange={(event) => setQ(event.target.value)} /></label><nav className="main-nav" aria-label="منوی اصلی"><button className={!genre && !selected && !q ? 'active' : ''} onClick={goHome}>خانه</button><div className="nav-genres"><span>ژانرها</span><div className="nav-genre-list">{genres.map((g) => <button key={g} className={genre === g && !selected ? 'active' : ''} onClick={() => goGenre(g)}>{g}</button>)}</div></div></nav></div></header>
    <main>{content}</main>
    <footer className="gt-footer"><div className="footer-inner"><div className="footer-main"><div><Brand onClick={goHome} /><p>جایی برای کشف دنیای بازی‌ها و پیدا کردن ماجراجویی بعدی شما.</p></div><div className="footer-genres"><h2>ژانر بازی‌ها</h2><div>{genres.map((g) => <button key={g} onClick={() => goGenre(g)}>{g}</button>)}</div></div><div className="footer-explore"><h2>گشت‌وگذار</h2><button onClick={goHome}>صفحه اصلی</button><button onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>بازگشت به بالا ↑</button></div></div><div className="footer-bottom"><p>تمامی حقوق این سایت متعلق به <b>GameTrail</b> است.</p><span dir="ltr">© 2026 GameTrail</span></div></div></footer>
  </div>;
}
