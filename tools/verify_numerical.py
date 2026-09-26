"""Recompute every numerical answer from the chart data and compare with the PDF key.

Each check is a small formula that reads the dataset JSON (the same data the site
shows). It returns either an option letter, or a number, which is matched to the
closest option. Run:  python tools/verify_numerical.py
"""
import json
import re
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "site" / "data"
TOLERANCE = 0.01  # a number must be within 1% of an option to count as that option


# ---------- helpers to read datasets ----------

def table(d, key, block=0):
    """Table block as {row label: {column: value}}."""
    b = d[key]["blocks"][block]
    return {r[0]: dict(zip(b["columns"][1:], r[1:])) for r in b["rows"]}


def series(d, key, block=0):
    """Chart block as {series name: {label: value}}."""
    b = d[key]["blocks"][block]
    return {s["name"]: dict(zip(b["labels"], s["values"])) for s in b["series"]}


def pct(part, whole):
    return part / whole * 100


class Approx(float):
    """For 'approximately' questions: match the nearest option, however far."""


# ---------- checks, one per question ----------

def n1_checks():
    def leads(d):
        s = series(d, "leads")
        return s["2003"], s["2004"]

    def curian(d):
        return series(d, "curian", 0), series(d, "curian", 1)

    def maint(d):
        return table(d, "maintenance")

    def plant_totals(d):
        t = maint(d)
        plants = next(iter(t.values())).keys()
        return {p: sum(t[row][p] for row in t) for p in plants}

    def hh(d):
        return table(d, "households")

    def ratio(r):
        return float(r.split(":")[0])

    def q08(d):
        t = maint(d)
        order = sorted(t, key=lambda row: -sum(t[row].values()))
        names = {"Administration": "Administration", "Misc": "Misc."}
        got = ", ".join(names.get(r, r) for r in order)
        opts = {"A": "Servicing, Administration, Misc., Rent, Insurance, Utilities",
                "B": "Servicing, Administration, Rent, Misc., Utilities, Insurance",
                "C": "Servicing, Administration, Rent, Misc., Insurance, Utilities",
                "D": "Servicing, Administration, Misc., Rent, Utilities, Insurance"}
        return next((k for k, v in opts.items() if v == got), "E")

    def q09(d):
        t = maint(d)
        hits = [p for p in t["Rent"] if abs(t["Administration"][p] / t["Rent"][p] - 12 / 5) < 0.01]
        return "E" if sorted(hits) == ["Bordeaux*", "Glasgow*"] else f"? {hits}"

    def q10(d):
        t = maint(d)
        total = plant_totals(d)["Glasgow*"]
        near7 = [row for row in t if abs(pct(t[row]["Glasgow*"], total) - 7) < 0.5]
        return "E" if sorted(near7) == ["Insurance", "Utilities"] else f"? {near7}"

    def q12(d):
        vals = list(plant_totals(d).values())
        return "E" if len(set(vals)) == len(vals) else "? duplicate totals"

    def q18(d):
        t = hh(d)
        towns = list(t["Total No. Vehicles"])
        best = max(towns, key=lambda c: t["Households with 2 or more vehicles"][c] / t["Total No. Vehicles"][c])
        return "ABCDE"[towns.index(best)]

    def households(d, town):
        t = hh(d)
        return t["Total No. Vehicles"][town] * ratio(t["Approximate Ratio (Households : Vehicles)"][town])

    tor = lambda d: table(d, "tornados")["Total"]
    co = lambda d: table(d, "companies")

    return {
        "N1-Q01": lambda d: 27200 / leads(d)[0]["Direct Mail"] * leads(d)[0]["Radio Advertising"],
        "N1-Q02": lambda d: 100000 / 1.25 / leads(d)[0]["eMarketing"] * leads(d)[0]["Newspaper Advertising"],
        "N1-Q03": lambda d: 80000 / 2 / leads(d)[1]["Direct Mail"] * leads(d)[1]["Telemarketing"],
        "N1-Q04": lambda d: 46000 / leads(d)[1]["Radio Advertising"] * leads(d)[1]["Newspaper Advertising"],
        "N1-Q05": lambda d: Approx(pct(curian(d)[0]["Total Bookings"]["2004"] + curian(d)[1]["Total Bookings"]["2004"],
                                sum(curian(d)[0]["Total Bookings"].values()) + sum(curian(d)[1]["Total Bookings"].values()))),
        "N1-Q06": lambda d: Approx(pct(curian(d)[0]["Web-based only"]["2002"],
                                curian(d)[0]["Web-based only"]["2002"] + curian(d)[1]["Web-based only"]["2002"])),
        # increase needed = (direct web 2004) x (3rd-party total/web ratio) - current 3rd-party total
        "N1-Q07": lambda d: curian(d)[1]["Web-based only"]["2004"]
                            * curian(d)[0]["Total Bookings"]["2004"] / curian(d)[0]["Web-based only"]["2004"]
                            - curian(d)[0]["Total Bookings"]["2004"],
        "N1-Q08": q08,
        "N1-Q09": q09,
        "N1-Q10": q10,
        "N1-Q11": lambda d: sum(maint(d)["Servicing"].values()) / 5 * 48,
        "N1-Q12": q12,
        "N1-Q13": lambda d: "B" if abs(tor(d)["2005"] / tor(d)["2008"] - 1.28) < 0.01 else "?",
        "N1-Q14": lambda d: pct(tor(d)["2006"] - tor(d)["2005"], tor(d)["2005"]),
        "N1-Q15": lambda d: pct(table(d, "tornados")["73-112"]["2007"], tor(d)["2007"]),
        "N1-Q16": lambda d: households(d, "Canning Turn"),
        "N1-Q17": lambda d: pct(hh(d)["Households with 2 or more vehicles"]["Kinsop"], households(d, "Kinsop")),
        "N1-Q18": q18,
        "N1-Q19": lambda d: pct(households(d, "Kinsop") - households(d, "Amber Hill"), households(d, "Amber Hill")),
        "N1-Q20": lambda d: 3500 * co(d)["Share Price (pence)"]["Hardlow plc"] / co(d)["Share Price (pence)"]["Aurore"],
    }


