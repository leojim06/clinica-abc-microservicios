function computeHttpSignature(config, headerHash) {
    var template = 'keyId="${keyId}",algorithm="${algorithm}",headers="${headers}",signature="${signature}"';
    var sig = template;
    // compute sig here
    var signingBase = '';
    config.headers.forEach(function (h) {
        if (signingBase !== '') { signingBase += '\n'; }
        signingBase += h.toLowerCase() + ": " + headerHash[h];
    });
    var hashf = (function () {
        switch (config.algorithm) {
            case 'hmac-sha1': return CryptoJS.HmacSHA1;
            case 'hmac-sha256': return CryptoJS.HmacSHA256;
            case 'hmac-sha512': return CryptoJS.HmacSHA512;
            default: return null;
        }
    }());
    var hash = hashf(signingBase, config.secretkey);
    var signatureOptions = {
        keyId: config.keyId,
        algorithm: config.algorithm,
        headers: config.headers,
        signature: CryptoJS.enc.Base64.stringify(hash)
    };
    // build sig string here
    Object.keys(signatureOptions).forEach(function (key) {
        var pattern = "${" + key + "}";
        var value = (typeof signatureOptions[key] != 'string') ? signatureOptions[key].join(' ') : signatureOptions[key];
        sig = sig.replace(pattern, value);
    });
    return sig;
}
var curDate = new Date().toGMTString();
var targetUrl = request.url.trim(); // there may be surrounding ws
targetUrl = targetUrl.replace(new RegExp('^https?://[^/]+/'), '/'); // strip hostname
var method = request.method.toLowerCase();
var sha256digest = CryptoJS.SHA256(request.data);
var base64sha256 = CryptoJS.enc.Base64.stringify(sha256digest);
var computedDigest = base64sha256;
var headerHash = Object.assign(Object.assign({}, pm.request.headers.toObject(true)), {
    date: curDate,
    digest: computedDigest,
    '(request-target)': targetUrl
});
var config = {
    algorithm: 'hmac-sha256',
    keyId: pm.environment.get("signature_key_id"),
    secretkey: pm.environment.get("signature_key"),
    headers: ['(request-target)', 'date', 'digest']
};
var sig = computeHttpSignature(config, headerHash);
console.log(computedDigest)
// Modificar body
 let body = pm.request.body
 console.log(body)
 body = {...body, raw: { nombre: "otro", apellido: "otro" } }
 console.log(body)
 pm.request.body.update(body);
pm.request.headers.add({ key: 'httpsig', value: sig })
pm.request.headers.add({ key: 'computed-digest', value: computedDigest })
pm.request.headers.add({ key: 'current-date', value: curDate })
pm.request.headers.add({ key: 'target-url', value: targetUrl })
pm.request.headers.add({ key: 'target-method', value: method })