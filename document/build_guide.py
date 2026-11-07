from pathlib import Path
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, Preformatted, KeepTogether, Flowable
)
from reportlab.pdfbase.pdfmetrics import stringWidth

SKILL_DIR = Path(r"C:/Users/captan/.gapcode/plugins/cache/gapgpt/pdf/26.722.10000/skills/pdf")
sys.path.insert(0, str(SKILL_DIR / "scripts"))
from fa_pdf import register_persian_fonts, rtl_line, rtl_paragraph, persian_digits, jalali_today_str

register_persian_fonts()

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "راهنمای_راه‌اندازی_و_ارائه_GameTrail.pdf"
SCREENSHOT = ROOT / "tmp" / "site_home.png"

ACCENT = colors.HexColor("#e9003b")
INK = colors.HexColor("#20222d")
MUTED = colors.HexColor("#687080")
LIGHT = colors.HexColor("#f5f7f9")
LINE = colors.HexColor("#d8dee4")
CODE_BG = colors.HexColor("#171922")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="FaTitle", fontName="Vazirmatn-Bold", fontSize=25, leading=38, alignment=TA_RIGHT, textColor=INK, spaceAfter=8))
styles.add(ParagraphStyle(name="FaH1", fontName="Vazirmatn-Bold", fontSize=17, leading=29, alignment=TA_RIGHT, textColor=INK, spaceBefore=4, spaceAfter=8))
styles.add(ParagraphStyle(name="FaH2", fontName="Vazirmatn-Bold", fontSize=13, leading=23, alignment=TA_RIGHT, textColor=INK, spaceBefore=3, spaceAfter=5))
styles.add(ParagraphStyle(name="FaBody", fontName="Vazirmatn", fontSize=10.5, leading=19, alignment=TA_RIGHT, textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle(name="FaSmall", fontName="Vazirmatn", fontSize=8.5, leading=15, alignment=TA_RIGHT, textColor=MUTED, spaceAfter=4))
styles.add(ParagraphStyle(name="FaCenter", fontName="Vazirmatn", fontSize=10, leading=18, alignment=TA_CENTER, textColor=INK))
styles.add(ParagraphStyle(name="FaH2White", fontName="Vazirmatn-Bold", fontSize=12, leading=20, alignment=TA_RIGHT, textColor=colors.white))
styles.add(ParagraphStyle(name="EnCode", fontName="Courier", fontSize=8.4, leading=12, textColor=colors.HexColor("#e6edf3"), leftIndent=0, rightIndent=0))
styles.add(ParagraphStyle(name="EnSmall", fontName="Helvetica", fontSize=8.4, leading=12, textColor=MUTED))


def fa(text, style="FaBody", width=170 * mm):
    return rtl_paragraph(text, styles[style], width)


def heading(text):
    return [Spacer(1, 4 * mm), fa(text, "FaH1"), Rule()]


class Rule(Flowable):
    def __init__(self, color=ACCENT, width=44 * mm, thickness=1.4):
        super().__init__()
        self.color, self.w, self.h = color, width, 3 * mm
        self.thickness = thickness

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.h / 2, self.w, self.h / 2)