def n2_checks():
    ipg = lambda d: table(d, "ipg")["Net sales"]
    demo = lambda d: table(d, "demographics")

    def tinco(d, year):
        b = d["tinco"]["blocks"][0 if year == 2008 else 1]
        return {k: v / 100 * b["total"] for k, v in zip(b["labels"], b["series"][0]["values"])}, b["total"]

    car = lambda d: series(d, "vehicles")
    air = lambda d: series(d, "airTraffic")

    def air_total(d, when):
        return sum(s[when] for s in air(d).values())

    def greenco(d, year):
        """{sector: (revenue, profit, companies)} for 1994 or 2000."""
        b = d["greenco"]["blocks"][0 if year == 1994 else 1]
        rev, prof = b["series"][0]["values"], b["series"][1]["values"]
        out = {}
        for i, label in enumerate(b["labels"]):
            name, n = re.match(r"(\w+) \((\d+)\)", label).groups()
            out[name] = (rev[i], prof[i], int(n))
        return out

    def growth(a, b):
        return (b - a) / a * 100

    def q01(d):
        industry_1997 = ipg(d)["1995"] * 1.2 ** 2
        return ipg(d)["1997"] - industry_1997

    def q02(d):
        s = ipg(d)
        return (growth(s["1998"], s["1999"]) + growth(s["1999"], s["2000"])) / 2

    def q03(d):
        urban_share = float(demo(d)["Urban : Rural Pop. (%)"]["Argentina"].split(":")[0]) / 100
        urban_cars = 0.9 * demo(d)["Vehicles – Cars (m)"]["Argentina"]
        return pct(urban_cars, urban_share * demo(d)["Population (m)"]["Argentina"])

    def q07(d):
        # plain reading: 2008 exploration + 100,000, over the 8%-larger total
        spend, total = tinco(d, 2008)
        return pct(spend["Exploration"] + 100000, total * 1.08)

    def q11(d):
        # the question says 5,800,000 but the chart is in '000: use 58 ('000)
        ford = car(d)["Ford"]
        rate = ford["2008"] / ford["2007"]
        value, years = ford["2008"], 0
        while value < 58:
            value, years = value * rate, years + 1
        return float(years)

    def q12(d):
        europe = air(d)["Europe"]
        return growth(europe["5 years ago"] * 1000, europe["Today"] * 800)

    def q14(d):
        return air_total(d, "Today") * air_total(d, "Today") / air_total(d, "5 years ago")

    def q17(d):
        return ((greenco(d, 2000)["Water"][0] / greenco(d, 1994)["Water"][0]) ** (1 / 6) - 1) * 100

    def q19(d):
        t = table(d, "oecd")
        best = max(t, key=lambda c: t[c]["Aid in $US millions"] / t[c]["Population in millions"])
        names = {"UK": "United Kingdom"}
        return next(k for k, v in {"A": "United Kingdom", "B": "Canada", "C": "Norway",
                                   "D": "New Zealand", "E": "US"}.items() if v == names.get(best, best))

    aid = lambda d: {c: r["Aid in $US millions"] for c, r in table(d, "oecd").items()}

    return {
        "N2-Q01": q01,
        "N2-Q02": q02,
        "N2-Q03": q03,
        "N2-Q04": lambda d: tinco(d, 2007)[0]["Mining"] + tinco(d, 2007)[0]["Logistics"],
        "N2-Q05": lambda d: growth(tinco(d, 2007)[0]["Exploration"], tinco(d, 2008)[0]["Exploration"]),
        "N2-Q06": lambda d: -growth(tinco(d, 2007)[0]["Mining"], tinco(d, 2008)[0]["Mining"]),
        "N2-Q07": q07,
        "N2-Q08": lambda d: -growth(car(d)["Nissan"]["2004"], car(d)["Nissan"]["2008"]),
        "N2-Q09": lambda d: car(d)["Ford"]["2008"] * 1000 * 0.8,
        "N2-Q10": lambda d: round(sum(s["2006"] for s in car(d).values()) * 1000 / 0.23, -3),
        "N2-Q11": q11,
        "N2-Q12": q12,
        "N2-Q13": lambda d: growth(air_total(d, "5 years ago"), air_total(d, "Today")),
        "N2-Q14": q14,
        "N2-Q15": lambda d: (greenco(d, 2000)["Water"][1] / greenco(d, 2000)["Water"][2]
                             - greenco(d, 1994)["Water"][1] / greenco(d, 1994)["Water"][2]) * 1e6,
        "N2-Q16": lambda d: sum(r for r, _, _ in greenco(d, 1994).values()) * 1e6
                            / sum(n for _, _, n in greenco(d, 1994).values()),
        "N2-Q17": q17,
        "N2-Q18": lambda d: sum(aid(d).values()) / 6,
        "N2-Q19": q19,
        "N2-Q20": lambda d: round(aid(d)["UK"] / 79191 * 360),
    }


