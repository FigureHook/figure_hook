from datetime import date

from babel.dates import format_date
from discord import Colour, Embed

embed_templates = {
    "en": {
        "maker": "Manufacturer",
        "series": "Series",
        "price": "Price",
        "release_date": "Release Date",
        "sculptors": "Sculptors",
        "paintworks": "Paintworks",
        "date_format": "MMM, yyyy"
    },
    "ja": {
        "maker": "メーカー",
        "series": "作品名",
        "price": "価格",
        "release_date": "発売時期",
        "sculptors": "原型制作",
        "paintworks": "彩色",
        "date_format": "yyyy MMM",
    },
    "zh-TW": {
        "maker": "製造商",
        "series": "作品名稱",
        "price": "價格",
        "release_date": "發售日期",
        "sculptors": "原型製作",
        "paintworks": "色彩",
        "date_format": "yyyy MMM",
    },
}

locale_mapping = {
    "en": "en",
    "ja": "ja",
    "zh-TW": "zh"
}


class DiscordEmbedFactory:
    @staticmethod
    def create_new_release(
        name: str,
        url: str,
        series: str,
        maker: str,
        price: int,
        image: str,
        release_date: date,
        sculptors: list[str],
        paintworks: list[str],
        template_lang: str = 'en'
    ):
        locale = locale_mapping.get(template_lang, "en")
        date_format = embed_templates[template_lang]["date_format"]
        release_date_text = format_date(release_date, date_format, locale=locale)
        embed = Embed(title=name, type="rich", url=url, colour=Colour.red())
        embed.set_image(url=image)
        embed.add_field(
            name=embed_templates[template_lang]["maker"], value=maker, inline=True
        ).add_field(
            name=embed_templates[template_lang]["series"], value=series, inline=True
        ).add_field(
            name=embed_templates[template_lang]["price"], value=f"JPY {price:,}", inline=True
        ).add_field(
            name=embed_templates[template_lang]["release_date"], value=release_date_text, inline=True
        ).add_field(
            name=embed_templates[template_lang]["sculptors"], value=sculptors, inline=True
        ).add_field(
            name=embed_templates[template_lang]["paintworks"], value=paintworks, inline=True
        )
        return embed