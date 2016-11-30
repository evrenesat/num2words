# -*- coding: utf-8 -*-
# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA

from __future__ import division, unicode_literals, print_function
from . import lang_EU


class Num2Word_TR(lang_EU.Num2Word_EU):
    def set_high_numwords(self, high):
        max = 3 + 3 * len(high)
        for word, n in zip(high, range(max, 3, -3)):
            self.cards[10 ** n] = word + "ilyon"

    def setup(self):
        self.negword = "eksi "
        self.pointword = "virgül"
        self.errmsg_nornum = "Sadece sayılar kelimelere dönüştürülebilir."
        self.exclude_title = ["ve", "nokta", "eksi"]

        self.mid_numwords = [(1000, "bin"), (100, "yüz"),
                             (90, "doksan"), (80, "seksen"), (70, "yetmiş"),
                             (60, "altmış"), (50, "elli"), (40, "kırt"),
                             (30, "otuz")]
        self.low_numwords = ["yirmi", "ondokuz", "onsekiz", "onyedi",
                             "onaltı", "onbeş", "ondört", "onüç",
                             "oniki", "onbir", "on", "dokuz", "sekiz",
                             "yedi", "altı", "beş", "dört", "üç", "iki",
                             "bir", "sıfır"]
        self.ords = {"bir": "ilk",
                     "iki": "ikinci",
                     "üç": "üçüncü",
                     "beş": "beşinci",
                     "sekiz": "sekizinci",
                     "dokuz": "dokuzuncu",
                     "oniki": "onikinci"}

    def merge(self, lpair, rpair):
        ltext, lnum = lpair
        rtext, rnum = rpair
        if lnum == 1 and rnum < 100:
            return (rtext, rnum)
        elif 100 > lnum > rnum:
            return ("%s%s" % (ltext, rtext), lnum + rnum)
        elif lnum >= 100 > rnum:
            return ("%s %s" % (ltext, rtext), lnum + rnum)
        elif rnum > lnum:
            return ("%s %s" % (ltext, rtext), lnum * rnum)
        return ("%s, %s" % (ltext, rtext), lnum + rnum)

    def to_ordinal(self, value):
        self.verify_ordinal(value)
        outwords = self.to_cardinal(value).split(" ")
        lastwords = outwords[-1].split("-")
        lastword = lastwords[-1].lower()
        try:
            lastword = self.ords[lastword]
        except KeyError:
            if lastword[-1] == "y":
                lastword = lastword[:-1] + "ie"
            lastword += "th"
        lastwords[-1] = self.title(lastword)
        outwords[-1] = "-".join(lastwords)
        return " ".join(outwords)

    def to_ordinal_num(self, value):
        self.verify_ordinal(value)
        return "%s%s" % (value, self.to_ordinal(value)[-2:])

    def to_year(self, val, longval=True):
        if not (val // 100) % 10:
            return self.to_cardinal(val)
        return self.to_splitnum(val, hightxt="yüz", jointxt=" ",
                                longval=longval)

    def to_cardinal(self, *args, **kwargs):
        return self.fix_one_prefix(super(Num2Word_TR, self).to_cardinal(*args, **kwargs))

    def fix_one_prefix(self, word):
        if word.startswith('bir bin'):
            return word.replace('bir bin', 'bin')
        if word.startswith('bir yüz'):
            return word.replace('bir yüz', 'yüz')
        else:
            return word

    def to_splitnum(self, *args, **kwargs):
        return self.fix_one_prefix(super(Num2Word_TR, self).to_splitnum(*args, **kwargs))

    def to_currency(self, val, longval=True):
        return self.to_splitnum(val, hightxt="lira", lowtxt="kuruş",
                                jointxt="ve", longval=longval, cents=True)


n2w = Num2Word_TR()
to_card = n2w.to_cardinal
to_ord = n2w.to_ordinal
to_ordnum = n2w.to_ordinal_num
to_year = n2w.to_year


def main():
    for val in [1, 11, 12, 21, 31, 33, 71, 80, 81, 91, 99, 100, 101, 102, 155,
                180, 300, 308, 832, 1000, 1001, 1061, 1100, 1500, 1701, 3000,
                8280, 8291, 150000, 500000, 1000000, 2000000, 2000001,
                -21212121211221211111, -2.121212, -1.0000100]:
        n2w.test(val)
    n2w.test(
        1325325436067876801768700107601001012212132143210473207540327057320957032975032975093275093275093270957329057320975093272950730)
    for val in [1, 120, 1000, 1120, 1800, 1976, 2000, 2010, 2099, 2171, 1452323, 923123]:
        print(val, "is", n2w.to_currency(val))
        # print(val, "is", n2w.to_cardinal(val))


if __name__ == "__main__":
    main()
