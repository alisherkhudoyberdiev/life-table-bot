from PIL import Image, ImageDraw, ImageFont, ImageOps
from datetime import datetime
import io
import textwrap
import random
from .helpers import calculate_weeks_passed


def generate_life_table_image(
    birthday: datetime,
    lang_code: str,
    locales: dict,
    quotes: dict,
    font_path: str = "assets/NotoSans-Regular.ttf"
) -> bytes:
    
    def get_text(key: str, default: str = None) -> str:
        try:
            keys = key.split('.')
            value = locales
            for k in keys:
                value = value[k]
            return value.get(lang_code, value.get('en', default or f"_{key}_"))
        except (KeyError, AttributeError):
            return default or f"_{key}_"

    total_weeks = 90 * 52
    weeks_passed = calculate_weeks_passed(birthday)

    # --- Setup ---
    cols, rows = 90, 52
    box_size = 12
    box_padding_x, box_padding_y = 3, 4 # Horizontal and vertical padding
    margin = {
        "top": 170, "bottom": 220, "left": 180, "right": 50
    }
    img_width = margin["left"] + cols * (box_size + box_padding_x) - box_padding_x + margin["right"]
    img_height = margin["top"] + rows * (box_size + box_padding_y) - box_padding_y + margin["bottom"]

    # --- Colors ---
    colors = {
        "text": "#333333", "outline": "#cccccc", "arrow": "#000000",
        "footer": "#aaaaaa",
        "childhood_adolescence": "#89cff0",  # Light Blue for 0-17
        "young_adulthood": "#90ee90",       # Light Green for 18-39
        "middle_age": "#ffd700",           # Gold for 40-64
        "seniority": "#da70d6",            # Orchid for 65-90
        "current_week": "#ff4500",
        "future": "#ffffff"
    }

    img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)

    # --- Fonts ---
    def load_font(size):
        try: return ImageFont.truetype(font_path, size=size)
        except (IOError, OSError): return ImageFont.load_default()
    
    fonts = {
        "title": load_font(40), "axis": load_font(30), "label": load_font(22),
        "legend": load_font(24), "quote": load_font(28), "footer": load_font(20)
    }

    # --- Main Title ---
    title_text = get_text("image_title")
    title_bbox = draw.textbbox((0, 0), title_text, font=fonts["title"])
    draw.text(((img_width - title_bbox[2]) / 2, 30), title_text, fill=colors["text"], font=fonts["title"])

    # --- Axes ---
    # X-Axis (Age in Years)
    x_axis_y = 120
    draw.line([(margin["left"], x_axis_y), (img_width - margin["right"], x_axis_y)], fill=colors["arrow"], width=2)
    draw.polygon([(img_width - margin["right"], x_axis_y - 6), (img_width - margin["right"], x_axis_y + 6), (img_width - margin["right"] + 10, x_axis_y)], fill=colors["arrow"])
    draw.text((margin["left"], x_axis_y - 50), get_text("x_axis_label"), fill=colors["text"], font=fonts["axis"])
    for i in range(5, cols + 1, 5):
        x = margin["left"] + i * (box_size + box_padding_x) - (box_size + box_padding_x) / 2
        draw.text((x, x_axis_y + 10), str(i), fill=colors["text"], font=fonts["label"], anchor="mt")

    # Y-Axis (Week of the Year)
    y_axis_x = 120
    draw.line([(y_axis_x, margin["top"]), (y_axis_x, img_height - margin["bottom"])], fill=colors["arrow"], width=2)
    draw.polygon([(y_axis_x - 6, img_height - margin["bottom"]), (y_axis_x + 6, img_height - margin["bottom"]), (y_axis_x, img_height - margin["bottom"] + 10)], fill=colors["arrow"])
    y_label_text = get_text("y_axis_label")
    y_label_bbox = draw.textbbox((0, 0), y_label_text, font=fonts["axis"])
    label_img = Image.new("RGBA", (y_label_bbox[2], y_label_bbox[3]), (255, 255, 255, 0))
    ImageDraw.Draw(label_img).text((0, 0), y_label_text, font=fonts["axis"], fill=colors["text"])
    rotated = label_img.rotate(90, expand=True)
    paste_x = y_axis_x - rotated.width - 50
    paste_y = margin["top"] + (img_height - margin["top"] - margin["bottom"]) // 2 - rotated.height // 2
    img.paste(rotated, (paste_x, paste_y), rotated)
    for i in range(5, rows + 1, 5):
        y = margin["top"] + i * (box_size + box_padding_y) - (box_size + box_padding_y) / 2
        draw.text((y_axis_x + 15, y), str(i), fill=colors["text"], font=fonts["label"], anchor="lm")

    # --- Grid Drawing ---
    life_stage_weeks = {
        "childhood_adolescence": 18 * 52,
        "young_adulthood": 40 * 52,
        "middle_age": 65 * 52,
    }
    for year in range(cols):
        for week_of_year in range(rows):
            x = margin["left"] + year * (box_size + box_padding_x)
            y = margin["top"] + week_of_year * (box_size + box_padding_y)
            current_week_index = year * 52 + week_of_year

            fill_color = colors["future"]
            if current_week_index == weeks_passed:
                fill_color = colors["current_week"]
            elif current_week_index < weeks_passed:
                if current_week_index < life_stage_weeks["childhood_adolescence"]:
                    fill_color = colors["childhood_adolescence"]
                elif current_week_index < life_stage_weeks["young_adulthood"]:
                    fill_color = colors["young_adulthood"]
                elif current_week_index < life_stage_weeks["middle_age"]:
                    fill_color = colors["middle_age"]
                else:
                    fill_color = colors["seniority"]
            
            draw.rectangle([x, y, x + box_size, y + box_size], fill=fill_color, outline=colors["outline"], width=1)

    # --- Legend ---
    legend_items = {
        f"0-17 ({get_text('legend_childhood_adolescence')})": colors["childhood_adolescence"],
        f"18-39 ({get_text('legend_young_adulthood')})": colors["young_adulthood"],
        f"40-64 ({get_text('legend_middle_age')})": colors["middle_age"],
        f"65-90 ({get_text('legend_seniority')})": colors["seniority"],
        get_text("legend_current"): colors["current_week"],
        get_text("legend_future"): colors["future"],
    }
    legend_y = img_height - 150
    legend_box_size = 20
    current_x = margin["left"]
    for label, color in legend_items.items():
        text_width = draw.textbbox((0,0), label, font=fonts["legend"])[2]
        if current_x + text_width + 40 > img_width - margin["right"]:
             legend_y += 35
             current_x = margin["left"]
        draw.rectangle([current_x, legend_y, current_x + legend_box_size, legend_y + legend_box_size], fill=color, outline=colors["outline"])
        current_x += legend_box_size + 10
        draw.text((current_x, legend_y + legend_box_size / 2), label, font=fonts["legend"], fill=colors["text"], anchor="lm")
        current_x += text_width + 30

    # --- Motivational Quote ---
    # Get the list of quotes for the specific language, fallback to English.
    lang_quotes = quotes.get(lang_code) or quotes.get("en", ["Your future is a blank canvas. Paint it well."])
    quote = random.choice(lang_quotes)
        
    avg_char_width = fonts["quote"].getbbox("A")[2] or fonts["quote"].size * 0.6
    max_chars_per_line = int((img_width - margin["left"] - margin["right"]) / avg_char_width)
    wrapped_quote = textwrap.wrap(quote, width=max_chars_per_line)
    
    quote_y = img_height - 85
    for i, line in enumerate(wrapped_quote):
        line_bbox = draw.textbbox((0, 0), line, font=fonts["quote"])
        draw.text(((img_width - line_bbox[2]) / 2, quote_y + i * (fonts["quote"].size + 5)), line, font=fonts["quote"], fill=colors["text"], align="center")

    # --- Footer ---
    footer = "t.me/life_table_time_bot"
    footer_bbox = draw.textbbox((0, 0), footer, font=fonts["footer"])
    draw.text((img_width - footer_bbox[2] - margin["right"], img_height - 30), footer, fill=colors["footer"], font=fonts["footer"])
    
    output = io.BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    return output.getvalue()
