function getSign(token, t, appkey, data) {
                return function(e) {
                    function t(e, t) {
                        return e << t | e >>> 32 - t
                    }
                    function n(e, t) {
                        var n, i, r, o, s;
                        return r = 2147483648 & e,
                        o = 2147483648 & t,
                        s = (1073741823 & e) + (1073741823 & t),
                        (n = 1073741824 & e) & (i = 1073741824 & t) ? 2147483648 ^ s ^ r ^ o : n | i ? 1073741824 & s ? 3221225472 ^ s ^ r ^ o : 1073741824 ^ s ^ r ^ o : s ^ r ^ o
                    }
                    function i(e, i, r, o, s, a, u) {
                        var c;
                        return n(t(e = n(e, n(n((c = i) & r | ~c & o, s), u)), a), i)
                    }
                    function r(e, i, r, o, s, a, u) {
                        var c;
                        return n(t(e = n(e, n(n(i & (c = o) | r & ~c, s), u)), a), i)
                    }
                    function o(e, i, r, o, s, a, u) {
                        return n(t(e = n(e, n(n(i ^ r ^ o, s), u)), a), i)
                    }
                    function s(e, i, r, o, s, a, u) {
                        return n(t(e = n(e, n(n(r ^ (i | ~o), s), u)), a), i)
                    }
                    function a(e) {
                        var t, n = "", i = "";
                        for (t = 0; t <= 3; t++)
                            n += (i = "0" + (e >>> 8 * t & 255).toString(16)).substr(i.length - 2, 2);
                        return n
                    }
                    var u, c, p, f, l, d, h, m, v, O;
                    for (u = function(e) {
                        for (var t, n = e.length, i = n + 8, r = 16 * ((i - i % 64) / 64 + 1), o = new Array(r - 1), s = 0, a = 0; a < n; )
                            s = a % 4 * 8,
                            o[t = (a - a % 4) / 4] = o[t] | e.charCodeAt(a) << s,
                            a++;
                        return s = a % 4 * 8,
                        o[t = (a - a % 4) / 4] = o[t] | 128 << s,
                        o[r - 2] = n << 3,
                        o[r - 1] = n >>> 29,
                        o
                    }(e = function(e) {
                        e = e.replace(/\r\n/g, "\n");
                        for (var t = "", n = 0; n < e.length; n++) {
                            var i = e.charCodeAt(n);
                            i < 128 ? t += String.fromCharCode(i) : (127 < i && i < 2048 ? t += String.fromCharCode(i >> 6 | 192) : (t += String.fromCharCode(i >> 12 | 224),
                            t += String.fromCharCode(i >> 6 & 63 | 128)),
                            t += String.fromCharCode(63 & i | 128))
                        }
                        return t
                    }(e)),
                    h = 1732584193,
                    m = 4023233417,
                    v = 2562383102,
                    O = 271733878,
                    c = 0; c < u.length; c += 16)
                        m = s(m = s(m = s(m = s(m = o(m = o(m = o(m = o(m = r(m = r(m = r(m = r(m = i(m = i(m = i(m = i(f = m, v = i(l = v, O = i(d = O, h = i(p = h, m, v, O, u[c + 0], 7, 3614090360), m, v, u[c + 1], 12, 3905402710), h, m, u[c + 2], 17, 606105819), O, h, u[c + 3], 22, 3250441966), v = i(v, O = i(O, h = i(h, m, v, O, u[c + 4], 7, 4118548399), m, v, u[c + 5], 12, 1200080426), h, m, u[c + 6], 17, 2821735955), O, h, u[c + 7], 22, 4249261313), v = i(v, O = i(O, h = i(h, m, v, O, u[c + 8], 7, 1770035416), m, v, u[c + 9], 12, 2336552879), h, m, u[c + 10], 17, 4294925233), O, h, u[c + 11], 22, 2304563134), v = i(v, O = i(O, h = i(h, m, v, O, u[c + 12], 7, 1804603682), m, v, u[c + 13], 12, 4254626195), h, m, u[c + 14], 17, 2792965006), O, h, u[c + 15], 22, 1236535329), v = r(v, O = r(O, h = r(h, m, v, O, u[c + 1], 5, 4129170786), m, v, u[c + 6], 9, 3225465664), h, m, u[c + 11], 14, 643717713), O, h, u[c + 0], 20, 3921069994), v = r(v, O = r(O, h = r(h, m, v, O, u[c + 5], 5, 3593408605), m, v, u[c + 10], 9, 38016083), h, m, u[c + 15], 14, 3634488961), O, h, u[c + 4], 20, 3889429448), v = r(v, O = r(O, h = r(h, m, v, O, u[c + 9], 5, 568446438), m, v, u[c + 14], 9, 3275163606), h, m, u[c + 3], 14, 4107603335), O, h, u[c + 8], 20, 1163531501), v = r(v, O = r(O, h = r(h, m, v, O, u[c + 13], 5, 2850285829), m, v, u[c + 2], 9, 4243563512), h, m, u[c + 7], 14, 1735328473), O, h, u[c + 12], 20, 2368359562), v = o(v, O = o(O, h = o(h, m, v, O, u[c + 5], 4, 4294588738), m, v, u[c + 8], 11, 2272392833), h, m, u[c + 11], 16, 1839030562), O, h, u[c + 14], 23, 4259657740), v = o(v, O = o(O, h = o(h, m, v, O, u[c + 1], 4, 2763975236), m, v, u[c + 4], 11, 1272893353), h, m, u[c + 7], 16, 4139469664), O, h, u[c + 10], 23, 3200236656), v = o(v, O = o(O, h = o(h, m, v, O, u[c + 13], 4, 681279174), m, v, u[c + 0], 11, 3936430074), h, m, u[c + 3], 16, 3572445317), O, h, u[c + 6], 23, 76029189), v = o(v, O = o(O, h = o(h, m, v, O, u[c + 9], 4, 3654602809), m, v, u[c + 12], 11, 3873151461), h, m, u[c + 15], 16, 530742520), O, h, u[c + 2], 23, 3299628645), v = s(v, O = s(O, h = s(h, m, v, O, u[c + 0], 6, 4096336452), m, v, u[c + 7], 10, 1126891415), h, m, u[c + 14], 15, 2878612391), O, h, u[c + 5], 21, 4237533241), v = s(v, O = s(O, h = s(h, m, v, O, u[c + 12], 6, 1700485571), m, v, u[c + 3], 10, 2399980690), h, m, u[c + 10], 15, 4293915773), O, h, u[c + 1], 21, 2240044497), v = s(v, O = s(O, h = s(h, m, v, O, u[c + 8], 6, 1873313359), m, v, u[c + 15], 10, 4264355552), h, m, u[c + 6], 15, 2734768916), O, h, u[c + 13], 21, 1309151649), v = s(v, O = s(O, h = s(h, m, v, O, u[c + 4], 6, 4149444226), m, v, u[c + 11], 10, 3174756917), h, m, u[c + 2], 15, 718787259), O, h, u[c + 9], 21, 3951481745),
                        h = n(h, p),
                        m = n(m, f),
                        v = n(v, l),
                        O = n(O, d);
                    return (a(h) + a(m) + a(v) + a(O)).toLowerCase()
                }( token+ "&" + t + "&" + appkey + "&" + data)
            }
