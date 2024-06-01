
#languages is a list of dictionaries that contain information about the languages that are being used in the project
#The dictionaries contain the following
#name: the name of the language
#language_code: the ISO code for the language
#name_column: the name of the column in the csv file that contains the name of the character
#char_column: the name of the column in the csv file that contains the character
#braille_column: the name of the column in the csv file that contains the braille code for the character
#replace: a list of strings that are to be removed from the name of the character
#language_information: a string that contains information about the language for Lib Louis
#contributors: a string that contains information about the people who have contributed to the project
languages=[
    {"name":"Akkadian","language_code":"akk","language_system_code":"akk-oracc","name_column":"Name","char_column":"Character","braille_column":"Braille","replace":["CUNEIFORM SIGN"],"included_braille_tables":["spaces.uti","litdigits6Dots.uti","latinLetterDef6Dots.uti","en-ueb-chardefs.uti"],"language_information":"""
#Cuneiform, generally known as Akkadian, is a writing system that was used through several stages of development, from the 31st century BC down to the second century AD, and preserves documents in several languages which span from Sumerian to Greek.  
#There is no braille standard set for these languages or this writing system. Thus, this table is innovative, but does provide access to all of the Cuneiform signs that are currently represented by Unicode.  This table provides support for the American  system and is different than the German (Borger) system. If you are desireing access to the German system, please see the Sumero- Akkadian table on Lib Louis for the full list of Borger names and corresponding braille.
#For more information on the different systems, please see:     
#https://en.wikipedia.org/wiki/Cuneiform_(Unicode_block)
#for more information on the Akkadian language, please go to:
#https://oracc.museum.upenn.edu/dcclt/signlists/signlists/
""","contributors":"""
#This braille code was developed by a group of both blind and sighted scholars in an academic setting. Special thank you to Louis Saenz,Inbal Baum, Shai Gordon for helping Matthew Yeater develop the braille code , and thank you to Ray McAllester, Sarah LaRose and Eric Harvey for their helpful contributions.  
#-maintainer: Paul Geoghegan <contact@envisionly.tech>
#-maintainer: Matityhau Yeshurun <yeatersink@gmail.com>
"""},
{"name":"Amharic","language_code":"amh","language_system_code":"amh","name_column":"Name","char_column":"Char","braille_column":"Braille","replace":["CUNEIFORM SIGN"],"language_information":"""
#for more information on braille in the Amharic language, please read this paper.
#https://www.researchgate.net/publication/303773888_RECOGNITION_OF_AMHARIC_BRAILLE
#The standard for Amharic has been set by the community mentioned above. 
""","contributors":"""
#This braille code was developed by a group of both blind and sighted scholars in an academic setting.
#-maintainer: Paul Geoghegan <contact@envisionly.tech>
#-maintainer: Matityhau Yeshurun <yeatersink@gmail.com>
"""},
        {"name":"Critical-Apparatus-NT","language_code":"Critical-Apparatus-NT","language_system_code":"critical-apparatus","name_column":"Name","char_column":"Char","braille_column":"Braille","replace":["CUNEIFORM SIGN"],"language_information":"""
#for more information on the Critical Apparatus , please check out this link:
#https://biblequestions.info/2020/10/24/what-do-the-sigla-in-a-new-testament-apparatus-mean-ubs-edition/
#The standard for the Critical Apparatus has been set by the community mentioned above. 
""","contributors":"""
#This braille code was developed by a group of both blind and sighted scholars in an academic setting.
#-maintainer: Paul Geoghegan <contact@envisionly.tech>
#-maintainer: Matityhau Yeshurun <yeatersink@gmail.com>
"""},
        {"name":"Transliterated-Cuneiform","language_code":"Transliterated-Cuneiform","supported_braille_languages":["akk-Latn","xhu-Latn","uga-Latn","peo-Latn","sux-Latn","xeb-Latn","elx-Latn","hit-Latn","xur-Latn","xlu-Latn"],"language_system_code":"Transliterated-Cuneiform-oracc","name_column":"Name","char_column":"Character","braille_column":"Braille","replace":[],"included_braille_tables":["spaces.uti","litdigits6Dots.uti","latinLetterDef6Dots.uti","en-ueb-chardefs.uti"],"language_information":"""
#Documents written in a writing system known as Cuneiform or Akkadian, are commonly preserved in clay, stone,  or even metal tablets.   When these tables are engaged academically, they are “transliterated” from their original Cuneiform, into Latin letters. Some of these letters have accents, dots, and lines associated with them. These are used to indicate specific sounds that are commonly made in Ancient Near Eastern  languages. This table provides braille support for the above mentioned languages that have been already transliterated into the latin characters mentioned above.
#This table is intended to provide support for the languages represented in the Cuneiform / Akkadian Writing system. This includes Sumerian, Hittite, Babylonian  Assyrian, Ugaritic and many others. Thus, the braille in this table reflects braille patterns commonly utilized in   other Semitic  languages such as Hebrew, Aramaic, and Syriac. For more information please see: 
#http://oracc.ub.uni-muenchen.de/doc/help/languages/ugaritic/index.html
""","contributors":"""
#This braille code was developed by a group of both blind and sighted scholars in an academic setting. Special thank you to Inbal Baum for helping Matthew Yeaterand Ray McAllester develop this braille code. Special thank you to Sarah LaRose and Eric Harvey for their helpful suggestions.  
#-maintainer: Paul Geoghegan <contact@envisionly.tech>
#-maintainer: Matityhau Yeshurun <yeatersink@gmail.com>
"""},
        {"name":"Greek","language_code":"grc-koine","name_column":"Name","char_column":"Character","braille_column":"Braille","replace":["CUNEIFORM SIGN"],"language_information":"""
#for more information on the Koine Greek language, please go to:
#https://www.koinegreek.com/
#The standard for Koine Greek has been set by the academic community . The braille code for Koine Greek follows the standard set.
""","contributors":"""
#This braille code was developed by a group of both blind and sighted scholars in an academic setting.
#-maintainer: Paul Geoghegan <contact@envisionly.tech>
#-maintainer: Matityhau Yeshurun <yeatersink@gmail.com>
"""},
        {"name":"Hebrew","language_code":"hbo","language_system_code":"hbo","name_column":"Name","char_column":"Character","braille_column":"Braille","replace":["point","punctuation","mark","letter","accent","*"],"included_braille_tables":["spaces.uti","litdigits6Dots.uti","latinLetterDef6Dots.uti","en-ueb-chardefs.uti"],"language_information":"""
#The first Hebrew Braille table hosted on Lib Louis was developed by the Library for the Blind and the Ministry of Education in Israel. That  table is based on the IHBC which was developed in the mid-1930’s. Please see World Braille usage 3rd edition, p. 74. 
#However, Classical or Biblical Hebrew, which is used in the Hebrew Bible and other liturgical literature, contains cantillation marks that are not supported by the Hebrew table mentioned above. This table seeks to provide access to these accents. This table is   also based upon the tables mentioned above.  This table only departs from it where the accents are concerned. With this table, the user will have access to the accents and Masorah in BHS and BHS Quinta. For more information about the IHBC and How it was developed:
#https://en.wikipedia.org/wiki/Hebrew_Braille#:~:text=The%20International%20Hebrew%20Braille%20Code
#also see: 
#https://huc.edu/library_blog/learning-about-hebrew-braille/#:~:text=The%20Code%20created%20by%20Brevis,books%20written%20in%20Hebrew%20Braille.
""","contributors":"""
#Special thank you to Ray McAllestor and Matthew Yeater for developing the braille for the cantillation. Also to Abby Howell for the suggestions to include support for Yiddish. Extra gratitude to Sarah LaRose, Eric Harvey, and Leonard de Ruijder for the helpful suggestions. 
#-maintainer: Paul Geoghegan <contact@envisionly.tech>
#-maintainer: Matityhau Yeshurun <yeatersink@gmail.com>
"""},
{"name":"Syriac","language_code":"syc","language_system_code":"syc","name_column":"Name","char_column":"Character","braille_column":"Braille","replace":[],"included_braille_tables":["spaces.uti","litdigits6Dots.uti","latinLetterDef6Dots.uti","en-ueb-chardefs.uti"],"language_information":"""
#This table provides support for ʾEsṭrangēlā, Maḏnḥāyā and Serṭā Syriac also known as  Old, Eastern and Western Syriac. 
#For more information, please see: 
#https://en.wikipedia.org/wiki/Syriac_language
""","contributors":"""
#This braille code was developed by a group of both blind and sighted scholars in an academic setting. Special thank you to Paul Keim, Ray McAllestor, and Matthew Yeater for development of the braille code for this language.  Also thanks to Sarah LaRose for the suggestions while serving on the committee. 
#-maintainer: Paul Geoghegan <contact@envisionly.tech>
#-maintainer: Matityhau Yeshurun <yeatersink@gmail.com>
"""},
{"name":"Sumero-Akkadian","language_code":"akk-sumero","language_system_code":"akk-sumero-oracc","name_column":"Name","char_column":"Character","braille_column":"Braille","replace":["CUNEIFORM SIGN"],"included_braille_tables":["spaces.uti","litdigits6Dots.uti","latinLetterDef6Dots.uti","en-ueb-chardefs.uti"],"language_information":"""
#This is a braille table for Sumero Akkadian. The braille in this table reflects the names for the Cuneiform signs represented in the German/ Borgers system. This is different than the American system. If you are looking for the braille that represents the American system, please find the table here on Lib Louis that represents the American system. For more information on the differences between these systems, please see: 
#https://en.wikipedia.org/wiki/Cuneiform_(Unicode_block)
#for more information on the Akkadian language, please go to:
#https://oracc.museum.upenn.edu/dcclt/signlists/signlists/
""","contributors":"""
#This braille code was developed by a group of both blind and sighted scholars in an academic setting.Special thank you to Matthew Yeater, Louis Saenz and Shai Gordon for your help in making this work possible.
#-maintainer: Matityhau Yeshurun <yeatersink@gmail.com>
"""},    \
        {"name":"Ugaritic","language_code":"uga","language_system_code":"uga-oracc","test_display_type":"unicode-without-blank.dis","name_column":"Name","char_column":"Character(decimal)","braille_column":"Braille","replace":["UGARITIC LETTER","UGARITIC "],"included_braille_tables":["spaces.uti","litdigits6Dots.uti","latinLetterDef6Dots.uti","en-ueb-chardefs.uti"],"language_information":"""
#The braille code for Ugaritic is innovative, but closely follows the Cuneiform represented at ORACC. The braille code for Ugaritic is represented in braille as the name for the sign in Ugaritic. Thus, if the Ugaritic sign is a "Alepha," then the braille code for this sign would be a dot 1, similar to Hebrew.
#for more information on the Ugaritic language, please go to:
#https://oracc.museum.upenn.edu/aemw/ugarit/corpus
""","contributors":"""
#This braille code was developed by a group of both blind and sighted scholars in an academic setting. Special thank you to Ray McAllestor and Matthew Yeater for your help in developing this braille code.
#-maintainer: Paul Geoghegan <contact@envisionly.tech>
#-maintainer: Matityhau Yeshurun <yeatersink@gmail.com>
"""}
]