class ArchitectureDiagram(Flowable):
    def __init__(self, width=170 * mm, height=66 * mm):
        super().__init__()
        self.width, self.height = width, height

    def draw_box(self, x, y, w, h, title, sub, fill, title_color=colors.white):
        c = self.canv
        c.setFillColor(fill)
        c.setStrokeColor(fill)
        c.roundRect(x, y, w, h, 5 * mm, fill=1, stroke=0)
        c.setFillColor(title_color)
        c.setFont("Vazirmatn-Bold", 9)
        c.drawCentredString(x + w / 2, y + h - 10 * mm, rtl_line(title))
        c.setFillColor(colors.HexColor("#dbe2ea") if fill != colors.HexColor("#f1f3f5") else MUTED)
        c.setFont("Vazirmatn", 7.2)
        c.drawCentredString(x + w / 2, y + 9 * mm, rtl_line(sub))

    def arrow(self, x1, y, x2):
        c = self.canv
        c.setStrokeColor(ACCENT)
        c.setFillColor(ACCENT)
        c.setLineWidth(1.6)
        c.line(x1, y, x2, y)
        c.line(x2, y, x2 - 3 * mm, y + 2 * mm)
        c.line(x2, y, x2 - 3 * mm, y - 2 * mm)

    def draw(self):
        w = self.width
        boxw, boxh = 40 * mm, 25 * mm
        y = self.height - boxh - 6 * mm
        xs = [0, 45 * mm, 90 * mm, 135 * mm]
        self.draw_box(xs[0], y, boxw, boxh, "مرورگر", "Chrome / Edge", INK)
        self.draw_box(xs[1], y, boxw, boxh, "React", "کامپوننت‌ها و state", ACCENT)
        self.draw_box(xs[2], y, boxw, boxh, "Vite", "dev server / build", colors.HexColor("#454b5c"))
        self.draw_box(xs[3], y, boxw, boxh, "هاست", "Vercel / Netlify / Pages", colors.HexColor("#f1f3f5"), INK)
        for a, b in zip(xs[:-1], xs[1:]):
            self.arrow(a + boxw + 1 * mm, y + boxh / 2, b - 1 * mm)
        c = self.canv
        c.setFillColor(MUTED)
        c.setFont("Vazirmatn", 8)
        c.drawRightString(w, 7 * mm, rtl_line("در حالت توسعه، Vite سایت را محلی سرو می‌کند؛ در انتشار، پوشه dist روی هاست قرار می‌گیرد."))