def n3_checks():
    mach = lambda d: series(d, "machinery")
    time = lambda d: table(d, "timeUsage")
    darwin = lambda d: table(d, "darwin")
    copiers = lambda d: table(d, "photocopiers")

    def pie(d, key, block=0):
        b = d[key]["blocks"][block]
        return dict(zip(b["labels"], b["series"][0]["values"]))

    staff = lambda d: {k: v / 100 * 2900 for k, v in pie(d, "staff").items()}

    def q01(d):
        s = series(d, "drugs")
        regions = [r for r in s if s[r]["Parnol"] > s[r]["Tequental"]]
        opts = {"A": "Rest of World", "B": "Rest of Asia", "C": "Korea", "D": "Japan", "E": "Hong Kong"}
        return next(k for k, v in opts.items() if [v] == regions)

    def q04(d):
        # The split of $2,000,000 between departments isn't given -> Cannot say.
        # (With equal spend it would be +60,000, which isn't an option either.)
        each = 2_000_000 / 5
        assert sum(v / 100 * each for v in mach(d)["Hire Purchase"].values()) * 0.2 == 60_000
        return "E"

    def q05(d):
        t = time(d)
        per_head = lambda row, n: (t[row]["Support / Admin"] + t[row]["New Products"]
                                   + t[row]["Product Extensions"]) / n
        return per_head("Marketing (3)", 3) - per_head("Specifications (3)", 3)

    def half_year(d, name):
        r = copiers(d)[name]
        return r["Actual Spend Jan-Mar ($)"] + r["Actual Spend Apr-Jun ($)"]

    def q14(d):
        left = {n: 52 * r["Expected average cost per week ($)"] - half_year(d, n)
                for n, r in copiers(d).items()}
        best = min(left, key=left.get)
        return "ABCDEF"[list(left).index(best)]

    def q15(d):
        expected = copiers(d)["PHTCPR05"]["Expected average cost per week ($)"] * 26
        return pct(half_year(d, "PHTCPR05") - expected, expected)

    def q18(d):
        qualified_now = 2900 - staff(d)["No quals."]
        courses = -(-(0.9 * 2900 - qualified_now) // 29)  # round up
        return courses * 1170

    def q19(d):
        s = staff(d)
        return s["No quals."] / 2 + s["Level 2"] / 4 + s["Level 3"] / 3

    ads = lambda d, m: sum(s[m] for s in series(d, "advertising").values())
    hk = lambda d: series(d, "exports")["Hong Kong"]

    return {
        "N3-Q01": q01,
        "N3-Q02": lambda d: mach(d)["Lease Purchase"]["Production"] / 100 * 575000,
        "N3-Q03": lambda d: "C" if round(800000 / (90000 / (mach(d)["Lease Purchase"]["Printing"] / 100))) == 4 else "?",
        "N3-Q04": q04,
        "N3-Q05": q05,
        "N3-Q06": lambda d: darwin(d)["Share Price (pence)"]["Year1"] / darwin(d)["Income (£m)"]["Year1"]
                            * darwin(d)["Income (£m)"]["Year3"],
        "N3-Q07": lambda d: darwin(d)["Turnover (£m)"]["Year3"] ** 2 / darwin(d)["Turnover (£m)"]["Year2"],
        "N3-Q08": lambda d: "E",  # rate is % of workforce; workforce size is not given
        "N3-Q09": lambda d: hk(d)["Y+2"] * 1.2 ** 2,
        "N3-Q10": lambda d: "E",  # pie charts have no money amounts
        "N3-Q11": lambda d: 814995 / (pie(d, "xda", 0)["Wages & Salaries"] / 100) * 1.1
                            * pie(d, "xda", 1)["Wages & Salaries"] / 100,
        "N3-Q12": lambda d: "E",  # half-year totals unknown
        "N3-Q13": lambda d: ads(d, "Apr") - ads(d, "Mar"),
        "N3-Q14": q14,
        "N3-Q15": q15,
        "N3-Q16": lambda d: (half_year(d, "PHTCPR01") - half_year(d, "PHTCPR02")) * 2,
        "N3-Q17": lambda d: staff(d)["No quals."],
        "N3-Q18": q18,
        "N3-Q19": q19,
        "N3-Q20": lambda d: pct(staff(d)["No quals."] + 500, 3900),
    }


def pie_values(d, key, block=0):
    b = d[key]["blocks"][block]
    return dict(zip(b["labels"], b["series"][0]["values"]))


def pick(options, wanted):
    """Letter of the option whose text equals `wanted` (else '?')."""
    return next((k for k, v in options.items() if v == wanted), f"? {wanted}")


def n4_checks():
    gdp = lambda d: series(d, "gdp")
    area = lambda d: series(d, "areaSales")
    fund = lambda d: {k: v / 100 * 160 for k, v in pie_values(d, "fund").items()}
    rooms = lambda d: {r: (v["Seating for"], v["Cost for room per day (€)"]) for r, v in table(d, "rooms").items()}
    mail = lambda d: series(d, "mailshots")
    fax = lambda d: table(d, "fax")

    def q01(d):
        uk, fr = gdp(d)["UK"], gdp(d)["France"]
        years = [y for y in uk if abs(fr[y] - uk[y]) / uk[y] * 100 > 3.3]
        opts = {"A": {"2005", "2007"}, "B": {"2006", "2008"}, "C": {"2007", "2008"},
                "D": {"2008", "2005"}, "E": {"2009", "2005"}}
        return next(k for k, v in opts.items() if v == set(years))

    def q02(d):
        per = {c: r["GDP Per person (£1000s)"] for c, r in table(d, "gdp", 1).items()}
        pairs = {"A": ("UK", "Italy"), "B": ("France", "Italy"), "C": ("Germany", "Italy"),
                 "D": ("Spain", "Italy"), "E": ("Spain", "France")}
        return min(pairs, key=lambda k: abs(per[pairs[k][0]] - per[pairs[k][1]]))

    def q03(d):
        uk, fr = gdp(d)["UK"], gdp(d)["France"]
        ys = list(uk)
        both_up = [f"{a}-{b}" for a, b in zip(ys, ys[1:]) if uk[b] > uk[a] and fr[b] > fr[a]]
        return pick({"A": "2008-2009", "B": "2007-2008", "C": "2006-2007", "D": "2005-2006"}, both_up[0]) \
            if len(both_up) == 1 else "E"

    def q04(d):
        fr = sum(gdp(d)["France"].values()) / 5
        uk = sum(gdp(d)["UK"].values()) / 5
        return pick({"A": "£23,500 and £23,200", "B": "£23,650 and £23,500", "C": "£23,500 and £23,000",
                     "D": "£23,000 and £23,500", "E": "£23,650 and £23,200"}, f"£{fr:,.0f} and £{uk:,.0f}")

    def q11(d):
        r = rooms(d)
        pairs = {"A": ("Haydn", "Lennon"), "B": ("Brahms", "Haydn"), "C": ("Brahms", "Lennon"),
                 "D": ("Dylan", "Haydn"), "E": ("Brahms", "Dylan")}
        ok = {k: r[a + " Room"][1] + r[b + " Room"][1] for k, (a, b) in pairs.items()
              if r[a + " Room"][0] + r[b + " Room"][0] >= 72}
        return min(ok, key=ok.get)

    def q12(d):
        r = rooms(d)
        dylan = 5 * r["Dylan Room"][1] + 43 * 5 * 28
        lennon = 5 * r["Lennon Room"][1] + 49 * 5 * 28
        return lennon - dylan

    def q13(d):
        per_day = (8100 - 4 * rooms(d)["Verdi Room"][1]) / 4
        return per_day // (28 * 0.75)

    def q14(d):
        from itertools import combinations
        r = rooms(d)
        price = lambda name: r[name][1] * (0.95 if name == "Lennon Room" else 1)
        best = min(sum(price(n) for n in trio) for trio in combinations(r, 3)
                   if sum(r[n][0] for n in trio) >= 107)
        return best * 3 + 107 * 10 * 2 + 107 * 28

    def q15(d):
        m = mail(d)
        ratio = {age: m["Sales"][age] / m["Enquiries"][age] for age in m["Sales"]}
        low = min(ratio, key=ratio.get)
        return "ABCDEF"[list(ratio).index(low)]

    def q19(d):
        f = fax(d)
        saving = lambda name: f[name]["Pre-Discount Price per Unit (€)"] - f[name]["Discount Price per Unit (€)"]
        return 45 * saving("Tele-Fax") + 24 * saving("Zoom-Fax") + 12 * saving("Info-Fax")

    def q20(d):
        t = table(d, "survey")
        units = list(t["Excellent"])
        share = {u: t["Excellent"][u] / sum(t[row][u] for row in t) for u in units}
        return "ABCD"[units.index(max(share, key=share.get))]

    return {
        "N4-Q01": q01,
        "N4-Q02": q02,
        "N4-Q03": q03,
        "N4-Q04": q04,
        "N4-Q05": lambda d: area(d)["North"]["Food"] / 100 * 2_400_000,
        "N4-Q06": lambda d: 390000 * area(d)["South"]["Magazine"] / area(d)["North"]["Magazine"],
        "N4-Q07": lambda d: "E",  # percentages only; group totals unknown
        "N4-Q08": lambda d: fund(d)["Japan"],
        "N4-Q09": lambda d: 2 * (fund(d)["US"] + fund(d)["Japan"]) - 160,
        "N4-Q10": lambda d: fund(d)["S.E. Asia"] * 0.9,
        "N4-Q11": q11,
        "N4-Q12": q12,
        "N4-Q13": q13,
        "N4-Q14": q14,
        "N4-Q15": q15,
        "N4-Q16": lambda d: (mail(d)["Enquiries"]["25-34 yo"] - mail(d)["Sales"]["25-34 yo"]) * 40,
        "N4-Q17": lambda d: 630 / mail(d)["Sales"]["45-54 yo"] * 10000,
        "N4-Q18": lambda d: mail(d)["Sales"]["65 & over yo"] * 190 - mail(d)["Sales"]["16-24 yo"] * 110,
        "N4-Q19": q19,
        "N4-Q20": q20,
    }


def n5_checks():
    claims = lambda d: series(d, "claims")
    houses = lambda d: series(d, "houses")
    regions = lambda d: table(d, "regions")
    casino = lambda d: series(d, "casino")
    flights = lambda d: series(d, "flights")["Flights"]
    price = {"£200,000": 200_000, "£300,000": 300_000, "£400,000": 400_000, "£500,000": 500_000}

    def half_value(d, half):
        return sum(n * price[p] for p, n in houses(d)[half].items()) / 1e6

    def sold(d, band):
        return sum(h[band] for h in houses(d).values())

    def q02(d):
        usa, eu = claims(d)["USA"], claims(d)["EUROPE"]
        closest = min(usa, key=lambda s: abs(usa[s] - eu[s]) / (usa[s] + eu[s]))
        return "ABCDE"[list(usa).index(closest)]

    def q10(d):
        t = regions(d)
        cols = ["Previous year", "Current year", "Next yr's projection"]
        ok = [r for r in t if all(t[r][b] >= t[r][a] for a, b in zip(cols, cols[1:]))]
        return "ABCDE"[list(t).index(ok[0])] if len(ok) == 1 else f"? {ok}"

    def q12(d):
        cut = {"Northern": 0.75, "Western": 0.75, "Southern": 0.8, "Eastern": 0.8, "Central": 1}
        return sum(r["Next yr's projection"] * cut[name] for name, r in regions(d).items())

    def q13(d):
        from math import gcd
        t = regions(d)
        ratio = lambda col: "{}:{}".format(*(v // gcd(t["Central"][col], t["Eastern"][col])
                                             for v in (t["Central"][col], t["Eastern"][col])))
        return pick({"A": "9:30 ; 3:11", "B": "20:50 ; 3:11", "C": "10:30 ; 5:11", "D": "11:29 ; 3:10",
                     "E": "5:11 ; 11:29"}, f"{ratio('Previous year')} ; {ratio('Current year')}")

    def q14(d):
        t = regions(d)
        order = " ".join(sorted(t, key=lambda r: t[r]["Current year"] + t[r]["Next yr's projection"]))
        return pick({"A": "Central Southern Western Eastern Northern", "B": "Southern Central Western Eastern Northern",
                     "C": "Central Western Southern Eastern Northern", "D": "Central Southern Western Northern Eastern",
                     "E": "Central Southern Northern Western Eastern"}, order)

    def q15(d):
        c = casino(d)
        years = ["2006", "2007", "2008", "2009"]
        both = sum(c["Slot machines"][y] + c["Roulette"][y] for y in years)
        other = sum(c["Other table games"][y] for y in years)
        return (other - both) * 100_000 / 1e6

    def q16(d):
        attend = table(d, "casino", 1)["2007"]["Annual attendances (100,000s)"]
        return Approx(casino(d)["Slot machines"]["2007"] / attend)  # both in 100,000s

    return {
        "N5-Q01": lambda d: 1_250_000 / 100_000 * claims(d)["EUROPE"]["Manufacturing"],
        "N5-Q02": q02,
        "N5-Q03": lambda d: 6 * claims(d)["EUROPE"]["Transport & Distribution"]
                            / claims(d)["USA"]["Transport & Distribution"],
        "N5-Q04": lambda d: 630 / claims(d)["USA"]["Agriculture & Fishing"] * 100_000,
        "N5-Q05": lambda d: sold(d, "£400,000") / 0.8 / 5,
        "N5-Q06": lambda d: sum(sold(d, b) * price[b] for b in price if price[b] > 250_000) * 0.03,
        "N5-Q07": lambda d: half_value(d, "Jan to June 2009") + half_value(d, "July to Dec 2009"),
        "N5-Q08": lambda d: (half_value(d, "July to Dec 2009") - half_value(d, "Jan to June 2009")) * 1.2,
        "N5-Q09": lambda d: (half_value(d, "July to Dec 2009") - half_value(d, "Jan to June 2009")) / 3,
        "N5-Q10": q10,
        "N5-Q11": lambda d: max(r["Current year"] for r in regions(d).values())
                            - min(r["Current year"] for r in regions(d).values()),
        "N5-Q12": q12,
        "N5-Q13": q13,
        "N5-Q14": q14,
        "N5-Q15": q15,
        "N5-Q16": q16,
        "N5-Q17": lambda d: flights(d)["USA"] - flights(d)["Europe"],
        "N5-Q18": lambda d: "E",  # no prices given
        "N5-Q19": lambda d: pct(0.2 * flights(d)["Europe"], flights(d)["Malaysia"]),
        "N5-Q20": lambda d: pct(flights(d)["Hong Kong"] - 30, flights(d)["Hong Kong"]),
    }


CHECKS = {1: n1_checks, 2: n2_checks, 3: n3_checks, 4: n4_checks, 5: n5_checks}


# ---------- matching and report ----------

def option_number(text):
    """'£48,000' -> 48000.0, '1:1.28' -> None, 'Cannot say' -> None."""
    if ":" in text:
        return None
    m = re.search(r"-?[\d,]*\.?\d+", text.replace(" ", ""))
    return float(m.group().replace(",", "")) if m else None


def closest_option(value, options):
    scored = [(abs(n - value) / max(abs(value), 1e-9), k)
              for k, t in options.items() if (n := option_number(t)) is not None]
    err, letter = min(scored)
    if err <= TOLERANCE or isinstance(value, Approx):
        return letter
    # no number fits: that's the answer if there is a "None of these" option
    return next((k for k, t in options.items() if "none of these" in t.lower()), None)


def main():
    mismatches = 0
    for test_no, make_checks in CHECKS.items():
        test = json.loads((DATA / f"numerical-{test_no}.json").read_text(encoding="utf-8"))
        checks = make_checks()
        print(f"\n=== Numerical Test {test_no} ===")
        for q in test["questions"]:
            check = checks.get(q["id"])
            if check is None:
                print(f"{q['id']}  NO CHECK")
                continue
            result = check(test["datasets"])
            if isinstance(result, str):
                computed, shown = result, result
            else:
                computed = closest_option(result, q["options"]) or "none"
                shown = f"{result:,.2f} -> {computed}"
            # The site scores against verifiedAnswer when present; a dropped question
            # (verifiedAnswer null) is right when no option matches.
            source = q.get("answerSource", "pdf")
            used = q["verifiedAnswer"] if "verifiedAnswer" in q else q["answer"]
            ok = computed == (used or "none")
            disputed = bool(q.get("flag")) and q["flag"]["type"] == "disputed"
            status = "ok " if ok else ("DISPUTED" if disputed else "MISMATCH")
            mismatches += not ok and not disputed
            note = f"[{source}: PDF {q['answer']} -> {used}]" if source != "pdf" else ""
            if disputed:
                note += " [disputed]" if source != "pdf" else " [disputed: PDF key kept]"
            print(f"{q['id']}  key {q['answer']}  computed {shown:<22} {status} {note}")
    print(f"\n{mismatches} unresolved mismatch(es). Each needs a decision in the JSON and REVIEW.md.")


if __name__ == "__main__":
    main()
