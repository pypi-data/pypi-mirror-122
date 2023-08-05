/*! For license information please see 16.dbf8f30e.chunk.js.LICENSE.txt */
(this["webpackJsonpstreamlit-browser"]=this["webpackJsonpstreamlit-browser"]||[]).push([[16],{2755:function(e,t,n){var r;!function(){"use strict";var o={not_string:/[^s]/,not_bool:/[^t]/,not_type:/[^T]/,not_primitive:/[^v]/,number:/[diefg]/,numeric_arg:/[bcdiefguxX]/,json:/[j]/,not_json:/[^j]/,text:/^[^\x25]+/,modulo:/^\x25{2}/,placeholder:/^\x25(?:([1-9]\d*)\$|\(([^)]+)\))?(\+)?(0|'[^$])?(-)?(\d+)?(?:\.(\d+))?([b-gijostTuvxX])/,key:/^([a-z_][a-z_\d]*)/i,key_access:/^\.([a-z_][a-z_\d]*)/i,index_access:/^\[(\d+)\]/,sign:/^[+-]/};function i(e){return s(u(e),arguments)}function a(e,t){return i.apply(null,[e].concat(t||[]))}function s(e,t){var n,r,a,s,c,u,l,p,f,d=1,m=e.length,b="";for(r=0;r<m;r++)if("string"===typeof e[r])b+=e[r];else if("object"===typeof e[r]){if((s=e[r]).keys)for(n=t[d],a=0;a<s.keys.length;a++){if(void 0==n)throw new Error(i('[sprintf] Cannot access property "%s" of undefined value "%s"',s.keys[a],s.keys[a-1]));n=n[s.keys[a]]}else n=s.param_no?t[s.param_no]:t[d++];if(o.not_type.test(s.type)&&o.not_primitive.test(s.type)&&n instanceof Function&&(n=n()),o.numeric_arg.test(s.type)&&"number"!==typeof n&&isNaN(n))throw new TypeError(i("[sprintf] expecting number but found %T",n));switch(o.number.test(s.type)&&(p=n>=0),s.type){case"b":n=parseInt(n,10).toString(2);break;case"c":n=String.fromCharCode(parseInt(n,10));break;case"d":case"i":n=parseInt(n,10);break;case"j":n=JSON.stringify(n,null,s.width?parseInt(s.width):0);break;case"e":n=s.precision?parseFloat(n).toExponential(s.precision):parseFloat(n).toExponential();break;case"f":n=s.precision?parseFloat(n).toFixed(s.precision):parseFloat(n);break;case"g":n=s.precision?String(Number(n.toPrecision(s.precision))):parseFloat(n);break;case"o":n=(parseInt(n,10)>>>0).toString(8);break;case"s":n=String(n),n=s.precision?n.substring(0,s.precision):n;break;case"t":n=String(!!n),n=s.precision?n.substring(0,s.precision):n;break;case"T":n=Object.prototype.toString.call(n).slice(8,-1).toLowerCase(),n=s.precision?n.substring(0,s.precision):n;break;case"u":n=parseInt(n,10)>>>0;break;case"v":n=n.valueOf(),n=s.precision?n.substring(0,s.precision):n;break;case"x":n=(parseInt(n,10)>>>0).toString(16);break;case"X":n=(parseInt(n,10)>>>0).toString(16).toUpperCase()}o.json.test(s.type)?b+=n:(!o.number.test(s.type)||p&&!s.sign?f="":(f=p?"+":"-",n=n.toString().replace(o.sign,"")),u=s.pad_char?"0"===s.pad_char?"0":s.pad_char.charAt(1):" ",l=s.width-(f+n).length,c=s.width&&l>0?u.repeat(l):"",b+=s.align?f+n+c:"0"===u?f+c+n:c+f+n)}return b}var c=Object.create(null);function u(e){if(c[e])return c[e];for(var t,n=e,r=[],i=0;n;){if(null!==(t=o.text.exec(n)))r.push(t[0]);else if(null!==(t=o.modulo.exec(n)))r.push("%");else{if(null===(t=o.placeholder.exec(n)))throw new SyntaxError("[sprintf] unexpected placeholder");if(t[2]){i|=1;var a=[],s=t[2],u=[];if(null===(u=o.key.exec(s)))throw new SyntaxError("[sprintf] failed to parse named argument key");for(a.push(u[1]);""!==(s=s.substring(u[0].length));)if(null!==(u=o.key_access.exec(s)))a.push(u[1]);else{if(null===(u=o.index_access.exec(s)))throw new SyntaxError("[sprintf] failed to parse named argument key");a.push(u[1])}t[2]=a}else i|=2;if(3===i)throw new Error("[sprintf] mixing positional and named placeholders is not (yet) supported");r.push({placeholder:t[0],param_no:t[1],keys:t[2],sign:t[3],pad_char:t[4],align:t[5],width:t[6],precision:t[7],type:t[8]})}n=n.substring(t[0].length)}return c[e]=r}t.sprintf=i,t.vsprintf=a,"undefined"!==typeof window&&(window.sprintf=i,window.vsprintf=a,void 0===(r=function(){return{sprintf:i,vsprintf:a}}.call(t,n,t,e))||(e.exports=r))}()},2787:function(e,t,n){"use strict";n(0);var r,o=n(43),i=n(137),a=n(11),s=n(189),c=n(13),u=n.n(c),l=n(92),p=Object(l.keyframes)(r||(r=Object(s.a)(["\n  50% {\n    color: rgba(0, 0, 0, 0);\n  }\n"]))),f=u()("span",{target:"e1m4n6jn0"})((function(e){var t=e.includeDot,n=e.shouldBlink,r=e.theme;return Object(a.a)(Object(a.a)({},t?{"&::before":{opacity:1,content:'"\u2022"',animation:"none",color:r.colors.gray,margin:"0 5px"}}:{}),n?{color:r.colors.red,animationName:"".concat(p),animationDuration:"0.5s",animationIterationCount:5}:{})}),""),d=n(5);t.a=function(e){var t=e.dirty,n=e.value,r=e.maxLength,a=e.className,s=e.type,c=[],u=function(e){var t=arguments.length>1&&void 0!==arguments[1]&&arguments[1];c.push(Object(d.jsx)(f,{includeDot:c.length>0,shouldBlink:t,children:e},c.length))};return t&&("multiline"===(void 0===s?"single":s)?Object(o.f)()?u("Press \u2318+Enter to apply"):u("Press Ctrl+Enter to apply"):u("Press Enter to apply")),r&&u("".concat(n.length,"/").concat(r),t&&n.length>=r),Object(d.jsx)(i.a,{className:a,children:c})}},2917:function(e,t,n){"use strict";var r=n(0),o=n(18),i=n(2833),a=n(2923),s=n(2747),c=n(90);function u(e){return(u="function"===typeof Symbol&&"symbol"===typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"===typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function l(){return(l=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e}).apply(this,arguments)}function p(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){if(!(Symbol.iterator in Object(e))&&"[object Arguments]"!==Object.prototype.toString.call(e))return;var n=[],r=!0,o=!1,i=void 0;try{for(var a,s=e[Symbol.iterator]();!(r=(a=s.next()).done)&&(n.push(a.value),!t||n.length!==t);r=!0);}catch(c){o=!0,i=c}finally{try{r||null==s.return||s.return()}finally{if(o)throw i}}return n}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()}function f(e,t){if(null==e)return{};var n,r,o=function(e,t){if(null==e)return{};var n,r,o={},i=Object.keys(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||(o[n]=e[n]);return o}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(o[n]=e[n])}return o}function d(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function m(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function b(e,t){return!t||"object"!==u(t)&&"function"!==typeof t?y(e):t}function h(e){return(h=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}function y(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function g(e,t){return(g=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function v(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}var j=function(e){function t(){var e,n;d(this,t);for(var r=arguments.length,o=new Array(r),i=0;i<r;i++)o[i]=arguments[i];return v(y(n=b(this,(e=h(t)).call.apply(e,[this].concat(o)))),"state",{isFocused:n.props.autoFocus||!1}),v(y(n),"onFocus",(function(e){n.setState({isFocused:!0}),n.props.onFocus(e)})),v(y(n),"onBlur",(function(e){n.setState({isFocused:!1}),n.props.onBlur(e)})),n}var n,u,j;return function(e,t){if("function"!==typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&g(e,t)}(t,e),n=t,(u=[{key:"render",value:function(){var e=this.props,t=e.startEnhancer,n=e.endEnhancer,u=e.overrides,d=u.Root,m=u.StartEnhancer,b=u.EndEnhancer,h=f(u,["Root","StartEnhancer","EndEnhancer"]),y=f(e,["startEnhancer","endEnhancer","overrides"]),g=p(Object(o.c)(d,s.d),2),v=g[0],j=g[1],x=p(Object(o.c)(m,s.c),2),O=x[0],k=x[1],S=p(Object(o.c)(b,s.c),2),E=S[0],_=S[1],V=Object(i.a)(this.props,this.state);return r.createElement(v,l({"data-baseweb":"input"},V,j,{$adjoined:w(t,n),$hasIconTrailing:this.props.clearable||"password"==this.props.type}),t&&r.createElement(O,l({},V,k,{$position:c.c.start}),"function"===typeof t?t(V):t),r.createElement(a.a,l({},y,{overrides:h,adjoined:w(t,n),onFocus:this.onFocus,onBlur:this.onBlur})),n&&r.createElement(E,l({},V,_,{$position:c.c.end}),"function"===typeof n?n(V):n))}}])&&m(n.prototype,u),j&&m(n,j),t}(r.Component);function w(e,t){return e&&t?c.a.both:e?c.a.left:t?c.a.right:c.a.none}v(j,"defaultProps",{autoComplete:"on",autoFocus:!1,disabled:!1,name:"",error:!1,onBlur:function(){},onFocus:function(){},overrides:{},required:!1,size:c.d.default,startEnhancer:null,endEnhancer:null,clearable:!1,type:"text"}),t.a=j},3859:function(e,t,n){"use strict";n.r(t),n.d(t,"default",(function(){return _}));var r=n(6),o=n(9),i=n(7),a=n(8),s=n(0),c=n.n(s),u=n(85),l=n(2755),p=n(234),f=n(21),d=n(20),m=n(138),b=n(70),h=n(71),y=n(2917),g=n(2787),v=n(137),j=n(13),w=n.n(j);var x=w()("div",{target:"e1jwn65y0"})((function(e){return{display:"flex",flexDirection:"row",flexWrap:"nowrap",alignItems:"center",input:{MozAppearance:"textfield","&::-webkit-inner-spin-button, &::-webkit-outer-spin-button":{WebkitAppearance:"none",margin:e.theme.spacing.none}}}}),""),O=w()("div",{target:"e1jwn65y1"})({name:"fjj0yo",styles:"height:49px;display:flex;flex-direction:row;"}),k=w()("button",{target:"e1jwn65y2"})((function(e){var t=e.theme;return{margin:t.spacing.none,border:"none",height:t.sizes.full,display:"flex",alignItems:"center",width:"".concat(45,"px"),justifyContent:"center",color:t.colors.bodyText,transition:"color 300ms, backgroundColor 300ms",backgroundColor:t.colors.secondaryBg,"&:hover:enabled, &:focus:enabled":{color:t.colors.white,backgroundColor:t.colors.primary,transition:"none",outline:"none"},"&:active":{outline:"none",border:"none"},"&:last-of-type":{borderTopRightRadius:t.radii.md,borderBottomRightRadius:t.radii.md}}}),""),S=w()("div",{target:"e1jwn65y3"})((function(e){return{position:"absolute",marginRight:e.theme.spacing.twoXS,left:0,right:"".concat(90,"px")}}),""),E=n(5);var _=function(e){Object(i.a)(n,e);var t=Object(a.a)(n);function n(e){var o;return Object(r.a)(this,n),(o=t.call(this,e)).formClearHelper=new p.b,o.inputRef=c.a.createRef(),o.formatValue=function(e){var t=function(e){return null==e||""===e?void 0:e}(o.props.element.format);if(null==t)return e.toString();try{return Object(l.sprintf)(t,e)}catch(n){return Object(f.d)("Error in sprintf(".concat(t,", ").concat(e,"): ").concat(n)),String(e)}},o.isIntData=function(){return o.props.element.dataType===d.n.DataType.INT},o.getMin=function(){return o.props.element.hasMin?o.props.element.min:-1/0},o.getMax=function(){return o.props.element.hasMax?o.props.element.max:1/0},o.getStep=function(){var e=o.props.element.step;return e||(o.isIntData()?1:.01)},o.commitWidgetValue=function(e){var t=o.state.value,n=o.props,r=n.element,i=n.widgetMgr,a=o.props.element,s=o.getMin(),c=o.getMax();if(s>t||t>c){var u=o.inputRef.current;u&&u.reportValidity()}else{var l=t||0===t?t:a.default;o.isIntData()?i.setIntValue(r,l,e):i.setDoubleValue(r,l,e),o.setState({dirty:!1,value:l,formattedValue:o.formatValue(l)})}},o.onFormCleared=function(){o.setState({value:o.props.element.default},(function(){return o.commitWidgetValue({fromUi:!0})}))},o.onBlur=function(){o.state.dirty&&o.commitWidgetValue({fromUi:!0})},o.onChange=function(e){var t,n=e.target.value;t=o.isIntData()?parseInt(n,10):parseFloat(n),o.setState({dirty:!0,value:t,formattedValue:n})},o.onKeyDown=function(e){switch(e.key){case"ArrowUp":e.preventDefault(),o.modifyValueUsingStep("increment")();break;case"ArrowDown":e.preventDefault(),o.modifyValueUsingStep("decrement")()}},o.onKeyPress=function(e){"Enter"===e.key&&o.state.dirty&&o.commitWidgetValue({fromUi:!0})},o.modifyValueUsingStep=function(e){return function(){var t=o.state.value,n=o.getStep();switch(e){case"increment":o.canIncrement&&o.setState({dirty:!0,value:t+n},(function(){o.commitWidgetValue({fromUi:!0})}));break;case"decrement":o.canDecrement&&o.setState({dirty:!0,value:t-n},(function(){o.commitWidgetValue({fromUi:!0})}))}}},o.render=function(){var e=o.props,t=e.element,n=e.width,r=e.disabled,i=e.widgetMgr,a=o.state,s=a.formattedValue,c=a.dirty,l={width:n};return o.formClearHelper.manageFormClearListener(i,t.formId,o.onFormCleared),Object(E.jsxs)("div",{className:"stNumberInput",style:l,children:[Object(E.jsx)(v.d,{label:t.label,children:t.help&&Object(E.jsx)(v.b,{children:Object(E.jsx)(m.a,{content:t.help,placement:b.b.TOP_RIGHT})})}),Object(E.jsxs)(x,{children:[Object(E.jsx)(y.a,{type:"number",inputRef:o.inputRef,value:s,onBlur:o.onBlur,onChange:o.onChange,onKeyPress:o.onKeyPress,onKeyDown:o.onKeyDown,disabled:r,overrides:{Input:{props:{step:o.getStep(),min:o.getMin(),max:o.getMax()}},InputContainer:{style:function(){return{borderTopRightRadius:0,borderBottomRightRadius:0}}},Root:{style:function(){return{borderTopRightRadius:0,borderBottomRightRadius:0}}}}}),Object(E.jsxs)(O,{children:[Object(E.jsx)(k,{className:"step-down",onClick:o.modifyValueUsingStep("decrement"),disabled:!o.canDecrement,children:Object(E.jsx)(h.a,{content:u.Minus,size:"xs",color:o.canDecrement?"inherit":"disabled"})}),Object(E.jsx)(k,{className:"step-up",onClick:o.modifyValueUsingStep("increment"),disabled:!o.canIncrement,children:Object(E.jsx)(h.a,{content:u.Plus,size:"xs",color:o.canIncrement?"inherit":"disabled"})})]})]}),Object(E.jsx)(S,{children:Object(E.jsx)(g.a,{dirty:c,value:s,className:"input-instructions"})})]})},o.state={dirty:!1,value:o.initialValue,formattedValue:o.formatValue(o.initialValue)},o}return Object(o.a)(n,[{key:"initialValue",get:function(){var e=this.props.widgetMgr.getIntValue(this.props.element);return void 0!==e?e:this.props.element.default}},{key:"componentDidMount",value:function(){this.props.element.setValue?this.updateFromProtobuf():this.commitWidgetValue({fromUi:!1})}},{key:"componentDidUpdate",value:function(){this.maybeUpdateFromProtobuf()}},{key:"componentWillUnmount",value:function(){this.formClearHelper.disconnect()}},{key:"maybeUpdateFromProtobuf",value:function(){this.props.element.setValue&&this.updateFromProtobuf()}},{key:"updateFromProtobuf",value:function(){var e=this,t=this.props.element.value;this.props.element.setValue=!1,this.setState({value:t,formattedValue:this.formatValue(t)},(function(){e.commitWidgetValue({fromUi:!1})}))}},{key:"canDecrement",get:function(){return this.state.value-this.getStep()>=this.getMin()}},{key:"canIncrement",get:function(){return this.state.value+this.getStep()<=this.getMax()}}]),n}(c.a.PureComponent)}}]);