class Callout(Flowable):
    def __init__(self, text, width=170 * mm, fill=LIGHT, accent=ACCENT):
        super().__init__()
        self.text, self.width, self.fill, self.accent = text, width, fill, accent
        self.height = 23 * mm

    def wrap(self, availWidth, availHeight):
        return min(self.width, availWidth), self.height

    def draw(self):
        c = self.canv
        c.setFillColor(self.fill)
        c.setStrokeColor(LINE)
        c.roundRect(0, 0, self.width, self.height, 4 * mm, fill=1, stroke=1)
        c.setFillColor(self.accent)
        c.roundRect(self.width - 4 * mm, 0, 4 * mm, self.height, 2 * mm, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("Vazirmatn", 9.3)
        lines = []
        words = self.text.split()
        current = ""
        for word in words:
            test = (current + " " + word).strip()
            if stringWidth(rtl_line(test), "Vazirmatn", 9.3) > self.width - 14 * mm and current:
                lines.append(current)
                current = word
            else:
                current = test
        if current:
            lines.append(current)
        y = self.height - 8 * mm
        for line in lines[:3]:
            c.drawRightString(self.width - 9 * mm, y, rtl_line(line))
            y -= 5 * mm


def code_block(code, width=170 * mm):
    p = Preformatted(code.strip(), styles["EnCode"], maxLineLength=100)
    t = Table([[p]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#3b3f50")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    return t


def bullet_rows(items):
    data = []
    for item in items:
        data.append([fa("• " + item, "FaBody", 155 * mm)])
    t = Table(data, colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.white),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def on_page(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(INK)
    canvas.rect(0, height - 10 * mm, width, 10 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(18 * mm, height - 6.7 * mm, "GameTrail")
    canvas.setFillColor(MUTED)
    canvas.setFont("Vazirmatn", 7.5)
    canvas.drawRightString(width - 18 * mm, 10 * mm, rtl_line(f"راهنمای پروژه • صفحه {persian_digits(doc.page)}"))
    canvas.setStrokeColor(LINE)
    canvas.line(18 * mm, 15 * mm, width - 18 * mm, 15 * mm)
    canvas.restoreState()


class GuideDoc(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(filename, pagesize=A4, rightMargin=20 * mm, leftMargin=20 * mm, topMargin=18 * mm, bottomMargin=21 * mm, title="راهنمای راه‌اندازی و ارائه GameTrail", author="GameTrail")
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="normal")
        self.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=on_page)])


story = []

# Cover
story += [Spacer(1, 14 * mm), fa("راهنمای راه‌اندازی، انتشار و ارائه وب‌سایت GameTrail", "FaTitle"), fa("پروژه React + Vite برای معرفی و جست‌وجوی بازی‌ها", "FaH2"), Spacer(1, 4 * mm)]
story.append(Rule(width=65 * mm, thickness=2.5))
story.append(Spacer(1, 7 * mm))
if SCREENSHOT.exists():
    im = Image(str(SCREENSHOT), width=170 * mm, height=118 * mm)
    story.append(im)
    story.append(Spacer(1, 3 * mm))
story.append(fa("این فایل برای ارائه پروژه آماده شده است و توضیح می‌دهد سایت چگونه ساخته شده، چگونه روی رایانه اجرا می‌شود و چگونه به یک آدرس عمومی منتقل می‌شود تا دوستان و استاد از هر سیستم به آن دسترسی داشته باشند.", "FaBody"))
story.append(Callout("پیشنهاد اصلی برای ارائه: پروژه را به GitHub متصل کنید و با Vercel یا Netlify منتشر کنید؛ هر تغییر بعدی با یک push دوباره build و منتشر می‌شود."))
story.append(Spacer(1, 5 * mm))
story.append(fa("تاریخ تهیه: " + jalali_today_str(), "FaSmall"))
story.append(PageBreak())

# Access answer
story += heading("پاسخ کوتاه: برای دسترسی از هر جا چه لازم است؟")
story.append(fa("بله. برای این‌که دوست یا استاد شما از اینترنت و با سیستم خودش سایت را باز کند، باید خروجی تولیدشده روی یک سرویس میزبانی وب قرار بگیرد. پروژه فعلی یک سایت استاتیک و سمت‌کاربر است؛ یعنی داده‌ها و رابط کاربری در مرورگر اجرا می‌شوند و در این نسخه به پایگاه‌داده یا سرور اختصاصی نیاز ندارد."))
story.append(bullet_rows([
    "فقط روی لپ‌تاپ خودتان: دستور npm run dev و آدرس localhost؛ فقط همان رایانه سایت را می‌بیند.",
    "روی شبکه خانه یا کلاس: با آدرس IP محلی و باز بودن فایروال؛ مناسب آزمایش کوتاه، اما دائمی نیست.",
    "برای ارائه از هر مکان: انتشار پوشه dist روی Vercel، Netlify یا GitHub Pages؛ یک URL عمومی دریافت می‌کنید.",
]))
story.append(Spacer(1, 5 * mm))
story.append(fa("در انتشار، کاربر نهایی لازم نیست Node.js یا React نصب کند. او فقط لینک را در مرورگر باز می‌کند؛ نصب Node.js فقط برای توسعه و build روی رایانه شما یا سرویس CI لازم است."))
story.append(ArchitectureDiagram())
story.append(PageBreak())

# Structure
story += heading("شناخت ساختار واقعی پروژه")
tree = """game website project/
├─ index.html              HTML entry and root element
├─ package.json            npm scripts and dependencies
├─ vite.config.js          Vite + React plugin
├─ public/
│  ├─ images/covers/       game cover images
│  └─ videos/              webm trailers
├─ src/
│  ├─ main.jsx             React root
│  ├─ App.jsx              UI, state and components
│  ├─ games.js             game data array
│  └─ styles.css           layout and responsive CSS
└─ dist/                   npm run build output"""
story.append(code_block(tree))
story.append(Spacer(1, 4 * mm))
story.append(fa("index.html فقط یک div با شناسه root دارد. در main.jsx، ReactDOM.createRoot همین عنصر را پیدا می‌کند و App را render می‌کند. از این‌جا به بعد تمام رابط کاربری با JSX ساخته می‌شود."))
story.append(fa("در App.jsx چند کامپوننت کوچک‌تر وجود دارد: Brand برای لوگو، GameCards برای کارت‌ها، GenreHome برای صفحه اصلی، GenreList برای فهرست یک ژانر و GameDetail برای صفحه جزئیات. useState وضعیت بازی انتخاب‌شده، ژانر فعال و متن جستجو را نگه می‌دارد."))
story.append(fa("در games.js هر بازی یک شیء ساده با id، title، genre، year، rating، description، trailer، cover و requirements است. برای افزودن بازی جدید، یک شیء با همین شکل اضافه کنید و فایل‌های تصویر و ویدئو را در public قرار دهید."))
story.append(PageBreak())

# React/Vite explanation
story += heading("React، Vite، JavaScript و CSS در این پروژه")
rows = [
    [fa("فناوری", "FaH2White", 35 * mm), fa("نقش آن در پروژه", "FaH2White", 125 * mm)],
    [fa("React", "FaBody", 35 * mm), fa("رابط کاربری را به کامپوننت‌های قابل استفاده مجدد تقسیم می‌کند. وقتی state تغییر می‌کند، React بخش لازم از صفحه را دوباره render می‌کند.", "FaBody", 125 * mm)],
    [fa("JSX", "FaBody", 35 * mm), fa("ترکیبی از JavaScript و نشانه‌گذاری شبیه HTML است؛ مثلاً <GameCards list={list} onSelect={selectGame} />.", "FaBody", 125 * mm)],
    [fa("Vite", "FaBody", 35 * mm), fa("در توسعه، سرور سریع و Hot Module Replacement می‌دهد؛ در انتشار، فایل‌ها را bundle و minify می‌کند.", "FaBody", 125 * mm)],
    [fa("JavaScript", "FaBody", 35 * mm), fa("فیلتر ژانرها، جستجو، انتخاب بازی و تولید داده‌های نمایشی با توابع و آرایه‌ها نوشته شده است.", "FaBody", 125 * mm)],
    [fa("CSS", "FaBody", 35 * mm), fa("رنگ، فاصله، grid کارت‌ها، حالت hover و breakpointهای موبایل در styles.css تعریف شده‌اند.", "FaBody", 125 * mm)],
]
t = Table(rows, colWidths=[42 * mm, 128 * mm], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), INK), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.4, LINE), ("BACKGROUND", (0, 1), (-1, -1), LIGHT),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 7),
    ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(t)
