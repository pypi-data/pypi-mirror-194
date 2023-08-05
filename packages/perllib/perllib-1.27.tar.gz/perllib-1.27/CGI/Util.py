#!/usr/bin/env python3
# Generated by "pythonizer -a Util.pm" v1.025 run by SNOOPYJC on Fri Feb 10 14:16:27 2023
__author__ = """Joe Cool"""
__email__ = "snoopyjc@gmail.com"
__version__ = "1.025"
import builtins, functools, perllib, re

_bn = lambda s: "" if s is None else s
_pb = lambda b: 1 if b else ""
_str = lambda s: "" if s is None else str(s)
perllib.init_package("CGI")
perllib.init_package("CGI.Util")


def __sortf(func, aa, bb):
    """Handle sort with user function - in perl the global $a and $b are compared"""
    global a, b
    a = aa
    b = bb
    return func([])


def ascii2ebcdic(*_args):
    _args = list(_args)
    data = _args.pop(0) if _args else None

    def _f311(_m_):
        global _m
        _m = _m_
        return chr(perllib.int_(CGI.Util.A2E_a[ord(_m.group(1))]))

    data = re.sub(re.compile(r"(.)"), _f311, _str(data), count=0)
    return data


CGI.Util.ascii2ebcdic = ascii2ebcdic


def ebcdic2ascii(*_args):
    _args = list(_args)
    data = _args.pop(0) if _args else None

    def _f305(_m_):
        global _m
        _m = _m_
        return chr(perllib.int_(CGI.Util.E2A_a[ord(_m.group(1))]))

    data = re.sub(re.compile(r"(.)"), _f305, _str(data), count=0)
    return data


CGI.Util.ebcdic2ascii = ebcdic2ascii

# This internal routine creates an expires time exactly some number of
# hours from the current time.  It incorporates modifications from
# Mark Fisher.


def expire_calc(*_args):
    [time] = perllib.list_of_n(_args, 1)
    mult = perllib.Hash(
        {
            "s": 1,
            "m": 60,
            "h": 60 * 60,
            "d": 60 * 60 * 24,
            "M": 60 * 60 * 24 * 30,
            "y": 60 * 60 * 24 * 365,
        }
    )
    # format for time can be in any of the forms...
    # "now" -- expire immediately
    # "+180s" -- in 180 seconds
    # "+2m" -- in 2 minutes
    # "+12h" -- in 12 hours
    # "+1d"  -- in 1 day
    # "+3M"  -- in 3 months
    # "+2y"  -- in 2 years
    # "-3m"  -- 3 minutes ago(!)
    # If you don't supply one of these forms, we assume you are
    # specifying the date yourself
    offset = None
    if not time or (_str(time).lower() == "now"):
        offset = 0
    elif re.search(r"^\d+", _str(time)):
        return time
    elif _m := re.search(r"^([+-]?(?:\d+|\d*\.\d*))([smhdMy])", _str(time)):
        offset = (perllib.num(mult.get(_m.group(2))) or 1) * perllib.num(_m.group(1))
    else:
        return time

    cur_time = perllib.time()
    return cur_time + perllib.num(offset)


CGI.Util.expire_calc = expire_calc

# This internal routine creates date strings suitable for use in
# cookies and HTTP headers.  (They differ, unfortunately.)
# Thanks to Mark Fisher for this.


def expires(*_args):
    [time, format_] = perllib.list_of_n(_args, 2)
    format_ = format_ or "http"

    MON = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
    WDAY = "Sun Mon Tue Wed Thu Fri Sat".split()

    # pass through preformatted dates for the sake of expire_calc()
    time = expire_calc(time)
    if not ((re.search(r"^\d+$", _str(time)))):
        return time

    # make HTTP/cookie date string from GMT'ed time
    # (cookies use '-' as date separator, HTTP uses ' ')

    [sc] = perllib.list_of_n(" ", 1)
    if _str(format_) == "cookie":
        sc = "-"

    [sec, min_, hour, mday, mon, year, wday] = perllib.list_of_n(
        perllib.gmtime(perllib.int_(time)), 7
    )
    year += 1900
    return perllib.format_(
        f"%s, %02d{_bn(sc)}%s{_bn(sc)}%04d %02d:%02d:%02d GMT",
        (WDAY[wday], mday, MON[mon], year, hour, min_, sec),
    )


CGI.Util.expires = expires

