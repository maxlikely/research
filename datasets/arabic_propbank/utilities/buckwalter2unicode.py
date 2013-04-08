#!/usr/bin/python

# buckwalter2unicode.py - A script to convert transliterated Arabic
#                         (using the Buckwalter system) to Unicode.
#
# Version 0.2 - 15th September 2004
# 
# Andrew Roberts (andyr [at] comp (dot) leeds [dot] ac (dot) uk)
#
# Project homepage: http://www.comp.leeds.ac.uk/andyr/software/
#
# Now, listen carefully...
#
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

# Declare a dictionary with Buckwalter's ASCII symbols as the keys, and
# their unicode equivalents as values.

buck2uni = {"'": u"\u0621", # hamza-on-the-line
            "|": u"\u0622", # madda
            ">": u"\u0623", # hamza-on-'alif
            "W": u"\u0624", # hamza-on-waaw    -- NONSTANDARD (standard is &)
            "<": u"\u0625", # hamza-under-'alif
            "}": u"\u0626", # hamza-on-yaa'
            "A": u"\u0627", # bare 'alif
            "b": u"\u0628", # baa'
            "p": u"\u0629", # taa' marbuuTa
            "t": u"\u062A", # taa'
            "v": u"\u062B", # thaa'
            "j": u"\u062C", # jiim
            "H": u"\u062D", # Haa'
            "x": u"\u062E", # khaa'
            "d": u"\u062F", # daal
            "*": u"\u0630", # dhaal
            "r": u"\u0631", # raa'
            "z": u"\u0632", # zaay
            "s": u"\u0633", # siin
            "$": u"\u0634", # shiin
            "S": u"\u0635", # Saad
            "D": u"\u0636", # Daad
            "T": u"\u0637", # Taa'
            "Z": u"\u0638", # Zaa' (DHaa')
            "E": u"\u0639", # cayn
            "g": u"\u063A", # ghayn
            "_": u"\u0640", # taTwiil
            "f": u"\u0641", # faa'
            "q": u"\u0642", # qaaf
            "k": u"\u0643", # kaaf
            "l": u"\u0644", # laam
            "m": u"\u0645", # miim
            "n": u"\u0646", # nuun
            "h": u"\u0647", # haa'
            "w": u"\u0648", # waaw
            "Y": u"\u0649", # 'alif maqSuura
            "y": u"\u064A", # yaa'
            "F": u"\u064B", # fatHatayn
            "N": u"\u064C", # Dammatayn
            "K": u"\u064D", # kasratayn
            "a": u"\u064E", # fatHa
            "u": u"\u064F", # Damma
            "i": u"\u0650", # kasra
            "~": u"\u0651", # shaddah
            "o": u"\u0652", # sukuun
            "`": u"\u0670", # dagger 'alif
            "{": u"\u0671", # waSla
}

# For a reverse transliteration (Unicode -> Buckwalter), a dictionary
# which is the reverse of the above buck2uni is essential.

uni2buck = {}

# Iterate through all the items in the buck2uni dict.
for (key, value) in buck2uni.iteritems():
    # The value from buck2uni becomes a key in uni2buck, and vice
    # versa for the keys.
    uni2buck[value] = key


# This function transliterates a given string. It checks the direction
# of the transliteration and then uses the appropriate dictionary. A
# transliterated string is returned.
def transliterateString(inString, toUnicode):

    out = ""
    
    # For normal ASCII -> Unicode transliteration..
    if toUnicode:

        inString = inString.replace("-", "")

        # Loop over each character in the string, inString.
        for char in inString:
            # Look up current char in the dictionary to get its
            # respective value. If there is no match, e.g., chars like
            # spaces, then just stick with the current char without any
            # conversion.
            out = out + buck2uni.get(char, char)
    
    # Same as above, just in the other direction.
    else:

        for char in inString:
            out = out + uni2buck.get(char, char)

    return out



