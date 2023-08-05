(self.webpackChunktvb_ext_bucket=self.webpackChunktvb_ext_bucket||[]).push([[747],{150:(n,e,t)=>{"use strict";t.d(e,{Z:()=>p});var o=t(645),r=t.n(o),i=t(667),a=t.n(i),l=t(719),c=t(453),s=t.n(c),d=r()((function(n){return n[1]})),u=a()(l.Z),f=a()(s());d.push([n.id,"/*\n    See the JupyterLab Developer Guide for useful CSS Patterns:\n\n    https://jupyterlab.readthedocs.io/en/stable/developer/css.html\n*/\n:root {\n  --bucket-download-color: #060;\n  --bucket-text-info-color: #d3d3d3;\n}\n\n/* --------- SPIN ANIMATION ---------- */\n@keyframes spin {\n  from {\n    -moz-transform: rotate(0deg);\n  }\n\n  to {\n    -moz-transform: rotate(360deg);\n  }\n}\n@keyframes spin {\n  from {\n    -webkit-transform: rotate(0deg);\n  }\n\n  to {\n    -webkit-transform: rotate(360deg);\n  }\n}\n@keyframes spin {\n  from {\n    transform: rotate(0deg);\n  }\n\n  to {\n    transform: rotate(360deg);\n  }\n}\n\n/* --------- END SPIN ANIMATION ---------- */\n\n.bucket-container,\n.tvb-bucketWidget {\n  background-color: var(--jp-layout-color1);\n  list-style-type: none;\n}\n\n.bucket-BreadCrumbs {\n  display: flex;\n  flex-flow: row wrap;\n  align-items: center;\n  justify-content: flex-start;\n}\n\n.bucket-BreadCrumbs-Item {\n  cursor: pointer;\n  color: var(--md-blue-500);\n}\n\n.bucket-BreadCrumbs-Item:hover {\n  background-color: var(--jp-layout-color2);\n}\n\n.bucket-container ul {\n  list-style-type: none;\n  padding: 0;\n  margin: 0;\n}\n\n.bucket-container ul > li {\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n  justify-content: flex-start;\n  padding-left: 1em;\n}\n\n.bucket-BrowserListItem:hover {\n  background-color: var(--jp-layout-color2);\n}\n\n.bucket-ContextMenu-container {\n  position: relative;\n}\n\n.bucket-ContextMenu {\n  position: absolute;\n  top: 10px;\n  left: 5px;\n  z-index: 10000;\n  padding: 4px 0;\n  font-size: var(--jp-ui-font-size1);\n  background: var(--jp-layout-color0);\n  color: var(--jp-ui-font-color1);\n  border: var(--jp-border-width) solid var(--jp-ui-font-size1);\n  box-shadow: var(--jp-elevation-z6);\n  white-space: nowrap;\n  overflow-x: hidden;\n  overflow-y: auto;\n  outline: none;\n  opacity: 1;\n  width: 200px;\n}\n\n.bucket-ContextMenu-item {\n  min-height: var(--jp-private-menu-item-height);\n  max-height: var(--jp-private-menu-item-height);\n  line-height: var(--jp-private-menu-item-height);\n}\n\n.bucket-ContextMenu-item div {\n  display: flex;\n  align-items: center;\n  justify-content: center;\n}\n\n.bucket-ContextMenu li:hover {\n  background-color: var(--jp-layout-color2);\n}\n\n.collab-logo {\n  display: inline-block;\n  background-image: url("+u+");\n  background-repeat: no-repeat;\n  background-size: contain;\n  height: 40px;\n  width: 30px;\n  margin-left: 1em;\n}\n\n.bucket-logo {\n  display: flex;\n  align-items: center;\n  justify-content: flex-start;\n}\n\n.bucket-logo-text {\n  margin-left: 0.2em;\n  font-size: 1.2em;\n  display: inline-block;\n}\n\n.bucket-CollabLogo {\n  background-image: url("+f+");\n  filter: opacity(70%);\n}\n\n.bucket-Spinner {\n  display: inline-block;\n  border: 3px solid #7f7f7f;\n  border-left: 3px solid #4ec261;\n  height: 1em;\n  width: 1em;\n  border-radius: 50%;\n  margin: 0 0.5em;\n  animation: spin 0.5s infinite linear;\n}\n\n.align-flex-horizontal {\n  display: flex;\n  flex-direction: row;\n  align-items: flex-start;\n  justify-content: center;\n}\n\n@keyframes rain {\n  0% {\n    top: -1em;\n    opacity: 0;\n  }\n\n  50% {\n    opacity: 1;\n  }\n\n  100% {\n    top: 1em;\n    opacity: 0;\n  }\n}\n\n/* download animation style */\n.bucket-DownloadAnimation {\n  display: inline-block;\n  z-index: 2;\n  position: relative;\n  height: 0.8em;\n  width: 1em;\n  margin-left: 0.5em;\n  margin-top: 0.2em;\n  overflow: hidden;\n  border-top: solid 1px var(--bucket-download-color);\n}\n\n.bucket-DownloadAnimation i {\n  color: var(--bucket-download-color);\n  position: absolute;\n  z-index: 1;\n  animation: linear 0.5s rain infinite;\n}\n\n/* end download animation style */\n\n/* upload animation style */\n.bucket-UploadAnimation {\n  display: inline-block;\n  z-index: 2;\n  position: relative;\n  height: 0.8em;\n  width: 1em;\n  margin-left: 0.5em;\n  margin-top: 0.2em;\n  overflow: hidden;\n  border-top: solid 1px var(--bucket-download-color);\n}\n\n.bucket-UploadAnimation > :first-child {\n  color: var(--bucket-download-color);\n  position: absolute;\n  z-index: 1;\n  animation: reverse 0.5s rain infinite;\n}\n\n/* end upload animation style */\n\n.bucket-DropZone {\n  margin: 0 auto;\n  padding: 0.5em;\n  width: 90%;\n  height: 4em;\n  border: dashed 2px var(--bucket-text-info-color);\n  border-radius: 7px;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n}\n\n.default {\n  border-color: var(--bucket-text-info-color);\n}\n\n.hover {\n  border-color: black;\n}\n\n.bucket-text-info {\n  color: var(--bucket-text-info-color);\n  font-style: italic;\n}\n\n.bucket-Tooltip {\n  position: absolute;\n  top: 5vh;\n  z-index: 99;\n  width: 100%;\n  height: 4em;\n  background-color: var(--jp-layout-color1);\n  border-radius: 7px;\n  box-shadow: var(--jp-elevation-z6);\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  justify-content: center;\n  padding: 0.5em;\n}\n\n.bucket-ShareLink {\n  color: var(--md-blue-500);\n}\n\n.bucket-ShareLink:hover {\n  text-decoration: underline;\n}\n",""]);const p=d},645:n=>{"use strict";n.exports=function(n){var e=[];return e.toString=function(){return this.map((function(e){var t=n(e);return e[2]?"@media ".concat(e[2]," {").concat(t,"}"):t})).join("")},e.i=function(n,t,o){"string"==typeof n&&(n=[[null,n,""]]);var r={};if(o)for(var i=0;i<this.length;i++){var a=this[i][0];null!=a&&(r[a]=!0)}for(var l=0;l<n.length;l++){var c=[].concat(n[l]);o&&r[c[0]]||(t&&(c[2]?c[2]="".concat(t," and ").concat(c[2]):c[2]=t),e.push(c))}},e}},667:n=>{"use strict";n.exports=function(n,e){return e||(e={}),"string"!=typeof(n=n&&n.__esModule?n.default:n)?n:(/^['"].*['"]$/.test(n)&&(n=n.slice(1,-1)),e.hash&&(n+=e.hash),/["'() \t\n]/.test(n)||e.needQuotes?'"'.concat(n.replace(/"/g,'\\"').replace(/\n/g,"\\n"),'"'):n)}},719:(n,e,t)=>{"use strict";t.d(e,{Z:()=>o});const o=t.p+"acb28ef48e64b689e3e44624dd56425825ae6f016b1ff6d65e9004f9d15b3301.png"},379:(n,e,t)=>{"use strict";var o,r=function(){var n={};return function(e){if(void 0===n[e]){var t=document.querySelector(e);if(window.HTMLIFrameElement&&t instanceof window.HTMLIFrameElement)try{t=t.contentDocument.head}catch(n){t=null}n[e]=t}return n[e]}}(),i=[];function a(n){for(var e=-1,t=0;t<i.length;t++)if(i[t].identifier===n){e=t;break}return e}function l(n,e){for(var t={},o=[],r=0;r<n.length;r++){var l=n[r],c=e.base?l[0]+e.base:l[0],s=t[c]||0,d="".concat(c," ").concat(s);t[c]=s+1;var u=a(d),f={css:l[1],media:l[2],sourceMap:l[3]};-1!==u?(i[u].references++,i[u].updater(f)):i.push({identifier:d,updater:b(f,e),references:1}),o.push(d)}return o}function c(n){var e=document.createElement("style"),o=n.attributes||{};if(void 0===o.nonce){var i=t.nc;i&&(o.nonce=i)}if(Object.keys(o).forEach((function(n){e.setAttribute(n,o[n])})),"function"==typeof n.insert)n.insert(e);else{var a=r(n.insert||"head");if(!a)throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");a.appendChild(e)}return e}var s,d=(s=[],function(n,e){return s[n]=e,s.filter(Boolean).join("\n")});function u(n,e,t,o){var r=t?"":o.media?"@media ".concat(o.media," {").concat(o.css,"}"):o.css;if(n.styleSheet)n.styleSheet.cssText=d(e,r);else{var i=document.createTextNode(r),a=n.childNodes;a[e]&&n.removeChild(a[e]),a.length?n.insertBefore(i,a[e]):n.appendChild(i)}}function f(n,e,t){var o=t.css,r=t.media,i=t.sourceMap;if(r?n.setAttribute("media",r):n.removeAttribute("media"),i&&"undefined"!=typeof btoa&&(o+="\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(i))))," */")),n.styleSheet)n.styleSheet.cssText=o;else{for(;n.firstChild;)n.removeChild(n.firstChild);n.appendChild(document.createTextNode(o))}}var p=null,m=0;function b(n,e){var t,o,r;if(e.singleton){var i=m++;t=p||(p=c(e)),o=u.bind(null,t,i,!1),r=u.bind(null,t,i,!0)}else t=c(e),o=f.bind(null,t,e),r=function(){!function(n){if(null===n.parentNode)return!1;n.parentNode.removeChild(n)}(t)};return o(n),function(e){if(e){if(e.css===n.css&&e.media===n.media&&e.sourceMap===n.sourceMap)return;o(n=e)}else r()}}n.exports=function(n,e){(e=e||{}).singleton||"boolean"==typeof e.singleton||(e.singleton=(void 0===o&&(o=Boolean(window&&document&&document.all&&!window.atob)),o));var t=l(n=n||[],e);return function(n){if(n=n||[],"[object Array]"===Object.prototype.toString.call(n)){for(var o=0;o<t.length;o++){var r=a(t[o]);i[r].references--}for(var c=l(n,e),s=0;s<t.length;s++){var d=a(t[s]);0===i[d].references&&(i[d].updater(),i.splice(d,1))}t=c}}}},453:n=>{n.exports="data:image/svg+xml,%3Csvg class='svg-icon' style='width: 1em; height: 1em;vertical-align: middle;fill: currentColor;overflow: hidden;' viewBox='0 0 1024 1024' version='1.1' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M667.428571 694.857143q0 18.857143-13.428571 32.285714T621.714286 740.571429t-32.285715-13.428572T576 694.857143t13.428571-32.285714T621.714286 649.142857t32.285714 13.428572 13.428571 32.285714z m146.285715 0q0 18.857143-13.428572 32.285714T768 740.571429t-32.285714-13.428572-13.428572-32.285714 13.428572-32.285714 32.285714-13.428572 32.285714 13.428572 13.428572 32.285714z m64 91.428571v-182.857143q0-7.428571-5.428572-12.857142t-12.857143-5.428572H164.571429q-7.428571 0-12.857143 5.428572T146.285714 603.428571v182.857143q0 7.428571 5.428572 12.857143t12.857143 5.428572h694.857142q7.428571 0 12.857143-5.428572t5.428572-12.857143zM174.857143 512h674.285714l-89.714286-275.428571q-2.285714-7.428571-9.142857-12.285715t-14.857143-4.857143H288.571429q-8 0-14.857143 4.857143T264.571429 236.571429z m776 91.428571v182.857143q0 37.714286-26.857143 64.571429t-64.571429 26.857143H164.571429q-37.714286 0-64.571429-26.857143T73.142857 786.285714v-182.857143q0-14.285714 9.142857-42.857142l112.571429-346.285715q9.714286-30.285714 36-49.142857t57.714286-18.857143h446.857142q31.428571 0 57.714286 18.857143t36 49.142857l112.571429 346.285715q9.142857 28.571429 9.142857 42.857142z' /%3E%3C/svg%3E"},747:(n,e,t)=>{"use strict";t.r(e);var o=t(379),r=t.n(o),i=t(150);r()(i.Z,{insert:"head",singleton:!1}),i.Z.locals}}]);