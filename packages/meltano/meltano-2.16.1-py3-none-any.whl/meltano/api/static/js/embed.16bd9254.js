(function(){var e={3171:function(e,t,s){"use strict";var r=s(8345),n=s(144),o=s(594),a=function(){var e=this,t=e._self._c;return t("div",{attrs:{id:"app"}},[t("router-view")],1)},l=[],i={name:"Embed"},c=i,u=s(1001),d=(0,u.Z)(c,a,l,!1,null,null,null),j=d.exports;function h(){return window.FLASK||{appUrl:"http://localhost:5000",oauthServiceUrl:"http://localhost:5000/-/oauth",oauthServiceProviders:"all".split(",").filter(Boolean),isAnalysisEnabled:!0,isNotificationEnabled:!1,isProjectReadonlyEnabled:!1,isReadonlyEnabled:!1,isAnonymousReadonlyEnabled:!1,isSendAnonymousUsageStats:!1,projectId:"none",version:"source"}}var m=function(){var e=this,t=e._self._c;return t("router-view-layout",[e.isLoading?t("div",{staticClass:"box is-marginless"},[t("progress",{staticClass:"progress is-small is-info"})]):t("div",{staticClass:"box is-marginless"},[t("div",{staticClass:"content has-text-centered"},[t("p",{staticClass:"is-italic"},[e._v(e._s(e.error))])])]),t("div",{staticClass:"is-pulled-right mt-05r scale-08"},[t("a",{staticClass:"is-size-7",attrs:{href:"https://meltano.com",target:"_blank"}},[t("span",{staticClass:"is-inline-block has-text-grey"},[e._v("Made with")]),t("Logo",{staticClass:"ml-05r"})],1)])])},f=[],p=s(6486),g=s.n(p),b=s(381),v=s.n(b);const y=(0,p.property)("name"),w=/(password|private|secret|token)/,k=/^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/,C=h();var z={root(e="/"){return C.appUrl?`${C.appUrl}${e}`:e},apiRoot(e="/"){return this.root(`/api/v1${e}`)},apiUrl(e,t=""){const s=[e,t].join("/");return this.apiRoot().concat(s)},docsUrl(e="/",t){return t=t?`#${t}`:"",`https://docs.meltano.com/${e}${t}`},downloadBlobAsFile(e,t){const s=window.URL.createObjectURL(new Blob([e])),r=document.createElement("a");r.href=s,r.setAttribute("download",t),document.body.appendChild(r),r.click(),document.body.removeChild(r)},getIsSubRouteOf(e,t){return 0===t.indexOf(e)},scrollToBottom(e=window){this.scrollToTarget(e,e.scrollHeight)},scrollToTarget(e,t){e.scrollTo({top:t,left:0,behavior:"smooth"})},scrollToTop(e=window){this.scrollToTarget(e,0)},colors:{backgroundColor:["rgba(255, 99, 132, 0.2)","rgba(54, 162, 235, 0.2)","rgba(255, 206, 86, 0.2)","rgba(75, 192, 192, 0.2)","rgba(153, 102, 255, 0.2)","rgba(255, 159, 64, 0.2)"],borderColor:["rgba(255,99,132,1)","rgba(54, 162, 235, 1)","rgba(255, 206, 86, 1)","rgba(75, 192, 192, 1)","rgba(153, 102, 255, 1)","rgba(255, 159, 64, 1)"]},getColor(e){const t=this.colors.backgroundColor.length;return{backgroundColor:this.colors.backgroundColor[e%t],borderColor:this.colors.borderColor[e%t]}},difference(e,t){return e.filter((e=>!t.includes(e))).concat(t.filter((t=>!e.includes(t))))},deepFreeze(e){const t=Object.getOwnPropertyNames(e);for(const s of t){const t=e[s];e[s]=t&&"object"===typeof t?this.deepFreeze(t):t}return Object.freeze(e)},capitalize(e){if(!e)return"";const t=e.toString();return t.charAt(0).toUpperCase()+t.slice(1)},extractFileNameFromPath(e){return e.replace(/^.*[\\/]/,"")},hyphenate(e,t){if(!e)return"";let s=`${t}-`||"";return s+=e.toLowerCase().replace(/\s\s*/g,"-"),s},inferInputType(e){return w.test(e)?"password":"text"},isValidEmail(e){return k.test(e)},jsDashify(e,t){return e&&t?this.hyphenate(t,`js-${e.toLowerCase()}`):""},key(...e){const t=e=>e["name"]||String(e);return e.map(t).join(":")},pretty(e){try{return JSON.stringify(JSON.parse(e),null,2)}catch(t){return e}},requiredConnectorSettingsKeys(e,t){return t&&t.length?g().intersection(...t):e.map(y)},singularize(e){if(!e)return"";let t=e.toString();const s=t[t.length-1];return"s"===s.toLowerCase()&&(t=t.slice(0,-1)),t},snowflakeAccountParser(e){const t="snowflakecomputing.com",s=e.indexOf(t);let r="";if(s>-1){let n=e.slice(0,s+t.length);n.indexOf("http")>-1&&(n=n.slice(n.indexOf("//")+2)),r=n.split(".")[0]}return r},titleCase(e){return e.replace(/\w\S*/g,(e=>e.charAt(0).toUpperCase()+e.substr(1).toLowerCase()))},truncate(e,t=50){return e.length>t?`${e.substring(0,t)}...`:e},underscoreToSpace(e){return e.replace(/_/g," ")},dateIso8601(e){return`${new Date(e).toISOString().split(".")[0]}Z`},dateIso8601Nullable(e){return e?this.dateIso8601(e):null},getFirstOfMonthAsYYYYMMDD(){const e=new Date,t=new Date(e.getFullYear(),e.getMonth(),1);return this.formatDateStringYYYYMMDD(t)},getInputDateMeta(){return{min:"2000-01-01",pattern:"[0-9]{4}-[0-9]{2}-[0-9]{2}",today:this.formatDateStringYYYYMMDD(new Date)}},getIsDateStringInFormatYYYYMMDD(e){const t=/[0-9]{4}-[0-9]{2}-[0-9]{2}/.test(e);return t},getDateFromYYYYMMDDString(e){const t=e.slice(0,10);if(this.getIsDateStringInFormatYYYYMMDD(t)){const[e,s,r]=t.split("-");return new Date(parseInt(e),parseInt(s)-1,parseInt(r))}return null},formatDateStringYYYYMMDD(e){const t=new Date(e),s=new Date(t.getTime()-6e4*t.getTimezoneOffset());return s.toISOString().split("T")[0]},momentFromNow(e){return v()(e).fromNow()},momentFormatlll(e){return v()(e).format("lll")},momentHumanizedDuration(e,t){const s=new(v())(e),r=new(v())(t),n=v().duration(r.diff(s)),o=(e,t)=>e?`${e} ${t} `:"",a=o(n.days(),"days"),l=o(n.hours(),"hours"),i=o(n.minutes(),"min"),c=o(n.seconds(),"sec");return`${a}${l}${i}${c}`},copyToClipboard(e){let t;e.select(),e.setSelectionRange(0,99999);try{t=document.execCommand("copy")}catch(s){t=!1}finally{document.getSelection().removeAllRanges()}return t}},S={generate(e){return o.Z.post(z.apiUrl("embeds","embed"),e)},load(e,t){let s=z.apiUrl("embeds/embed",e);return t&&(s+=`?today=${t}`),o.Z.get(s)}},O=function(){var e=this,t=e._self._c;return t("svg",{attrs:{xmlns:"http://www.w3.org/2000/svg",width:"101.508",height:"53",viewBox:"0 15 327.15 91.82"}},[t("g",{attrs:{id:"meltano-logo-with-text"}},[t("path",{attrs:{d:"M145.56,77.71H138.7V59.8c0-5.08-2.69-7.26-6.06-7.26-3.19,0-6.25,1.15-8,4.05.06.67.12,1.34.12,2V77.71h-6.86V59.08c0-4.6-2.69-6.54-6.06-6.54A9.19,9.19,0,0,0,103.55,57V77.71H96.69V47.46h6.86v3.2l.37.19a12.44,12.44,0,0,1,9.61-4A10.78,10.78,0,0,1,123,51.69a14.59,14.59,0,0,1,11.39-4.84c6.25,0,11.21,4.36,11.21,12.95ZM180.4,60.53v3.63H157.86c.49,5.63,3.74,8.35,10.35,8.47a21.78,21.78,0,0,0,9-1.81L178.5,76a23.3,23.3,0,0,1-10.29,2.36c-10.28,0-17.26-5.93-17.26-15.67,0-8.29,5.81-15.68,15.18-15.8C174.46,46.85,179.85,51.63,180.4,60.53ZM158.17,59.2h15.31c-.31-4.48-3.31-6.66-7.16-6.66C161.91,52.54,159.09,55.26,158.17,59.2ZM197,78.26c-7.11,0-10.9-3.33-10.9-9.68v-35h6.85V68.09c0,2.79,1.84,4.06,4.66,4.24Zm1-30.8h4.71V37.77h6.86v9.69h8.33V52.9h-8.33V67c0,3.57,2,5.09,4.78,5.09a11.75,11.75,0,0,0,4.34-.67l1.23,5.33A15,15,0,0,1,213.59,78c-6.18,0-10.9-3.88-10.9-10.77V52.9H198Zm47.34,2.24.31-.13V47.46h6.86V77.71h-6.86V74.63l-.37-.12a12.47,12.47,0,0,1-9.49,3.81c-8.2,0-14.76-7-14.76-15.73a15.45,15.45,0,0,1,15.37-15.74C240.49,46.85,243.3,48,245.32,49.7ZM245.63,68v-13a13.94,13.94,0,0,0-8.39-2.54c-5.14,0-9.37,4.36-9.37,10.05s4.23,10,9.37,10C240.67,72.63,243.85,71.36,245.63,68Zm14.61-20.57h6.86v3.69l.37.12c2.2-2.6,5.88-4.42,10.72-4.42,6.06,0,11.08,4.3,11.08,12.71V77.71h-6.86V59.8c0-5.08-3-7.26-6.67-7.26a10.13,10.13,0,0,0-8.64,4.12v21h-6.86Zm50.46-.61c9.37,0,16.47,7,16.47,15.74s-7.1,15.73-16.47,15.73-16.42-7-16.42-15.73S301.39,46.85,310.7,46.85Zm0,25.78c5.45,0,9.61-4.36,9.61-10s-4.16-10.05-9.61-10.05-9.56,4.42-9.56,10.05S305.31,72.63,310.7,72.63Z",fill:"#464acb","fill-rule":"evenodd"}}),t("path",{attrs:{d:"M126,18.14c-6.73,9.06-21.22,11.1-22.85,5.7s6.79-9.14,11.22-9.67C88.73,7.23,93.38,25.71,79.2,27.5c7.84,3.85,16,10.25,21.49,11C110.13,39.89,123.35,34.71,126,18.14Z",fill:"#464acb","fill-rule":"evenodd"}}),t("path",{attrs:{d:"M62.41,23.79A38.1,38.1,0,0,1,58,21.15a4.58,4.58,0,0,1-1.76-5.27,8.63,8.63,0,0,1,.6-1.23c.22.2,1.59,3.1,7.45,5.8,2,.94,9.43,4.53,9.69,4.59,2.69.61,7.07-2.27,5.86-4.5-.86-1.27-4.69-5.44-5.14-7.8-.36-1.92-.31-4.92-4.44-8.69C66.34.44,57.85-.59,51.89.3,53.6,1.82,56.51,4.55,53.72,6a28.9,28.9,0,0,0-4.63,2.73c-4.58,3.72-5,11.7.38,16.49,4.14,3.65,9.14,9,3.17,15.23-4.1,4.27-14,2.12-20.2-4.22-6.86-7-7.56-20.29-.89-30.62l.91-1.43a8.55,8.55,0,0,0-1,.2c-1.58.58-3.19,1.09-4.72,1.79A45.32,45.32,0,0,0,4.93,26.6C2.58,31-6.11,51.19,7.34,71.49c.35-6.57,2.35-13,4.7-16.37,2.53-3.59,7.93-6.77,13,0C28.3,59.46,29,66,33.13,66s5-6.63,7.84-10.88c4.59-7,10.83-4.25,13.07-.63a23.55,23.55,0,0,1,2.76,17C53.79,86.21,26.92,86,18,83c0,0,9.39,8.63,27,8.82,6.28.07,27.12-2.48,35.31-24.81C90,40.62,66.48,26.05,62.41,23.79Zm-1.6-16.2C64.92,3.18,71,9.1,70.73,16.25c-5.34-5.6-7.89-6.11-12.13-4.42C58.51,10.56,60.21,8.22,60.81,7.59Z",fill:"#464acb","fill-rule":"evenodd"}})])])},D=[],M={name:"Logo"},x=M,Y=(0,u.Z)(x,O,D,!1,null,null,null),Z=Y.exports,T=function(){var e=this,t=e._self._c;return t("div",{staticClass:"columns is-gapless"},[t("section",{staticClass:"column is-full"},[t("div",{staticClass:"box-transparent box is-radiusless is-shadowless"},[e._t("default")],2)])])},_=[],$={name:"RouterViewLayout"},A=$,V=(0,u.Z)(A,T,_,!1,null,"2ca706dc",null),L=V.exports,I={name:"ResourceEmbed",components:{Logo:Z,RouterViewLayout:L},props:{token:{type:String,default:null},today:{type:String,default:null}},data(){return{error:null,isLoading:!0,resource:null,resourceType:null}},created(){this.initialize()},methods:{initialize(){S.load(this.token,this.today).then((e=>{this.resource=e.data.resource,this.resourceType=e.data.resourceType})).catch((e=>{this.error=e.response.data.code})).finally((()=>this.isLoading=!1))}}},E=I,F=(0,u.Z)(E,m,f,!1,null,null,null),U=F.exports;const R=new r.ZP({mode:"history",routes:[{path:"/-/embed/:token",name:"resource-embed",component:U,meta:{title:"Meltano Resource Embed"},props:e=>({...e.params,today:e.query.today})}]});var N=R;n["default"].use(r.ZP),o.Z.defaults.headers.common["X-JSON-SCHEME"]="camel",n["default"].prototype.$flask=h(),new n["default"]({el:"#app",router:N,render:e=>e(j)})},6700:function(e,t,s){var r={"./af":2786,"./af.js":2786,"./ar":867,"./ar-dz":4130,"./ar-dz.js":4130,"./ar-kw":6135,"./ar-kw.js":6135,"./ar-ly":6440,"./ar-ly.js":6440,"./ar-ma":7702,"./ar-ma.js":7702,"./ar-sa":6040,"./ar-sa.js":6040,"./ar-tn":7100,"./ar-tn.js":7100,"./ar.js":867,"./az":1083,"./az.js":1083,"./be":9808,"./be.js":9808,"./bg":8338,"./bg.js":8338,"./bm":7438,"./bm.js":7438,"./bn":8905,"./bn-bd":6225,"./bn-bd.js":6225,"./bn.js":8905,"./bo":1560,"./bo.js":1560,"./br":1278,"./br.js":1278,"./bs":622,"./bs.js":622,"./ca":2468,"./ca.js":2468,"./cs":5822,"./cs.js":5822,"./cv":877,"./cv.js":877,"./cy":7373,"./cy.js":7373,"./da":4780,"./da.js":4780,"./de":9740,"./de-at":217,"./de-at.js":217,"./de-ch":894,"./de-ch.js":894,"./de.js":9740,"./dv":5300,"./dv.js":5300,"./el":837,"./el.js":837,"./en-au":8348,"./en-au.js":8348,"./en-ca":7925,"./en-ca.js":7925,"./en-gb":2243,"./en-gb.js":2243,"./en-ie":6436,"./en-ie.js":6436,"./en-il":7207,"./en-il.js":7207,"./en-in":4175,"./en-in.js":4175,"./en-nz":6319,"./en-nz.js":6319,"./en-sg":1662,"./en-sg.js":1662,"./eo":2915,"./eo.js":2915,"./es":5655,"./es-do":5251,"./es-do.js":5251,"./es-mx":6112,"./es-mx.js":6112,"./es-us":1146,"./es-us.js":1146,"./es.js":5655,"./et":5603,"./et.js":5603,"./eu":7763,"./eu.js":7763,"./fa":6959,"./fa.js":6959,"./fi":1897,"./fi.js":1897,"./fil":2549,"./fil.js":2549,"./fo":4694,"./fo.js":4694,"./fr":4470,"./fr-ca":3049,"./fr-ca.js":3049,"./fr-ch":2330,"./fr-ch.js":2330,"./fr.js":4470,"./fy":5044,"./fy.js":5044,"./ga":9295,"./ga.js":9295,"./gd":2101,"./gd.js":2101,"./gl":8794,"./gl.js":8794,"./gom-deva":7884,"./gom-deva.js":7884,"./gom-latn":3168,"./gom-latn.js":3168,"./gu":5349,"./gu.js":5349,"./he":4206,"./he.js":4206,"./hi":94,"./hi.js":94,"./hr":316,"./hr.js":316,"./hu":2138,"./hu.js":2138,"./hy-am":1423,"./hy-am.js":1423,"./id":9218,"./id.js":9218,"./is":135,"./is.js":135,"./it":626,"./it-ch":150,"./it-ch.js":150,"./it.js":626,"./ja":9183,"./ja.js":9183,"./jv":4286,"./jv.js":4286,"./ka":2105,"./ka.js":2105,"./kk":7772,"./kk.js":7772,"./km":8758,"./km.js":8758,"./kn":9282,"./kn.js":9282,"./ko":3730,"./ko.js":3730,"./ku":1408,"./ku.js":1408,"./ky":3291,"./ky.js":3291,"./lb":6841,"./lb.js":6841,"./lo":5466,"./lo.js":5466,"./lt":7010,"./lt.js":7010,"./lv":7595,"./lv.js":7595,"./me":9861,"./me.js":9861,"./mi":5493,"./mi.js":5493,"./mk":5966,"./mk.js":5966,"./ml":7341,"./ml.js":7341,"./mn":5115,"./mn.js":5115,"./mr":370,"./mr.js":370,"./ms":9847,"./ms-my":1237,"./ms-my.js":1237,"./ms.js":9847,"./mt":2126,"./mt.js":2126,"./my":6165,"./my.js":6165,"./nb":4924,"./nb.js":4924,"./ne":6744,"./ne.js":6744,"./nl":3901,"./nl-be":9814,"./nl-be.js":9814,"./nl.js":3901,"./nn":3877,"./nn.js":3877,"./oc-lnc":2135,"./oc-lnc.js":2135,"./pa-in":5858,"./pa-in.js":5858,"./pl":4495,"./pl.js":4495,"./pt":9520,"./pt-br":7971,"./pt-br.js":7971,"./pt.js":9520,"./ro":6459,"./ro.js":6459,"./ru":1793,"./ru.js":1793,"./sd":950,"./sd.js":950,"./se":490,"./se.js":490,"./si":124,"./si.js":124,"./sk":4249,"./sk.js":4249,"./sl":4985,"./sl.js":4985,"./sq":1104,"./sq.js":1104,"./sr":9131,"./sr-cyrl":9915,"./sr-cyrl.js":9915,"./sr.js":9131,"./ss":5893,"./ss.js":5893,"./sv":8760,"./sv.js":8760,"./sw":1172,"./sw.js":1172,"./ta":7333,"./ta.js":7333,"./te":3110,"./te.js":3110,"./tet":2095,"./tet.js":2095,"./tg":7321,"./tg.js":7321,"./th":9041,"./th.js":9041,"./tk":9005,"./tk.js":9005,"./tl-ph":5768,"./tl-ph.js":5768,"./tlh":9444,"./tlh.js":9444,"./tr":2397,"./tr.js":2397,"./tzl":8254,"./tzl.js":8254,"./tzm":1106,"./tzm-latn":699,"./tzm-latn.js":699,"./tzm.js":1106,"./ug-cn":9288,"./ug-cn.js":9288,"./uk":7691,"./uk.js":7691,"./ur":3795,"./ur.js":3795,"./uz":6791,"./uz-latn":588,"./uz-latn.js":588,"./uz.js":6791,"./vi":5666,"./vi.js":5666,"./x-pseudo":4378,"./x-pseudo.js":4378,"./yo":5805,"./yo.js":5805,"./zh-cn":3839,"./zh-cn.js":3839,"./zh-hk":5726,"./zh-hk.js":5726,"./zh-mo":9807,"./zh-mo.js":9807,"./zh-tw":4152,"./zh-tw.js":4152};function n(e){var t=o(e);return s(t)}function o(e){if(!s.o(r,e)){var t=new Error("Cannot find module '"+e+"'");throw t.code="MODULE_NOT_FOUND",t}return r[e]}n.keys=function(){return Object.keys(r)},n.resolve=o,e.exports=n,n.id=6700}},t={};function s(r){var n=t[r];if(void 0!==n)return n.exports;var o=t[r]={id:r,loaded:!1,exports:{}};return e[r].call(o.exports,o,o.exports,s),o.loaded=!0,o.exports}s.m=e,function(){var e=[];s.O=function(t,r,n,o){if(!r){var a=1/0;for(u=0;u<e.length;u++){r=e[u][0],n=e[u][1],o=e[u][2];for(var l=!0,i=0;i<r.length;i++)(!1&o||a>=o)&&Object.keys(s.O).every((function(e){return s.O[e](r[i])}))?r.splice(i--,1):(l=!1,o<a&&(a=o));if(l){e.splice(u--,1);var c=n();void 0!==c&&(t=c)}}return t}o=o||0;for(var u=e.length;u>0&&e[u-1][2]>o;u--)e[u]=e[u-1];e[u]=[r,n,o]}}(),function(){s.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return s.d(t,{a:t}),t}}(),function(){s.d=function(e,t){for(var r in t)s.o(t,r)&&!s.o(e,r)&&Object.defineProperty(e,r,{enumerable:!0,get:t[r]})}}(),function(){s.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"===typeof window)return window}}()}(),function(){s.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)}}(),function(){s.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})}}(),function(){s.nmd=function(e){return e.paths=[],e.children||(e.children=[]),e}}(),function(){s.j=991}(),function(){var e={991:0};s.O.j=function(t){return 0===e[t]};var t=function(t,r){var n,o,a=r[0],l=r[1],i=r[2],c=0;if(a.some((function(t){return 0!==e[t]}))){for(n in l)s.o(l,n)&&(s.m[n]=l[n]);if(i)var u=i(s)}for(t&&t(r);c<a.length;c++)o=a[c],s.o(e,o)&&e[o]&&e[o][0](),e[o]=0;return s.O(u)},r=self["webpackChunkmeltano_webapp"]=self["webpackChunkmeltano_webapp"]||[];r.forEach(t.bind(null,0)),r.push=t.bind(null,r.push.bind(r))}();var r=s.O(void 0,[998],(function(){return s(3171)}));r=s.O(r)})();
//# sourceMappingURL=embed.16bd9254.js.map