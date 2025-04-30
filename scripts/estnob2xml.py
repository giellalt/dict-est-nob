#!/usr/bin/env python3

"""Parse est-nob custom dictionary format to giella-style xml dictionary."""

import argparse
import re
import sys
from dataclasses import dataclass, field
from collections import deque
import xml.etree.ElementTree as ET

ERRORMSG_ANALYSE_BUT_NO_HFST_PACKAGE = """
ERROR: --analyse given, but cannot load python library 'hfst', nor 'pyhfst'.
Install one of them to use --analyse.

Hint: Create a virtual environment, and install the packages
there

If you have the `uv` python runner, you can alternatively run
the script with the packages you want directly from the command
line, as follows:

uv run --with hfst estnob2xml.py --analyse est_nor_2005_utf8.txt

OR

uv run --with pyhfst estnob2xml.py --analyse est_nor_2005_utf8.txt

---

The difference between the two kinds of hfst python libraries:
- hfst: uses the native (c++) system libhfst library installed to run
        analysis, so it's very fast, but you must have hfst installed on
        the system
- pyhfst: uses a pure-python implementation of hfst to run analysis,
        so it is not required to have libhfst installed.
        it is a bit slower than hfst, but gets the job done too
"""


def get_fst_loader():
    try:
        import hfst
    except ImportError:
        try:
            import pyhfst
        except ImportError:
            return None
        else:
            def load_fst(lang, analyser_fst):
                apnightly_transducer_path = f"/usr/share/giella/{lang}/{analyser_fst}"
                input_stream = pyhfst.HfstInputStream(apnightly_transducer_path)
                try:
                    tr = input_stream.read()
                except Exception:
                    sys.exit(
                        "ERROR: --analyse given, but failed to load analysis "
                        f"file\n{apnightly_transducer_path}\nFile missing, "
                        "reading error, or file is not an fst."
                    )

                def lookup(string):
                    return [s[0] for s in tr.lookup(string)]
                return lookup
            return load_fst
    else:
        def load_fst(lang, analyser_fst):
            apnightly_transducer_path = f"/usr/share/giella/{lang}/{analyser_fst}"
            try:
                stream = hfst.HfstInputStream(apnightly_transducer_path)
            except Exception:
                sys.exit(
                    "ERROR: --analyse given, but failed to load analysis "
                    f"file\n{apnightly_transducer_path}\nFile missing, "
                    "reading error, or file is not an fst."
                )
            tr = stream.read()
            # libhfst has these things surrounded by @'s...
            pat = re.compile(r"@[^@]*@")

            def lookup(string):
                # every result from tr.lookup() is a 2-tuple (result, weight)
                return [re.sub(pat, "", s[0]) for s in tr.lookup(string)]
            return lookup
        return load_fst


POSES = {
    "1": "A|N",
    "1e": "A|N",

    "tp+1/16": "A|N",
    "tp+11/9": "A|N",
    "tp+12/10": "A|N",
    "tp+1/6": "A|N",
    "tp+2/22i": "A|N",
    "tp+2/8": "A|N",
    "tp+2e/2": "A|N",
    "tp+2e/22e": "A|N",
    "tp+3/5": "A|N",
    "tp+5/3": "A|N",
    "tp+5e/7e": "A|N",
    "tp+6/5": "A|N",
    "tp+16/1": "A|N",
    "tp+16/6": "A|N",
    "tp+17/16": "A|N",
    "tp+17/18": "A|N",
    "tp+18/17": "A|N",
    "tp+19/2e": "A|N",
    "tp+22*&3/5": "A|N",

    "2": "A|N",
    "2e": "A|N",
    "3": "A|N",
    "4": "A|N",
    "5": "A|N",
    "5e": "A|N",
    "6": "A|N",
    "7": "A|N",
    "7e": "A|N",
    "8": "A|N",
    "9": "A|N",
    "10": "A|N",
    "10^12": "A|N",
    "11": "A|N",
    "11^9": "A|N",
    "12": "A|N",
    "12^10": "A|N",
    "13": "A|N",
    "14": "A|N",
    "15": "A|N",
    "16": "A|N",
    "17": "A|N",
    "17e": "A|N",
    "17i": "A|N",
    "17u": "A|N",
    "18": "A|N",
    "18e": "A|N",
    "18u": "A|N",
    "19": "A|N",
    "20": "A|N",
    "21": "A|N",
    "22e": "A|N",
    "22i": "A|N",
    "22u": "A|N",
    "23e": "A|N",
    "23e^22e": "A|N",
    "23i": "A|N",
    "23i^22i": "A|N",
    "23u": "A|N",
    "23u^22u": "A|N",
    "24u": "A|N",
    "24e": "A|N",
    "24i": "A|N",
    "25": "A|N",
    "26": "A|N",
    "26i": "A|N",

    "27": "V",
    "tp+27/28": "V",
    "tp+27/28*": "V",
    "tp+28/27": "V",
    "tp+29/27": "V",
    "tp+31/27": "V",

    "28": "V",
    "29": "V",
    "30": "V",
    "31": "V",
    "32": "V",
    "33": "V",
    "34": "V",
    "35": "V",
    "36": "V",
    "37": "V",
    "37i": "V",
    "38": "V",
    "38i": "V",
}


