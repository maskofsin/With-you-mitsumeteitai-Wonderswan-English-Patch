#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import json

MAPPING = json.loads(r"""{"Aa": "829F", "Ab": "82A0", "Ac": "82A1", "Ad": "82A2", "Ae": "82A3", "Af": "82A4", "Ag": "82A5", "Ah": "82A6", "Ai": "82A7", "Aj": "82A8", "Ak": "82A9", "Al": "82AA", "Am": "82AB", "An": "82AC", "Ao": "82AD", "Ap": "82AE", "Aq": "82AF", "Ar": "82B0", "As": "82B1", "At": "82B2", "Au": "82B3", "Av": "82B4", "Aw": "82B5", "Ax": "82B6", "Ay": "82B7", "Az": "82B8", "Ba": "82B9", "Bb": "82BA", "Bc": "82BB", "Bd": "82BC", "Be": "82BD", "Bf": "82BE", "Bg": "82BF", "Bh": "82C0", "Bi": "82C1", "Bj": "82C2", "Bk": "82C3", "Bl": "82C4", "Bm": "82C5", "Bn": "82C6", "Bo": "82C7", "Bp": "82C8", "Bq": "82C9", "Br": "82CA", "Bs": "82CB", "Bt": "82CC", "Bu": "82CD", "Bv": "82CE", "Bw": "82CF", "Bx": "82D0", "By": "82D1", "Bz": "82D2", "Ca": "82D3", "Cb": "82D4", "Cc": "82D5", "Cd": "82D6", "Ce": "82D7", "Cf": "82D8", "Cg": "82D9", "Ch": "82DA", "Ci": "82DB", "Cj": "82DC", "Ck": "82DD", "Cl": "82DE", "Cm": "82DF", "Cn": "82E0", "Co": "82E1", "Cp": "82E2", "Cq": "82E3", "Cr": "82E4", "Cs": "82E5", "Ct": "82E6", "Cu": "82E7", "Cv": "82E8", "Cw": "82E9", "Cx": "82EA", "Cy": "82EB", "Cz": "82EC", "Da": "82ED", "Db": "82EE", "Dc": "82EF", "Dd": "82F0", "De": "82F1", "Df": "8340", "Dg": "8341", "Dh": "8342", "Di": "8343", "Dj": "8344", "Dk": "8345", "Dl": "8346", "Dm": "8347", "Dn": "8348", "Do": "8349", "Dp": "834A", "Dq": "834B", "Dr": "834C", "Ds": "834D", "Dt": "834E", "Du": "834F", "Dv": "8350", "Dw": "8351", "Dx": "8352", "Dy": "8353", "Dz": "8354", "Ea": "8355", "Eb": "8356", "Ec": "8357", "Ed": "8358", "Ee": "8359", "Ef": "835A", "Eg": "835B", "Eh": "835C", "Ei": "835D", "Ej": "835E", "Ek": "835F", "El": "8360", "Em": "8361", "En": "8362", "Eo": "8363", "Ep": "8364", "Eq": "8365", "Er": "8366", "Es": "8367", "Et": "8368", "Eu": "8369", "Ev": "836A", "Ew": "836B", "Ex": "836C", "Ey": "836D", "Ez": "836E", "Fa": "836F", "Fb": "8370", "Fc": "8371", "Fd": "8372", "Fe": "8373", "Ff": "8374", "Fg": "8375", "Fh": "8376", "Fi": "8377", "Fj": "8378", "Fk": "8379", "Fl": "837A", "Fm": "837B", "Fn": "837C", "Fo": "837D", "Fp": "837E", "Fq": "8380", "Fr": "8381", "Fs": "8382", "Ft": "8383", "Fu": "8384", "Fv": "8385", "Fw": "8386", "Fx": "8387", "Fy": "8388", "Fz": "8389", "Ga": "838A", "Gb": "838B", "Gc": "838C", "Gd": "838D", "Ge": "838E", "Gf": "838F", "Gg": "8390", "Gh": "8391", "Gi": "8392", "Gj": "8393", "Gk": "8394", "Gl": "8395", "Gm": "8396", "Gn": "889F", "Go": "88A2", "Gp": "88A3", "Gq": "88A4", "Gr": "88A5", "Gs": "88A7", "Gt": "88A8", "Gu": "88A9", "Gv": "88AB", "Gw": "88AC", "Gx": "88AE", "Gy": "88B0", "Gz": "88B3", "Ha": "88B5", "Hb": "88B6", "Hc": "88BB", "Hd": "88BC", "He": "88C0", "Hf": "88C1", "Hg": "88C3", "Hh": "88C4", "Hi": "88C5", "Hj": "88C7", "Hk": "88C8", "Hl": "88C9", "Hm": "88CA", "Hn": "88CB", "Ho": "88CC", "Hp": "88CD", "Hq": "88CF", "Hr": "88D0", "Hs": "88D1", "Ht": "88D3", "Hu": "88D4", "Hv": "88D5", "Hw": "88D6", "Hx": "88D7", "Hy": "88D9", "Hz": "88DA", "Ia": "88DB", "Ib": "88DD", "Ic": "88DF", "Id": "88E1", "Ie": "88E2", "If": "88E3", "Ig": "88E4", "Ih": "88E5", "Ii": "88E6", "Ij": "88E7", "Ik": "88E8", "Il": "88E9", "Im": "88EA", "In": "88EB", "Io": "88EC", "Ip": "88ED", "Iq": "88EE", "Ir": "88F0", "Is": "88F3", "It": "88F5", "Iu": "88F6", "Iv": "88F8", "Iw": "88F9", "Ix": "8940", "Iy": "8941", "Iz": "8942", "Ja": "8943", "Jb": "8945", "Jc": "8946", "Jd": "8948", "Je": "894A", "Jf": "8951", "Jg": "8952", "Jh": "8953", "Ji": "8959", "Jj": "895A", "Jk": "895C", "Jl": "895D", "Jm": "895E", "Jn": "895F", "Jo": "8960", "Jp": "8963", "Jq": "8965", "Jr": "8966", "Js": "8968", "Jt": "8969", "Ju": "896A", "Jv": "8970", "Jw": "8971", "Jx": "8972", "Jy": "8973", "Jz": "8974", "Ka": "8976", "Kb": "8977", "Kc": "8978", "Kd": "897A", "Ke": "897C", "Kf": "897E", "Kg": "8980", "Kh": "8983", "Ki": "8984", "Kj": "8985", "Kk": "8987", "Kl": "8988", "Km": "8989", "Kn": "898A", "Ko": "898C", "Kp": "898D", "Kq": "898E", "Kr": "898F", "Ks": "8991", "Kt": "8993", "Ku": "8996", "Kv": "8998", "Kw": "899B", "Kx": "899C", "Ky": "899D", "Kz": "899E", "La": "899F", "Lb": "89A1", "Lc": "89A2", "Ld": "89A3", "Le": "89A4", "Lf": "89A5", "Lg": "89A9", "Lh": "89AA", "Li": "89AB", "Lj": "89AC", "Lk": "89AD", "Ll": "89AE", "Lm": "89AF", "Ln": "89B0", "Lo": "89B1", "Lp": "89B3", "Lq": "89B4", "Lr": "89B5", "Ls": "89B6", "Lt": "89B7", "Lu": "89B8", "Lv": "89B9", "Lw": "89BA", "Lx": "89BB", "Ly": "89BC", "Lz": "89BD", "Ma": "89BF", "Mb": "89C0", "Mc": "89C1", "Md": "89C2", "Me": "89C3", "Mf": "89C4", "Mg": "89C5", "Mh": "89C6", "Mi": "89C7", "Mj": "89C8", "Mk": "89C9", "Ml": "89CA", "Mm": "89CB", "Mn": "89CC", "Mo": "89CD", "Mp": "89CE", "Mq": "89D2", "Mr": "89D3", "Ms": "89D4", "Mt": "89D5", "Mu": "89D7", "Mv": "89D8", "Mw": "89D9", "Mx": "89DB", "My": "89DC", "Mz": "89DD", "Na": "89DE", "Nb": "89DF", "Nc": "89E0", "Nd": "89E3", "Ne": "89E4", "Nf": "89E5", "Ng": "89E6", "Nh": "89E8", "Ni": "89E9", "Nj": "89EA", "Nk": "89EB", "Nl": "89EC", "Nm": "89EE", "Nn": "89EF", "No": "89F0", "Np": "89F1", "Nq": "89F2", "Nr": "89F3", "Ns": "89F4", "Nt": "89F5", "Nu": "89F6", "Nv": "89F7", "Nw": "89F9", "Nx": "89FA", "Ny": "89FB", "Nz": "89FC", "Oa": "8A40", "Ob": "8A42", "Oc": "8A43", "Od": "8A44", "Oe": "8A45", "Of": "8A46", "Og": "8A47", "Oh": "8A48", "Oi": "8A4A", "Oj": "8A4B", "Ok": "8A4C", "Ol": "8A4D", "Om": "8A4F", "On": "8A51", "Oo": "8A52", "Op": "8A54", "Oq": "8A57", "Or": "8A58", "Os": "8A5A", "Ot": "8A5D", "Ou": "8A5F", "Ov": "8A60", "Ow": "8A65", "Ox": "8A67", "Oy": "8A69", "Oz": "8A6A", "Pa": "8A6B", "Pb": "8A6C", "Pc": "8A6D", "Pd": "8A6E", "Pe": "8A6F", "Pf": "8A70", "Pg": "8A73", "Ph": "8A74", "Pi": "8A75", "Pj": "8A76", "Pk": "8A77", "Pl": "8A78", "Pm": "8A79", "Pn": "8A7A", "Po": "8A7B", "Pp": "8A7C", "Pq": "8A7D", "Pr": "8A81", "Ps": "8A83", "Pt": "8A84", "Pu": "8A88", "Pv": "8A89", "Pw": "8A8A", "Px": "8A8B", "Py": "8A8C", "Pz": "8A8E", "Qu": "8A8F", "Ra": "8A90", "Rb": "8A92", "Rc": "8A93", "Rd": "8A94", "Re": "8A95", "Rf": "8A97", "Rg": "8A98", "Rh": "8A99", "Ri": "8A9B", "Rj": "8A9D", "Rk": "8AA0", "Rl": "8AA1", "Rm": "8AA2", "Rn": "8AA3", "Ro": "8AA5", "Rp": "8AA6", "Rq": "8AA7", "Rr": "8AA8", "Rs": "8AA9", "Rt": "8AAA", "Ru": "8AAB", "Rv": "8AAC", "Rw": "8AAE", "Rx": "8AAF", "Ry": "8AB1", "Rz": "8AB2", "Sa": "8AB3", "Sb": "8AB4", "Sc": "8AB5", "Sd": "8AB7", "Se": "8AB8", "Sf": "8AB9", "Sg": "8ABA", "Sh": "8ABD", "Si": "8ABE", "Sj": "8ABF", "Sk": "8AC2", "Sl": "8AC3", "Sm": "8AC4", "Sn": "8AC5", "So": "8AC7", "Sp": "8AC8", "Sq": "8AC9", "Sr": "8ACA", "Ss": "8ACC", "St": "8ACF", "Su": "8AD1", "Sv": "8AD2", "Sw": "8AD3", "Sx": "8AD4", "Sy": "8AD6", "Sz": "8AD7", "Ta": "8AD9", "Tb": "8ADB", "Tc": "8ADC", "Td": "8ADD", "Te": "8ADE", "Tf": "8AE1", "Tg": "8AE2", "Th": "8AE5", "Ti": "8AE6", "Tj": "8AE7", "Tk": "8AE8", "Tl": "8AE9", "Tm": "8AEA", "Tn": "8AEB", "To": "8AEC", "Tp": "8AED", "Tq": "8AEE", "Tr": "8AEF", "Ts": "8AF0", "Tt": "8AF1", "Tu": "8AF2", "Tv": "8AF3", "Tw": "8AF4", "Tx": "8AF5", "Ty": "8AF6", "Tz": "8AF7", "Ua": "8AF8", "Ub": "8AFA", "Uc": "8AFC", "Ud": "8B40", "Ue": "8B41", "Uf": "8B42", "Ug": "8B43", "Uh": "8B46", "Ui": "8B47", "Uj": "8B48", "Uk": "8B49", "Ul": "8B4B", "Um": "8B4C", "Un": "8B4D", "Uo": "8B4E", "Up": "8B4F", "Uq": "8B50", "Ur": "8B51", "Us": "8B53", "Ut": "8B54", "Uu": "8B55", "Uv": "8B56", "Uw": "8B59", "Ux": "8B5A", "Uy": "8B5D", "Uz": "8B5E", "Va": "8B60", "Vb": "8B63", "Vc": "8B65", "Vd": "8B67", "Ve": "8B69", "Vf": "8B6B", "Vg": "8B6C", "Vh": "8B70", "Vi": "8B71", "Vj": "8B72", "Vk": "8B73", "Vl": "8B74", "Vm": "8B75", "Vn": "8B76", "Vo": "8B78", "Vp": "8B79", "Vq": "8B7A", "Vr": "8B7B", "Vs": "8B7C", "Vt": "8B7D", "Vu": "8B7E", "Vv": "8B80", "Vw": "8B81", "Vx": "8B83", "Vy": "8B84", "Vz": "8B85", "Wa": "8B86", "Wb": "8B89", "Wc": "8B8B", "Wd": "8B8C", "We": "8B8D", "Wf": "8B8E", "Wg": "8B8F", "Wh": "8B90", "Wi": "8B91", "Wj": "8B92", "Wk": "8B93", "Wl": "8B95", "Wm": "8B96", "Wn": "8B97", "Wo": "8B99", "Wp": "8B9B", "Wq": "8B9E", "Wr": "8B9F", "Ws": "8BA3", "Wt": "8BA4", "Wu": "8BA6", "Wv": "8BA9", "Ww": "8BAA", "Wx": "8BAB", "Wy": "8BAD", "Wz": "8BAF", "Xa": "8BB0", "Xb": "8BB1", "Xc": "8BB2", "Xd": "8BB3", "Xe": "8BB4", "Xf": "8BB5", "Xg": "8BB6", "Xh": "8BB7", "Xi": "8BB8", "Xj": "8BB9", "Xk": "8BBA", "Xl": "8BBB", "Xm": "8BBD", "Xn": "8BBE", "Xo": "8BBF", "Xp": "8BC1", "Xq": "8BC2", "Xr": "8BC3", "Xs": "8BC5", "Xt": "8BC6", "Xu": "8BC7", "Xv": "8BC8", "Xw": "8BC9", "Xx": "8BCA", "Xy": "8BCB", "Xz": "8BCD", "Ya": "8BCE", "Yb": "8BCF", "Yc": "8BD0", "Yd": "8BD1", "Ye": "8BD2", "Yf": "8BD4", "Yg": "8BD5", "Yh": "8BD6", "Yi": "8BD8", "Yj": "8BD9", "Yk": "8BDA", "Yl": "8BDC", "Ym": "8BDF", "Yn": "8BE0", "Yo": "8BE1", "Yp": "8BE2", "Yq": "8BE3", "Yr": "8BE5", "Ys": "8BE6", "Yt": "8BE7", "Yu": "8BEA", "Yv": "8BEC", "Yw": "8BEE", "Yx": "8BEF", "Yy": "8BF3", "Yz": "8BF4", "Za": "8BF6", "Zb": "8BF7", "Zc": "8BF8", "Zd": "8BFC", "Ze": "8C40", "Zf": "8C43", "Zg": "8C45", "Zh": "8C46", "Zi": "8C47", "Zj": "8C49", "Zk": "8C4A", "Zl": "8C4B", "Zm": "8C4D", "Zn": "8C4E", "Zo": "8C4F", "Zp": "8C50", "Zq": "8C51", "Zr": "8C52", "Zs": "8C53", "Zt": "8C55", "Zu": "8C57", "Zv": "8C58", "Zw": "8C59", "Zx": "8C5A", "Zy": "8C5B", "Zz": "8C5C", "aa": "8C5E", "ab": "8C5F", "ac": "8C60", "ad": "8C61", "ae": "8C62", "af": "8C63", "ag": "8C65", "ah": "8C66", "ai": "8C67", "aj": "8C68", "ak": "8C69", "al": "8C6A", "am": "8C6E", "an": "8C6F", "ao": "8C70", "ap": "8C71", "aq": "8C75", "ar": "8C76", "as": "8C77", "at": "8C78", "au": "8C79", "av": "8C7C", "aw": "8C7D", "ax": "8C7E", "ay": "8C80", "az": "8C82", "ba": "8C83", "bb": "8C84", "bc": "8C87", "bd": "8C88", "be": "8C89", "bf": "8C8A", "bg": "8C8B", "bh": "8C8C", "bi": "8C8E", "bj": "8C8F", "bk": "8C90", "bl": "8C92", "bm": "8C93", "bn": "8C94", "bo": "8C95", "bp": "8C96", "bq": "8C97", "br": "8C98", "bs": "8C99", "bt": "8C9A", "bu": "8C9B", "bv": "8C9C", "bw": "8C9D", "bx": "8C9F", "by": "8CA0", "bz": "8CA2", "ca": "8CA3", "cb": "8CA4", "cc": "8CA6", "cd": "8CA7", "ce": "8CA8", "cf": "8CA9", "cg": "8CAA", "ch": "8CAB", "ci": "8CAC", "cj": "8CAD", "ck": "8CAE", "cl": "8CAF", "cm": "8CB1", "cn": "8CB2", "co": "8CB3", "cp": "8CB4", "cq": "8CB5", "cr": "8CB6", "cs": "8CB8", "ct": "8CB9", "cu": "8CBA", "cv": "8CBB", "cw": "8CBE", "cx": "8CC0", "cy": "8CC1", "cz": "8CC2", "da": "8CC3", "db": "8CC4", "dc": "8CC5", "dd": "8CC6", "de": "8CC7", "df": "8CC8", "dg": "8CC9", "dh": "8CCA", "di": "8CCB", "dj": "8CCC", "dk": "8CCD", "dl": "8CCE", "dm": "8CCF", "dn": "8CD1", "do": "8CD2", "dp": "8CD3", "dq": "8CD5", "dr": "8CD6", "ds": "8CD7", "dt": "8CD9", "du": "8CDA", "dv": "8CDB", "dw": "8CDC", "dx": "8CDD", "dy": "8CDF", "dz": "8CE0", "ea": "8CE1", "eb": "8CE3", "ec": "8CE4", "ed": "8CE5", "ee": "8CEA", "ef": "8CEB", "eg": "8CEC", "eh": "8CED", "ei": "8CEE", "ej": "8CEF", "ek": "8CF0", "el": "8CF3", "em": "8CF5", "en": "8CF6", "eo": "8CF7", "ep": "8CF8", "eq": "8CFA", "er": "8CFB", "es": "8CFC", "et": "8D41", "eu": "8D42", "ev": "8D44", "ew": "8D45", "ex": "8D46", "ey": "8D47", "ez": "8D48", "fa": "8D49", "fb": "8D4A", "fc": "8D4B", "fd": "8D4C", "fe": "8D4E", "ff": "8D4F", "fg": "8D50", "fh": "8D51", "fi": "8D52", "fj": "8D54", "fk": "8D55", "fl": "8D56", "fm": "8D57", "fn": "8D58", "fo": "8D59", "fp": "8D5A", "fq": "8D5C", "fr": "8D5D", "fs": "8D5E", "ft": "8D5F", "fu": "8D60", "fv": "8D61", "fw": "8D62", "fx": "8D63", "fy": "8D65", "fz": "8D67", "ga": "8D69", "gb": "8D6A", "gc": "8D6B", "gd": "8D6C", "ge": "8D6D", "gf": "8D71", "gg": "8D72", "gh": "8D73", "gi": "8D74", "gj": "8D75", "gk": "8D76", "gl": "8D77", "gm": "8D7A", "gn": "8D7C", "go": "8D7E", "gp": "8D80", "gq": "8D81", "gr": "8D82", "gs": "8D83", "gt": "8D84", "gu": "8D86", "gv": "8D87", "gw": "8D89", "gx": "8D8A", "gy": "8D8B", "gz": "8D8C", "ha": "8D8E", "hb": "8D8F", "hc": "8D90", "hd": "8D91", "he": "8D92", "hf": "8D93", "hg": "8D95", "hh": "8D96", "hi": "8D98", "hj": "8D9A", "hk": "8D9B", "hl": "8D9C", "hm": "8D9E", "hn": "8D9F", "ho": "8DA0", "hp": "8DA1", "hq": "8DA2", "hr": "8DA5", "hs": "8DA6", "ht": "8DA8", "hu": "8DA9", "hv": "8DAA", "hw": "8DAC", "hx": "8DAE", "hy": "8DB0", "hz": "8DB1", "ia": "8DB2", "ib": "8DB3", "ic": "8DB4", "id": "8DB5", "ie": "8DB6", "if": "8DB7", "ig": "8DB8", "ih": "8DB9", "ii": "8DBB", "ij": "8DBD", "ik": "8DBE", "il": "8DC0", "im": "8DC1", "in": "8DC2", "io": "8DC3", "ip": "8DC4", "iq": "8DC5", "ir": "8DC6", "is": "8DC7", "it": "8DC8", "iu": "8DC9", "iv": "8DCA", "iw": "8DCB", "ix": "8DCD", "iy": "8DCE", "iz": "8DCF", "ja": "8DD3", "jb": "8DD5", "jc": "8DD6", "jd": "8DD7", "je": "8DD8", "jf": "8DD9", "jg": "8DDA", "jh": "8DDB", "ji": "8DDD", "jj": "8DDE", "jk": "8DDF", "jl": "8DE0", "jm": "8DE1", "jn": "8DE2", "jo": "8DE3", "jp": "8DE4", "jq": "8DE5", "jr": "8DE7", "js": "8DE8", "jt": "8DEC", "ju": "8DED", "jv": "8DF0", "jw": "8DF2", "jx": "8DF4", "jy": "8DF5", "jz": "8DF6", "ka": "8DF7", "kb": "8DF8", "kc": "8DF9", "kd": "8DFB", "ke": "8DFC", "kf": "8E40", "kg": "8E41", "kh": "8E42", "ki": "8E43", "kj": "8E44", "kk": "8E45", "kl": "8E47", "km": "8E4C", "kn": "8E4D", "ko": "8E4E", "kp": "8E4F", "kq": "8E50", "kr": "8E51", "ks": "8E52", "kt": "8E53", "ku": "8E55", "kv": "8E58", "kw": "8E59", "kx": "8E5A", "ky": "8E5D", "kz": "8E5E", "la": "8E61", "lb": "8E63", "lc": "8E64", "ld": "8E66", "le": "8E67", "lf": "8E68", "lg": "8E69", "lh": "8E6A", "li": "8E6C", "lj": "8E6D", "lk": "8E6E", "ll": "8E6F", "lm": "8E70", "ln": "8E71", "lo": "8E73", "lp": "8E74", "lq": "8E75", "lr": "8E76", "ls": "8E77", "lt": "8E78", "lu": "8E7B", "lv": "8E7C", "lw": "8E7D", "lx": "8E7E", "ly": "8E80", "lz": "8E81", "ma": "8E84", "mb": "8E85", "mc": "8E86", "md": "8E87", "me": "8E88", "mf": "8E89", "mg": "8E8A", "mh": "8E8B", "mi": "8E8C", "mj": "8E8D", "mk": "8E8E", "ml": "8E8F", "mm": "8E91", "mn": "8E93", "mo": "8E94", "mp": "8E95", "mq": "8E96", "mr": "8E97", "ms": "8E98", "mt": "8E99", "mu": "8E9A", "mv": "8E9B", "mw": "8E9C", "mx": "8E9D", "my": "8E9E", "mz": "8E9F", "na": "8EA0", "nb": "8EA1", "nc": "8EA5", "nd": "8EA6", "ne": "8EA8", "nf": "8EA9", "ng": "8EAB", "nh": "8EAC", "ni": "8EAD", "nj": "8EAE", "nk": "8EAF", "nl": "8EB0", "nm": "8EB1", "nn": "8EB2", "no": "8EB4", "np": "8EB5", "nq": "8EB6", "nr": "8EB8", "ns": "8EB9", "nt": "8EBA", "nu": "8EBC", "nv": "8EBD", "nw": "8EBE", "nx": "8EBF", "ny": "8EC0", "nz": "8EC2", "oa": "8EC3", "ob": "8EC4", "oc": "8EC5", "od": "8EC9", "oe": "8ECA", "of": "8ECB", "og": "8ECC", "oh": "8ECD", "oi": "8ECE", "oj": "8ECF", "ok": "8ED0", "ol": "8ED1", "om": "8ED2", "on": "8ED3", "oo": "8ED4", "op": "8ED5", "oq": "8ED6", "or": "8ED7", "os": "8ED8", "ot": "8EDA", "ou": "8EDC", "ov": "8EDD", "ow": "8EDF", "ox": "8EE1", "oy": "8EE2", "oz": "8EE3", "pa": "8EE5", "pb": "8EE6", "pc": "8EE7", "pd": "8EE8", "pe": "8EE9", "pf": "8EEA", "pg": "8EEB", "ph": "8EED", "pi": "8EEE", "pj": "8EEF", "pk": "8EF0", "pl": "8EF1", "pm": "8EF2", "pn": "8EF3", "po": "8EF4", "pp": "8EF5", "pq": "8EF6", "pr": "8EF7", "ps": "8EFB", "pt": "8EFC", "pu": "8F40", "pv": "8F41", "pw": "8F42", "px": "8F43", "py": "8F45", "pz": "8F46", "qu": "8F47", "ra": "8F48", "rb": "8F49", "rc": "8F4B", "rd": "8F4C", "re": "8F4F", "rf": "8F50", "rg": "8F52", "rh": "8F54", "ri": "8F56", "rj": "8F57", "rk": "8F59", "rl": "8F5A", "rm": "8F5B", "rn": "8F5C", "ro": "8F5D", "rp": "8F5F", "rq": "8F60", "rr": "8F61", "rs": "8F62", "rt": "8F63", "ru": "8F64", "rv": "8F65", "rw": "8F66", "rx": "8F68", "ry": "8F69", "rz": "8F6A", "sa": "8F6B", "sb": "8F6D", "sc": "8F6E", "sd": "8F6F", "se": "8F70", "sf": "8F71", "sg": "8F72", "sh": "8F73", "si": "8F74", "sj": "8F75", "sk": "8F77", "sl": "8F78", "sm": "8F79", "sn": "8F7A", "so": "8F7B", "sp": "8F7E", "sq": "8F80", "sr": "8F81", "ss": "8F82", "st": "8F83", "su": "8F84", "sv": "8F87", "sw": "8F88", "sx": "8F89", "sy": "8F8A", "sz": "8F8B", "ta": "8F8C", "tb": "8F8D", "tc": "8F8E", "td": "8F8F", "te": "8F90", "tf": "8F91", "tg": "8F94", "th": "8F95", "ti": "8F96", "tj": "8F97", "tk": "8F98", "tl": "8F99", "tm": "8F9C", "tn": "8F9D", "to": "8F9E", "tp": "8F9F", "tq": "8FA0", "tr": "8FA1", "ts": "8FA2", "tt": "8FA4", "tu": "8FA5", "tv": "8FA7", "tw": "8FAB", "tx": "8FAC", "ty": "8FAD", "tz": "8FAE", "ua": "8FAF", "ub": "8FB0", "uc": "8FB2", "ud": "8FB3", "ue": "8FB4", "uf": "8FB5", "ug": "8FB6", "uh": "8FB8", "ui": "8FB9", "uj": "8FBA", "uk": "8FBB", "ul": "8FBC", "um": "8FC0", "un": "8FC1", "uo": "8FC2", "up": "8FC3", "uq": "8FC4", "ur": "8FC5", "us": "8FC6", "ut": "8FC7", "uu": "8FC8", "uv": "8FC9", "uw": "8FCB", "ux": "8FCC", "uy": "8FCD", "uz": "8FCE", "va": "8FCF", "vb": "8FD0", "vc": "8FD1", "vd": "8FD4", "ve": "8FD5", "vf": "8FD7", "vg": "8FD8", "vh": "8FD9", "vi": "8FDA", "vj": "8FDB", "vk": "8FDC", "vl": "8FE0", "vm": "8FE1", "vn": "8FE3", "vo": "8FE4", "vp": "8FE6", "vq": "8FE7", "vr": "8FE8", "vs": "8FE9", "vt": "8FEA", "vu": "8FEC", "vv": "8FED", "vw": "8FEE", "vx": "8FF0", "vy": "8FF1", "vz": "8FF2", "wa": "8FF3", "wb": "8FF4", "wc": "8FF6", "wd": "8FF7", "we": "8FF8", "wf": "8FF9", "wg": "8FFC", "wh": "9040", "wi": "9041", "wj": "9042", "wk": "9044", "wl": "9045", "wm": "9046", "wn": "9047", "wo": "9048", "wp": "904B", "wq": "904C", "wr": "904D", "ws": "904E", "wt": "904F", "wu": "9050", "wv": "9051", "ww": "9052", "wx": "9053", "wy": "9054", "wz": "9055", "xa": "9056", "xb": "9057", "xc": "9058", "xd": "905A", "xe": "905B", "xf": "905C", "xg": "905D", "xh": "905E", "xi": "905F", "xj": "9061", "xk": "9062", "xl": "9063", "xm": "9065", "xn": "9066", "xo": "9067", "xp": "9068", "xq": "9069", "xr": "906A", "xs": "906B", "xt": "906C", "xu": "906D", "xv": "906E", "xw": "906F", "xx": "9070", "xy": "9071", "xz": "9072", "ya": "9073", "yb": "9074", "yc": "9077", "yd": "907B", "ye": "907C", "yf": "907D", "yg": "9081", "yh": "9082", "yi": "9083", "yj": "9084", "yk": "9085", "yl": "9086", "ym": "9087", "yn": "9088", "yo": "908B", "yp": "908C", "yq": "908F", "yr": "9090", "ys": "9092", "yt": "9093", "yu": "9094", "yv": "9097", "yw": "9098", "yx": "9099", "yy": "909B", "yz": "909E", "za": "909F", "zb": "90A2", "zc": "90A3", "zd": "90A5", "ze": "90A6", "zf": "90A7", "zg": "90A8", "zh": "90AA", "zi": "90AB", "zj": "90AC", "zk": "90AD", "zl": "90AE", "zm": "90AF", "zn": "90B0", "zo": "90B1", "zp": "90B3", "zq": "90B4", "zr": "90B5", "zs": "90B6", "zt": "90B7", "zu": "90B8", "zv": "90B9", "zw": "90BA", "zx": "90BB", "zy": "90BC", "zz": "90BD", "a ": "90BE", "a,": "90BF", "a.": "90C2", "a!": "90C3", "a?": "90C4", "b ": "90C5", "b,": "90C7", "b.": "90C8", "b!": "90C9", "b?": "90CC", "c ": "90CE", "c,": "90CF", "c.": "90D1", "c!": "90D3", "c?": "90D4", "d ": "90D5", "d,": "90D8", "d.": "90D9", "d!": "90DA", "d?": "90DC", "e ": "90DD", "e,": "90DF", "e.": "90E0", "e!": "90E1", "e?": "90E2", "f ": "90E3", "f,": "90E5", "f.": "90E6", "f!": "90E7", "f?": "90E8", "g ": "90E9", "g,": "90EA", "g.": "90EC", "g!": "90ED", "g?": "90EE", "h ": "90EF", "h,": "90F2", "h.": "90F3", "h!": "90F4", "h?": "90F5", "i ": "90F6", "i,": "90F7", "i.": "90FC", "i!": "9140", "i?": "9141", "j ": "9142", "j,": "9144", "j.": "9145", "j!": "9146", "j?": "9148", "k ": "9149", "k,": "914B", "k.": "914D", "k!": "914E", "k?": "914F", "l ": "9150", "l,": "9151", "l.": "9152", "l!": "9153", "l?": "9154", "m ": "9155", "m,": "9156", "m.": "9158", "m!": "915D", "m?": "915F", "n ": "9161", "n,": "9163", "n.": "9165", "n!": "9166", "n?": "9167", "o ": "9168", "o,": "916A", "o.": "916D", "o!": "916E", "o?": "916F", "p ": "9171", "p,": "9173", "p.": "9174", "p!": "9176", "p?": "9177", "q ": "9179", "q,": "917A", "q.": "917B", "q!": "917C", "q?": "917D", "r ": "917E", "r,": "9180", "r.": "9181", "r!": "9182", "r?": "9183", "s ": "9186", "s,": "9187", "s.": "9188", "s!": "918A", "s?": "918B", "t ": "918D", "t,": "918F", "t.": "9190", "t!": "9193", "t?": "9194", "u ": "9195", "u,": "9196", "u.": "9197", "u!": "9198", "u?": "919B", "v ": "919C", "v,": "919D", "v.": "919E", "v!": "919F", "v?": "91A0", "w ": "91A1", "w,": "91A2", "w.": "91A3", "w!": "91A4", "w?": "91A5", "x ": "91A6", "x,": "91A7", "x.": "91A8", "x!": "91A9", "x?": "91AA", "y ": "91AB", "y,": "91AC", "y.": "91AD", "y!": "91AE", "y?": "91AF", "z ": "91B0", "z,": "91B1", "z.": "91B2", "z!": "91B3", "z?": "91B5", "n'": "91B6", "v'": "91B7", "I'": "91B8", "e'": "91B9", "y'": "91BA", "'s": "91BB", "'n": "91BC", "'e": "91BD", "'t": "91BE", "A ": "91BF", "I ": "91C1", " A": "91C2", " B": "91C3", " C": "91C5", " D": "91CA", " E": "91CC", " F": "91CE", " G": "91CF", " H": "91D1", " I": "91D2", " J": "91D3", " K": "91D4", " L": "91D5", " M": "91D6", " N": "91D7", " O": "91D8", " P": "91D9", " Q": "91DB", " R": "91DC", " S": "91DD", " T": "91DE", " U": "91DF", " V": "91E0", " W": "91E2", " X": "91E3", " Y": "91E4", " Z": "91E5", " a": "91E6", " b": "91E7", " c": "91E8", " d": "91E9", " e": "91EA", " f": "91EC", " g": "91ED", " h": "91EE", " i": "91F0", " j": "91F1", " k": "91F2", " l": "91F4", " m": "91F5", " n": "91FC", " o": "9240", " p": "9241", " q": "9242", " r": "9243", " s": "9244", " t": "9245", " u": "9249", " v": "924A", " w": "924B", " x": "924E", " y": "924F", " z": "9250", "AA": "9251", "AB": "9253", "AC": "9254", "AD": "9255", "AE": "9257", "AF": "9259", "AG": "925A", "AH": "925B", "AI": "925E", "AJ": "925F", "AK": "9261", "AL": "9262", "AM": "9263", "AN": "9264", "AO": "9265", "AP": "9266", "AQ": "9267", "AR": "9269", "AS": "926A", "AT": "926B", "AU": "926C", "AV": "926D", "AW": "926E", "AX": "926F", "AY": "9270", "AZ": "9271", "BA": "9272", "BB": "9273", "BC": "9274", "BD": "9275", "BE": "9276", "BF": "9278", "BG": "9279", "BH": "927A", "BI": "927B", "BJ": "927C", "BK": "927D", "BL": "9280", "BM": "9283", "BN": "9285", "BO": "9286", "BP": "9287", "BQ": "9288", "BR": "9289", "BS": "928A", "BT": "928B", "BU": "928C", "BV": "928D", "BW": "928E", "BX": "9293", "BY": "9296", "BZ": "9298", "CA": "9299", "CB": "929A", "CC": "929B", "CD": "929D", "CE": "929F", "CF": "92A0", "CG": "92A1", "CH": "92A3", "CI": "92A4", "CJ": "92A5", "CK": "92A6", "CL": "92A7", "CM": "92A9", "CN": "92AA", "CO": "92AC", "CP": "92AD", "CQ": "92AE", "CR": "92B0", "CS": "92B1", "CT": "92B2", "CU": "92B4", "CV": "92B5", "CW": "92B7", "CX": "92B8", "CY": "92B9", "CZ": "92BA", "DA": "92BC", "DB": "92BE", "DC": "92BF", "DD": "92C0", "DE": "92C2", "DF": "92C3", "DG": "92C5", "DH": "92C7", "DI": "92C9", "DJ": "92CA", "DK": "92CB", "DL": "92CD", "DM": "92D0", "DN": "92D2", "DO": "92D4", "DP": "92D6", "DQ": "92D7", "DR": "92D8", "DS": "92DC", "DT": "92DD", "DU": "92DE", "DV": "92DF", "DW": "92E0", "DX": "92E1", "DY": "92E2", "DZ": "92E3", "EA": "92E5", "EB": "92E6", "EC": "92E7", "ED": "92E8", "EE": "92E9", "EF": "92EA", "EG": "92EB", "EH": "92EC", "EI": "92ED", "EJ": "92EF", "EK": "92F1", "EL": "92F4", "EM": "92F6", "EN": "92F7", "EO": "92F8", "EP": "92F9", "EQ": "92FA", "ER": "9342", "ES": "9344", "ET": "9345", "EU": "9347", "EV": "9349", "EW": "934A", "EX": "934B", "EY": "934E", "EZ": "934F", "FA": "9350", "FB": "9352", "FC": "9353", "FD": "9354", "FE": "9356", "FF": "9357", "FG": "9358", "FH": "9359", "FI": "935C", "FJ": "935D", "FK": "935E", "FL": "935F", "FM": "9360", "FN": "9361", "FO": "9363", "FP": "9364", "FQ": "9366", "FR": "9368", "FS": "9369", "FT": "936B", "FU": "936C", "FV": "936E", "FW": "936F", "FX": "9371", "FY": "9372", "FZ": "9373", "GA": "9377", "GB": "9378", "GC": "9379", "GD": "937A", "GE": "937B", "GF": "937C", "GG": "937D", "GH": "937E", "GI": "9380", "GJ": "9381", "GK": "9382", "GL": "9383", "GM": "9386", "GN": "9387", "GO": "9388", "GP": "9389", "GQ": "938A", "GR": "938B", "GS": "938C", "GT": "938F", "GU": "9390", "GV": "9391", "GW": "9392", "GX": "9394", "GY": "9396", "GZ": "9399", "HA": "939A", "HB": "939B", "HC": "939C", "HD": "939D", "HE": "939E", "HF": "939F", "HG": "93A1", "HH": "93A2", "HI": "93A4", "HJ": "93A5", "HK": "93A6", "HL": "93A7", "HM": "93A9", "HN": "93AA", "HO": "93AC", "HP": "93AD", "HQ": "93AE", "HR": "93AF", "HS": "93B0", "HT": "93B1", "HU": "93B2", "HV": "93B4", "HW": "93B5", "HX": "93B6", "HY": "93B7", "HZ": "93B9", "IA": "93BA", "IB": "93BB", "IC": "93BE", "ID": "93BF", "IE": "93C1", "IF": "93C2", "IG": "93C4", "IH": "93C5", "II": "93C6", "IJ": "93C7", "IK": "93CB", "IL": "93CD", "IM": "93D0", "IN": "93D4", "IO": "93D5", "IP": "93D6", "IQ": "93D8", "IR": "93DA", "IS": "93DC", "IT": "93DD", "IU": "93DE", "IV": "93DF", "IW": "93E0", "IX": "93E3", "IY": "93E4", "IZ": "93E5", "JA": "93E7", "JB": "93E9", "JC": "93EA", "JD": "93EC", "JE": "93ED", "JF": "93EE", "JG": "93EF", "JH": "93F1", "JI": "93F2", "JJ": "93F5", "JK": "93F6", "JL": "93F7", "JM": "93F8", "JN": "93F9", "JO": "93FA", "JP": "93FB", "JQ": "93FC", "JR": "9440", "JS": "9441", "JT": "9443", "JU": "9444", "JV": "9445", "JW": "9446", "JX": "9447", "JY": "944A", "JZ": "944C", "KA": "944D", "KB": "944E", "KC": "944F", "KD": "9450", "KE": "9452", "KF": "9454", "KG": "9456", "KH": "9459", "KI": "945A", "KJ": "945B", "KK": "945C", "KL": "945D", "KM": "945E", "KN": "945F", "KO": "9460", "KP": "9462", "KQ": "9463", "KR": "9464", "KS": "9465", "KT": "9467", "KU": "9468", "KV": "946A", "KW": "946B", "KX": "946D", "KY": "946E", "KZ": "946F", "LA": "9473", "LB": "9474", "LC": "9477", "LD": "9478", "LE": "9479", "LF": "947A", "LG": "947B", "LH": "947C", "LI": "947E", "LJ": "9483", "LK": "9484", "LL": "9487", "LM": "948B", "LN": "948C", "LO": "948E", "LP": "948F", "LQ": "9491", "LR": "9492", "LS": "9493", "LT": "9496", "LU": "9497", "LV": "9499", "LW": "949A", "LX": "949B", "LY": "949E", "LZ": "949F", "MA": "94A0", "MB": "94A6", "MC": "94A7", "MD": "94A8", "ME": "94A9", "MF": "94AA", "MG": "94AB", "MH": "94AD", "MI": "94AF", "MJ": "94B1", "MK": "94B2", "ML": "94B5", "MM": "94B9", "MN": "94BA", "MO": "94BB", "MP": "94BC", "MQ": "94BD", "MR": "94BF", "MS": "94C0", "MT": "94C2", "MU": "94C3", "MV": "94C4", "MW": "94C5", "MX": "94C6", "MY": "94C8", "MZ": "94C9", "NA": "94CA", "NB": "94CB", "NC": "94CC", "ND": "94CD", "NE": "94CE", "NF": "94CF", "NG": "94D1", "NH": "94D3", "NI": "94D4", "NJ": "94D5", "NK": "94D6", "NL": "94D7", "NM": "94D8", "NN": "94DA", "NO": "94DB", "NP": "94DC", "NQ": "94DE", "NR": "94DF", "NS": "94E0", "NT": "94E3", "NU": "94E4", "NV": "94E5", "NW": "94E6", "NX": "94E7", "NY": "94E8", "NZ": "94E9", "OA": "94EA", "OB": "94EC", "OC": "94ED", "OD": "94EE", "OE": "94EF", "OF": "94F0", "OG": "94F1", "OH": "94F2", "OI": "94F5", "OJ": "94F6", "OK": "94F7", "OL": "94FB", "OM": "94FC", "ON": "9540", "OO": "9541", "OP": "9543", "OQ": "9546", "OR": "9547", "OS": "9549", "OT": "954B", "OU": "954D", "OV": "9550", "OW": "9552", "OX": "9553", "OY": "9555", "OZ": "9557", "PA": "9558", "PB": "9559", "PC": "955B", "PD": "955C", "PE": "955D", "PF": "955E", "PG": "9560", "PH": "9561", "PI": "9562", "PJ": "9563", "PK": "9567", "PL": "9569", "PM": "956C", "PN": "956D", "PO": "956E", "PP": "9570", "PQ": "9571", "PR": "9572", "PS": "9573", "PT": "9574", "PU": "9576", "PV": "9577", "PW": "9578", "PX": "9579", "PY": "957A", "PZ": "957B", "QU": "957C", "RA": "957E", "RB": "9581", "RC": "9582", "RD": "9583", "RE": "9584", "RF": "9585", "RG": "9588", "RH": "9589", "RI": "958C", "RJ": "958E", "RK": "958F", "RL": "9590", "RM": "9591", "RN": "9594", "RO": "9595", "RP": "9596", "RQ": "9597", "RR": "959A", "RS": "959B", "RT": "959C", "RU": "959D", "RV": "959E", "RW": "959F", "RX": "95A0", "RY": "95A1", "RZ": "95A2", "SA": "95A3", "SB": "95A4", "SC": "95A5", "SD": "95A6", "SE": "95A7", "SF": "95A8", "SG": "95AA", "SH": "95AC", "SI": "95AD", "SJ": "95B1", "SK": "95B2", "SL": "95B4", "SM": "95B5", "SN": "95B6", "SO": "95B7", "SP": "95B9", "SQ": "95BA", "SR": "95BB", "SS": "95BD", "ST": "95BE", "SU": "95BF", "SV": "95C0", "SW": "95C2", "SX": "95C3", "SY": "95C4", "SZ": "95C5", "TA": "95C7", "TB": "95C8", "TC": "95C9", "TD": "95CA", "TE": "95CB", "TF": "95CC", "TG": "95CE", "TH": "95CF", "TI": "95D0", "TJ": "95D2", "TK": "95D3", "TL": "95D4", "TM": "95D5", "TN": "95D6", "TO": "95D7", "TP": "95D9", "TQ": "95DB", "TR": "95DF", "TS": "95E0", "TT": "95E1", "TU": "95E2", "TV": "95E4", "TW": "95E5", "TX": "95E8", "TY": "95E9", "TZ": "95EA", "UA": "95EB", "UB": "95EF", "UC": "95F0", "UD": "95F1", "UE": "95F2", "UF": "95F3", "UG": "95F4", "UH": "95F5", "UI": "95F6", "UJ": "95F8", "UK": "95FA", "UL": "95FB", "UM": "95FC", "UN": "9640", "UO": "9641", "UP": "9643", "UQ": "9645", "UR": "9646", "US": "9647", "UT": "9649", "UU": "964A", "UV": "964B", "UW": "964C", "UX": "964D", "UY": "964E", "UZ": "964F", "VA": "9650", "VB": "9652", "VC": "9653", "VD": "9654", "VE": "9656", "VF": "9658", "VG": "9659", "VH": "965A", "VI": "965B", "VJ": "965C", "VK": "965D", "VL": "965E", "VM": "965F", "VN": "9660", "VO": "9661", "VP": "9663", "VQ": "9664", "VR": "9665", "VS": "9666", "VT": "9668", "VU": "9669", "VV": "966A", "VW": "966B", "VX": "966C", "VY": "966E", "VZ": "966F", "WA": "9670", "WB": "9671", "WC": "9676", "WD": "9677", "WE": "9678", "WF": "9679", "WG": "967B", "WH": "967D", "WI": "967E", "WJ": "9680", "WK": "9681", "WL": "9682", "WM": "9683", "WN": "9684", "WO": "9685", "WP": "9687", "WQ": "9688", "WR": "968B", "WS": "968C", "WT": "968D", "WU": "9694", "WV": "9695", "WW": "9696", "WX": "969B", "WY": "969C", "WZ": "969D", "XA": "969E", "XB": "969F", "XC": "96A1", "XD": "96A2", "XE": "96A3", "XF": "96A4", "XG": "96A6", "XH": "96A7", "XI": "96AB", "XJ": "96AD", "XK": "96AF", "XL": "96B0", "XM": "96B1", "XN": "96B2", "XO": "96B3", "XP": "96B5", "XQ": "96B6", "XR": "96BA", "XS": "96BC", "XT": "96BD", "XU": "96BE", "XV": "96BF", "XW": "96C0", "XX": "96C1", "XY": "96C2", "XZ": "96C5", "YA": "96C6", "YB": "96C8", "YC": "96CA", "YD": "96CB", "YE": "96CD", "YF": "96CE", "YG": "96D1", "YH": "96D2", "YI": "96D4", "YJ": "96D8", "YK": "96D9", "YL": "96DA", "YM": "96DC", "YN": "96DD", "YO": "96DF", "YP": "96E1", "YQ": "96E2", "YR": "96E3", "YS": "96E4", "YT": "96E5", "YU": "96E7", "YV": "96E8", "YW": "96E9", "YX": "96EA", "YY": "96EC", "YZ": "96ED", "ZA": "96EE", "ZB": "96F0", "ZC": "96F1", "ZD": "96F2", "ZE": "96F3", "ZF": "96F4", "ZG": "96F5", "ZH": "96F6", "ZI": "96F7", "ZJ": "96FB", "ZK": "9740", "ZL": "9741", "ZM": "9742", "ZN": "9743", "ZO": "9744", "ZP": "9745", "ZQ": "9746", "ZR": "9748", "ZS": "9749", "ZT": "974A", "ZU": "974C", "ZV": "974E", "ZW": "9752", "ZX": "9753", "ZY": "9754", "ZZ": "9755"}""")
MAPPING.update({". ": "815D", ", ": "815E", "! ": "815F", "? ": "815C"})