story.append(Spacer(1, 5 * mm))
story.append(fa("چرخه اجرای نمونه: کاربر در کارت یک بازی کلیک می‌کند؛ onSelect همان بازی را به setSelected می‌دهد؛ App از روی selected، GameDetail را نشان می‌دهد؛ در GameDetail توضیح، تریلر، جدول سیستم موردنیاز و بازی‌های مشابه نمایش داده می‌شوند."))
story.append(PageBreak())

# Local run
story += heading("اجرای پروژه روی رایانه خودتان")
story.append(fa("پیش‌نیازها: Node.js نسخه LTS، یک ویرایشگر مثل VS Code و پوشه کامل پروژه. در PowerShell داخل ریشه پروژه این دستورات را اجرا کنید:"))
story.append(code_block("npm install\nnpm run dev"))
story.append(fa("بعد از اجرای دستور دوم، Vite معمولاً آدرس http://localhost:5173 را نشان می‌دهد. این آدرس فقط برای همان رایانه است. برای build نهایی از دستور زیر استفاده کنید:"))
story.append(code_block("npm run build"))
story.append(fa("در این پروژه build با موفقیت اجرا شد و پوشه dist ساخته شد. این پوشه شامل index.html و فایل‌های بهینه‌شده JavaScript و CSS است و همان چیزی است که سرویس‌های استاتیک منتشر می‌کنند."))
story.append(Callout("اگر تصویر یا ویدئو نمایش داده نشد، نام فایل و مسیر آن را دقیقاً با مقدار cover و trailer در games.js مقایسه کنید؛ فاصله، حروف بزرگ و کوچک و پسوند مهم هستند."))
story.append(Spacer(1, 4 * mm))
story.append(fa("برای آزمایش روی تلفن یا رایانه‌ای در همان شبکه، Vite را با --host اجرا کنید و آدرس IP محلی رایانه را به‌جای localhost بگذارید. این روش برای ارائه نهایی مناسب نیست، چون رایانه شما باید روشن و به همان شبکه متصل بماند."))
story.append(PageBreak())

# Vercel deployment
story += heading("روش پیشنهادی انتشار عمومی: GitHub + Vercel")
story.append(fa("این مسیر برای ارائه مناسب است چون یک URL عمومی می‌دهد و با هر push می‌تواند دوباره build شود. ابتدا یک مخزن GitHub بسازید و پروژه را در آن قرار دهید."))
story.append(code_block("git init\ngit add .\ngit commit -m \"Initial GameTrail project\"\ngit branch -M main\ngit remote add origin https://github.com/USERNAME/REPOSITORY.git\ngit push -u origin main"))
story.append(fa("سپس در Vercel با حساب GitHub وارد شوید، گزینه Add New Project را بزنید و مخزن را Import کنید. برای این پروژه تنظیمات معمولاً این است: Framework = Vite، Install Command = npm install یا npm ci، Build Command = npm run build و Output Directory = dist."))
story.append(code_block("# Optional CLI deployment\nnpm install -g vercel\nvercel"))
story.append(fa("پس از پایان deployment، Vercel یک آدرس مانند your-project.vercel.app می‌دهد. همان لینک را برای استاد بفرستید. هر بار که تغییرات را با git push ارسال کنید، نسخه جدید ساخته می‌شود."))
story.append(bullet_rows([
    "قبل از انتشار، npm run build را محلی اجرا کنید.",
    "public را commit کنید؛ تصویرها و ویدئوها از همین پوشه سرو می‌شوند.",
    "اطلاعات خصوصی یا کلید API را داخل پروژه عمومی قرار ندهید.",
    "لینک production را در دو مرورگر و یک تلفن آزمایش کنید.",
]))
story.append(PageBreak())