# URL-encode data
#
# We cannot use the %u escapes, they were rejected by W3C, so the official
# way is %XX-escaped utf-8 encoding.
# Naturally, Unicode strings have to be converted to their utf-8 byte
# representation.
# Byte strings were traditionally used directly as a sequence of octets.
# This worked if they actually represented binary data (i.e. in CGI::Compress).
# This also worked if these byte strings were actually utf-8 encoded; e.g.,
# when the source file used utf-8 without the appropriate "use utf8;".
# This fails if the byte string is actually a Latin 1 encoded string, but it
# was always so and cannot be fixed without breaking the binary data case.
# -- Stepan Kasal <skasal@redhat.com>
#


def escape(*_args):
    _args = list(_args)
    # If we being called in an OO-context, discard the first argument.
    if len(_args) > 1 and (
        perllib.ref_scalar(_args[0])
        or (
            (1 < len(_args) and _args[1] is not None)
            and _str(_args[0]) == _str(CGI.DefaultClass_v)
        )
    ):
        (_args.pop(0) if _args else None)

    toencode = _args.pop(0) if _args else None
    if toencode is None:
        return None

    if perllib.utf8_is_utf8(_str(toencode)):
        ((toencode := (_s := perllib.utf8_encode(_str(toencode)))[0]), _s[1])[1]

    if CGI.Util._EBCDIC_v:

        def _f236(_m_):
            global _m
            _m = _m_
            return perllib.format_("%%%02x", CGI.Util.E2A_a[ord(_m.group(1))]).upper()

        toencode = re.sub(re.compile(r"([^a-zA-Z0-9_.~-])"), _f236, _str(toencode), count=0)
    else:

        def _f238(_m_):
            global _m
            _m = _m_
            return perllib.format_("%%%02x", ord(_m.group(1))).upper()

        toencode = re.sub(re.compile(r"([^a-zA-Z0-9_.~-])"), _f238, _str(toencode), count=0)

    return toencode


CGI.Util.escape = escape


def utf8_chr(*_args):
    _args = list(_args)
    c = _args.pop(0) if _args else None
    u = chr(perllib.int_(c))
    ((u := (_s := perllib.utf8_encode(u))[0]), _s[1])[1]  # drop utf8 flag
    return u


CGI.Util.utf8_chr = utf8_chr

# unescape URL-encoded data


def unescape(*_args):
    _args = list(_args)
    if len(_args) > 0 and (
        perllib.ref_scalar(_args[0])
        or (
            (1 < len(_args) and _args[1] is not None)
            and _str(_args[0]) == _str(CGI.DefaultClass_v)
        )
    ):
        (_args.pop(0) if _args else None)

    todecode = _args.pop(0) if _args else None
    if todecode is None:
        return None

    todecode = _str(todecode).translate(str.maketrans("+", " "))  # pluses become spaces
    if CGI.Util._EBCDIC_v:

        def _f195(_m_):
            global _m
            _m = _m_
            return chr(perllib.int_(CGI.Util.A2E_a[int(_m.group(1), 16)]))

        todecode = re.sub(re.compile(r"%([0-9a-fA-F]{2})"), _f195, _str(todecode), count=0)
    else:
        # handle surrogate pairs first -- dankogai. Ref: http://unicode.org/faq/utf_bom.html#utf16-2
        def _f207(_m_):
            global _m
            _m = _m_

            return utf8_chr(
                0x10000
                + (int(_m.group(1), 16) - 0xD800) * 0x400
                + (int(_m.group(2), 16) - 0xDC00)
            )

        todecode = re.sub(
            re.compile(
                r"""
            %u([Dd][89a-bA-B][0-9a-fA-F]{2}) # hi
                %u([Dd][c-fC-F][0-9a-fA-F]{2})   # lo
              """,
                re.X,
            ),
            _f207,
            _str(todecode),
            count=0,
        )

        def _f209(_m_):
            global _m
            _m = _m_

            return (
                (chr(int(_m.group(1), 16)))
                if (_m is not None and 1 <= len(_m.groups()))
                else utf8_chr(int(_m.group(2), 16))
            )

        todecode = re.sub(
            re.compile(r"%(?:([0-9a-fA-F]{2})|u([0-9a-fA-F]{4}))"), _f209, _str(todecode), count=0
        )

    return todecode


CGI.Util.unescape = unescape


def simple_escape(*_args):
    _args = list(_args)
    if not ((toencode := (_args.pop(0) if _args else None)) is not None):
        return

    toencode = re.sub(re.compile(r"&", re.S), r"&amp;", _str(toencode), count=0)
    toencode = re.sub(re.compile(r"<", re.S), r"&lt;", _str(toencode), count=0)
    toencode = re.sub(re.compile(r">", re.S), r"&gt;", _str(toencode), count=0)
    toencode = re.sub(re.compile(r"\"", re.S), r"&quot;", _str(toencode), count=0)
    # Doesn't work.  Can't work.  forget it.
    #  $toencode =~ s{\x8b}{&#139;}gso;
    #  $toencode =~ s{\x9b}{&#155;}gso;
    return toencode