def uniq(it):
    """Yield elements from the iterator `it`, but skip the ones where it's
    the same as the previous element."""
    prev = next(it)
    yield prev
    for line in it:
        if line != prev:
            yield line
            continue
        prev = line


def read_bulks(iostream):
    """Read bulks of entries from the iostream. A bulk is sequence of non-empty
    lines.
    """
    q = deque(uniq(s.strip() for s in iostream))
    while True:
        lines = []
        while True:
            try:
                line = q.popleft()
            except IndexError:
                if lines:
                    yield lines
                return
            line = line.strip()
            if not line:
                yield lines
                break
            lines.append(line)


@dataclass
class Translation:
    translation: str | None = None
    examples: list[(str, str)] = field(default_factory=list)

    def is_empty(self):
        return self.translation is None and len(self.examples) == 0

    def to_xml(self):
        mg = ET.Element("mg")
        tg = ET.SubElement(mg, "tg")
        if self.translation is not None:
            t = ET.SubElement(tg, "t")
            t.text = self.translation
        for x, xt in self.examples:
            xg = ET.SubElement(tg, "xg")
            x_el = ET.SubElement(xg, "x")
            x_el.text = x
            xt_el = ET.SubElement(xg, "xt")
            xt_el.text = xt
        return mg


@dataclass
class Entry:
    lemma: str | None = None
    pos: str | None = None
    translations: list[Translation] = field(default_factory=list)

    @classmethod
    def from_bulk(cls, bulk, analyse=False):
        obj = cls()
        ex = None
        translation = Translation()

        for line in bulk:
            typ, data = line.split("+", maxsplit=1)
            if typ == "me":
                obj.lemma = data.replace("+", "").replace("|", "").replace("\\", "")
            elif typ == "nn":
                if not translation.is_empty():
                    obj.translations.append(translation)
                    translation = Translation()
                translation.translation = data.replace("|", "")
            elif typ == "fe":
                ex = data
            elif typ == "fn":
                assert ex is not None, "fn must come after fe"
                translation.examples.append((ex, data))
            elif typ == "tp":
                obj.pos = POSES.get(data)

        if not translation.is_empty():
            obj.translations.append(translation)

        return obj

    def to_xml(self):
        if self.lemma is None:
            return None

        e = ET.Element("e")
        lg = ET.SubElement(e, "lg")
        lemma = ET.SubElement(lg, "l")
        lemma.text = self.lemma
        if self.pos is not None:
            lemma.attrib["pos"] = self.pos
        for trans in self.translations:
            e.append(trans.to_xml())

        return e

    def try_find_pos_by_analysis(self, est_lookup, nob_lookup):
        lookup_results = est_lookup(self.lemma)

        possible_poses = set()
        all_poses = set()
        for lookup_result in lookup_results:
            word_form, pos, *rest_tags = lookup_result.split("+")
            if word_form == self.lemma:
                possible_poses.add(pos)
            else:
                all_poses.add(pos)

        if len(possible_poses) == 1:
            self.pos = possible_poses.pop()
        elif len(all_poses) == 1:
            self.pos = all_poses.pop()
        else:
            # try nob..
            nob_lemma_match = set()
            nob_all = set()
            for t in self.translations:
                if t.translation is None:
                    continue

                for result in nob_lookup(t.translation):
                    word_form, pos, *rest_tags = result.split("+")
                    if word_form == t.translation:
                        nob_lemma_match.add(pos)
                    else:
                        nob_all.add(pos)

            if len(nob_lemma_match) == 1:
                # assume it is the pos
                self.pos = nob_lemma_match.pop()
            #elif len(nob_all) == 1:
            #    self.pos = nob_all.pop()


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "input",
        help="The input file, typically est_nor_2005_utf8.txt",
        type=argparse.FileType("r"),
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output file, by default '-' (standard output)",
        type=argparse.FileType("w+"),
        default="-",
    )
    parser.add_argument(
        "--analyse",
        help="Run analysis on lemmas to find missing poses.",
        action="store_true",
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    if args.analyse:
        load_fst = get_fst_loader()
        if load_fst is None:
            sys.exit(ERRORMSG_ANALYSE_BUT_NO_HFST_PACKAGE)
        est_fst_lookup = load_fst("est", "analyser-gt-desc.hfstol")
        nob_fst_lookup = load_fst("nob", "analyser-gt-desc.hfstol")

    r = ET.Element("r")
    for bulk in read_bulks(args.input):
        entry = Entry.from_bulk(bulk, analyse=args.analyse)
        if args.analyse:
            missing_pos = (entry.pos == "A|N" or entry.pos is None)
            if missing_pos and args.analyse:
                entry.try_find_pos_by_analysis(est_fst_lookup, nob_fst_lookup)
        e = entry.to_xml()
        if e is not None:
            r.append(e)

    ET.indent(r)
    string = ET.tostring(r, encoding="unicode", xml_declaration=True)
    print(string, file=args.output)


if __name__ == "__main__":
    raise SystemExit(main())
