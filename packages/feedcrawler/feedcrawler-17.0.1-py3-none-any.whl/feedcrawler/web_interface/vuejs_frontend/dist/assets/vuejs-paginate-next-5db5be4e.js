import{R as s,D as i,F as l,L as k,W as r,K as g,M as P,Q as x,S as b,l as y,N as C}from"./@vue-15490d82.js";var L=(d,n)=>{const e=d.__vccOpts||d;for(const[f,u]of n)e[f]=u;return e};const v={data(){return{innerValue:1}},props:{modelValue:{type:Number},pageCount:{type:Number,required:!0},initialPage:{type:Number,default:1},forcePage:{type:Number},clickHandler:{type:Function,default:()=>{}},pageRange:{type:Number,default:3},marginPages:{type:Number,default:1},prevText:{type:String,default:"Prev"},nextText:{type:String,default:"Next"},breakViewText:{type:String,default:"…"},containerClass:{type:String,default:"pagination"},pageClass:{type:String,default:"page-item"},pageLinkClass:{type:String,default:"page-link"},prevClass:{type:String,default:"page-item"},prevLinkClass:{type:String,default:"page-link"},nextClass:{type:String,default:"page-item"},nextLinkClass:{type:String,default:"page-link"},breakViewClass:{type:String},breakViewLinkClass:{type:String},activeClass:{type:String,default:"active"},disabledClass:{type:String,default:"disabled"},noLiSurround:{type:Boolean,default:!1},firstLastButton:{type:Boolean,default:!1},firstButtonText:{type:String,default:"First"},lastButtonText:{type:String,default:"Last"},hidePrevNext:{type:Boolean,default:!1}},computed:{selected:{get:function(){return this.modelValue||this.innerValue},set:function(d){this.innerValue=d}},pages:function(){let d={};if(this.pageCount<=this.pageRange)for(let n=0;n<this.pageCount;n++){let e={index:n,content:n+1,selected:n===this.selected-1};d[n]=e}else{const n=Math.floor(this.pageRange/2);let e=t=>{let c={index:t,content:t+1,selected:t===this.selected-1};d[t]=c},f=t=>{let c={disabled:!0,breakView:!0};d[t]=c};for(let t=0;t<this.marginPages;t++)e(t);let u=0;this.selected-n>0&&(u=this.selected-1-n);let a=u+this.pageRange-1;a>=this.pageCount&&(a=this.pageCount-1,u=a-this.pageRange+1);for(let t=u;t<=a&&t<=this.pageCount-1;t++)e(t);u>this.marginPages&&f(u-1),a+1<this.pageCount-this.marginPages&&f(a+1);for(let t=this.pageCount-1;t>=this.pageCount-this.marginPages;t--)e(t)}return d}},methods:{handlePageSelected(d){this.selected!==d&&(this.innerValue=d,this.$emit("update:modelValue",d),this.clickHandler(d))},prevPage(){this.selected<=1||this.handlePageSelected(this.selected-1)},nextPage(){this.selected>=this.pageCount||this.handlePageSelected(this.selected+1)},firstPageSelected(){return this.selected===1},lastPageSelected(){return this.selected===this.pageCount||this.pageCount===0},selectFirstPage(){this.selected<=1||this.handlePageSelected(1)},selectLastPage(){this.selected>=this.pageCount||this.handlePageSelected(this.pageCount)}},beforeMount(){this.innerValue=this.initialPage},beforeUpdate(){this.forcePage!==void 0&&this.forcePage!==this.selected&&(this.selected=this.forcePage)}},h=["tabindex","innerHTML"],S=["tabindex","innerHTML"],T=["onClick","onKeyup"],m=["tabindex","innerHTML"],V=["tabindex","innerHTML"],H=["innerHTML"],M=["innerHTML"],w=["onClick","onKeyup"],B=["innerHTML"],N=["innerHTML"];function K(d,n,e,f,u,a){return e.noLiSurround?(s(),i("div",{key:1,class:l(e.containerClass)},[e.firstLastButton?(s(),i("a",{key:0,onClick:n[8]||(n[8]=t=>a.selectFirstPage()),onKeyup:n[9]||(n[9]=r(t=>a.selectFirstPage(),["enter"])),class:l([e.pageLinkClass,a.firstPageSelected()?e.disabledClass:""]),tabindex:"0",innerHTML:e.firstButtonText},null,42,H)):g("",!0),a.firstPageSelected()&&e.hidePrevNext?g("",!0):(s(),i("a",{key:1,onClick:n[10]||(n[10]=t=>a.prevPage()),onKeyup:n[11]||(n[11]=r(t=>a.prevPage(),["enter"])),class:l([e.prevLinkClass,a.firstPageSelected()?e.disabledClass:""]),tabindex:"0",innerHTML:e.prevText},null,42,M)),(s(!0),i(P,null,x(a.pages,t=>(s(),i(P,null,[t.breakView?(s(),i("a",{key:t.index,class:l([e.pageLinkClass,e.breakViewLinkClass,t.disabled?e.disabledClass:""]),tabindex:"0"},[b(d.$slots,"breakViewContent",{},()=>[y(C(e.breakViewText),1)])],2)):t.disabled?(s(),i("a",{key:t.index,class:l([e.pageLinkClass,t.selected?e.activeClass:"",e.disabledClass]),tabindex:"0"},C(t.content),3)):(s(),i("a",{key:t.index,onClick:c=>a.handlePageSelected(t.index+1),onKeyup:r(c=>a.handlePageSelected(t.index+1),["enter"]),class:l([e.pageLinkClass,t.selected?e.activeClass:""]),tabindex:"0"},C(t.content),43,w))],64))),256)),a.lastPageSelected()&&e.hidePrevNext?g("",!0):(s(),i("a",{key:2,onClick:n[12]||(n[12]=t=>a.nextPage()),onKeyup:n[13]||(n[13]=r(t=>a.nextPage(),["enter"])),class:l([e.nextLinkClass,a.lastPageSelected()?e.disabledClass:""]),tabindex:"0",innerHTML:e.nextText},null,42,B)),e.firstLastButton?(s(),i("a",{key:3,onClick:n[14]||(n[14]=t=>a.selectLastPage()),onKeyup:n[15]||(n[15]=r(t=>a.selectLastPage(),["enter"])),class:l([e.pageLinkClass,a.lastPageSelected()?e.disabledClass:""]),tabindex:"0",innerHTML:e.lastButtonText},null,42,N)):g("",!0)],2)):(s(),i("ul",{key:0,class:l(e.containerClass)},[e.firstLastButton?(s(),i("li",{key:0,class:l([e.pageClass,a.firstPageSelected()?e.disabledClass:""])},[k("a",{onClick:n[0]||(n[0]=t=>a.selectFirstPage()),onKeyup:n[1]||(n[1]=r(t=>a.selectFirstPage(),["enter"])),class:l(e.pageLinkClass),tabindex:a.firstPageSelected()?-1:0,innerHTML:e.firstButtonText},null,42,h)],2)):g("",!0),a.firstPageSelected()&&e.hidePrevNext?g("",!0):(s(),i("li",{key:1,class:l([e.prevClass,a.firstPageSelected()?e.disabledClass:""])},[k("a",{onClick:n[2]||(n[2]=t=>a.prevPage()),onKeyup:n[3]||(n[3]=r(t=>a.prevPage(),["enter"])),class:l(e.prevLinkClass),tabindex:a.firstPageSelected()?-1:0,innerHTML:e.prevText},null,42,S)],2)),(s(!0),i(P,null,x(a.pages,t=>(s(),i("li",{key:t.index,class:l([e.pageClass,t.selected?e.activeClass:"",t.disabled?e.disabledClass:"",t.breakView?e.breakViewClass:""])},[t.breakView?(s(),i("a",{key:0,class:l([e.pageLinkClass,e.breakViewLinkClass]),tabindex:"0"},[b(d.$slots,"breakViewContent",{},()=>[y(C(e.breakViewText),1)])],2)):t.disabled?(s(),i("a",{key:1,class:l(e.pageLinkClass),tabindex:"0"},C(t.content),3)):(s(),i("a",{key:2,onClick:c=>a.handlePageSelected(t.index+1),onKeyup:r(c=>a.handlePageSelected(t.index+1),["enter"]),class:l(e.pageLinkClass),tabindex:"0"},C(t.content),43,T))],2))),128)),a.lastPageSelected()&&e.hidePrevNext?g("",!0):(s(),i("li",{key:2,class:l([e.nextClass,a.lastPageSelected()?e.disabledClass:""])},[k("a",{onClick:n[4]||(n[4]=t=>a.nextPage()),onKeyup:n[5]||(n[5]=r(t=>a.nextPage(),["enter"])),class:l(e.nextLinkClass),tabindex:a.lastPageSelected()?-1:0,innerHTML:e.nextText},null,42,m)],2)),e.firstLastButton?(s(),i("li",{key:3,class:l([e.pageClass,a.lastPageSelected()?e.disabledClass:""])},[k("a",{onClick:n[6]||(n[6]=t=>a.selectLastPage()),onKeyup:n[7]||(n[7]=r(t=>a.selectLastPage(),["enter"])),class:l(e.pageLinkClass),tabindex:a.lastPageSelected()?-1:0,innerHTML:e.lastButtonText},null,42,V)],2)):g("",!0)],2))}var F=L(v,[["render",K]]);export{F as P};
