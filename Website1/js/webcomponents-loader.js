/**
 * @license
 * Copyright (c) 2018 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at http://polymer.github.io/PATENTS.txt
 */
! function() {
	var e = document.createElement("script");
	if(!("noModule" in e) && "onbeforeload" in e) {
		var n = !1;
		document.addEventListener("beforeload", (function(t) {
			if(t.target === e) n = !0;
			else if(!t.target.hasAttribute("nomodule") || !n) return;
			t.preventDefault()
		}), !0), e.type = "module", e.src = ".", document.head.appendChild(e), e.remove()
	}
}(),
function() {
	"use strict";
	var e, n = !1,
		t = [],
		o = !1;

	function c() {
		window.WebComponents.ready = !0, document.dispatchEvent(new CustomEvent("WebComponentsReady", {
			bubbles: !0
		}))
	}

	function r() {
		o = !1;
		var n = t.map((function(e) {
			return e instanceof Function ? e() : e
		}));
		return t = [], Promise.all(n).then((function() {
			o = !0, e && e()
		})).catch((function(e) {
			console.error(e)
		}))
	}
	window.WebComponents = window.WebComponents || {}, window.WebComponents.ready = window.WebComponents.ready || !1, window.WebComponents.waitFor = window.WebComponents.waitFor || function(e) {
		e && (t.push(e), n && r())
	}, window.WebComponents._batchCustomElements = function() {
		window.customElements && customElements.polyfillWrapFlushCallback && customElements.polyfillWrapFlushCallback((function(n) {
			e = n, o && e()
		}))
	};
	var i = "webcomponents-loader.2.8.0.js",
		d = [];
	(!("attachShadow" in Element.prototype) || !("getRootNode" in Element.prototype) || window.ShadyDOM && window.ShadyDOM.force) && d.push("sd"), window.customElements && !window.customElements.forcePolyfill || d.push("ce");
	var a = function() {
		var e = document.createElement("template");
		if(!("content" in e)) return !0;
		if(!(e.content.cloneNode() instanceof DocumentFragment)) return !0;
		var n = document.createElement("template");
		n.content.appendChild(document.createElement("div")), e.content.appendChild(n);
		var t = e.cloneNode(!0);
		return 0 === t.content.childNodes.length || 0 === t.content.firstChild.content.childNodes.length
	}();
	if(window.Promise && Array.from && window.URL && window.Symbol && !a || (d = ["sd-ce-pf"]), d.length) {
		var l, m = "bundles/webcomponents-" + d.join("-") + ".2.8.0.js";
		l = document.querySelector('script[src*="' + i + '"]').src.replace(i, m);
		var s = document.createElement("script");
		s.src = l, s.setAttribute("onload", "window.WebComponents._batchCustomElements()"), document.write(s.outerHTML), document.addEventListener("DOMContentLoaded", (function() {
			window.HTMLTemplateElement && HTMLTemplateElement.bootstrap && HTMLTemplateElement.bootstrap(window.document), n = !0, r().then(c)
		}))
	} else n = !0, c()
}();