#!/usr/bin/env python3

from typing import List
from typing import Union
from typing import Literal
from typing import Optional
from dataclasses import field
from dataclasses import asdict
from dataclasses import dataclass

try:
    from typing import Iterator
except:
    from collections.abc import Iterator

LL_DICT = {
    "aa": {"code": "aa", "name": "Afar", "native": "Afar", "alias": [], "rtl": False},
    "ab": {
        "code": "ab",
        "name": "Abkhazian",
        "native": "Аҧсуа",
        "alias": [],
        "rtl": False,
    },
    "af": {
        "code": "af",
        "name": "Afrikaans",
        "native": "Afrikaans",
        "alias": [],
        "rtl": False,
    },
    "ak": {"code": "ak", "name": "Akan", "native": "Akana", "alias": [], "rtl": False},
    "am": {
        "code": "am",
        "name": "Amharic",
        "native": "አማርኛ",
        "alias": [],
        "rtl": False,
    },
    "an": {
        "code": "an",
        "name": "Aragonese",
        "native": "Aragonés",
        "alias": [],
        "rtl": False,
    },
    "ar": {
        "code": "ar",
        "name": "Arabic",
        "native": "العربية",
        "alias": [],
        "rtl": True,
    },
    "as": {
        "code": "as",
        "name": "Assamese",
        "native": "অসমীয়া",
        "alias": [],
        "rtl": False,
    },
    "av": {"code": "av", "name": "Avar", "native": "Авар", "alias": [], "rtl": False},
    "ay": {
        "code": "ay",
        "name": "Aymara",
        "native": "Aymar",
        "alias": [],
        "rtl": False,
    },
    "az": {
        "code": "az",
        "name": "Azerbaijani",
        "native": "Azərbaycanca / آذربايجان",
        "alias": [],
        "rtl": False,
    },
    "ba": {
        "code": "ba",
        "name": "Bashkir",
        "native": "Башҡорт",
        "alias": [],
        "rtl": False,
    },
    "be": {
        "code": "be",
        "name": "Belarusian",
        "native": "Беларуская",
        "alias": [],
        "rtl": False,
    },
    "bg": {
        "code": "bg",
        "name": "Bulgarian",
        "native": "Български",
        "alias": [],
        "rtl": False,
    },
    "bh": {
        "code": "bh",
        "name": "Bihari",
        "native": "भोजपुरी",
        "alias": [],
        "rtl": False,
    },
    "bi": {
        "code": "bi",
        "name": "Bislama",
        "native": "Bislama",
        "alias": [],
        "rtl": False,
    },
    "bm": {
        "code": "bm",
        "name": "Bambara",
        "native": "Bamanankan",
        "alias": [],
        "rtl": False,
    },
    "bn": {
        "code": "bn",
        "name": "Bengali",
        "native": "বাংলা",
        "alias": [],
        "rtl": False,
    },
    "bo": {
        "code": "bo",
        "name": "Tibetan",
        "native": "བོད་ཡིག / Bod skad",
        "alias": [],
        "rtl": False,
    },
    "br": {
        "code": "br",
        "name": "Breton",
        "native": "Brezhoneg",
        "alias": [],
        "rtl": False,
    },
    "bs": {
        "code": "bs",
        "name": "Bosnian",
        "native": "Bosanski",
        "alias": [],
        "rtl": False,
    },
    "ca": {
        "code": "ca",
        "name": "Catalan",
        "native": "Català",
        "alias": [],
        "rtl": False,
    },
    "ce": {
        "code": "ce",
        "name": "Chechen",
        "native": "Нохчийн",
        "alias": [],
        "rtl": False,
    },
    "ch": {
        "code": "ch",
        "name": "Chamorro",
        "native": "Chamoru",
        "alias": [],
        "rtl": False,
    },
    "co": {
        "code": "co",
        "name": "Corsican",
        "native": "Corsu",
        "alias": [],
        "rtl": False,
    },
    "cr": {
        "code": "cr",
        "name": "Cree",
        "native": "Nehiyaw",
        "alias": [],
        "rtl": False,
    },
    "cs": {
        "code": "cs",
        "name": "Czech",
        "native": "Čeština",
        "alias": ["cz"],
        "rtl": False,
    },
    "cu": {
        "code": "cu",
        "name": "Old Church Slavonic / Old Bulgarian",
        "native": "словѣньскъ / slověnĭskŭ",
        "alias": [],
        "rtl": False,
    },
    "cv": {
        "code": "cv",
        "name": "Chuvash",
        "native": "Чăваш",
        "alias": [],
        "rtl": False,
    },
    "cy": {
        "code": "cy",
        "name": "Welsh",
        "native": "Cymraeg",
        "alias": [],
        "rtl": False,
    },
    "da": {
        "code": "da",
        "name": "Danish",
        "native": "Dansk",
        "alias": ["dk"],
        "rtl": False,
    },
    "de": {
        "code": "de",
        "name": "German",
        "native": "Deutsch",
        "alias": [],
        "rtl": False,
    },
    "dv": {
        "code": "dv",
        "name": "Divehi",
        "native": "ދިވެހިބަސް",
        "alias": [],
        "rtl": True,
    },
    "dz": {
        "code": "dz",
        "name": "Dzongkha",
        "native": "ཇོང་ཁ",
        "alias": [],
        "rtl": False,
    },
    "ee": {"code": "ee", "name": "Ewe", "native": "Ɛʋɛ", "alias": [], "rtl": False},
    "el": {
        "code": "el",
        "name": "Greek",
        "native": "Ελληνικά",
        "alias": ["gr"],
        "rtl": False,
    },
    "en": {
        "code": "en",
        "name": "English",
        "native": "English",
        "alias": ["uk", "us"],
        "rtl": False,
    },
    "eo": {
        "code": "eo",
        "name": "Esperanto",
        "native": "Esperanto",
        "alias": [],
        "rtl": False,
    },
    "es": {
        "code": "es",
        "name": "Spanish",
        "native": "Español",
        "alias": [],
        "rtl": False,
    },
    "et": {
        "code": "et",
        "name": "Estonian",
        "native": "Eesti",
        "alias": [],
        "rtl": False,
    },
    "eu": {
        "code": "eu",
        "name": "Basque",
        "native": "Euskara",
        "alias": [],
        "rtl": False,
    },
    "fa": {
        "code": "fa",
        "name": "Persian",
        "native": "فارسی",
        "alias": [],
        "rtl": True,
    },
    "ff": {
        "code": "ff",
        "name": "Peul",
        "native": "Fulfulde",
        "alias": [],
        "rtl": False,
    },
    "fi": {
        "code": "fi",
        "name": "Finnish",
        "native": "Suomi",
        "alias": [],
        "rtl": False,
    },
    "fj": {
        "code": "fj",
        "name": "Fijian",
        "native": "Na Vosa Vakaviti",
        "alias": [],
        "rtl": False,
    },
    "fo": {
        "code": "fo",
        "name": "Faroese",
        "native": "Føroyskt",
        "alias": [],
        "rtl": False,
    },
    "fr": {
        "code": "fr",
        "name": "French",
        "native": "Français",
        "alias": [],
        "rtl": False,
    },
    "fy": {
        "code": "fy",
        "name": "West Frisian",
        "native": "Frysk",
        "alias": [],
        "rtl": False,
    },
    "ga": {
        "code": "ga",
        "name": "Irish",
        "native": "Gaeilge",
        "alias": [],
        "rtl": False,
    },
    "gd": {
        "code": "gd",
        "name": "Scottish Gaelic",
        "native": "Gàidhlig",
        "alias": [],
        "rtl": False,
    },
    "gl": {
        "code": "gl",
        "name": "Galician",
        "native": "Galego",
        "alias": [],
        "rtl": False,
    },
    "gn": {
        "code": "gn",
        "name": "Guarani",
        "native": "Avañe'ẽ",
        "alias": [],
        "rtl": False,
    },
    "gu": {
        "code": "gu",
        "name": "Gujarati",
        "native": "ગુજરાતી",
        "alias": [],
        "rtl": False,
    },
    "gv": {"code": "gv", "name": "Manx", "native": "Gaelg", "alias": [], "rtl": False},
    "ha": {"code": "ha", "name": "Hausa", "native": "هَوُسَ", "alias": [], "rtl": True},
    "he": {"code": "he", "name": "Hebrew", "native": "עברית", "alias": [], "rtl": True},
    "hi": {
        "code": "hi",
        "name": "Hindi",
        "native": "हिन्दी",
        "alias": [],
        "rtl": False,
    },
    "ho": {
        "code": "ho",
        "name": "Hiri Motu",
        "native": "Hiri Motu",
        "alias": [],
        "rtl": False,
    },
    "hr": {
        "code": "hr",
        "name": "Croatian",
        "native": "Hrvatski",
        "alias": [],
        "rtl": False,
    },
    "ht": {
        "code": "ht",
        "name": "Haitian",
        "native": "Krèyol ayisyen",
        "alias": [],
        "rtl": False,
    },
    "hu": {
        "code": "hu",
        "name": "Hungarian",
        "native": "Magyar",
        "alias": [],
        "rtl": False,
    },
    "hy": {
        "code": "hy",
        "name": "Armenian",
        "native": "Հայերեն",
        "alias": [],
        "rtl": False,
    },
    "hz": {
        "code": "hz",
        "name": "Herero",
        "native": "Otsiherero",
        "alias": [],
        "rtl": False,
    },
    "ia": {
        "code": "ia",
        "name": "Interlingua",
        "native": "Interlingua",
        "alias": [],
        "rtl": False,
    },
    "id": {
        "code": "id",
        "name": "Indonesian",
        "native": "Bahasa Indonesia",
        "alias": [],
        "rtl": False,
    },
    "ie": {
        "code": "ie",
        "name": "Interlingue",
        "native": "Interlingue",
        "alias": [],
        "rtl": False,
    },
    "ig": {"code": "ig", "name": "Igbo", "native": "Igbo", "alias": [], "rtl": False},
    "ii": {
        "code": "ii",
        "name": "Sichuan Yi",
        "native": "ꆇꉙ / 四川彝语",
        "alias": [],
        "rtl": False,
    },
    "ik": {
        "code": "ik",
        "name": "Inupiak",
        "native": "Iñupiak",
        "alias": [],
        "rtl": False,
    },
    "io": {"code": "io", "name": "Ido", "native": "Ido", "alias": [], "rtl": False},
    "is": {
        "code": "is",
        "name": "Icelandic",
        "native": "Íslenska",
        "alias": [],
        "rtl": False,
    },
    "it": {
        "code": "it",
        "name": "Italian",
        "native": "Italiano",
        "alias": [],
        "rtl": False,
    },
    "iu": {
        "code": "iu",
        "name": "Inuktitut",
        "native": "ᐃᓄᒃᑎᑐᑦ",
        "alias": [],
        "rtl": False,
    },
    "ja": {
        "code": "ja",
        "name": "Japanese",
        "native": "日本語",
        "alias": ["jp"],
        "rtl": False,
    },
    "jv": {
        "code": "jv",
        "name": "Javanese",
        "native": "Basa Jawa",
        "alias": [],
        "rtl": False,
    },
    "ka": {
        "code": "ka",
        "name": "Georgian",
        "native": "ქართული",
        "alias": [],
        "rtl": False,
    },
    "kg": {
        "code": "kg",
        "name": "Kongo",
        "native": "KiKongo",
        "alias": [],
        "rtl": False,
    },
    "ki": {
        "code": "ki",
        "name": "Kikuyu",
        "native": "Gĩkũyũ",
        "alias": [],
        "rtl": False,
    },
    "kj": {
        "code": "kj",
        "name": "Kuanyama",
        "native": "Kuanyama",
        "alias": [],
        "rtl": False,
    },
    "kk": {
        "code": "kk",
        "name": "Kazakh",
        "native": "Қазақша",
        "alias": [],
        "rtl": False,
    },
    "kl": {
        "code": "kl",
        "name": "Greenlandic",
        "native": "Kalaallisut",
        "alias": [],
        "rtl": False,
    },
    "km": {
        "code": "km",
        "name": "Cambodian",
        "native": "ភាសាខ្មែរ",
        "alias": [],
        "rtl": False,
    },
    "kn": {
        "code": "kn",
        "name": "Kannada",
        "native": "ಕನ್ನಡ",
        "alias": [],
        "rtl": False,
    },
    "ko": {"code": "ko", "name": "Korean", "native": "한국어", "alias": [], "rtl": False},
    "kr": {
        "code": "kr",
        "name": "Kanuri",
        "native": "Kanuri",
        "alias": [],
        "rtl": False,
    },
    "ks": {
        "code": "ks",
        "name": "Kashmiri",
        "native": "कश्मीरी / كشميري",
        "alias": [],
        "rtl": True,
    },
    "ku": {
        "code": "ku",
        "name": "Kurdish",
        "native": "Kurdî / كوردی",
        "alias": [],
        "rtl": True,
    },
    "kv": {"code": "kv", "name": "Komi", "native": "Коми", "alias": [], "rtl": False},
    "kw": {
        "code": "kw",
        "name": "Cornish",
        "native": "Kernewek",
        "alias": [],
        "rtl": False,
    },
    "ky": {
        "code": "ky",
        "name": "Kyrgyz",
        "native": "Кыргызча",
        "alias": [],
        "rtl": False,
    },
    "la": {
        "code": "la",
        "name": "Latin",
        "native": "Latina",
        "alias": [],
        "rtl": False,
    },
    "lb": {
        "code": "lb",
        "name": "Luxembourgish",
        "native": "Lëtzebuergesch",
        "alias": [],
        "rtl": False,
    },
    "lg": {
        "code": "lg",
        "name": "Ganda",
        "native": "Luganda",
        "alias": [],
        "rtl": False,
    },
    "li": {
        "code": "li",
        "name": "Limburgian",
        "native": "Limburgs",
        "alias": [],
        "rtl": False,
    },
    "ln": {
        "code": "ln",
        "name": "Lingala",
        "native": "Lingála",
        "alias": [],
        "rtl": False,
    },
    "lo": {
        "code": "lo",
        "name": "Laotian",
        "native": "ລາວ / Pha xa lao",
        "alias": [],
        "rtl": False,
    },
    "lt": {
        "code": "lt",
        "name": "Lithuanian",
        "native": "Lietuvių",
        "alias": [],
        "rtl": False,
    },
    "lu": {
        "code": "lu",
        "name": "Luba-Katanga",
        "native": "Tshiluba",
        "alias": [],
        "rtl": False,
    },
    "lv": {
        "code": "lv",
        "name": "Latvian",
        "native": "Latviešu",
        "alias": [],
        "rtl": False,
    },
    "mg": {
        "code": "mg",
        "name": "Malagasy",
        "native": "Malagasy",
        "alias": [],
        "rtl": False,
    },
    "mh": {
        "code": "mh",
        "name": "Marshallese",
        "native": "Kajin Majel / Ebon",
        "alias": [],
        "rtl": False,
    },
    "mi": {"code": "mi", "name": "Maori", "native": "Māori", "alias": [], "rtl": False},
    "mk": {
        "code": "mk",
        "name": "Macedonian",
        "native": "Македонски",
        "alias": [],
        "rtl": False,
    },
    "ml": {
        "code": "ml",
        "name": "Malayalam",
        "native": "മലയാളം",
        "alias": [],
        "rtl": False,
    },
    "mn": {
        "code": "mn",
        "name": "Mongolian",
        "native": "Монгол",
        "alias": [],
        "rtl": False,
    },
    "mo": {
        "code": "mo",
        "name": "Moldovan",
        "native": "Moldovenească",
        "alias": [],
        "rtl": False,
    },
    "mr": {
        "code": "mr",
        "name": "Marathi",
        "native": "मराठी",
        "alias": [],
        "rtl": False,
    },
    "ms": {
        "code": "ms",
        "name": "Malay",
        "native": "Bahasa Melayu",
        "alias": [],
        "rtl": False,
    },
    "mt": {
        "code": "mt",
        "name": "Maltese",
        "native": "bil-Malti",
        "alias": [],
        "rtl": False,
    },
    "my": {
        "code": "my",
        "name": "Burmese",
        "native": "မြန်မာစာ",
        "alias": [],
        "rtl": False,
    },
    "na": {
        "code": "na",
        "name": "Nauruan",
        "native": "Dorerin Naoero",
        "alias": [],
        "rtl": False,
    },
    "nb": {
        "code": "nb",
        "name": "Norwegian Bokmål",
        "native": "Norsk bokmål",
        "alias": [],
        "rtl": False,
    },
    "nd": {
        "code": "nd",
        "name": "North Ndebele",
        "native": "Sindebele",
        "alias": [],
        "rtl": False,
    },
    "ne": {
        "code": "ne",
        "name": "Nepali",
        "native": "नेपाली",
        "alias": [],
        "rtl": False,
    },
    "ng": {
        "code": "ng",
        "name": "Ndonga",
        "native": "Oshiwambo",
        "alias": [],
        "rtl": False,
    },
    "nl": {
        "code": "nl",
        "name": "Dutch",
        "native": "Nederlands",
        "alias": [],
        "rtl": False,
    },
    "nn": {
        "code": "nn",
        "name": "Norwegian Nynorsk",
        "native": "Norsk nynorsk",
        "alias": [],
        "rtl": False,
    },
    "no": {
        "code": "no",
        "name": "Norwegian",
        "native": "Norsk",
        "alias": [],
        "rtl": False,
    },
    "nr": {
        "code": "nr",
        "name": "South Ndebele",
        "native": "isiNdebele",
        "alias": [],
        "rtl": False,
    },
    "nv": {
        "code": "nv",
        "name": "Navajo",
        "native": "Diné bizaad",
        "alias": [],
        "rtl": False,
    },
    "ny": {
        "code": "ny",
        "name": "Chichewa",
        "native": "Chi-Chewa",
        "alias": [],
        "rtl": False,
    },
    "oc": {
        "code": "oc",
        "name": "Occitan",
        "native": "Occitan",
        "alias": [],
        "rtl": False,
    },
    "oj": {
        "code": "oj",
        "name": "Ojibwa",
        "native": "ᐊᓂᔑᓈᐯᒧᐎᓐ / Anishinaabemowin",
        "alias": [],
        "rtl": False,
    },
    "om": {
        "code": "om",
        "name": "Oromo",
        "native": "Oromoo",
        "alias": [],
        "rtl": False,
    },
    "or": {"code": "or", "name": "Oriya", "native": "ଓଡ଼ିଆ", "alias": [], "rtl": False},
    "os": {
        "code": "os",
        "name": "Ossetian / Ossetic",
        "native": "Иронау",
        "alias": [],
        "rtl": False,
    },
    "pa": {
        "code": "pa",
        "name": "Panjabi / Punjabi",
        "native": "ਪੰਜਾਬੀ / पंजाबी / پنجابي",
        "alias": [],
        "rtl": False,
    },
    "pi": {
        "code": "pi",
        "name": "Pali",
        "native": "Pāli / पाऴि",
        "alias": [],
        "rtl": False,
    },
    "pl": {
        "code": "pl",
        "name": "Polish",
        "native": "Polski",
        "alias": [],
        "rtl": False,
    },
    "ps": {"code": "ps", "name": "Pashto", "native": "پښتو", "alias": [], "rtl": True},
    "pt": {
        "code": "pt",
        "name": "Portuguese",
        "native": "Português",
        "alias": [],
        "rtl": False,
    },
    "qu": {
        "code": "qu",
        "name": "Quechua",
        "native": "Runa Simi",
        "alias": [],
        "rtl": False,
    },
    "rm": {
        "code": "rm",
        "name": "Raeto Romance",
        "native": "Rumantsch",
        "alias": [],
        "rtl": False,
    },
    "rn": {
        "code": "rn",
        "name": "Kirundi",
        "native": "Kirundi",
        "alias": [],
        "rtl": False,
    },
    "ro": {
        "code": "ro",
        "name": "Romanian",
        "native": "Română",
        "alias": [],
        "rtl": False,
    },
    "ru": {
        "code": "ru",
        "name": "Russian",
        "native": "Русский",
        "alias": [],
        "rtl": False,
    },
    "rw": {
        "code": "rw",
        "name": "Rwandi",
        "native": "Kinyarwandi",
        "alias": [],
        "rtl": False,
    },
    "sa": {
        "code": "sa",
        "name": "Sanskrit",
        "native": "संस्कृतम्",
        "alias": [],
        "rtl": False,
    },
    "sc": {
        "code": "sc",
        "name": "Sardinian",
        "native": "Sardu",
        "alias": [],
        "rtl": False,
    },
    "sd": {
        "code": "sd",
        "name": "Sindhi",
        "native": "सिनधि",
        "alias": [],
        "rtl": False,
    },
    "se": {
        "code": "se",
        "name": "Northern Sami",
        "native": "Sámegiella",
        "alias": [],
        "rtl": False,
    },
    "sg": {"code": "sg", "name": "Sango", "native": "Sängö", "alias": [], "rtl": False},
    "sh": {
        "code": "sh",
        "name": "Serbo-Croatian",
        "native": "Srpskohrvatski / Српскохрватски",
        "alias": [],
        "rtl": False,
    },
    "si": {
        "code": "si",
        "name": "Sinhalese",
        "native": "සිංහල",
        "alias": [],
        "rtl": False,
    },
    "sk": {
        "code": "sk",
        "name": "Slovak",
        "native": "Slovenčina",
        "alias": [],
        "rtl": False,
    },
    "sl": {
        "code": "sl",
        "name": "Slovenian",
        "native": "Slovenščina",
        "alias": [],
        "rtl": False,
    },
    "sm": {
        "code": "sm",
        "name": "Samoan",
        "native": "Gagana Samoa",
        "alias": [],
        "rtl": False,
    },
    "sn": {
        "code": "sn",
        "name": "Shona",
        "native": "chiShona",
        "alias": [],
        "rtl": False,
    },
    "so": {
        "code": "so",
        "name": "Somalia",
        "native": "Soomaaliga",
        "alias": [],
        "rtl": False,
    },
    "sq": {
        "code": "sq",
        "name": "Albanian",
        "native": "Shqip",
        "alias": [],
        "rtl": False,
    },
    "sr": {
        "code": "sr",
        "name": "Serbian",
        "native": "Српски",
        "alias": [],
        "rtl": False,
    },
    "ss": {
        "code": "ss",
        "name": "Swati",
        "native": "SiSwati",
        "alias": [],
        "rtl": False,
    },
    "st": {
        "code": "st",
        "name": "Southern Sotho",
        "native": "Sesotho",
        "alias": [],
        "rtl": False,
    },
    "su": {
        "code": "su",
        "name": "Sundanese",
        "native": "Basa Sunda",
        "alias": [],
        "rtl": False,
    },
    "sv": {
        "code": "sv",
        "name": "Swedish",
        "native": "Svenska",
        "alias": [],
        "rtl": False,
    },
    "sw": {
        "code": "sw",
        "name": "Swahili",
        "native": "Kiswahili",
        "alias": [],
        "rtl": False,
    },
    "ta": {"code": "ta", "name": "Tamil", "native": "தமிழ்", "alias": [], "rtl": False},
    "te": {
        "code": "te",
        "name": "Telugu",
        "native": "తెలుగు",
        "alias": [],
        "rtl": False,
    },
    "tg": {
        "code": "tg",
        "name": "Tajik",
        "native": "Тоҷикӣ",
        "alias": [],
        "rtl": False,
    },
    "th": {
        "code": "th",
        "name": "Thai",
        "native": "ไทย / Phasa Thai",
        "alias": [],
        "rtl": False,
    },
    "ti": {
        "code": "ti",
        "name": "Tigrinya",
        "native": "ትግርኛ",
        "alias": [],
        "rtl": False,
    },
    "tk": {
        "code": "tk",
        "name": "Turkmen",
        "native": "Туркмен / تركمن",
        "alias": [],
        "rtl": False,
    },
    "tl": {
        "code": "tl",
        "name": "Tagalog / Filipino",
        "native": "Tagalog",
        "alias": [],
        "rtl": False,
    },
    "tn": {
        "code": "tn",
        "name": "Tswana",
        "native": "Setswana",
        "alias": [],
        "rtl": False,
    },
    "to": {
        "code": "to",
        "name": "Tonga",
        "native": "Lea Faka-Tonga",
        "alias": [],
        "rtl": False,
    },
    "tr": {
        "code": "tr",
        "name": "Turkish",
        "native": "Türkçe",
        "alias": [],
        "rtl": False,
    },
    "ts": {
        "code": "ts",
        "name": "Tsonga",
        "native": "Xitsonga",
        "alias": [],
        "rtl": False,
    },
    "tt": {
        "code": "tt",
        "name": "Tatar",
        "native": "Tatarça",
        "alias": [],
        "rtl": False,
    },
    "tw": {"code": "tw", "name": "Twi", "native": "Twi", "alias": [], "rtl": False},
    "ty": {
        "code": "ty",
        "name": "Tahitian",
        "native": "Reo Mā`ohi",
        "alias": [],
        "rtl": False,
    },
    "ug": {
        "code": "ug",
        "name": "Uyghur",
        "native": "Uyƣurqə / ئۇيغۇرچە",
        "alias": [],
        "rtl": False,
    },
    "uk": {
        "code": "uk",
        "name": "Ukrainian",
        "native": "Українська",
        "alias": [],
        "rtl": False,
    },
    "ur": {"code": "ur", "name": "Urdu", "native": "اردو", "alias": [], "rtl": True},
    "uz": {"code": "uz", "name": "Uzbek", "native": "Ўзбек", "alias": [], "rtl": False},
    "ve": {
        "code": "ve",
        "name": "Venda",
        "native": "Tshivenḓa",
        "alias": [],
        "rtl": False,
    },
    "vi": {
        "code": "vi",
        "name": "Vietnamese",
        "native": "Tiếng Việt",
        "alias": [],
        "rtl": False,
    },
    "vo": {
        "code": "vo",
        "name": "Volapük",
        "native": "Volapük",
        "alias": [],
        "rtl": False,
    },
    "wa": {
        "code": "wa",
        "name": "Walloon",
        "native": "Walon",
        "alias": [],
        "rtl": False,
    },
    "wo": {
        "code": "wo",
        "name": "Wolof",
        "native": "Wollof",
        "alias": [],
        "rtl": False,
    },
    "xh": {
        "code": "xh",
        "name": "Xhosa",
        "native": "isiXhosa",
        "alias": [],
        "rtl": False,
    },
    "yi": {
        "code": "yi",
        "name": "Yiddish",
        "native": "ייִדיש",
        "alias": [],
        "rtl": True,
    },
    "yo": {
        "code": "yo",
        "name": "Yoruba",
        "native": "Yorùbá",
        "alias": [],
        "rtl": False,
    },
    "za": {
        "code": "za",
        "name": "Zhuang",
        "native": "Cuengh / Tôô / 壮语",
        "alias": [],
        "rtl": False,
    },
    "zh": {"code": "zh", "name": "Chinese", "native": "中文", "alias": [], "rtl": False},
    "zu": {
        "code": "zu",
        "name": "Zulu",
        "native": "isiZulu",
        "alias": [],
        "rtl": False,
    },
}