CGI.Util.simple_escape = simple_escape


def make_attributes(*_args, wantarray=False):
    _args = list(_args)
    global _d
    attr = _args.pop(0) if _args else None
    if not (attr and perllib.ref_scalar(attr) and perllib.refs(attr) == "HASH"):
        return perllib.Array() if wantarray else None

    escape_v = (_args.pop(0) if _args else None) or 0
    do_not_quote = _args.pop(0) if _args else None

    quote = "" if do_not_quote else '"'

    attr_keys = perllib.Array(sorted((attr if attr is not None else perllib.Hash()).keys()))
    att = perllib.Array()
    for _d in attr_keys:
        [key] = perllib.list_of_n(_d, 1)
        key = re.sub(r"^\-", r"", _str(key), count=1)  # get rid of initial - if present

        # old way: breaks EBCDIC!
        # $key=~tr/A-Z_/a-z-/; # parameters are lower case, use dashes

        key = f"{(_bn(key)).lower()}".translate(
            str.maketrans("_", "-")
        )  # parameters are lower case, use dashes

        value = simple_escape(attr.get(_str(_d))) if escape_v else attr.get(_str(_d))
        att.extend(
            perllib.make_list(
                f"{_bn(key)}={quote}{_bn(value)}{quote}"
                if attr.get(_str(_d)) is not None
                else f"{_bn(key)}"
            )
        )

    return sorted(att)


CGI.Util.make_attributes = make_attributes


def _rearrange_params(*_args):
    global _d, a, b
    [order, *param] = perllib.list_of_at_least_n(_args, 1)
    param = perllib.Array(param)
    if not param:
        return perllib.Array()

    if perllib.refs(param[0]) == "HASH":
        param = perllib.Array(param[0])
    else:
        if not (param.get(0) is not None and _str(param[0])[0:1] == "-"):
            return param

    # map parameters into positional indices

    i = 0
    pos = perllib.Hash()
    i = 0
    for _d in order:
        for _d in _d if perllib.refs(_d) == "ARRAY" else [_d]:
            pos[_str(_d).lower()] = i

        i += 1

    params_as_hash = perllib.Hash(
        {**{param[_i]: param[_i + 1] for _i in range(0, len(param), 2)}}
    )

    result_a = perllib.Array()
    leftover_h = perllib.Hash()
    perllib.set_last_ndx(result_a, (len(order) - 1))  # preextend

    # sort keys alphabetically but favour certain keys before others
    # specifically for the case where there could be several options
    # for a param key, but one should be preferred (see GH #155)
    def _f125(*_args):
        if re.search(re.compile(r"content", re.I), _str(a)):
            return 1
        elif re.search(re.compile(r"content", re.I), _str(b)):
            return -1
        else:
            return perllib.cmp(a, b)

    for k_l in sorted(
        list(params_as_hash.keys()), key=functools.cmp_to_key(lambda a, b: __sortf(_f125, a, b))
    ):
        key = _str(k_l).lower()
        key = re.sub(r"^\-", r"", key, count=1)
        if key in pos:
            result_a[perllib.int_(pos[key])] = params_as_hash.get(_str(k_l))
        else:
            leftover_h[key] = params_as_hash.get(_str(k_l))

    return result_a, leftover_h


CGI.Util._rearrange_params = _rearrange_params


def rearrange_header(*_args):
    [order, *param] = perllib.list_of_at_least_n(_args, 1)
    param = perllib.Array(param)

    [result, leftover] = perllib.list_of_n(_rearrange_params(order, *param), 2)
    if len((leftover if leftover is not None else perllib.Hash()).keys()):
        result.extend(perllib.make_list(make_attributes(leftover, 0, 1, wantarray=True)))

    return result


CGI.Util.rearrange_header = rearrange_header

# Smart rearrangement of parameters to allow named parameter
# calling.  We do the rearrangement if:
# the first parameter begins with a -


def rearrange(*_args):
    [order, *param] = perllib.list_of_at_least_n(_args, 1)
    param = perllib.Array(param)
    [result, leftover] = perllib.list_of_n(_rearrange_params(order, *param), 2)
    if len((leftover if leftover is not None else perllib.Hash()).keys()):
        result.extend(
            perllib.make_list(
                make_attributes(
                    leftover, CGI.Q_v.get("escape") if CGI.Q_v is not None else 1, wantarray=True
                )
            )
        )

    return result