def visible_token(tok: str) -> str:
    return tok.replace(" ", "␠")

def encode_line(line: str, append_trailing_space: bool = True):
    work = line
    info = []
    errors = []
    if len(work) % 2 == 1:
        if append_trailing_space:
            work += " "
        else:
            errors.append("Odd-length line without trailing-space fix.")
            return {
                "tokens": [],
                "codes": [],
                "bytes": [],
                "errors": errors,
                "normalized": work,
            }
    tokens = [work[i:i+2] for i in range(0, len(work), 2)]
    codes = []
    bytes_out = []
    for idx, tok in enumerate(tokens):
        code = MAPPING.get(tok)
        if code is None:
            errors.append(f"Unsupported token at pair {idx+1}: {visible_token(tok)}")
            codes.append("????")
            bytes_out.append("?? ??")
        else:
            codes.append(code)
            bytes_out.append(code[:2] + " " + code[2:])
    return {
        "tokens": tokens,
        "codes": codes,
        "bytes": bytes_out,
        "errors": errors,
        "normalized": work,
    }

def encode_text(text: str, append_trailing_space: bool = True):
    lines = text.splitlines()
    if text.endswith("\n"):
        # splitlines() drops the terminal empty line; preserve it
        lines.append("")
    results = [encode_line(line, append_trailing_space) for line in lines]
    return results

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("With You Bigram Encoder")
        self.geometry("1180x760")
        self.minsize(980, 640)

        self.append_space_var = tk.BooleanVar(value=True)
        self.auto_var = tk.BooleanVar(value=True)

        self._build_ui()
        self.bind_all("<Control-Return>", lambda e: self.run_encode())
        self.bind_all("<Control-l>", lambda e: self.clear_all())

    def _build_ui(self):
        top = ttk.Frame(self, padding=8)
        top.pack(fill="x")

        ttk.Label(top, text="Type ASCII text here. Encoding uses the existing bigram tilemap.").pack(anchor="w")
        opts = ttk.Frame(top)
        opts.pack(fill="x", pady=(6, 0))

        ttk.Checkbutton(
            opts,
            text="Odd-numbered lines auto-append trailing space",
            variable=self.append_space_var,
            command=self.run_encode,
        ).pack(side="left")

        ttk.Checkbutton(
            opts,
            text="Auto-encode while typing",
            variable=self.auto_var,
        ).pack(side="left", padx=(16, 0))

        ttk.Button(opts, text="Encode", command=self.run_encode).pack(side="left", padx=(16, 0))
        ttk.Button(opts, text="Clear", command=self.clear_all).pack(side="left", padx=(8, 0))

        body = ttk.Panedwindow(self, orient="horizontal")
        body.pack(fill="both", expand=True, padx=8, pady=8)

        left = ttk.Frame(body)
        right = ttk.Frame(body)
        body.add(left, weight=1)
        body.add(right, weight=1)

        ttk.Label(left, text="Input").pack(anchor="w")
        self.input_text = tk.Text(left, wrap="word", height=16, undo=True, font=("Consolas", 11))
        self.input_text.pack(fill="both", expand=True)
        self.input_text.bind("<<Modified>>", self._on_modified)

        summary = ttk.LabelFrame(right, text="Summary", padding=8)
        summary.pack(fill="x")
        self.summary_var = tk.StringVar(value="No input yet.")
        ttk.Label(summary, textvariable=self.summary_var, justify="left").pack(anchor="w")

        out_pane = ttk.Notebook(right)
        out_pane.pack(fill="both", expand=True, pady=(8, 0))

        self.tokens_text = self._make_output_tab(out_pane, "Token pairs")
        self.codes_text = self._make_output_tab(out_pane, "Code hex")
        self.bytes_text = self._make_output_tab(out_pane, "Script bytes")
        self.errors_text = self._make_output_tab(out_pane, "Warnings / unsupported")

        btns = ttk.Frame(right)
        btns.pack(fill="x", pady=(8, 0))
        ttk.Button(btns, text="Copy token pairs", command=lambda: self.copy_widget(self.tokens_text)).pack(side="left")
        ttk.Button(btns, text="Copy code hex", command=lambda: self.copy_widget(self.codes_text)).pack(side="left", padx=(8, 0))
        ttk.Button(btns, text="Copy script bytes", command=lambda: self.copy_widget(self.bytes_text)).pack(side="left", padx=(8, 0))

        footer = ttk.Label(
            self,
            text="Notes: pairs are taken exactly two characters at a time, per line. Unsupported pairs are flagged. Ctrl+Enter encodes.",
            padding=(8, 0, 8, 8),
        )
        footer.pack(anchor="w")

    def _make_output_tab(self, notebook, title):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=title)
        txt = tk.Text(frame, wrap="word", height=10, font=("Consolas", 11))
        txt.pack(fill="both", expand=True)
        txt.configure(state="disabled")
        return txt

    def _on_modified(self, event=None):
        if self.input_text.edit_modified():
            self.input_text.edit_modified(False)
            if self.auto_var.get():
                self.run_encode()

    def set_output(self, widget, text):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.configure(state="disabled")

    def copy_widget(self, widget):
        text = widget.get("1.0", "end-1c")
        self.clipboard_clear()
        self.clipboard_append(text)

    def clear_all(self):
        self.input_text.delete("1.0", "end")
        self.set_output(self.tokens_text, "")
        self.set_output(self.codes_text, "")
        self.set_output(self.bytes_text, "")
        self.set_output(self.errors_text, "")
        self.summary_var.set("No input yet.")

    def run_encode(self):
        src = self.input_text.get("1.0", "end-1c")
        if src == "":
            self.clear_all()
            return

        results = encode_text(src, self.append_space_var.get())

        token_lines = []
        code_lines = []
        byte_lines = []
        error_lines = []

        total_pairs = 0
        bad_pairs = 0
        padded_lines = 0

        for line_no, result in enumerate(results, start=1):
            toks = result["tokens"]
            codes = result["codes"]
            bys = result["bytes"]
            errs = result["errors"]


            total_pairs += len(toks)
            bad_pairs += sum(1 for c in codes if c == "????")

            token_lines.append(" ".join(visible_token(t) for t in toks))
            code_lines.append(" ".join(codes))
            byte_lines.append(" ".join(bys))

            if errs:
                error_lines.append(f"Line {line_no}:")
                for err in errs:
                    error_lines.append(f"  - {err}")

        self.set_output(self.tokens_text, "\n".join(token_lines))
        self.set_output(self.codes_text, "\n".join(code_lines))
        self.set_output(self.bytes_text, "\n".join(byte_lines))
        self.set_output(self.errors_text, "\n".join(error_lines) if error_lines else "No unsupported pairs.")

        odd_note = []
        src_lines = src.splitlines()
        if src.endswith("\n"):
            src_lines.append("")
        for i, line in enumerate(src_lines, start=1):
            if len(line) % 2 == 1 and self.append_space_var.get():
                odd_note.append(str(i))
        padded_lines = len(odd_note)

        summary = (
            f"Lines: {len(results)}\n"
            f"Pairs: {total_pairs}\n"
            f"Unsupported pairs: {bad_pairs}\n"
            f"Odd lines padded with trailing space: {padded_lines}"
        )
        if odd_note:
            summary += "\nPadded line numbers: " + ", ".join(odd_note[:20])
            if len(odd_note) > 20:
                summary += " ..."
        self.summary_var.set(summary)

if __name__ == "__main__":
    app = App()
    app.mainloop()