CURR_DICT = {
    "AED": {"code": "AED", "symbol": "د.إ;", "name": "UAE dirham"},
    "AFN": {"code": "AFN", "symbol": "Afs", "name": "Afghan afghani"},
    "ALL": {"code": "ALL", "symbol": "L", "name": "Albanian lek"},
    "AMD": {"code": "AMD", "symbol": "AMD", "name": "Armenian dram"},
    "ANG": {"code": "ANG", "symbol": "NAƒ", "name": "Netherlands Antillean gulden"},
    "AOA": {"code": "AOA", "symbol": "Kz", "name": "Angolan kwanza"},
    "ARS": {"code": "ARS", "symbol": "$", "name": "Argentine peso"},
    "AUD": {"code": "AUD", "symbol": "$", "name": "Australian dollar"},
    "AWG": {"code": "AWG", "symbol": "ƒ", "name": "Aruban florin"},
    "AZN": {"code": "AZN", "symbol": "AZN", "name": "Azerbaijani manat"},
    "BAM": {
        "code": "BAM",
        "symbol": "KM",
        "name": "Bosnia and Herzegovina konvertibilna marka",
    },
    "BBD": {"code": "BBD", "symbol": "Bds$", "name": "Barbadian dollar"},
    "BDT": {"code": "BDT", "symbol": "৳", "name": "Bangladeshi taka"},
    "BGN": {"code": "BGN", "symbol": "BGN", "name": "Bulgarian lev"},
    "BHD": {"code": "BHD", "symbol": ".د.ب", "name": "Bahraini dinar"},
    "BIF": {"code": "BIF", "symbol": "FBu", "name": "Burundi franc"},
    "BMD": {"code": "BMD", "symbol": "BD$", "name": "Bermudian dollar"},
    "BND": {"code": "BND", "symbol": "B$", "name": "Brunei dollar"},
    "BOB": {"code": "BOB", "symbol": "Bs.", "name": "Bolivian boliviano"},
    "BRL": {"code": "BRL", "symbol": "R$", "name": "Brazilian real"},
    "BSD": {"code": "BSD", "symbol": "B$", "name": "Bahamian dollar"},
    "BTC": {"code": "BTC", "symbol": "₿", "name": "Bitcoin"},
    "BTN": {"code": "BTN", "symbol": "Nu.", "name": "Bhutanese ngultrum"},
    "BWP": {"code": "BWP", "symbol": "P", "name": "Botswana pula"},
    "BYR": {"code": "BYR", "symbol": "Br", "name": "Belarusian ruble"},
    "BZD": {"code": "BZD", "symbol": "BZ$", "name": "Belize dollar"},
    "CAD": {"code": "CAD", "symbol": "$", "name": "Canadian dollar"},
    "CDF": {"code": "CDF", "symbol": "F", "name": "Congolese franc"},
    "CHF": {"code": "CHF", "symbol": "Fr.", "name": "Swiss franc"},
    "CLP": {"code": "CLP", "symbol": "$", "name": "Chilean peso"},
    "CNY": {"code": "CNY", "symbol": "¥", "name": "Chinese/Yuan renminbi"},
    "COP": {"code": "COP", "symbol": "Col$", "name": "Colombian peso"},
    "CRC": {"code": "CRC", "symbol": "₡", "name": "Costa Rican colon"},
    "CUC": {"code": "CUC", "symbol": "$", "name": "Cuban peso"},
    "CVE": {"code": "CVE", "symbol": "Esc", "name": "Cape Verdean escudo"},
    "CZK": {"code": "CZK", "symbol": "Kč", "name": "Czech koruna"},
    "DJF": {"code": "DJF", "symbol": "Fdj", "name": "Djiboutian franc"},
    "DKK": {"code": "DKK", "symbol": "Kr", "name": "Danish krone"},
    "DOP": {"code": "DOP", "symbol": "RD$", "name": "Dominican peso"},
    "DZD": {"code": "DZD", "symbol": "د.ج", "name": "Algerian dinar"},
    "EEK": {"code": "EEK", "symbol": "KR", "name": "Estonian kroon"},
    "EGP": {"code": "EGP", "symbol": "£", "name": "Egyptian pound"},
    "ERN": {"code": "ERN", "symbol": "Nfa", "name": "Eritrean nakfa"},
    "ETB": {"code": "ETB", "symbol": "Br", "name": "Ethiopian birr"},
    "EUR": {"code": "EUR", "symbol": "€", "name": "European Euro"},
    "FJD": {"code": "FJD", "symbol": "FJ$", "name": "Fijian dollar"},
    "FKP": {"code": "FKP", "symbol": "£", "name": "Falkland Islands pound"},
    "GBP": {"code": "GBP", "symbol": "£", "name": "British pound"},
    "GEL": {"code": "GEL", "symbol": "GEL", "name": "Georgian lari"},
    "GHS": {"code": "GHS", "symbol": "GH₵", "name": "Ghanaian cedi"},
    "GIP": {"code": "GIP", "symbol": "£", "name": "Gibraltar pound"},
    "GMD": {"code": "GMD", "symbol": "D", "name": "Gambian dalasi"},
    "GNF": {"code": "GNF", "symbol": "FG", "name": "Guinean franc"},
    "GQE": {"code": "GQE", "symbol": "CFA", "name": "Central African CFA franc"},
    "GTQ": {"code": "GTQ", "symbol": "Q", "name": "Guatemalan quetzal"},
    "GYD": {"code": "GYD", "symbol": "GY$", "name": "Guyanese dollar"},
    "HKD": {"code": "HKD", "symbol": "HK$", "name": "Hong Kong dollar"},
    "HNL": {"code": "HNL", "symbol": "L", "name": "Honduran lempira"},
    "HRK": {"code": "HRK", "symbol": "kn", "name": "Croatian kuna"},
    "HTG": {"code": "HTG", "symbol": "G", "name": "Haitian gourde"},
    "HUF": {"code": "HUF", "symbol": "Ft", "name": "Hungarian forint"},
    "IDR": {"code": "IDR", "symbol": "Rp", "name": "Indonesian rupiah"},
    "ILS": {"code": "ILS", "symbol": "₪", "name": "Israeli new sheqel"},
    "INR": {"code": "INR", "symbol": "₹", "name": "Indian rupee"},
    "IQD": {"code": "IQD", "symbol": "د.ع", "name": "Iraqi dinar"},
    "IRR": {"code": "IRR", "symbol": "IRR", "name": "Iranian rial"},
    "ISK": {"code": "ISK", "symbol": "kr", "name": "Icelandic króna"},
    "JMD": {"code": "JMD", "symbol": "J$", "name": "Jamaican dollar"},
    "JOD": {"code": "JOD", "symbol": "JOD", "name": "Jordanian dinar"},
    "JPY": {"code": "JPY", "symbol": "¥", "name": "Japanese yen"},
    "KES": {"code": "KES", "symbol": "KSh", "name": "Kenyan shilling"},
    "KGS": {"code": "KGS", "symbol": "сом", "name": "Kyrgyzstani som"},
    "KHR": {"code": "KHR", "symbol": "៛", "name": "Cambodian riel"},
    "KMF": {"code": "KMF", "symbol": "KMF", "name": "Comorian franc"},
    "KPW": {"code": "KPW", "symbol": "W", "name": "North Korean won"},
    "KRW": {"code": "KRW", "symbol": "W", "name": "South Korean won"},
    "KWD": {"code": "KWD", "symbol": "KWD", "name": "Kuwaiti dinar"},
    "KYD": {"code": "KYD", "symbol": "KY$", "name": "Cayman Islands dollar"},
    "KZT": {"code": "KZT", "symbol": "T", "name": "Kazakhstani tenge"},
    "LAK": {"code": "LAK", "symbol": "KN", "name": "Lao kip"},
    "LBP": {"code": "LBP", "symbol": "£", "name": "Lebanese lira"},
    "LKR": {"code": "LKR", "symbol": "Rs", "name": "Sri Lankan rupee"},
    "LRD": {"code": "LRD", "symbol": "L$", "name": "Liberian dollar"},
    "LSL": {"code": "LSL", "symbol": "M", "name": "Lesotho loti"},
    "LTL": {"code": "LTL", "symbol": "Lt", "name": "Lithuanian litas"},
    "LVL": {"code": "LVL", "symbol": "Ls", "name": "Latvian lats"},
    "LYD": {"code": "LYD", "symbol": "LD", "name": "Libyan dinar"},
    "MAD": {"code": "MAD", "symbol": "MAD", "name": "Moroccan dirham"},
    "MDL": {"code": "MDL", "symbol": "MDL", "name": "Moldovan leu"},
    "MGA": {"code": "MGA", "symbol": "FMG", "name": "Malagasy ariary"},
    "MKD": {"code": "MKD", "symbol": "MKD", "name": "Macedonian denar"},
    "MMK": {"code": "MMK", "symbol": "K", "name": "Myanma kyat"},
    "MNT": {"code": "MNT", "symbol": "₮", "name": "Mongolian tugrik"},
    "MOP": {"code": "MOP", "symbol": "P", "name": "Macanese pataca"},
    "MRO": {"code": "MRO", "symbol": "UM", "name": "Mauritanian ouguiya"},
    "MUR": {"code": "MUR", "symbol": "Rs", "name": "Mauritian rupee"},
    "MVR": {"code": "MVR", "symbol": "Rf", "name": "Maldivian rufiyaa"},
    "MWK": {"code": "MWK", "symbol": "MK", "name": "Malawian kwacha"},
    "MXN": {"code": "MXN", "symbol": "$", "name": "Mexican peso"},
    "MYR": {"code": "MYR", "symbol": "RM", "name": "Malaysian ringgit"},
    "MZM": {"code": "MZM", "symbol": "MTn", "name": "Mozambican metical"},
    "NAD": {"code": "NAD", "symbol": "N$", "name": "Namibian dollar"},
    "NGN": {"code": "NGN", "symbol": "₦", "name": "Nigerian naira"},
    "NIO": {"code": "NIO", "symbol": "C$", "name": "Nicaraguan córdoba"},
    "NOK": {"code": "NOK", "symbol": "kr", "name": "Norwegian krone"},
    "NPR": {"code": "NPR", "symbol": "NRs", "name": "Nepalese rupee"},
    "NZD": {"code": "NZD", "symbol": "NZ$", "name": "New Zealand dollar"},
    "OMR": {"code": "OMR", "symbol": "OMR", "name": "Omani rial"},
    "PAB": {"code": "PAB", "symbol": "B./", "name": "Panamanian balboa"},
    "PEN": {"code": "PEN", "symbol": "S/.", "name": "Peruvian nuevo sol"},
    "PGK": {"code": "PGK", "symbol": "K", "name": "Papua New Guinean kina"},
    "PHP": {"code": "PHP", "symbol": "₱", "name": "Philippine peso"},
    "PKR": {"code": "PKR", "symbol": "Rs.", "name": "Pakistani rupee"},
    "PLN": {"code": "PLN", "symbol": "zł", "name": "Polish zloty"},
    "PYG": {"code": "PYG", "symbol": "₲", "name": "Paraguayan guarani"},
    "QAR": {"code": "QAR", "symbol": "QR", "name": "Qatari riyal"},
    "RON": {"code": "RON", "symbol": "L", "name": "Romanian leu"},
    "RSD": {"code": "RSD", "symbol": "din.", "name": "Serbian dinar"},
    "RUB": {"code": "RUB", "symbol": "₽", "name": "Russian ruble"},
    "SAR": {"code": "SAR", "symbol": "SR", "name": "Saudi riyal"},
    "SBD": {"code": "SBD", "symbol": "SI$", "name": "Solomon Islands dollar"},
    "SCR": {"code": "SCR", "symbol": "SR", "name": "Seychellois rupee"},
    "SDG": {"code": "SDG", "symbol": "SDG", "name": "Sudanese pound"},
    "SEK": {"code": "SEK", "symbol": "kr", "name": "Swedish krona"},
    "SGD": {"code": "SGD", "symbol": "S$", "name": "Singapore dollar"},
    "SHP": {"code": "SHP", "symbol": "£", "name": "Saint Helena pound"},
    "SLL": {"code": "SLL", "symbol": "Le", "name": "Sierra Leonean leone"},
    "SOS": {"code": "SOS", "symbol": "Sh.", "name": "Somali shilling"},
    "SRD": {"code": "SRD", "symbol": "$", "name": "Surinamese dollar"},
    "SYP": {"code": "SYP", "symbol": "LS", "name": "Syrian pound"},
    "SZL": {"code": "SZL", "symbol": "E", "name": "Swazi lilangeni"},
    "THB": {"code": "THB", "symbol": "฿", "name": "Thai baht"},
    "TJS": {"code": "TJS", "symbol": "TJS", "name": "Tajikistani somoni"},
    "TMT": {"code": "TMT", "symbol": "m", "name": "Turkmen manat"},
    "TND": {"code": "TND", "symbol": "DT", "name": "Tunisian dinar"},
    "TRY": {"code": "TRY", "symbol": "TRY", "name": "Turkish new lira"},
    "TTD": {"code": "TTD", "symbol": "TT$", "name": "Trinidad and Tobago dollar"},
    "TWD": {"code": "TWD", "symbol": "NT$", "name": "New Taiwan dollar"},
    "TZS": {"code": "TZS", "symbol": "TZS", "name": "Tanzanian shilling"},
    "UAH": {"code": "UAH", "symbol": "UAH", "name": "Ukrainian hryvnia"},
    "UGX": {"code": "UGX", "symbol": "USh", "name": "Ugandan shilling"},
    "USD": {"code": "USD", "symbol": "US$", "name": "United States dollar"},
    "UYU": {"code": "UYU", "symbol": "$U", "name": "Uruguayan peso"},
    "UZS": {"code": "UZS", "symbol": "UZS", "name": "Uzbekistani som"},
    "VEB": {"code": "VEB", "symbol": "Bs", "name": "Venezuelan bolivar"},
    "VEF": {"code": "VEF", "symbol": "Bs", "name": "Venezuelan bolivar"},
    "VND": {"code": "VND", "symbol": "₫", "name": "Vietnamese dong"},
    "VUV": {"code": "VUV", "symbol": "VT", "name": "Vanuatu vatu"},
    "WST": {"code": "WST", "symbol": "WS$", "name": "Samoan tala"},
    "XAF": {"code": "XAF", "symbol": "CFA", "name": "Central African CFA franc"},
    "XCD": {"code": "XCD", "symbol": "EC$", "name": "East Caribbean dollar"},
    "XDR": {"code": "XDR", "symbol": "SDR", "name": "Special Drawing Rights"},
    "XOF": {"code": "XOF", "symbol": "CFA", "name": "West African CFA franc"},
    "XPF": {"code": "XPF", "symbol": "F", "name": "CFP franc"},
    "YER": {"code": "YER", "symbol": "YER", "name": "Yemeni rial"},
    "ZAR": {"code": "ZAR", "symbol": "R", "name": "South African rand"},
    "ZMK": {"code": "ZMK", "symbol": "ZK", "name": "Zambian kwacha"},
    "ZWR": {"code": "ZWR", "symbol": "Z$", "name": "Zimbabwean dollar"},
    "RWF": {"code": "FRW", "symbol": "FRw", "name": "Rwandan franc"},
    "SSP": {"code": "SSP", "symbol": "SS£", "name": "South Sudanese pound"},
    "STD": {"code": "STD", "symbol": "Db", "name": "São Tomé and Príncipe dobra"},
    "TOP": {"code": "TOP", "symbol": "T$", "name": "Tongan paʻanga"},
    "TVD": {"code": "TVD", "symbol": "$", "name": "Tuvaluan dollar"},
}


