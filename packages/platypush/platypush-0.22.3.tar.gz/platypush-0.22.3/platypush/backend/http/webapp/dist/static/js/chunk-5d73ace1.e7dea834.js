(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-5d73ace1"],{"74d4":function(e,t,c){"use strict";c("8a53")},"8a53":function(e,t,c){},"9b92":function(e,t,c){"use strict";c.r(t);c("b0c0");var i=c("7a23"),n=Object(i["K"])("data-v-0fad5251");Object(i["u"])("data-v-0fad5251");var a={class:"camera component-row"},r={class:"feed-container",ref:"container"},s={key:2},b={class:"controls"},o={key:0,class:"fa fa-play"},l={key:1,class:"fa fa-pause"};Object(i["s"])();var d=n((function(e,t,c,n,d,u){return Object(i["r"])(),Object(i["e"])("div",a,[Object(i["h"])("div",r,[d.visible?Object(i["f"])("",!0):(Object(i["r"])(),Object(i["e"])("div",{key:0,class:"no-content",textContent:Object(i["C"])(c.name)},null,8,["textContent"])),d.visible&&"image"===c.type?(Object(i["r"])(),Object(i["e"])("img",{key:1,alt:"Camera feed",src:u.imgUrl},null,8,["src"])):d.visible&&"video"===c.type?(Object(i["r"])(),Object(i["e"])("video",s,[Object(i["h"])("source",{src:c.src},null,8,["src"])])):Object(i["f"])("",!0)],512),Object(i["h"])("div",b,[Object(i["h"])("button",{class:"toggle-btn",onClick:t[1]||(t[1]=function(e){return d.visible=!d.visible})},[d.visible?(Object(i["r"])(),Object(i["e"])("i",l)):(Object(i["r"])(),Object(i["e"])("i",o))])])])})),u=(c("d3b7"),c("25f0"),c("3e54")),f={name:"Camera",mixins:[u["a"]],props:{src:{type:String,required:!0},type:{type:String,default:"image"},name:{type:String}},computed:{imgUrl:function(){if("image"===this.type)return this.src+(this.src.indexOf("?")>0?"&":"?")+"_t="+(new Date).getTime().toString()}},data:function(){return{visible:!1}}};c("74d4");f.render=d,f.__scopeId="data-v-0fad5251";t["default"]=f}}]);
//# sourceMappingURL=chunk-5d73ace1.e7dea834.js.map