CGI.Util.rearrange = rearrange

CGI.DefaultClass_v = perllib.init_global("CGI", "DefaultClass_v", None)
CGI.Q_v = perllib.init_global("CGI", "Q_v", perllib.Hash())
CGI.Util.A2E_a = perllib.init_global("CGI.Util", "A2E_a", perllib.Array())
CGI.Util.E2A_a = perllib.init_global("CGI.Util", "E2A_a", perllib.Array())
CGI.Util.ISA_a = perllib.init_global("CGI.Util", "ISA_a", perllib.Array())
CGI.Util._EBCDIC_v = perllib.init_global("CGI.Util", "_EBCDIC_v", None)
a = ""
b = ""

builtins.__PACKAGE__ = "CGI.Util"
# SKIPPED: use parent 'Exporter';
CGI.Util.ISA_a.append("Exporter")
# SKIPPED: require 5.008001;
# SKIPPED: use strict;
CGI.Util.EXPORT_OK_a = "rearrange rearrange_header make_attributes unescape escape expires ebcdic2ascii ascii2ebcdic".split()

CGI.Util.VERSION_v = "4.54"

CGI.Util._EBCDIC_v = _pb("\t" != "\011")

appease_cpants_kwalitee = """
use strict;
use warnings;
#"""

# (ord('^') == 95) for codepage 1047 as on os390, vmesa
CGI.Util.A2E_a = perllib.Array(
    [
        0,
        1,
        2,
        3,
        55,
        45,
        46,
        47,
        22,
        5,
        21,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        60,
        61,
        50,
        38,
        24,
        25,
        63,
        39,
        28,
        29,
        30,
        31,
        64,
        90,
        127,
        123,
        91,
        108,
        80,
        125,
        77,
        93,
        92,
        78,
        107,
        96,
        75,
        97,
        240,
        241,
        242,
        243,
        244,
        245,
        246,
        247,
        248,
        249,
        122,
        94,
        76,
        126,
        110,
        111,
        124,
        193,
        194,
        195,
        196,
        197,
        198,
        199,
        200,
        201,
        209,
        210,
        211,
        212,
        213,
        214,
        215,
        216,
        217,
        226,
        227,
        228,
        229,
        230,
        231,
        232,
        233,
        173,
        224,
        189,
        95,
        109,
        121,
        129,
        130,
        131,
        132,
        133,
        134,
        135,
        136,
        137,
        145,
        146,
        147,
        148,
        149,
        150,
        151,
        152,
        153,
        162,
        163,
        164,
        165,
        166,
        167,
        168,
        169,
        192,
        79,
        208,
        161,
        7,
        32,
        33,
        34,
        35,
        36,
        37,
        6,
        23,
        40,
        41,
        42,
        43,
        44,
        9,
        10,
        27,
        48,
        49,
        26,
        51,
        52,
        53,
        54,
        8,
        56,
        57,
        58,
        59,
        4,
        20,
        62,
        255,
        65,
        170,
        74,
        177,
        159,
        178,
        106,
        181,
        187,
        180,
        154,
        138,
        176,
        202,
        175,
        188,
        144,
        143,
        234,
        250,
        190,
        160,
        182,
        179,
        157,
        218,
        155,
        139,
        183,
        184,
        185,
        171,
        100,
        101,
        98,
        102,
        99,
        103,
        158,
        104,
        116,
        113,
        114,
        115,
        120,
        117,
        118,
        119,
        172,
        105,
        237,
        238,
        235,
        239,
        236,
        191,
        128,
        253,
        254,
        251,
        252,
        186,
        174,
        89,
        68,
        69,
        66,
        70,
        67,
        71,
        156,
        72,
        84,
        81,
        82,
        83,
        88,
        85,
        86,
        87,
        140,
        73,
        205,
        206,
        203,
        207,
        204,
        225,
        112,
        221,
        222,
        219,
        220,
        141,
        142,
        223,
    ]
)
CGI.Util.E2A_a = perllib.Array(
    [
        0,
        1,
        2,
        3,
        156,
        9,
        134,
        127,
        151,
        141,
        142,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        157,
        10,
        8,
        135,
        24,
        25,
        146,
        143,
        28,
        29,
        30,
        31,
        128,
        129,
        130,
        131,
        132,
        133,
        23,
        27,
        136,
        137,
        138,
        139,
        140,
        5,
        6,
        7,
        144,
        145,
        22,
        147,
        148,
        149,
        150,
        4,
        152,
        153,
        154,
        155,
        20,
        21,
        158,
        26,
        32,
        160,
        226,
        228,
        224,
        225,
        227,
        229,
        231,
        241,
        162,
        46,
        60,
        40,
        43,
        124,
        38,
        233,
        234,
        235,
        232,
        237,
        238,
        239,
        236,
        223,
        33,
        36,
        42,
        41,
        59,
        94,
        45,
        47,
        194,
        196,
        192,
        193,
        195,
        197,
        199,
        209,
        166,
        44,
        37,
        95,
        62,
        63,
        248,
        201,
        202,
        203,
        200,
        205,
        206,
        207,
        204,
        96,
        58,
        35,
        64,
        39,
        61,
        34,
        216,
        97,
        98,
        99,
        100,
        101,
        102,
        103,
        104,
        105,
        171,
        187,
        240,
        253,
        254,
        177,
        176,
        106,
        107,
        108,
        109,
        110,
        111,
        112,
        113,
        114,
        170,
        186,
        230,
        184,
        198,
        164,
        181,
        126,
        115,
        116,
        117,
        118,
        119,
        120,
        121,
        122,
        161,
        191,
        208,
        91,
        222,
        174,
        172,
        163,
        165,
        183,
        169,
        167,
        182,
        188,
        189,
        190,
        221,
        168,
        175,
        93,
        180,
        215,
        123,
        65,
        66,
        67,
        68,
        69,
        70,
        71,
        72,
        73,
        173,
        244,
        246,
        242,
        243,
        245,
        125,
        74,
        75,
        76,
        77,
        78,
        79,
        80,
        81,
        82,
        185,
        251,
        252,
        249,
        250,
        255,
        92,
        247,
        83,
        84,
        85,
        86,
        87,
        88,
        89,
        90,
        178,
        212,
        214,
        210,
        211,
        213,
        48,
        49,
        50,
        51,
        52,
        53,
        54,
        55,
        56,
        57,
        179,
        219,
        220,
        217,
        218,
        159,
    ]
)