CC_DICT = {
    "AD": {
        "code": "AD",
        "name": "Andorra",
        "native": "Andorra",
        "year": 1974,
        "phone": [376],
        "tld": [".ad"],
        "alias": [""],
        "languages": ["ca"],
        "currencies": [
            "EUR",
        ],
    },
    "AE": {
        "code": "AE",
        "name": "United Arab Emirates",
        "native": "دولة الإمارات العربية المتحدة",
        "year": 1974,
        "phone": [971],
        "tld": [".ae"],
        "alias": [""],
        "languages": ["ar"],
        "currencies": [
            "AED",
        ],
    },
    "AF": {
        "code": "AF",
        "name": "Afghanistan",
        "native": "افغانستان",
        "year": 1974,
        "phone": [93],
        "tld": [".af"],
        "alias": [""],
        "languages": ["ps", "uz", "tk"],
        "currencies": [
            "AFN",
        ],
    },
    "AG": {
        "code": "AG",
        "name": "Antigua and Barbuda",
        "native": "Antigua and Barbuda",
        "year": 1974,
        "phone": [1268],
        "tld": [".ag"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "XCD",
        ],
    },
    "AI": {
        "code": "AI",
        "name": "Anguilla",
        "native": "Anguilla",
        "year": 1985,
        "phone": [1264],
        "tld": [".ai"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "XCD",
        ],
    },
    "AL": {
        "code": "AL",
        "name": "Albania",
        "native": "Shqipëria",
        "year": 1974,
        "phone": [355],
        "tld": [".al"],
        "alias": [""],
        "languages": ["sq"],
        "currencies": [
            "ALL",
        ],
    },
    "AM": {
        "code": "AM",
        "name": "Armenia",
        "native": "Հայաստան",
        "year": 1992,
        "phone": [374],
        "tld": [".am"],
        "alias": [""],
        "languages": ["hy", "ru"],
        "currencies": [
            "AMD",
        ],
    },
    "AO": {
        "code": "AO",
        "name": "Angola",
        "native": "Angola",
        "year": 1974,
        "phone": [244],
        "tld": [".ao"],
        "alias": [""],
        "languages": ["pt"],
        "currencies": [
            "AOA",
        ],
    },
    "AQ": {
        "code": "AQ",
        "name": "Antarctica",
        "native": "Antarctica",
        "year": 1974,
        "phone": [672],
        "tld": [".aq"],
        "alias": [""],
        "languages": [],
        "currencies": [],
    },
    "AR": {
        "code": "AR",
        "name": "Argentina",
        "native": "Argentina",
        "year": 1974,
        "phone": [54],
        "tld": [".ar"],
        "alias": [""],
        "languages": ["es", "gn"],
        "currencies": [
            "ARS",
        ],
    },
    "AS": {
        "code": "AS",
        "name": "American Samoa",
        "native": "American Samoa",
        "year": 1974,
        "phone": [1684],
        "tld": [".as"],
        "alias": [""],
        "languages": ["en", "sm"],
        "currencies": [
            "USD",
        ],
    },
    "AT": {
        "code": "AT",
        "name": "Austria",
        "native": "Österreich",
        "year": 1974,
        "phone": [43],
        "tld": [".at"],
        "alias": [""],
        "languages": ["de"],
        "currencies": [
            "EUR",
        ],
    },
    "AU": {
        "code": "AU",
        "name": "Australia",
        "native": "Australia",
        "year": 1974,
        "phone": [61],
        "tld": [".au"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "AUD",
        ],
    },
    "AW": {
        "code": "AW",
        "name": "Aruba",
        "native": "Aruba",
        "year": 1986,
        "phone": [297],
        "tld": [".aw"],
        "alias": [""],
        "languages": ["nl", "pa"],
        "currencies": [
            "AWG",
        ],
    },
    "AX": {
        "code": "AX",
        "name": "Åland Islands",
        "native": "Åland",
        "year": 2004,
        "phone": [358],
        "tld": [".ax"],
        "alias": [""],
        "languages": ["sv"],
        "currencies": [
            "EUR",
        ],
    },
    "AZ": {
        "code": "AZ",
        "name": "Azerbaijan",
        "native": "Azərbaycan",
        "year": 1992,
        "phone": [994],
        "tld": [".az"],
        "alias": [""],
        "languages": ["az"],
        "currencies": [
            "AZN",
        ],
    },
    "BA": {
        "code": "BA",
        "name": "Bosnia and Herzegovina",
        "native": "Bosna i Hercegovina",
        "year": 1992,
        "phone": [387],
        "tld": [".ba"],
        "alias": [""],
        "languages": ["bs", "hr", "sr"],
        "currencies": [
            "BAM",
        ],
    },
    "BB": {
        "code": "BB",
        "name": "Barbados",
        "native": "Barbados",
        "year": 1974,
        "phone": [1246],
        "tld": [".bb"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "BBD",
        ],
    },
    "BD": {
        "code": "BD",
        "name": "Bangladesh",
        "native": "Bangladesh",
        "year": 1974,
        "phone": [880],
        "tld": [".bd"],
        "alias": [""],
        "languages": ["bn"],
        "currencies": [
            "BDT",
        ],
    },
    "BE": {
        "code": "BE",
        "name": "Belgium",
        "native": "België",
        "year": 1974,
        "phone": [32],
        "tld": [".be"],
        "alias": [""],
        "languages": ["nl", "fr", "de"],
        "currencies": [
            "EUR",
        ],
    },
    "BF": {
        "code": "BF",
        "name": "Burkina Faso",
        "native": "Burkina Faso",
        "year": 1984,
        "phone": [226],
        "tld": [".bf"],
        "alias": [""],
        "languages": ["fr", "ff"],
        "currencies": [
            "XOF",
        ],
    },
    "BG": {
        "code": "BG",
        "name": "Bulgaria",
        "native": "България",
        "year": 1974,
        "phone": [359],
        "tld": [".bg"],
        "alias": [""],
        "languages": ["bg"],
        "currencies": [
            "BGN",
        ],
    },
    "BH": {
        "code": "BH",
        "name": "Bahrain",
        "native": "\u200fالبحرين",
        "year": 1974,
        "phone": [973],
        "tld": [".bh"],
        "alias": [""],
        "languages": ["ar"],
        "currencies": [
            "BHD",
        ],
    },
    "BI": {
        "code": "BI",
        "name": "Burundi",
        "native": "Burundi",
        "year": 1974,
        "phone": [257],
        "tld": [".bi"],
        "alias": [""],
        "languages": ["fr", "rn"],
        "currencies": [
            "BIF",
        ],
    },
    "BJ": {
        "code": "BJ",
        "name": "Benin",
        "native": "Bénin",
        "year": 1977,
        "phone": [229],
        "tld": [".bj"],
        "alias": [""],
        "languages": ["fr"],
        "currencies": [
            "XOF",
        ],
    },
    "BL": {
        "code": "BL",
        "name": "Saint Barthélemy",
        "native": "Saint-Barthélemy",
        "year": 2007,
        "phone": [590],
        "tld": [".bl"],
        "alias": [""],
        "languages": ["fr"],
        "currencies": [
            "EUR",
        ],
    },
    "BM": {
        "code": "BM",
        "name": "Bermuda",
        "native": "Bermuda",
        "year": 1974,
        "phone": [1441],
        "tld": [".bm"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "BMD",
        ],
    },
    "BN": {
        "code": "BN",
        "name": "Brunei Darussalam",
        "native": "Negara Brunei Darussalam",
        "year": 1974,
        "phone": [673],
        "tld": [".bn"],
        "alias": [""],
        "languages": ["ms"],
        "currencies": [
            "BND",
        ],
    },
    "BO": {
        "code": "BO",
        "name": "Bolivia [Plurinational State of]",
        "native": "Bolivia",
        "year": 1974,
        "phone": [591],
        "tld": [".bo"],
        "alias": [""],
        "languages": ["es", "ay", "qu"],
        "currencies": [
            "BOB",
        ],
    },
    "BQ": {
        "code": "BQ",
        "name": "Bonaire, Sint Eustatius and Saba",
        "native": "Bonaire",
        "year": 2010,
        "phone": [5997],
        "tld": [".bq"],
        "alias": [""],
        "languages": ["nl"],
        "currencies": [
            "USD",
        ],
    },
    "BR": {
        "code": "BR",
        "name": "Brazil",
        "native": "Brasil",
        "year": 1974,
        "phone": [55],
        "tld": [".br"],
        "alias": [""],
        "languages": ["pt"],
        "currencies": [
            "BRL",
        ],
    },
    "BS": {
        "code": "BS",
        "name": "Bahamas",
        "native": "Bahamas",
        "year": 1974,
        "phone": [1242],
        "tld": [".bs"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "BSD",
        ],
    },
    "BT": {
        "code": "BT",
        "name": "Bhutan",
        "native": "ʼbrug-yul",
        "year": 1974,
        "phone": [975],
        "tld": [".bt"],
        "alias": [""],
        "languages": ["dz"],
        "currencies": ["BTN", "INR"],
    },
    "BV": {
        "code": "BV",
        "name": "Bouvet Island",
        "native": "Bouvetøya",
        "year": 1974,
        "phone": [47],
        "tld": [".bv"],
        "alias": [""],
        "languages": ["no", "nb", "nn"],
        "currencies": [
            "NOK",
        ],
    },
    "BW": {
        "code": "BW",
        "name": "Botswana",
        "native": "Botswana",
        "year": 1974,
        "phone": [267],
        "tld": [".bw"],
        "alias": [""],
        "languages": ["en", "tn"],
        "currencies": [
            "BWP",
        ],
    },
    "BY": {
        "code": "BY",
        "name": "Belarus",
        "native": "Белару́сь",
        "year": 1974,
        "phone": [375],
        "tld": [".by"],
        "alias": [""],
        "languages": ["be", "ru"],
        "currencies": [
            "BYR",
        ],
    },
    "BZ": {
        "code": "BZ",
        "name": "Belize",
        "native": "Belize",
        "year": 1974,
        "phone": [501],
        "tld": [".bz"],
        "alias": [""],
        "languages": ["en", "es"],
        "currencies": [
            "BZD",
        ],
    },
    "CA": {
        "code": "CA",
        "name": "Canada",
        "native": "Canada",
        "year": 1974,
        "phone": [1],
        "tld": [".ca"],
        "alias": [""],
        "languages": ["en", "fr"],
        "currencies": [
            "CAD",
        ],
    },
    "CC": {
        "code": "CC",
        "name": "Cocos [Keeling] Islands",
        "native": "Cocos [Keeling] Islands",
        "year": 1974,
        "phone": [61],
        "tld": [".cc"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "AUD",
        ],
    },
    "CD": {
        "code": "CD",
        "name": "Congo, Democratic Republic of the",
        "native": "République démocratique du Congo",
        "year": 1997,
        "phone": [243],
        "tld": [".cd"],
        "alias": [""],
        "languages": ["fr", "ln", "kg", "sw", "lu"],
        "currencies": [
            "CDF",
        ],
    },
    "CF": {
        "code": "CF",
        "name": "Central African Republic",
        "native": "Ködörösêse tî Bêafrîka",
        "year": 1974,
        "phone": [236],
        "tld": [".cf"],
        "alias": [""],
        "languages": ["fr", "sg"],
        "currencies": [
            "XAF",
        ],
    },
    "CG": {
        "code": "CG",
        "name": "Congo",
        "native": "République du Congo",
        "year": 1974,
        "phone": [242],
        "tld": [".cg"],
        "alias": [""],
        "languages": ["fr", "ln"],
        "currencies": [
            "XAF",
        ],
    },
    "CH": {
        "code": "CH",
        "name": "Switzerland",
        "native": "Schweiz",
        "year": 1974,
        "phone": [41],
        "tld": [".ch"],
        "alias": [""],
        "languages": ["de", "fr", "it"],
        "currencies": [
            "CHF",
        ],
    },
    "CI": {
        "code": "CI",
        "name": "Côte d'Ivoire",
        "native": "Côte d'Ivoire",
        "year": 1974,
        "phone": [225],
        "tld": [".ci"],
        "alias": [""],
        "languages": ["fr"],
        "currencies": [
            "XOF",
        ],
    },
    "CK": {
        "code": "CK",
        "name": "Cook Islands",
        "native": "Cook Islands",
        "year": 1974,
        "phone": [682],
        "tld": [".ck"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "NZD",
        ],
    },
    "CL": {
        "code": "CL",
        "name": "Chile",
        "native": "Chile",
        "year": 1974,
        "phone": [56],
        "tld": [".cl"],
        "alias": [""],
        "languages": ["es"],
        "currencies": [
            "CLP",
        ],
    },
    "CM": {
        "code": "CM",
        "name": "Cameroon",
        "native": "Cameroon",
        "year": 1974,
        "phone": [237],
        "tld": [".cm"],
        "alias": [""],
        "languages": ["en", "fr"],
        "currencies": [
            "XAF",
        ],
    },
    "CN": {
        "code": "CN",
        "name": "China",
        "native": "中国",
        "year": 1974,
        "phone": [86],
        "tld": [".cn"],
        "alias": [""],
        "languages": ["zh"],
        "currencies": [
            "CNY",
        ],
    },
    "CO": {
        "code": "CO",
        "name": "Colombia",
        "native": "Colombia",
        "year": 1974,
        "phone": [57],
        "tld": [".co"],
        "alias": [""],
        "languages": ["es"],
        "currencies": [
            "COP",
        ],
    },
    "CR": {
        "code": "CR",
        "name": "Costa Rica",
        "native": "Costa Rica",
        "year": 1974,
        "phone": [506],
        "tld": [".cr"],
        "alias": [""],
        "languages": ["es"],
        "currencies": [
            "CRC",
        ],
    },
    "CU": {
        "code": "CU",
        "name": "Cuba",
        "native": "Cuba",
        "year": 1974,
        "phone": [53],
        "tld": [".cu"],
        "alias": [""],
        "languages": ["es"],
        "currencies": ["CUC"],
    },
    "CV": {
        "code": "CV",
        "name": "Cabo Verde",
        "native": "Cabo Verde",
        "year": 1974,
        "phone": [238],
        "tld": [".cv"],
        "alias": [""],
        "languages": ["pt"],
        "currencies": [
            "CVE",
        ],
    },
    "CW": {
        "code": "CW",
        "name": "Curaçao",
        "native": "Curaçao",
        "year": 2010,
        "phone": [5999],
        "tld": [".cw"],
        "alias": [""],
        "languages": ["nl", "pa", "en"],
        "currencies": [
            "ANG",
        ],
    },
    "CX": {
        "code": "CX",
        "name": "Christmas Island",
        "native": "Christmas Island",
        "year": 1974,
        "phone": [61],
        "tld": [".cx"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "AUD",
        ],
    },
    "CY": {
        "code": "CY",
        "name": "Cyprus",
        "native": "Κύπρος",
        "year": 1974,
        "phone": [357],
        "tld": [".cy"],
        "alias": [""],
        "languages": ["el", "tr", "hy"],
        "currencies": [
            "EUR",
        ],
    },
    "CZ": {
        "code": "CZ",
        "name": "Czechia",
        "native": "Česká republika",
        "year": 1993,
        "phone": [420],
        "tld": [".cz"],
        "alias": [""],
        "languages": ["cs", "sk"],
        "currencies": [
            "CZK",
        ],
    },
    "DE": {
        "code": "DE",
        "name": "Germany",
        "native": "Deutschland",
        "year": 1974,
        "phone": [49],
        "tld": [".de"],
        "alias": [""],
        "languages": ["de"],
        "currencies": [
            "EUR",
        ],
    },
    "DJ": {
        "code": "DJ",
        "name": "Djibouti",
        "native": "Djibouti",
        "year": 1977,
        "phone": [253],
        "tld": [".dj"],
        "alias": [""],
        "languages": ["fr", "ar"],
        "currencies": [
            "DJF",
        ],
    },
    "DK": {
        "code": "DK",
        "name": "Denmark",
        "native": "Danmark",
        "year": 1974,
        "phone": [45],
        "tld": [".dk"],
        "alias": [""],
        "languages": ["da"],
        "currencies": [
            "DKK",
        ],
    },
    "DM": {
        "code": "DM",
        "name": "Dominica",
        "native": "Dominica",
        "year": 1974,
        "phone": [1767],
        "tld": [".dm"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "XCD",
        ],
    },
    "DO": {
        "code": "DO",
        "name": "Dominican Republic",
        "native": "República Dominicana",
        "year": 1974,
        "phone": [1809, 1829, 1849],
        "tld": [".do"],
        "alias": [""],
        "languages": ["es"],
        "currencies": [
            "DOP",
        ],
    },
    "DZ": {
        "code": "DZ",
        "name": "Algeria",
        "native": "الجزائر",
        "year": 1974,
        "phone": [213],
        "tld": [".dz"],
        "alias": [""],
        "languages": ["ar"],
        "currencies": [
            "DZD",
        ],
    },
    "EC": {
        "code": "EC",
        "name": "Ecuador",
        "native": "Ecuador",
        "year": 1974,
        "phone": [593],
        "tld": [".ec"],
        "alias": [""],
        "languages": ["es"],
        "currencies": [
            "USD",
        ],
    },
    "EE": {
        "code": "EE",
        "name": "Estonia",
        "native": "Eesti",
        "year": 1992,
        "phone": [372],
        "tld": [".ee"],
        "alias": [""],
        "languages": ["et"],
        "currencies": [
            "EUR",
        ],
    },
    "EG": {
        "code": "EG",
        "name": "Egypt",
        "native": "مصر\u200e",
        "year": 1974,
        "phone": [20],
        "tld": [".eg"],
        "alias": [""],
        "languages": ["ar"],
        "currencies": [
            "EGP",
        ],
    },
    "EH": {
        "code": "EH",
        "name": "Western Sahara",
        "native": "الصحراء الغربية",
        "year": 1974,
        "phone": [212],
        "tld": [""],
        "alias": [""],
        "languages": ["es"],
        "currencies": [
            "MAD",
        ],
    },
    "ER": {
        "code": "ER",
        "name": "Eritrea",
        "native": "ኤርትራ",
        "year": 1993,
        "phone": [291],
        "tld": [".er"],
        "alias": [""],
        "languages": ["ti", "ar", "en"],
        "currencies": ["ETB", "ERN"],
    },
    "ES": {
        "code": "ES",
        "name": "Spain",
        "native": "España",
        "year": 1974,
        "phone": [34],
        "tld": [".es"],
        "alias": [""],
        "languages": ["es", "eu", "ca", "gl", "oc"],
        "currencies": [
            "EUR",
        ],
    },
    "ET": {
        "code": "ET",
        "name": "Ethiopia",
        "native": "ኢትዮጵያ",
        "year": 1974,
        "phone": [251],
        "tld": [".et"],
        "alias": [""],
        "languages": ["am"],
        "currencies": [
            "ETB",
        ],
    },
    "FI": {
        "code": "FI",
        "name": "Finland",
        "native": "Suomi",
        "year": 1974,
        "phone": [358],
        "tld": [".fi"],
        "alias": [""],
        "languages": ["fi", "sv"],
        "currencies": [
            "EUR",
        ],
    },
    "FJ": {
        "code": "FJ",
        "name": "Fiji",
        "native": "Fiji",
        "year": 1974,
        "phone": [679],
        "tld": [".fj"],
        "alias": [""],
        "languages": ["en", "fj", "hi", "ur"],
        "currencies": [
            "FJD",
        ],
    },
    "FK": {
        "code": "FK",
        "name": "Falkland Islands [Malvinas]",
        "native": "Falkland Islands",
        "year": 1974,
        "phone": [500],
        "tld": [".fk"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "FKP",
        ],
    },
    "FM": {
        "code": "FM",
        "name": "Micronesia [Federated States of]",
        "native": "Micronesia",
        "year": 1986,
        "phone": [691],
        "tld": [".fm"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "USD",
        ],
    },
    "FO": {
        "code": "FO",
        "name": "Faroe Islands",
        "native": "Føroyar",
        "year": 1974,
        "phone": [298],
        "tld": [".fo"],
        "alias": [""],
        "languages": ["fo"],
        "currencies": [
            "DKK",
        ],
    },
    "FR": {
        "code": "FR",
        "name": "France",
        "native": "France",
        "year": 1974,
        "phone": [33],
        "tld": [".fr"],
        "alias": [""],
        "languages": ["fr"],
        "currencies": [
            "EUR",
        ],
    },
    "GA": {
        "code": "GA",
        "name": "Gabon",
        "native": "Gabon",
        "year": 1974,
        "phone": [241],
        "tld": [".ga"],
        "alias": [""],
        "languages": ["fr"],
        "currencies": [
            "XAF",
        ],
    },
    "GB": {
        "code": "GB",
        "name": "United Kingdom of Great Britain and Northern Ireland",
        "native": "United Kingdom",
        "year": 1974,
        "phone": [44],
        "tld": [".gb", ".uk"],
        "alias": ["UK"],
        "languages": ["en"],
        "currencies": [
            "GBP",
        ],
    },
    "GD": {
        "code": "GD",
        "name": "Grenada",
        "native": "Grenada",
        "year": 1974,
        "phone": [1473],
        "tld": [".gd"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "XCD",
        ],
    },
    "GE": {
        "code": "GE",
        "name": "Georgia",
        "native": "საქართველო",
        "year": 1992,
        "phone": [995],
        "tld": [".ge"],
        "alias": [""],
        "languages": ["ka"],
        "currencies": [
            "GEL",
        ],
    },
    "GF": {
        "code": "GF",
        "name": "French Guiana",
        "native": "Guyane française",
        "year": 1974,
        "phone": [594],
        "tld": [".gf"],
        "alias": [""],
        "languages": ["fr"],
        "currencies": [
            "EUR",
        ],
    },
    "GG": {
        "code": "GG",
        "name": "Guernsey",
        "native": "Guernsey",
        "year": 2006,
        "phone": [44],
        "tld": [".gg"],
        "alias": [""],
        "languages": ["en", "fr"],
        "currencies": [
            "GBP",
        ],
    },
    "GH": {
        "code": "GH",
        "name": "Ghana",
        "native": "Ghana",
        "year": 1974,
        "phone": [233],
        "tld": [".gh"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "GHS",
        ],
    },
    "GI": {
        "code": "GI",
        "name": "Gibraltar",
        "native": "Gibraltar",
        "year": 1974,
        "phone": [350],
        "tld": [".gi"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "GIP",
        ],
    },
    "GL": {
        "code": "GL",
        "name": "Greenland",
        "native": "Kalaallit Nunaat",
        "year": 1974,
        "phone": [299],
        "tld": [".gl"],
        "alias": [""],
        "languages": ["kl"],
        "currencies": [
            "DKK",
        ],
    },
    "GM": {
        "code": "GM",
        "name": "Gambia",
        "native": "Gambia",
        "year": 1974,
        "phone": [220],
        "tld": [".gm"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "GMD",
        ],
    },
    "GN": {
        "code": "GN",
        "name": "Guinea",
        "native": "Guinée",
        "year": 1974,
        "phone": [224],
        "tld": [".gn"],
        "alias": [""],
        "languages": ["fr", "ff"],
        "currencies": [
            "GNF",
        ],
    },
    "GP": {
        "code": "GP",
        "name": "Guadeloupe",
        "native": "Guadeloupe",
        "year": 1974,
        "phone": [590],
        "tld": [".gp"],
        "alias": [""],
        "languages": ["fr"],
        "currencies": [
            "EUR",
        ],
    },
    "GQ": {
        "code": "GQ",
        "name": "Equatorial Guinea",
        "native": "Guinea Ecuatorial",
        "year": 1974,
        "phone": [240],
        "tld": [".gq"],
        "alias": [""],
        "languages": ["es", "fr"],
        "currencies": [
            "XAF",
        ],
    },
    "GR": {
        "code": "GR",
        "name": "Greece",
        "native": "Ελλάδα",
        "year": 1974,
        "phone": [30],
        "tld": [".gr"],
        "alias": ["EL"],
        "languages": ["el"],
        "currencies": [
            "EUR",
        ],
    },
    "GS": {
        "code": "GS",
        "name": "South Georgia and the South Sandwich Islands",
        "native": "South Georgia",
        "year": 1993,
        "phone": [500],
        "tld": [".gs"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "GBP",
        ],
    },
    "GT": {
        "code": "GT",
        "name": "Guatemala",
        "native": "Guatemala",
        "year": 1974,
        "phone": [502],
        "tld": [".gt"],
        "alias": [""],
        "languages": ["es"],
        "currencies": [
            "GTQ",
        ],
    },
    "GU": {
        "code": "GU",
        "name": "Guam",
        "native": "Guam",
        "year": 1974,
        "phone": [1671],
        "tld": [".gu"],
        "alias": [""],
        "languages": ["en", "ch", "es"],
        "currencies": [
            "USD",
        ],
    },
    "GW": {
        "code": "GW",
        "name": "Guinea-Bissau",
        "native": "Guiné-Bissau",
        "year": 1974,
        "phone": [245],
        "tld": [".gw"],
        "alias": [""],
        "languages": ["pt"],
        "currencies": [
            "XOF",
        ],
    },
    "GY": {
        "code": "GY",
        "name": "Guyana",
        "native": "Guyana",
        "year": 1974,
        "phone": [592],
        "tld": [".gy"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "GYD",
        ],
    },
    "HK": {
        "code": "HK",
        "name": "Hong Kong",
        "native": "香港",
        "year": 1974,
        "phone": [852],
        "tld": [".hk"],
        "alias": [""],
        "languages": ["zh", "en"],
        "currencies": [
            "HKD",
        ],
    },
    "HM": {
        "code": "HM",
        "name": "Heard Island and McDonald Islands",
        "native": "Heard Island and McDonald Islands",
        "year": 1974,
        "phone": [61],
        "tld": [".hm"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "AUD",
        ],
    },
    "HN": {
        "code": "HN",
        "name": "Honduras",
        "native": "Honduras",
        "year": 1974,
        "phone": [504],
        "tld": [".hn"],
        "alias": [""],
        "languages": ["es"],
        "currencies": [
            "HNL",
        ],
    },
    "HR": {
        "code": "HR",
        "name": "Croatia",
        "native": "Hrvatska",
        "year": 1992,
        "phone": [385],
        "tld": [".hr"],
        "alias": [""],
        "languages": ["hr"],
        "currencies": [
            "HRK",
        ],
    },
    "HT": {
        "code": "HT",
        "name": "Haiti",
        "native": "Haïti",
        "year": 1974,
        "phone": [509],
        "tld": [".ht"],
        "alias": [""],
        "languages": ["fr", "ht"],
        "currencies": ["HTG", "USD"],
    },
    "HU": {
        "code": "HU",
        "name": "Hungary",
        "native": "Magyarország",
        "year": 1974,
        "phone": [36],
        "tld": [".hu"],
        "alias": [""],
        "languages": ["hu"],
        "currencies": [
            "HUF",
        ],
    },
    "ID": {
        "code": "CODE",
        "name": "Indonesia",
        "native": "Indonesia",
        "year": 1974,
        "phone": [62],
        "tld": [".id"],
        "alias": [""],
        "languages": ["id"],
        "currencies": [
            "IDR",
        ],
    },
    "IE": {
        "code": "IE",
        "name": "Ireland",
        "native": "Éire",
        "year": 1974,
        "phone": [353],
        "tld": [".ie"],
        "alias": [""],
        "languages": ["ga", "en"],
        "currencies": [
            "EUR",
        ],
    },
    "IL": {
        "code": "IL",
        "name": "Israel",
        "native": "יִשְׂרָאֵל",
        "year": 1974,
        "phone": [972],
        "tld": [".il"],
        "alias": [""],
        "languages": ["he", "ar"],
        "currencies": [
            "ILS",
        ],
    },
    "IM": {
        "code": "IM",
        "name": "Isle of Man",
        "native": "Isle of Man",
        "year": 2006,
        "phone": [44],
        "tld": [".im"],
        "alias": [""],
        "languages": ["en", "gv"],
        "currencies": [
            "GBP",
        ],
    },
    "IN": {
        "code": "IN",
        "name": "India",
        "native": "भारत",
        "year": 1974,
        "phone": [91],
        "tld": [".in"],
        "alias": [""],
        "languages": ["hi", "en"],
        "currencies": [
            "INR",
        ],
    },
    "IO": {
        "code": "IO",
        "name": "British Indian Ocean Territory",
        "native": "British Indian Ocean Territory",
        "year": 1974,
        "phone": [246],
        "tld": [".io"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "USD",
        ],
    },
    "IQ": {
        "code": "IQ",
        "name": "Iraq",
        "native": "العراق",
        "year": 1974,
        "phone": [964],
        "tld": [".iq"],
        "alias": [""],
        "languages": ["ar", "ku"],
        "currencies": [
            "IQD",
        ],
    },
    "IR": {
        "code": "IR",
        "name": "Iran [Islamic Republic of]",
        "native": "ایران",
        "year": 1974,
        "phone": [98],
        "tld": [".ir"],
        "alias": [""],
        "languages": ["fa"],
        "currencies": [
            "IRR",
        ],
    },
    "IS": {
        "code": "IS",
        "name": "Iceland",
        "native": "Ísland",
        "year": 1974,
        "phone": [354],
        "tld": [".is"],
        "alias": [""],
        "languages": ["is"],
        "currencies": [
            "ISK",
        ],
    },
    "IT": {
        "code": "IT",
        "name": "Italy",
        "native": "Italia",
        "year": 1974,
        "phone": [39],
        "tld": [".it"],
        "alias": [""],
        "languages": ["it"],
        "currencies": [
            "EUR",
        ],
    },
    "JE": {
        "code": "JE",
        "name": "Jersey",
        "native": "Jersey",
        "year": 2006,
        "phone": [44],
        "tld": [".je"],
        "alias": [""],
        "languages": ["en", "fr"],
        "currencies": [
            "GBP",
        ],
    },
    "JM": {
        "code": "JM",
        "name": "Jamaica",
        "native": "Jamaica",
        "year": 1974,
        "phone": [1876],
        "tld": [".jm"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "JMD",
        ],
    },
    "JO": {
        "code": "JO",
        "name": "Jordan",
        "native": "الأردن",
        "year": 1974,
        "phone": [962],
        "tld": [".jo"],
        "alias": [""],
        "languages": ["ar"],
        "currencies": [
            "JOD",
        ],
    },
    "JP": {
        "code": "JP",
        "name": "Japan",
        "native": "日本",
        "year": 1974,
        "phone": [81],
        "tld": [".jp"],
        "alias": [""],
        "languages": ["ja"],
        "currencies": [
            "JPY",
        ],
    },
    "KE": {
        "code": "KE",
        "name": "Kenya",
        "native": "Kenya",
        "year": 1974,
        "phone": [254],
        "tld": [".ke"],
        "alias": [""],
        "languages": ["en", "sw"],
        "currencies": [
            "KES",
        ],
    },
    "KG": {
        "code": "KG",
        "name": "Kyrgyzstan",
        "native": "Кыргызстан",
        "year": 1992,
        "phone": [996],
        "tld": [".kg"],
        "alias": [""],
        "languages": ["ky", "ru"],
        "currencies": [
            "KGS",
        ],
    },
    "KH": {
        "code": "KH",
        "name": "Cambodia",
        "native": "Kâmpŭchéa",
        "year": 1974,
        "phone": [855],
        "tld": [".kh"],
        "alias": [""],
        "languages": ["km"],
        "currencies": [
            "KHR",
        ],
    },
    "KI": {
        "code": "KI",
        "name": "Kiribati",
        "native": "Kiribati",
        "year": 1979,
        "phone": [686],
        "tld": [".ki"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "AUD",
        ],
    },
    "KM": {
        "code": "KM",
        "name": "Comoros",
        "native": "Komori",
        "year": 1974,
        "phone": [269],
        "tld": [".km"],
        "alias": [""],
        "languages": ["ar", "fr"],
        "currencies": [
            "KMF",
        ],
    },
    "KN": {
        "code": "KN",
        "name": "Saint Kitts and Nevis",
        "native": "Saint Kitts and Nevis",
        "year": 1974,
        "phone": [1869],
        "tld": [".kn"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "XCD",
        ],
    },
    "KP": {
        "code": "KP",
        "name": "Korea [Democratic People's Republic of]",
        "native": "북한",
        "year": 1974,
        "phone": [850],
        "tld": [".kp"],
        "alias": [""],
        "languages": ["ko"],
        "currencies": [
            "KPW",
        ],
    },
    "KR": {
        "code": "KR",
        "name": "Korea, Republic of",
        "native": "대한민국",
        "year": 1974,
        "phone": [82],
        "tld": [".kr"],
        "alias": [""],
        "languages": ["ko"],
        "currencies": [
            "KRW",
        ],
    },
    "KW": {
        "code": "KW",
        "name": "Kuwait",
        "native": "الكويت",
        "year": 1974,
        "phone": [965],
        "tld": [".kw"],
        "alias": [""],
        "languages": ["ar"],
        "currencies": [
            "KWD",
        ],
    },
    "KY": {
        "code": "KY",
        "name": "Cayman Islands",
        "native": "Cayman Islands",
        "year": 1974,
        "phone": [1345],
        "tld": [".ky"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "KYD",
        ],
    },
    "KZ": {
        "code": "KZ",
        "name": "Kazakhstan",
        "native": "Қазақстан",
        "year": 1992,
        "phone": [76, 77],
        "tld": [".kz"],
        "alias": [""],
        "languages": ["kk", "ru"],
        "currencies": [
            "KZT",
        ],
    },
    "LA": {
        "code": "LA",
        "name": "Lao People's Democratic Republic",
        "native": "ສປປລາວ",
        "year": 1974,
        "phone": [856],
        "tld": [".la"],
        "alias": [""],
        "languages": ["lo"],
        "currencies": [
            "LAK",
        ],
    },
    "LB": {
        "code": "LB",
        "name": "Lebanon",
        "native": "لبنان",
        "year": 1974,
        "phone": [961],
        "tld": [".lb"],
        "alias": [""],
        "languages": ["ar", "fr"],
        "currencies": [
            "LBP",
        ],
    },
    "LC": {
        "code": "LC",
        "name": "Saint Lucia",
        "native": "Saint Lucia",
        "year": 1974,
        "phone": [1758],
        "tld": [".lc"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "XCD",
        ],
    },
    "LI": {
        "code": "LI",
        "name": "Liechtenstein",
        "native": "Liechtenstein",
        "year": 1974,
        "phone": [423],
        "tld": [".li"],
        "alias": [""],
        "languages": ["de"],
        "currencies": [
            "CHF",
        ],
    },
    "LK": {
        "code": "LK",
        "name": "Sri Lanka",
        "native": "śrī laṃkāva",
        "year": 1974,
        "phone": [94],
        "tld": [".lk"],
        "alias": [""],
        "languages": ["si", "ta"],
        "currencies": [
            "LKR",
        ],
    },
    "LR": {
        "code": "LR",
        "name": "Liberia",
        "native": "Liberia",
        "year": 1974,
        "phone": [231],
        "tld": [".lr"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "LRD",
        ],
    },
    "LS": {
        "code": "LS",
        "name": "Lesotho",
        "native": "Lesotho",
        "year": 1974,
        "phone": [266],
        "tld": [".ls"],
        "alias": [""],
        "languages": ["en", "st"],
        "currencies": ["LSL", "ZAR"],
    },
    "LT": {
        "code": "LT",
        "name": "Lithuania",
        "native": "Lietuva",
        "year": 1992,
        "phone": [370],
        "tld": [".lt"],
        "alias": [""],
        "languages": ["lt"],
        "currencies": [
            "LTL",
        ],
    },
    "LU": {
        "code": "LU",
        "name": "Luxembourg",
        "native": "Luxembourg",
        "year": 1974,
        "phone": [352],
        "tld": [".lu"],
        "alias": [""],
        "languages": ["fr", "de", "lb"],
        "currencies": [
            "EUR",
        ],
    },
    "LV": {
        "code": "LV",
        "name": "Latvia",
        "native": "Latvija",
        "year": 1992,
        "phone": [371],
        "tld": [".lv"],
        "alias": [""],
        "languages": ["lv"],
        "currencies": [
            "EUR",
        ],
    },
    "LY": {
        "code": "LY",
        "name": "Libya",
        "native": "\u200fليبيا",
        "year": 1974,
        "phone": [218],
        "tld": [".ly"],
        "alias": [""],
        "languages": ["ar"],
        "currencies": [
            "LYD",
        ],
    },
    "MA": {
        "code": "MA",
        "name": "Morocco",
        "native": "المغرب",
        "year": 1974,
        "phone": [212],
        "tld": [".ma"],
        "alias": [""],
        "languages": ["ar"],
        "currencies": [
            "MAD",
        ],
    },
    "MC": {
        "code": "MC",
        "name": "Monaco",
        "native": "Monaco",
        "year": 1974,
        "phone": [377],
        "tld": [".mc"],
        "alias": [""],
        "languages": ["fr"],
        "currencies": [
            "EUR",
        ],
    },
    "MD": {
        "code": "MD",
        "name": "Moldova, Republic of",
        "native": "Moldova",
        "year": 1992,
        "phone": [373],
        "tld": [".md"],
        "alias": [""],
        "languages": ["ro"],
        "currencies": [
            "MDL",
        ],
    },
    "ME": {
        "code": "ME",
        "name": "Montenegro",
        "native": "Црна Гора",
        "year": 2006,
        "phone": [382],
        "tld": [".me"],
        "alias": [""],
        "languages": ["sr", "bs", "sq", "hr"],
        "currencies": [
            "EUR",
        ],
    },
    "MF": {
        "code": "MF",
        "name": "Saint Martin [French part]",
        "native": "Saint-Martin",
        "year": 2007,
        "phone": [590],
        "tld": [".mf"],
        "alias": [""],
        "languages": ["en", "fr", "nl"],
        "currencies": [
            "EUR",
        ],
    },
    "MG": {
        "code": "MG",
        "name": "Madagascar",
        "native": "Madagasikara",
        "year": 1974,
        "phone": [261],
        "tld": [".mg"],
        "alias": [""],
        "languages": ["fr", "mg"],
        "currencies": [
            "MGA",
        ],
    },
    "MH": {
        "code": "MH",
        "name": "Marshall Islands",
        "native": "M̧ajeļ",
        "year": 1986,
        "phone": [692],
        "tld": [".mh"],
        "alias": [""],
        "languages": ["en", "mh"],
        "currencies": [
            "USD",
        ],
    },
    "MK": {
        "code": "MK",
        "name": "North Macedonia",
        "native": "Северна Македонија",
        "year": 1993,
        "phone": [389],
        "tld": [".mk"],
        "alias": [""],
        "languages": ["mk"],
        "currencies": [
            "MKD",
        ],
    },
    "ML": {
        "code": "ML",
        "name": "Mali",
        "native": "Mali",
        "year": 1974,
        "phone": [223],
        "tld": [".ml"],
        "alias": [""],
        "languages": ["fr"],
        "currencies": [
            "XOF",
        ],
    },
    "MM": {
        "code": "MM",
        "name": "Myanmar",
        "native": "မြန်မာ",
        "year": 1989,
        "phone": [95],
        "tld": [".mm"],
        "alias": [""],
        "languages": ["my"],
        "currencies": [
            "MMK",
        ],
    },
    "MN": {
        "code": "MN",
        "name": "Mongolia",
        "native": "Монгол улс",
        "year": 1974,
        "phone": [976],
        "tld": [".mn"],
        "alias": [""],
        "languages": ["mn"],
        "currencies": [
            "MNT",
        ],
    },
    "MO": {
        "code": "MO",
        "name": "Macao",
        "native": "澳門",
        "year": 1974,
        "phone": [853],
        "tld": [".mo"],
        "alias": [""],
        "languages": ["zh", "pt"],
        "currencies": [
            "MOP",
        ],
    },
    "MP": {
        "code": "MP",
        "name": "Northern Mariana Islands",
        "native": "Northern Mariana Islands",
        "year": 1986,
        "phone": [1670],
        "tld": [".mp"],
        "alias": [""],
        "languages": ["en", "ch"],
        "currencies": [
            "USD",
        ],
    },
    "MQ": {
        "code": "MQ",
        "name": "Martinique",
        "native": "Martinique",
        "year": 1974,
        "phone": [596],
        "tld": [".mq"],
        "alias": [""],
        "languages": ["fr"],
        "currencies": [
            "EUR",
        ],
    },
    "MR": {
        "code": "MR",
        "name": "Mauritania",
        "native": "موريتانيا",
        "year": 1974,
        "phone": [222],
        "tld": [".mr"],
        "alias": [""],
        "languages": ["ar"],
        "currencies": [
            "MRO",
        ],
    },
    "MS": {
        "code": "MS",
        "name": "Montserrat",
        "native": "Montserrat",
        "year": 1974,
        "phone": [1664],
        "tld": [".ms"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "XCD",
        ],
    },
    "MT": {
        "code": "MT",
        "name": "Malta",
        "native": "Malta",
        "year": 1974,
        "phone": [356],
        "tld": [".mt"],
        "alias": [""],
        "languages": ["mt", "en"],
        "currencies": [
            "EUR",
        ],
    },
    "MU": {
        "code": "MU",
        "name": "Mauritius",
        "native": "Maurice",
        "year": 1974,
        "phone": [230],
        "tld": [".mu"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "MUR",
        ],
    },
    "MV": {
        "code": "MV",
        "name": "Maldives",
        "native": "Maldives",
        "year": 1974,
        "phone": [960],
        "tld": [".mv"],
        "alias": [""],
        "languages": ["dv"],
        "currencies": [
            "MVR",
        ],
    },
    "MW": {
        "code": "MW",
        "name": "Malawi",
        "native": "Malawi",
        "year": 1974,
        "phone": [265],
        "tld": [".mw"],
        "alias": [""],
        "languages": ["en", "ny"],
        "currencies": [
            "MWK",
        ],
    },
    "MX": {
        "code": "MX",
        "name": "Mexico",
        "native": "México",
        "year": 1974,
        "phone": [52],
        "tld": [".mx"],
        "alias": [""],
        "languages": ["es"],
        "currencies": [
            "MXN",
        ],
    },
    "MY": {
        "code": "MY",
        "name": "Malaysia",
        "native": "Malaysia",
        "year": 1974,
        "phone": [60],
        "tld": [".my"],
        "alias": [""],
        "languages": ["ms"],
        "currencies": [
            "MYR",
        ],
    },
    "MZ": {
        "code": "MZ",
        "name": "Mozambique",
        "native": "Moçambique",
        "year": 1974,
        "phone": [258],
        "tld": [".mz"],
        "alias": [""],
        "languages": ["pt"],
        "currencies": [
            "MZM",
        ],
    },
    "NA": {
        "code": "NA",
        "name": "Namibia",
        "native": "Namibia",
        "year": 1974,
        "phone": [264],
        "tld": [".na"],
        "alias": [""],
        "languages": ["en", "af"],
        "currencies": ["NAD", "ZAR"],
    },
    "NC": {
        "code": "NC",
        "name": "New Caledonia",
        "native": "Nouvelle-Calédonie",
        "year": 1974,
        "phone": [687],
        "tld": [".nc"],
        "alias": [""],
        "languages": ["fr"],
        "currencies": [
            "XPF",
        ],
    },
    "NE": {
        "code": "NE",
        "name": "Niger",
        "native": "Niger",
        "year": 1974,
        "phone": [227],
        "tld": [".ne"],
        "alias": [""],
        "languages": ["fr"],
        "currencies": [
            "XOF",
        ],
    },
    "NF": {
        "code": "NF",
        "name": "Norfolk Island",
        "native": "Norfolk Island",
        "year": 1974,
        "phone": [672],
        "tld": [".nf"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "AUD",
        ],
    },
    "NG": {
        "code": "NG",
        "name": "Nigeria",
        "native": "Nigeria",
        "year": 1974,
        "phone": [234],
        "tld": [".ng"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "NGN",
        ],
    },
    "NI": {
        "code": "NI",
        "name": "Nicaragua",
        "native": "Nicaragua",
        "year": 1974,
        "phone": [505],
        "tld": [".ni"],
        "alias": [""],
        "languages": ["es"],
        "currencies": [
            "NIO",
        ],
    },
    "NL": {
        "code": "NL",
        "name": "Netherlands",
        "native": "Nederland",
        "year": 1974,
        "phone": [31],
        "tld": [".nl"],
        "alias": [""],
        "languages": ["nl"],
        "currencies": [
            "EUR",
        ],
    },
    "NO": {
        "code": "NO",
        "name": "Norway",
        "native": "Norge",
        "year": 1974,
        "phone": [47],
        "tld": [".no"],
        "alias": [""],
        "languages": ["no", "nb", "nn"],
        "currencies": [
            "NOK",
        ],
    },
    "NP": {
        "code": "NP",
        "name": "Nepal",
        "native": "नपल",
        "year": 1974,
        "phone": [977],
        "tld": [".np"],
        "alias": [""],
        "languages": ["ne"],
        "currencies": [
            "NPR",
        ],
    },
    "NR": {
        "code": "NR",
        "name": "Nauru",
        "native": "Nauru",
        "year": 1974,
        "phone": [674],
        "tld": [".nr"],
        "alias": [""],
        "languages": ["en", "na"],
        "currencies": [
            "AUD",
        ],
    },
    "NU": {
        "code": "NU",
        "name": "Niue",
        "native": "Niuē",
        "year": 1974,
        "phone": [683],
        "tld": [".nu"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "NZD",
        ],
    },
    "NZ": {
        "code": "NZ",
        "name": "New Zealand",
        "native": "New Zealand",
        "year": 1974,
        "phone": [64],
        "tld": [".nz"],
        "alias": [""],
        "languages": ["en", "mi"],
        "currencies": [
            "NZD",
        ],
    },
    "OM": {
        "code": "OM",
        "name": "Oman",
        "native": "عمان",
        "year": 1974,
        "phone": [968],
        "tld": [".om"],
        "alias": [""],
        "languages": ["ar"],
        "currencies": [
            "OMR",
        ],
    },
    "PA": {
        "code": "PA",
        "name": "Panama",
        "native": "Panamá",
        "year": 1974,
        "phone": [507],
        "tld": [".pa"],
        "alias": [""],
        "languages": ["es"],
        "currencies": ["PAB", "USD"],
    },
    "PE": {
        "code": "PE",
        "name": "Peru",
        "native": "Perú",
        "year": 1974,
        "phone": [51],
        "tld": [".pe"],
        "alias": [""],
        "languages": ["es"],
        "currencies": [
            "PEN",
        ],
    },
    "PF": {
        "code": "PF",
        "name": "French Polynesia",
        "native": "Polynésie française",
        "year": 1974,
        "phone": [689],
        "tld": [".pf"],
        "alias": [""],
        "languages": ["fr"],
        "currencies": [
            "XPF",
        ],
    },
    "PG": {
        "code": "PG",
        "name": "Papua New Guinea",
        "native": "Papua Niugini",
        "year": 1974,
        "phone": [675],
        "tld": [".pg"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "PGK",
        ],
    },
    "PH": {
        "code": "PH",
        "name": "Philippines",
        "native": "Pilipinas",
        "year": 1974,
        "phone": [63],
        "tld": [".ph"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "PHP",
        ],
    },
    "PK": {
        "code": "PK",
        "name": "Pakistan",
        "native": "Pakistan",
        "year": 1974,
        "phone": [92],
        "tld": [".pk"],
        "alias": [""],
        "languages": ["en", "ur"],
        "currencies": [
            "PKR",
        ],
    },
    "PL": {
        "code": "PL",
        "name": "Poland",
        "native": "Polska",
        "year": 1974,
        "phone": [48],
        "tld": [".pl"],
        "alias": [""],
        "languages": ["pl"],
        "currencies": [
            "PLN",
        ],
    },
    "PM": {
        "code": "PM",
        "name": "Saint Pierre and Miquelon",
        "native": "Saint-Pierre-et-Miquelon",
        "year": 1974,
        "phone": [508],
        "tld": [".pm"],
        "alias": [""],
        "languages": ["fr"],
        "currencies": [
            "EUR",
        ],
    },
    "PN": {
        "code": "PN",
        "name": "Pitcairn",
        "native": "Pitcairn Islands",
        "year": 1974,
        "phone": [64],
        "tld": [".pn"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "NZD",
        ],
    },
    "PR": {
        "code": "PR",
        "name": "Puerto Rico",
        "native": "Puerto Rico",
        "year": 1974,
        "phone": [1787, 1939],
        "tld": [".pr"],
        "alias": [""],
        "languages": ["es", "en"],
        "currencies": [
            "USD",
        ],
    },
    "PS": {
        "code": "PS",
        "name": "Palestine, State of",
        "native": "فلسطين",
        "year": 1999,
        "phone": [970],
        "tld": [".ps"],
        "alias": [""],
        "languages": ["ar"],
        "currencies": [],
    },
    "PT": {
        "code": "PT",
        "name": "Portugal",
        "native": "Portugal",
        "year": 1974,
        "phone": [351],
        "tld": [".pt"],
        "alias": [""],
        "languages": ["pt"],
        "currencies": [
            "EUR",
        ],
    },
    "PW": {
        "code": "PW",
        "name": "Palau",
        "native": "Palau",
        "year": 1986,
        "phone": [680],
        "tld": [".pw"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "USD",
        ],
    },
    "PY": {
        "code": "PY",
        "name": "Paraguay",
        "native": "Paraguay",
        "year": 1974,
        "phone": [595],
        "tld": [".py"],
        "alias": [""],
        "languages": ["es", "gn"],
        "currencies": [
            "PYG",
        ],
    },
    "QA": {
        "code": "QA",
        "name": "Qatar",
        "native": "قطر",
        "year": 1974,
        "phone": [974],
        "tld": [".qa"],
        "alias": [""],
        "languages": ["ar"],
        "currencies": [
            "QAR",
        ],
    },
    "RE": {
        "code": "RE",
        "name": "Réunion",
        "native": "La Réunion",
        "year": 1974,
        "phone": [262],
        "tld": [".re"],
        "alias": [""],
        "languages": ["fr"],
        "currencies": [
            "EUR",
        ],
    },
    "RO": {
        "code": "RO",
        "name": "Romania",
        "native": "România",
        "year": 1974,
        "phone": [40],
        "tld": [".ro"],
        "alias": [""],
        "languages": ["ro"],
        "currencies": [
            "RON",
        ],
    },
    "RS": {
        "code": "RS",
        "name": "Serbia",
        "native": "Србија",
        "year": 2006,
        "phone": [381],
        "tld": [".rs"],
        "alias": [""],
        "languages": ["sr"],
        "currencies": [
            "RSD",
        ],
    },
    "RU": {
        "code": "RU",
        "name": "Russian Federation",
        "native": "Россия",
        "year": 1992,
        "phone": [7],
        "tld": [".ru"],
        "alias": [""],
        "languages": ["ru"],
        "currencies": [
            "RUB",
        ],
    },
    "RW": {
        "code": "RW",
        "name": "Rwanda",
        "native": "Rwanda",
        "year": 1974,
        "phone": [250],
        "tld": [".rw"],
        "alias": [""],
        "languages": ["rw", "en", "fr"],
        "currencies": [
            "RWF",
        ],
    },
    "SA": {
        "code": "SA",
        "name": "Saudi Arabia",
        "native": "العربية السعودية",
        "year": 1974,
        "phone": [966],
        "tld": [".sa"],
        "alias": [""],
        "languages": ["ar"],
        "currencies": [
            "SAR",
        ],
    },
    "SB": {
        "code": "SB",
        "name": "Solomon Islands",
        "native": "Solomon Islands",
        "year": 1974,
        "phone": [677],
        "tld": [".sb"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "SBD",
        ],
    },
    "SC": {
        "code": "SC",
        "name": "Seychelles",
        "native": "Seychelles",
        "year": 1974,
        "phone": [248],
        "tld": [".sc"],
        "alias": [""],
        "languages": ["fr", "en"],
        "currencies": [
            "SCR",
        ],
    },
    "SD": {
        "code": "SD",
        "name": "Sudan",
        "native": "السودان",
        "year": 1974,
        "phone": [249],
        "tld": [".sd"],
        "alias": [""],
        "languages": ["ar", "en"],
        "currencies": [
            "SDG",
        ],
    },
    "SE": {
        "code": "SE",
        "name": "Sweden",
        "native": "Sverige",
        "year": 1974,
        "phone": [46],
        "tld": [".se"],
        "alias": [""],
        "languages": ["sv"],
        "currencies": [
            "SEK",
        ],
    },
    "SG": {
        "code": "SG",
        "name": "Singapore",
        "native": "Singapore",
        "year": 1974,
        "phone": [65],
        "tld": [".sg"],
        "alias": [""],
        "languages": ["en", "ms", "ta", "zh"],
        "currencies": [
            "SGD",
        ],
    },
    "SH": {
        "code": "SH",
        "name": "Saint Helena, Ascension and Tristan da Cunha",
        "native": "Saint Helena",
        "year": 1974,
        "phone": [290],
        "tld": [".sh"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "SHP",
        ],
    },
    "SI": {
        "code": "SI",
        "name": "Slovenia",
        "native": "Slovenija",
        "year": 1992,
        "phone": [386],
        "tld": [".si"],
        "alias": [""],
        "languages": ["sl"],
        "currencies": [
            "EUR",
        ],
    },
    "SJ": {
        "code": "SJ",
        "name": "Svalbard and Jan Mayen",
        "native": "Svalbard og Jan Mayen",
        "year": 1974,
        "phone": [4779],
        "tld": [".sj"],
        "alias": [""],
        "languages": ["no"],
        "currencies": [
            "NOK",
        ],
    },
    "SK": {
        "code": "SK",
        "name": "Slovakia",
        "native": "Slovensko",
        "year": 1993,
        "phone": [421],
        "tld": [".sk"],
        "alias": [""],
        "languages": ["sk"],
        "currencies": [
            "EUR",
        ],
    },
    "SL": {
        "code": "SL",
        "name": "Sierra Leone",
        "native": "Sierra Leone",
        "year": 1974,
        "phone": [232],
        "tld": [".sl"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "SLL",
        ],
    },
    "SM": {
        "code": "SM",
        "name": "San Marino",
        "native": "San Marino",
        "year": 1974,
        "phone": [378],
        "tld": [".sm"],
        "alias": [""],
        "languages": ["it"],
        "currencies": [
            "EUR",
        ],
    },
    "SN": {
        "code": "SN",
        "name": "Senegal",
        "native": "Sénégal",
        "year": 1974,
        "phone": [221],
        "tld": [".sn"],
        "alias": [""],
        "languages": ["fr"],
        "currencies": [
            "XOF",
        ],
    },
    "SO": {
        "code": "SO",
        "name": "Somalia",
        "native": "Soomaaliya",
        "year": 1974,
        "phone": [252],
        "tld": [".so"],
        "alias": [""],
        "languages": ["so", "ar"],
        "currencies": [
            "SOS",
        ],
    },
    "SR": {
        "code": "SR",
        "name": "Suriname",
        "native": "Suriname",
        "year": 1974,
        "phone": [597],
        "tld": [".sr"],
        "alias": [""],
        "languages": ["nl"],
        "currencies": [
            "SRD",
        ],
    },
    "SS": {
        "code": "SS",
        "name": "South Sudan",
        "native": "South Sudan",
        "year": 2011,
        "phone": [211],
        "tld": [".ss"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "SSP",
        ],
    },
    "ST": {
        "code": "ST",
        "name": "Sao Tome and Principe",
        "native": "São Tomé e Príncipe",
        "year": 1974,
        "phone": [239],
        "tld": [".st"],
        "alias": [""],
        "languages": ["pt"],
        "currencies": [
            "STD",
        ],
    },
    "SV": {
        "code": "SV",
        "name": "El Salvador",
        "native": "El Salvador",
        "year": 1974,
        "phone": [503],
        "tld": [".sv"],
        "alias": [""],
        "languages": ["es"],
        "currencies": [
            "USD",
        ],
    },
    "SX": {
        "code": "SX",
        "name": "Sint Maarten [Dutch part]",
        "native": "Sint Maarten",
        "year": 2010,
        "phone": [1721],
        "tld": [".sx"],
        "alias": [""],
        "languages": ["nl", "en"],
        "currencies": [
            "ANG",
        ],
    },
    "SY": {
        "code": "SY",
        "name": "Syrian Arab Republic",
        "native": "سوريا",
        "year": 1974,
        "phone": [963],
        "tld": [".sy"],
        "alias": [""],
        "languages": ["ar"],
        "currencies": [
            "SYP",
        ],
    },
    "SZ": {
        "code": "SZ",
        "name": "Eswatini",
        "native": "Swaziland",
        "year": 1974,
        "phone": [268],
        "tld": [".sz"],
        "alias": [""],
        "languages": ["en", "ss"],
        "currencies": [
            "SZL",
        ],
    },
    "TC": {
        "code": "TC",
        "name": "Turks and Caicos Islands",
        "native": "Turks and Caicos Islands",
        "year": 1974,
        "phone": [1649],
        "tld": [".tc"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "USD",
        ],
    },
    "TD": {
        "code": "TD",
        "name": "Chad",
        "native": "Tchad",
        "year": 1974,
        "phone": [235],
        "tld": [".td"],
        "alias": [""],
        "languages": ["fr", "ar"],
        "currencies": [
            "XAF",
        ],
    },
    "TF": {
        "code": "TF",
        "name": "French Southern Territories",
        "native": "Territoire des Terres australes et antarctiques fr",
        "year": 1979,
        "phone": [262],
        "tld": [".tf"],
        "alias": [""],
        "languages": ["fr"],
        "currencies": [
            "EUR",
        ],
    },
    "TG": {
        "code": "TG",
        "name": "Togo",
        "native": "Togo",
        "year": 1974,
        "phone": [228],
        "tld": [".tg"],
        "alias": [""],
        "languages": ["fr"],
        "currencies": [
            "XOF",
        ],
    },
    "TH": {
        "code": "TH",
        "name": "Thailand",
        "native": "ประเทศไทย",
        "year": 1974,
        "phone": [66],
        "tld": [".th"],
        "alias": [""],
        "languages": ["th"],
        "currencies": [
            "THB",
        ],
    },
    "TJ": {
        "code": "TJ",
        "name": "Tajikistan",
        "native": "Тоҷикистон",
        "year": 1992,
        "phone": [992],
        "tld": [".tj"],
        "alias": [""],
        "languages": ["tg", "ru"],
        "currencies": [
            "TJS",
        ],
    },
    "TK": {
        "code": "TK",
        "name": "Tokelau",
        "native": "Tokelau",
        "year": 1974,
        "phone": [690],
        "tld": [".tk"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "NZD",
        ],
    },
    "TL": {
        "code": "TL",
        "name": "Timor-Leste",
        "native": "Timor-Leste",
        "year": 2002,
        "phone": [670],
        "tld": [".tl"],
        "alias": [""],
        "languages": ["pt"],
        "currencies": [
            "USD",
        ],
    },
    "TM": {
        "code": "TM",
        "name": "Turkmenistan",
        "native": "Türkmenistan",
        "year": 1992,
        "phone": [993],
        "tld": [".tm"],
        "alias": [""],
        "languages": ["tk", "ru"],
        "currencies": [
            "TMT",
        ],
    },
    "TN": {
        "code": "TN",
        "name": "Tunisia",
        "native": "تونس",
        "year": 1974,
        "phone": [216],
        "tld": [".tn"],
        "alias": [""],
        "languages": ["ar"],
        "currencies": [
            "TND",
        ],
    },
    "TO": {
        "code": "TO",
        "name": "Tonga",
        "native": "Tonga",
        "year": 1974,
        "phone": [676],
        "tld": [".to"],
        "alias": [""],
        "languages": ["en", "to"],
        "currencies": [
            "TOP",
        ],
    },
    "TR": {
        "code": "TR",
        "name": "Turkey",
        "native": "Türkiye",
        "year": 1974,
        "phone": [90],
        "tld": [".tr"],
        "alias": [""],
        "languages": ["tr"],
        "currencies": [
            "TRY",
        ],
    },
    "TT": {
        "code": "TT",
        "name": "Trinidad and Tobago",
        "native": "Trinidad and Tobago",
        "year": 1974,
        "phone": [1868],
        "tld": [".tt"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "TTD",
        ],
    },
    "TV": {
        "code": "TV",
        "name": "Tuvalu",
        "native": "Tuvalu",
        "year": 1977,
        "phone": [688],
        "tld": [".tv"],
        "alias": [""],
        "languages": ["en"],
        "currencies": ["TVD", "AUD"],
    },
    "TW": {
        "code": "TW",
        "name": "Taiwan, Province of China",
        "native": "臺灣",
        "year": 1974,
        "phone": [886],
        "tld": [".tw"],
        "alias": [""],
        "languages": ["zh"],
        "currencies": [
            "TWD",
        ],
    },
    "TZ": {
        "code": "TZ",
        "name": "Tanzania, United Republic of",
        "native": "Tanzania",
        "year": 1974,
        "phone": [255],
        "tld": [".tz"],
        "alias": [""],
        "languages": ["sw", "en"],
        "currencies": [
            "TZS",
        ],
    },
    "UA": {
        "code": "UA",
        "name": "Ukraine",
        "native": "Україна",
        "year": 1974,
        "phone": [380],
        "tld": [".ua"],
        "alias": [""],
        "languages": ["uk"],
        "currencies": [
            "UAH",
        ],
    },
    "UG": {
        "code": "UG",
        "name": "Uganda",
        "native": "Uganda",
        "year": 1974,
        "phone": [256],
        "tld": [".ug"],
        "alias": [""],
        "languages": ["en", "sw"],
        "currencies": [
            "UGX",
        ],
    },
    "UM": {
        "code": "UM",
        "name": "United States Minor Outlying Islands",
        "native": "United States Minor Outlying Islands",
        "year": 1986,
        "phone": [1],
        "tld": [""],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "USD",
        ],
    },
    "US": {
        "code": "US",
        "name": "United States of America",
        "native": "United States",
        "year": 1974,
        "phone": [1],
        "tld": [".us"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "USD",
        ],
    },
    "UY": {
        "code": "UY",
        "name": "Uruguay",
        "native": "Uruguay",
        "year": 1974,
        "phone": [598],
        "tld": [".uy"],
        "alias": [""],
        "languages": ["es"],
        "currencies": [
            "UYU",
        ],
    },
    "UZ": {
        "code": "UZ",
        "name": "Uzbekistan",
        "native": "O‘zbekiston",
        "year": 1992,
        "phone": [998],
        "tld": [".uz"],
        "alias": [""],
        "languages": ["uz", "ru"],
        "currencies": [
            "UZS",
        ],
    },
    "VA": {
        "code": "VA",
        "name": "Holy See",
        "native": "Vaticano",
        "year": 1974,
        "phone": [379],
        "tld": [".va"],
        "alias": [""],
        "languages": ["it", "la"],
        "currencies": [
            "EUR",
        ],
    },
    "VC": {
        "code": "VC",
        "name": "Saint Vincent and the Grenadines",
        "native": "Saint Vincent and the Grenadines",
        "year": 1974,
        "phone": [1784],
        "tld": [".vc"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "XCD",
        ],
    },
    "VE": {
        "code": "VE",
        "name": "Venezuela [Bolivarian Republic of]",
        "native": "Venezuela",
        "year": 1974,
        "phone": [58],
        "tld": [".ve"],
        "alias": [""],
        "languages": ["es"],
        "currencies": [
            "VEF",
        ],
    },
    "VG": {
        "code": "VG",
        "name": "Virgin Islands [British]",
        "native": "British Virgin Islands",
        "year": 1974,
        "phone": [1284],
        "tld": [".vg"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "USD",
        ],
    },
    "VI": {
        "code": "VI",
        "name": "Virgin Islands [U.S.]",
        "native": "United States Virgin Islands",
        "year": 1974,
        "phone": [1340],
        "tld": [".vi"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "USD",
        ],
    },
    "VN": {
        "code": "VN",
        "name": "Viet Nam",
        "native": "Việt Nam",
        "year": 1974,
        "phone": [84],
        "tld": [".vn"],
        "alias": [""],
        "languages": ["vi"],
        "currencies": [
            "VND",
        ],
    },
    "VU": {
        "code": "VU",
        "name": "Vanuatu",
        "native": "Vanuatu",
        "year": 1980,
        "phone": [678],
        "tld": [".vu"],
        "alias": [""],
        "languages": ["bi", "en", "fr"],
        "currencies": [
            "VUV",
        ],
    },
    "WF": {
        "code": "WF",
        "name": "Wallis and Futuna",
        "native": "Wallis et Futuna",
        "year": 1974,
        "phone": [681],
        "tld": [".wf"],
        "alias": [""],
        "languages": ["fr"],
        "currencies": [
            "XPF",
        ],
    },
    "WS": {
        "code": "WS",
        "name": "Samoa",
        "native": "Samoa",
        "year": 1974,
        "phone": [685],
        "tld": [".ws"],
        "alias": [""],
        "languages": ["sm", "en"],
        "currencies": [
            "WST",
        ],
    },
    "YE": {
        "code": "YE",
        "name": "Yemen",
        "native": "اليَمَن",
        "year": 1974,
        "phone": [967],
        "tld": [".ye"],
        "alias": [""],
        "languages": ["ar"],
        "currencies": [
            "YER",
        ],
    },
    "YT": {
        "code": "YT",
        "name": "Mayotte",
        "native": "Mayotte",
        "year": 1993,
        "phone": [262],
        "tld": [".yt"],
        "alias": [""],
        "languages": ["fr"],
        "currencies": [
            "EUR",
        ],
    },
    "ZA": {
        "code": "ZA",
        "name": "South Africa",
        "native": "South Africa",
        "year": 1974,
        "phone": [27],
        "tld": [".za"],
        "alias": [""],
        "languages": ["af", "en", "nr", "st", "ss", "tn", "ts", "ve", "xh", "zu"],
        "currencies": [
            "ZAR",
        ],
    },
    "ZM": {
        "code": "ZM",
        "name": "Zambia",
        "native": "Zambia",
        "year": 1974,
        "phone": [260],
        "tld": [".zm"],
        "alias": [""],
        "languages": ["en"],
        "currencies": [
            "ZMK",
        ],
    },
    "ZW": {
        "code": "ZW",
        "name": "Zimbabwe",
        "native": "Zimbabwe",
        "year": 1980,
        "phone": [263],
        "tld": [".zw"],
        "alias": [""],
        "languages": ["en", "sn", "nd"],
        "currencies": ["USD", "ZAR", "BWP", "GBP", "EUR"],
    },
}


