/*! For license information please see 25.3131b986.chunk.js.LICENSE.txt */
(this["webpackJsonpstreamlit-browser"]=this["webpackJsonpstreamlit-browser"]||[]).push([[25],{3853:function(e,t,a){"use strict";a.r(t),a.d(t,"default",(function(){return T}));var n=a(11),r=a(22),i=a(10),s=a.n(i),o=a(14),c=a(6),h=a(9),u=a(7),l=a(8),d=a(0),g=a(39),f=a(21),p=a(35),v=a(188),b=a(118),w=a(2924),m=a.n(w),O=a(2838),j=a(13),x=a.n(j)()("div",{target:"everg990"})((function(e){var t=e.theme;return{"&.vega-embed":{".vega-actions":{zIndex:t.zIndices.popupMenu},summary:{height:"auto",zIndex:t.zIndices.menuButton}}}}),""),y=a(5),V="(index)",k="source",z=new Set([b.a.DatetimeIndex,b.a.Float64Index,b.a.Int64Index,b.a.RangeIndex,b.a.UInt64Index]),D=function(e){Object(u.a)(a,e);var t=Object(l.a)(a);function a(){var e;Object(c.a)(this,a);for(var n=arguments.length,r=new Array(n),i=0;i<n;i++)r[i]=arguments[i];return(e=t.call.apply(t,[this].concat(r))).vegaView=void 0,e.vegaFinalizer=void 0,e.defaultDataName=k,e.element=null,e.state={error:void 0},e.finalizeView=function(){e.vegaFinalizer&&e.vegaFinalizer(),e.vegaFinalizer=void 0,e.vegaView=void 0},e.generateSpec=function(){var t=e.props,a=t.element,n=t.theme,r=JSON.parse(a.spec),i=a.useContainerWidth;if(r.config=N(r.config,n),e.props.height?(r.width=e.props.width-38,r.height=e.props.height):i&&(r.width=e.props.width-38),r.padding||(r.padding={}),null==r.padding.bottom&&(r.padding.bottom=20),r.datasets)throw new Error("Datasets should not be passed as part of the spec");return r},e}return Object(h.a)(a,[{key:"componentDidMount",value:function(){var e=Object(o.a)(s.a.mark((function e(){return s.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,this.createView();case 3:e.next=8;break;case 5:e.prev=5,e.t0=e.catch(0),this.setState({error:e.t0});case 8:case"end":return e.stop()}}),e,this,[[0,5]])})));return function(){return e.apply(this,arguments)}}()},{key:"componentWillUnmount",value:function(){this.finalizeView()}},{key:"componentDidUpdate",value:function(){var e=Object(o.a)(s.a.mark((function e(t){var a,n,i,o,c,h,u,l,d,g,p,v,b,w,m,O,j,x,y,V,k;return s.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(a=t.element,n=t.theme,i=this.props,o=i.element,c=i.theme,h=a.spec,u=o.spec,this.vegaView&&h===u&&n===c&&t.width===this.props.width&&t.height===this.props.height){e.next=15;break}return Object(f.c)("Vega spec changed."),e.prev=6,e.next=9,this.createView();case 9:e.next=14;break;case 11:e.prev=11,e.t0=e.catch(6),this.setState({error:e.t0});case 14:return e.abrupt("return");case 15:for(l=a.data,d=o.data,(l||d)&&this.updateData(this.defaultDataName,l,d),g=S(a)||{},p=S(o)||{},v=0,b=Object.entries(p);v<b.length;v++)w=Object(r.a)(b[v],2),m=w[0],O=w[1],j=m||this.defaultDataName,x=g[j],this.updateData(j,x,O);for(y=0,V=Object.keys(g);y<V.length;y++)k=V[y],p.hasOwnProperty(k)||k===this.defaultDataName||this.updateData(k,null,null);this.vegaView.resize().runAsync();case 23:case"end":return e.stop()}}),e,this,[[6,11]])})));return function(t){return e.apply(this,arguments)}}()},{key:"updateData",value:function(e,t,a){if(!this.vegaView)throw new Error("Chart has not been drawn yet");if(a&&0!==a.data.length)if(t&&0!==t.data.length){var n=t.data.length>0?[t.data.length,t.data[0].length]:[0,0],i=Object(r.a)(n,2),s=i[0],o=i[1],c=a.data.length>0?[a.data.length,a.data[0].length]:[0,0],h=Object(r.a)(c,2),u=h[0];if(function(e,t,a,n,r,i){if(a!==i)return!1;if(t>r)return!1;if(0===t)return!1;var s=e.data,o=n.data,c=i-1,h=t-1;if(Object(p.get)(s,[c,0])!==Object(p.get)(o,[c,0])||Object(p.get)(s,[c,h])!==Object(p.get)(o,[c,h]))return!1;return!0}(t,s,o,a,u,h[1]))s<u&&this.vegaView.insert(e,I(a,s));else{var l=O.changeset().remove(O.truthy).insert(I(a));this.vegaView.change(e,l),Object(f.c)("Had to clear the ".concat(e," dataset before inserting data through Vega view."))}}else this.vegaView.insert(e,I(a));else this.vegaView._runtime.data.hasOwnProperty(e)&&this.vegaView.remove(e,O.truthy)}},{key:"createView",value:function(){var e=Object(o.a)(s.a.mark((function e(){var t,a,n,i,o,c,h,u,l,d,g,p,v,b,w,O;return s.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(Object(f.c)("Creating a new Vega view."),this.element){e.next=3;break}throw Error("Element missing.");case 3:return this.finalizeView(),t=this.props.element,a=this.generateSpec(),e.next=8,m()(this.element,a);case 8:if(n=e.sent,i=n.vgSpec,o=n.view,c=n.finalize,this.vegaView=o,this.vegaFinalizer=c,h=C(t),1===(u=h?Object.keys(h):[]).length?(l=Object(r.a)(u,1),d=l[0],this.defaultDataName=d):0===u.length&&i.data&&(this.defaultDataName=k),(g=F(t))&&o.insert(this.defaultDataName,g),h)for(p=0,v=Object.entries(h);p<v.length;p++)b=Object(r.a)(v[p],2),w=b[0],O=b[1],o.insert(w,O);return e.next=22,o.runAsync();case 22:this.vegaView.resize().runAsync();case 23:case"end":return e.stop()}}),e,this)})));return function(){return e.apply(this,arguments)}}()},{key:"render",value:function(){var e=this;if(this.state.error)throw this.state.error;return Object(y.jsx)(x,{"data-testid":"stArrowVegaLiteChart",ref:function(t){e.element=t}})}}]),a}(d.PureComponent);function F(e){var t=e.data;return t&&0!==t.data.length?I(t):null}function C(e){var t=S(e);if(null==t)return null;for(var a={},n=0,i=Object.entries(t);n<i.length;n++){var s=Object(r.a)(i[n],2),o=s[0],c=s[1];a[o]=I(c)}return a}function S(e){var t;if(0===(null===(t=e.datasets)||void 0===t?void 0:t.length))return null;var a={};return e.datasets.forEach((function(e){if(e){var t=e.hasName?e.name:null;a[t]=e.data}})),a}function I(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:0;if(0===e.index.length||0===e.data.length||0===e.columns.length)return[];for(var a=[],n=e.data.length,r=e.data[0].length,i=b.b.getTypeName(e.types.index[0]),s=z.has(i),o=t;o<n;o++){var c={};s&&(c[V]=e.index[o][0]);for(var h=0;h<r;h++)c[e.columns[0][h]]=e.data[o][h];a.push(c)}return a}function N(e,t){var a=t.colors,r=t.fontSizes,i=t.genericFonts,s={labelFont:i.bodyFont,titleFont:i.bodyFont,labelFontSize:r.twoSmPx,titleFontSize:r.twoSmPx},o={background:a.bgColor,axis:Object(n.a)({labelColor:a.bodyText,titleColor:a.bodyText,gridColor:a.fadedText10},s),legend:Object(n.a)({labelColor:a.bodyText,titleColor:a.bodyText},s),title:Object(n.a)({color:a.bodyText,subtitleColor:a.bodyText},s)};return e?Object(p.merge)({},o,e||{}):o}var T=Object(g.withTheme)(Object(v.a)(D))}}]);