if CGI.Util._EBCDIC_v and ord("^") == 106:  # as in the BS2000 posix-bc coded character set
    CGI.Util.A2E_a[91] = 187
    CGI.Util.A2E_a[92] = 188
    CGI.Util.A2E_a[94] = 106
    CGI.Util.A2E_a[96] = 74
    CGI.Util.A2E_a[123] = 251
    CGI.Util.A2E_a[125] = 253
    CGI.Util.A2E_a[126] = 255
    CGI.Util.A2E_a[159] = 95
    CGI.Util.A2E_a[162] = 176
    CGI.Util.A2E_a[166] = 208
    CGI.Util.A2E_a[168] = 121
    CGI.Util.A2E_a[172] = 186
    CGI.Util.A2E_a[175] = 161
    CGI.Util.A2E_a[217] = 224
    CGI.Util.A2E_a[219] = 221
    CGI.Util.A2E_a[221] = 173
    CGI.Util.A2E_a[249] = 192

    CGI.Util.E2A_a[74] = 96
    CGI.Util.E2A_a[95] = 159
    CGI.Util.E2A_a[106] = 94
    CGI.Util.E2A_a[121] = 168
    CGI.Util.E2A_a[161] = 175
    CGI.Util.E2A_a[173] = 221
    CGI.Util.E2A_a[176] = 162
    CGI.Util.E2A_a[186] = 172
    CGI.Util.E2A_a[187] = 91
    CGI.Util.E2A_a[188] = 92
    CGI.Util.E2A_a[192] = 249
    CGI.Util.E2A_a[208] = 166
    CGI.Util.E2A_a[221] = 219
    CGI.Util.E2A_a[224] = 217
    CGI.Util.E2A_a[251] = 123
    CGI.Util.E2A_a[253] = 125
    CGI.Util.E2A_a[255] = 126
elif CGI.Util._EBCDIC_v and ord("^") == 176:  # as in codepage 037 on os400
    CGI.Util.A2E_a[10] = 37
    CGI.Util.A2E_a[91] = 186
    CGI.Util.A2E_a[93] = 187
    CGI.Util.A2E_a[94] = 176
    CGI.Util.A2E_a[133] = 21
    CGI.Util.A2E_a[168] = 189
    CGI.Util.A2E_a[172] = 95
    CGI.Util.A2E_a[221] = 173

    CGI.Util.E2A_a[21] = 133
    CGI.Util.E2A_a[37] = 10
    CGI.Util.E2A_a[95] = 172
    CGI.Util.E2A_a[173] = 221
    CGI.Util.E2A_a[176] = 94
    CGI.Util.E2A_a[186] = 91
    CGI.Util.E2A_a[187] = 93
    CGI.Util.E2A_a[189] = 168