class AsDictMixin(object):
    def as_dict(self):
        return asdict(self)


@dataclass
class Currency(AsDictMixin):
    """
    A Currency holds:
    * `code` 3-Letter ISO 4217 Code.
    * `name` the verbose name in standard-english.
    """

    code: str
    name: str
    symbol: str

    def __getitem__(self, key):
        if isinstance(self, Currency) or issubclass(self, Currency):
            return getattr(self, key)
        else:
            raise NotImplementedError


@dataclass
class Currencies(AsDictMixin):
    """
    A Currencies holds:
    * `worldwide` a list of Currencies
    """

    worldwide: List[Currency] = field(default_factory=list)

    def __post_init__(self) -> Literal[None]:
        self.worldwide.append(Currency(code="XX", name="Unknown", symbol="X"))
        for code, data in CURR_DICT.items():
            name, symbol = [
                data.get(_)
                for _ in [
                    "name",
                    "symbol",
                ]
            ]
            self.worldwide.append(Currency(code=code, name=name, symbol=symbol))

    def __getitem__(self, key):
        if isinstance(self, Currencies) or issubclass(self, Currencies):
            return getattr(self, key)
        else:
            raise NotImplementedError

    def __iter__(self, **kwargs: dict) -> Iterator[Currency]:
        for currency in self.worldwide:
            yield currency

    def __find(
        self,
        attr: str,
        value: str,
        *args: list,
        **kwargs: dict,
    ) -> List[Optional[Currency]]:
        def match(current: str, value: str) -> List[Optional[Currency]]:
            if isinstance(current, str):
                return lang if value.lower() == current.lower() else None
            elif isinstance(current, bool):
                return lang if value == current else None
            elif isinstance(current, list):
                return lang if value in current else None

        result = []
        for lang in self:
            if match(getattr(lang, attr), value):
                result.append(lang)

        return result

    def __unknown(self):
        return self.__find("code", "XX")[0]

    def find_by_code(self, **kwargs: dict) -> Currency:
        value = kwargs.get("value", "")
        result = self.__find("code", value)
        return result[0] if result else self.__unknown()

    def find_by_name(self, **kwargs: dict) -> Currency:
        value = kwargs.get("value", "")
        result = self.__find("name", value)
        return result[0] if result else self.__unknown()

    def find_by_symbol(self, **kwargs: dict) -> Currency:
        value = kwargs.get("value", "")
        result = self.__find("native", value)
        return result[0] if result else self.__unknown()

    def find(self, **kwargs: dict) -> List[Currency]:
        finders = [
            getattr(self, f"find_by_{name}") for name in ["code", "name", "symbol"]
        ]

        return list(filter(lambda c: c, [finder(**kwargs) for finder in finders]))