# Alternatives
story += heading("دو گزینه جایگزین: Netlify و GitHub Pages")
story.append(fa("Netlify: پروژه را به GitHub وصل کنید، شاخه main را انتخاب کنید، Build Command را روی npm run build و Publish Directory را روی dist بگذارید و Deploy را بزنید. Netlify برای هر push می‌تواند preview و production deployment بسازد."))
story.append(code_block("# Netlify CLI deployment\nnpm install -g netlify-cli\nnetlify init\nnetlify deploy\nnetlify deploy --prod"))
story.append(Spacer(1, 4 * mm))
story.append(fa("GitHub Pages: چون Vite قبل از انتشار build لازم دارد، بهتر است از GitHub Actions استفاده کنید. اگر پروژه در آدرس github.com/USERNAME/REPOSITORY قرار دارد، مقدار base در vite.config.js باید با نام مخزن هماهنگ باشد:"))
story.append(code_block("import { defineConfig } from 'vite';\nimport react from '@vitejs/plugin-react';\n\nexport default defineConfig({\n  plugins: [react()],\n  base: '/REPOSITORY/'\n});"))
story.append(fa("برای دامنه شخصی یا زمانی که repository در ریشه دامنه منتشر می‌شود، base معمولاً '/' است. بعد از فعال‌کردن Pages و workflow، آدرس github.io ساخته می‌شود. برای این پروژه Vercel یا Netlify معمولاً ساده‌تر است، چون تنظیم base و مسیر fallback کمتر دردسر دارد."))
story.append(PageBreak())

# Usage/presentation
story += heading("راهنمای استفاده از سایت برای کاربر نهایی")
story.append(bullet_rows([
    "در نوار بالا روی خانه کلیک کنید تا همه ژانرها دیده شوند.",
    "از کادر جستجو نام بازی را تایپ کنید؛ نتایج بر اساس title فیلتر می‌شوند.",
    "با دکمه‌های ژانر، فهرست کامل همان ژانر باز می‌شود.",
    "با کلیک روی کارت، صفحه معرفی، امتیاز، توضیحات، تریلر و جدول سیستم موردنیاز نمایش داده می‌شود.",
    "دکمه بازگشت و لوگو برای برگشت به خانه استفاده می‌شوند؛ صفحه در موبایل نیز با CSS responsive تنظیم شده است.",
]))
story.append(Spacer(1, 5 * mm))
story.append(fa("برای ارائه شفاهی می‌توانید این جمله را بگویید: «من داده‌های بازی‌ها را در یک آرایه نگه داشتم، رابط را با کامپوننت‌های React ساختم، وضعیت انتخاب و جستجو را با useState کنترل کردم، Vite را برای dev server و build استفاده کردم و فایل‌های رسانه‌ای را در public قرار دادم. در پایان با npm run build خروجی dist را تولید و روی یک سرویس استاتیک منتشر کردم.»"))
story.append(Spacer(1, 5 * mm))
story.append(Callout("چک‌لیست روز ارائه: لینک عمومی باز می‌شود، صفحه اصلی و یک صفحه جزئیات تست شده‌اند، تریلرها بارگذاری می‌شوند، نسخه موبایل بررسی شده و build نهایی روی آخرین commit قرار دارد."))
story.append(Spacer(1, 5 * mm))
story.append(fa("منابع رسمی برای مطالعه بیشتر: راهنمای Vite در vite.dev/guide، بخش Deploying a Static Site در vite.dev/guide/static-deploy، راهنمای Vercel برای Vite و مستندات GitHub Pages. این منابع روش‌های build و انتشار را به‌روز نگه می‌دارند.", "FaSmall"))

doc = GuideDoc(str(OUT))
doc.build(story)
sys.stdout.buffer.write((str(OUT) + "\n").encode("utf-8"))