@dataclass
class Language(AsDictMixin):
    """
    A Language holds:
    * `code` 2-Letter ISO 3166-1 Alpha-2 Country Code.
    * `name` the verbose name in standard-english.
    * `native` the verbose name in the original language.
    * `rtl` Right to Left writing?
    """

    code: str
    name: str
    native: Optional[str]
    alias: List[str] = field(default_factory=list)
    rtl: bool = field(default=False)

    def __getitem__(self, key):
        if isinstance(self, Language) or issubclass(self, Language):
            return getattr(self, key)
        else:
            raise NotImplementedError


@dataclass
class Languages(AsDictMixin):
    """
    A Languages holds:
    * `worldwide` a list of Language representation
    """

    worldwide: List[Language] = field(default_factory=list)

    def __post_init__(self) -> Literal[None]:
        self.worldwide.append(
            Language(code="XX", name="Unknown", native="Unknown", rtl=False)
        )
        for code, data in LL_DICT.items():
            name, native, rtl = [
                data.get(_)
                for _ in [
                    "name",
                    "native",
                    "rtl",
                ]
            ]
            self.worldwide.append(
                Language(code=code, name=name, native=native, rtl=rtl)
            )

    def __getitem__(self, key):
        if isinstance(self, Languages) or issubclass(self, Languages):
            return getattr(self, key)
        else:
            raise NotImplementedError

    def __iter__(self, **kwargs: dict) -> Iterator[Language]:
        for language in self.worldwide:
            yield language

    def __find(
        self,
        attr: str,
        value: str,
        *args: list,
        **kwargs: dict,
    ) -> List[Optional[Language]]:
        def match(current: str, value: str) -> List[Optional[Language]]:
            if isinstance(current, str):
                return lang if value.lower() == current.lower() else None
            elif isinstance(current, bool):
                return lang if value == current else None
            elif isinstance(current, list):
                return lang if value in current else None

        result = []
        for lang in self:
            if match(getattr(lang, attr), value):
                result.append(lang)

        return result

    def __unknown(self):
        return self.__find("code", "XX")[0]

    def find_by_code(self, **kwargs: dict) -> Language:
        value = kwargs.get("value", "")
        result = self.__find("code", value)
        return result[0] if result else self.__unknown()

    def find_by_name(self, **kwargs: dict) -> Language:
        value = kwargs.get("value", "")
        result = self.__find("name", value)
        return result[0] if result else self.__unknown()

    def find_by_native(self, **kwargs: dict) -> Language:
        value = kwargs.get("value", "")
        result = self.__find("native", value)
        return result[0] if result else self.__unknown()

    def find_by_alias(self, **kwargs: dict) -> Language:
        value = kwargs.get("value", "")
        result = self.__find("alias", value)
        return result[0] if result else self.__unknown()

    def find_by_rtl(self, **kwargs: dict) -> List[Language]:
        value = kwargs.get("value", True)
        return self.__find("rtl", value)

    def find(self, **kwargs: dict) -> List[Language]:
        finders = [
            getattr(self, f"find_by_{name}")
            for name in ["code", "name", "native", "rtl"]
        ]

        return list(filter(lambda c: c, [finder(**kwargs) for finder in finders]))


@dataclass
class Country(AsDictMixin):
    """
    A Country holds:
    * `code` 2-Letter ISO 3166-1 Alpha-2 Country Code.
    * `name` The verbose name in standard-english.
    * `native` The verbose name in the original language.
    * `year` The year the alpha-2 code was officialized
    * `phone` A list of Phone code
    * `tld` Top Level Domain.
    * `alias` An alternative `code`.
    * `language` A list of ISO-639-1 Representations.
    """

    code: str
    name: str
    native: str
    year: int
    phone: List[int]
    tld: List[str]
    alias: List[str] = field(default_factory=list)
    languages: List[Language] = field(default_factory=list)
    currencies: List[str] = field(default_factory=list)

    def __getitem__(self, key):
        if isinstance(self, Country) or issubclass(self, Country):
            return getattr(self, key)
        else:
            raise NotImplementedError


@dataclass(frozen=True)
class World(AsDictMixin):
    """
    A World holds little info:
    * `countries` a list of Countries.
    """

    countries: Optional[List[Country]] = field(default_factory=list)

    def __post_init__(self, **kwargs: dict) -> Literal[None]:
        self.countries.append(
            Country(
                code="XX",
                name="Unknown",
                native="Unknown",
                year="0000",
                phone=[],
                tld=[],
                alias=[],
                languages=[],
            )
        )
        for code, data in CC_DICT.items():
            name, native, year, phone, tld, alias, languages = [
                data.get(_)
                for _ in [
                    "name",
                    "native",
                    "year",
                    "phone",
                    "tld",
                    "alias",
                    "languages",
                ]
            ]

            languages = [Language(**LL_DICT.get(_)) for _ in data.get("languages")]
            currencies = [Currency(**CURR_DICT.get(_)) for _ in data.get("currencies")]
            self.countries.append(
                Country(
                    code=code,
                    name=name,
                    native=native,
                    year=year,
                    phone=phone,
                    tld=tld,
                    alias=alias,
                    languages=languages,
                    currencies=currencies,
                )
            )

    def __iter__(self, **kwargs: dict) -> Iterator[Country]:
        for country in self.countries:
            yield country

    def __find(
        self,
        attr: str,
        value: str,
        strict: bool = False,
        multiple: bool = True,
        *args: list,
        **kwargs: dict,
    ) -> Optional[List[Country]]:
        def match(
            current: Union[str, list], value: str, strict: bool = False
        ) -> Optional[Country]:
            if isinstance(current, str):
                return (
                    country
                    if (not strict and value.lower() == current.lower())
                    or (strict and value == current)
                    else None
                )
            elif isinstance(current, list):
                return (
                    country
                    if (not strict and value.lower() in [_.lower() for _ in current])
                    or (strict and value in current)
                    else None
                )

        result = []
        for country in self:
            if match(getattr(country, attr), value, strict):
                result.append(country)
                if not multiple:
                    break

        return result

    def __unknown(self):
        return self.__find("code", "XX", True, False)[0]

    def find_by_code(self, **kwargs: dict) -> List[Country]:
        value = kwargs.get("value", None)
        strict = kwargs.get("strict", True)
        result = self.__find("code", value, False, False)
        return result[0] if result else self.__unknown()

    def find_by_name(self, **kwargs: dict) -> Country:
        value = kwargs.get("value", None)
        strict = kwargs.get("strict", True)
        result = self.__find("name", value, strict, False)
        return result[0] if result else self.__unknown()

    def find_by_tld(self, **kwargs: dict) -> Country:
        value = kwargs.get("value", None)
        strict = kwargs.get("strict", True)
        result = self.__find("tld", value, strict, False)
        return result[0] if result else self.__unknown()

    def find_by_alias(self, **kwargs: dict) -> Country:
        value = kwargs.get("value", None)
        strict = kwargs.get("strict", True)
        result = self.__find("alias", value, strict, False)
        return result[0] if result else self.__unknown()

    def find_by_language(self, **kwargs: dict) -> List[Country]:
        value = kwargs.get("value", None)
        strict = kwargs.get("strict", True)
        multiple = kwargs.get("multiple", True)
        result = self.__find("languages", value, strict, multiple)
        if kwargs.get("exact", False):
            result = [_ for _ in result if _.languages == [value]]
        return result

    def find(self, **kwargs: dict) -> Optional[List[Country]]:
        finders = [
            getattr(self, f"find_by_{name}")
            for name in ["code", "name", "tld", "alias", "language"]
        ]

        return list(filter(lambda c: c, [finder(**kwargs) for finder in finders]))
