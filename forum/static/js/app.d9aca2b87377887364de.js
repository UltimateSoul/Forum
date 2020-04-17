webpackJsonp([16],{"7vQG":function(t,e){},"7zck":function(t,e){},"9M+g":function(t,e){},Jmt5:function(t,e){},NHnr:function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var a=n("7+uW"),i=n("mtWM"),o=n.n(i),r=n("Dd8w"),s=n.n(r),u=n("NYxO"),c=n("sHmK"),l={name:"Sidebar",components:{Reveal:c.Reveal},methods:{loginClick:function(){this.isLogged?(this.$router.push({name:"login"}),this.$store.commit("logout")):this.$router.push({name:"login"})},profileClick:function(){var t=this.$store.getters.getUserData;this.$router.push({name:"user-profile",params:{id:t.userID}})}},computed:s()({},Object(u.b)(["isLogged"]),Object(u.c)(["logout"]),{logText:function(){return this.isLogged?"Logout":"Login"}})},d={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[n("Reveal",[n("router-link",{attrs:{to:"/"}},[n("span",[t._v(" Home ")])]),t._v(" "),n("a",{on:{click:t.loginClick}},[n("span",[t._v(" "+t._s(t.logText)+" ")])]),t._v(" "),n("router-link",{attrs:{to:"/shop"}},[n("span",[t._v(" Shop ")])]),t._v(" "),n("router-link",{attrs:{to:"/get-started"}},[n("span",[t._v(" Get Started ")])]),t._v(" "),t.isLogged?n("router-link",{attrs:{to:"/sections"}},[n("span",[t._v(" Sections ")])]):t._e(),t._v(" "),t.isLogged?n("router-link",{attrs:{to:"/teams"}},[n("span",[t._v(" Teams ")])]):t._e(),t._v(" "),t.isLogged?n("a",{on:{click:t.profileClick}},[n("span",[t._v(" Profile ")])]):t._e()],1)],1)},staticRenderFns:[]};var p={name:"App",data:function(){return{notifications:[]}},created:function(){var t=sessionStorage.getItem("auth_token");Boolean(t)?(this.$store.commit("setAuthToken"),this.$store.dispatch("fetchUser")):this.$router.push({name:"login"}),this.$store.getters.isLogged&&setInterval(this.getNotifications,3e4)},methods:{getNotifications:function(){var t=this;o.a.get("http://0.0.0.0:5000/core/notifications-list/").then(function(e){switch(e.status){case 200:t.notifications=e.data}})},deleteNotification:function(t){var e=this;o.a.delete("http://0.0.0.0:5000/core/delete-notification/"+t+"/").then(function(t){switch(t.status){case 204:e.getNotifications()}})},getNotificationType:function(t){switch(t){case 1:return"success";case 2:return"info";case 3:return"warning";case 4:return"error"}}},components:{sidebar:n("VU/8")(l,d,!1,function(t){n("a0PA")},"data-v-8a26c25a",null).exports}},h={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("v-app",[n("div",{attrs:{id:"app"}},[n("sidebar"),t._v(" "),n("main",{attrs:{id:"page-wrap"}},[n("div",{staticClass:"container-fluid"},[n("div",{staticClass:"page-container"},[t._l(t.notifications,function(e){return t.notifications.length?n("div",{staticClass:"clickable",on:{click:function(n){return t.deleteNotification(e.id)}}},[n("v-alert",{key:e.id,attrs:{type:t.getNotificationType(e.notification_type)}},[t._v("\n              "+t._s(e.message)+"\n            ")])],1):t._e()}),t._v(" "),n("transition",{attrs:{name:"slide",mode:"out-in"}},[n("router-view")],1)],2)])])],1)])},staticRenderFns:[]};var m=n("VU/8")(p,h,!1,function(t){n("7vQG")},null,null).exports,f=n("Tqaz"),g=(n("Jmt5"),n("9M+g"),n("/ocq")),v={name:"Home",data:function(){return{fields:["avatar","title","description","posts_quantity"],show:!1,popularTopics:[],loading:!1}},created:function(){this.isLogged||this.$router.push({name:"login"}),this.getPopularTopics()},methods:{getDaysHere:function(){var t=Date.now();return Math.round(Math.abs((t-this.user.dateJoined)/864e5))},getPopularTopics:function(){var t=this;this.loading=!0,o.a.get("http://0.0.0.0:5000/core/get-popular-topics/").then(function(e){switch(e.status){case 200:t.popularTopics=e.data,t.loading=!1;break;default:t.loading=!1}})},profileClick:function(){this.$router.push({name:"user-profile",params:{id:this.user.userID}})},clickTopic:function(t){this.$router.push({name:"topic",params:{section:t.section,topicID:t.id}})}},computed:s()({},Object(u.b)({isLogged:"isLogged",user:"getUserData"})),filters:{getDateFormat:function(t){return new Date(t).toLocaleDateString()}}},_={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[n("div",{staticClass:"center-card"},[n("b-card",{staticClass:"overflow-hidden special-card",staticStyle:{"max-width":"540px"},attrs:{"no-body":""}},[n("b-row",{attrs:{"no-gutters":""}},[n("b-col",{attrs:{md:"6"}},[n("b-card-img",{staticClass:"rounded-0",attrs:{src:t.user.avatar?t.user.avatar:"http://0.0.0.0:5000/static/images/default.jpg",alt:"Image"}})],1),t._v(" "),n("b-col",{attrs:{md:"6"}},[n("b-card-body",{attrs:{title:t.user.username}},[t._v("\n              You are with us for "+t._s(t.getDaysHere())+" days.\n            ")])],1)],1)],1)],1),t._v(" "),n("b-row",{staticClass:"button-control"},[n("b-col",[n("router-link",{attrs:{to:"/get-started"}},[n("b-button",{attrs:{variant:"dark"}},[t._v("Get Started")])],1)],1),t._v(" "),n("b-col",[n("b-button",{attrs:{variant:"dark"},on:{click:t.profileClick}},[t._v("Profile")])],1)],1),t._v(" "),t.popularTopics.length?n("div",[n("h1",[t._v("\n        The most popular topics:\n      ")]),t._v(" "),n("b-table",{staticClass:"clicable",attrs:{striped:"",hover:"",items:t.popularTopics,fields:t.fields},on:{"row-clicked":t.clickTopic},scopedSlots:t._u([{key:"cell(avatar)",fn:function(t){return[n("img",{attrs:{src:t.item.author.avatar?t.item.author.avatar:"http://0.0.0.0:5000/static/images/default.jpg",height:"100",width:"100"}})]}},{key:"cell(created_at)",fn:function(e){return[t._v("\n          "+t._s(t._f("getDateFormat")(e.item.created_at))+"\n        ")]}}],null,!1,3961643236)})],1):t._e()],1)},staticRenderFns:[]};var b=n("VU/8")(v,_,!1,function(t){n("XSaP")},"data-v-3b0d2fc9",null).exports;a.default.use(g.a);var k=new g.a({scrollBehavior:function(t,e,n){return n||(t.hash?{selector:t.hash}:{x:0,y:0})},routes:[{path:"",name:"home",component:b},{path:"/login",name:"login",component:function(t){n.e(7).then(function(){t(n("95qr"))}.bind(null,n)).catch(n.oe)}},{path:"/conversation/:section",name:"conversation",component:function(t){n.e(10).then(function(){t(n("EAzr"))}.bind(null,n)).catch(n.oe)}},{path:"/conversation/:section/topic/:topicID",name:"topic",component:function(t){n.e(2).then(function(){t(n("AuW7"))}.bind(null,n)).catch(n.oe)}},{path:"/topic-creation/:section",name:"topic-creation",component:function(t){Promise.all([n.e(0),n.e(9)]).then(function(){t(n("SmpO"))}.bind(null,n)).catch(n.oe)}},{path:"/topic-editing/:section/:topicID",name:"topic-editing",component:function(t){Promise.all([n.e(0),n.e(8)]).then(function(){t(n("ipG8"))}.bind(null,n)).catch(n.oe)}},{path:"/shop",name:"shop",component:function(t){n.e(14).then(function(){t(n("KCKD"))}.bind(null,n)).catch(n.oe)}},{path:"/teams",name:"teams",component:function(t){n.e(4).then(function(){t(n("cU/W"))}.bind(null,n)).catch(n.oe)}},{path:"/teams/:teamID",name:"team",component:function(t){n.e(5).then(function(){t(n("+2Fi"))}.bind(null,n)).catch(n.oe)}},{path:"/edit-team/:teamID",name:"edit-team",component:function(t){n.e(13).then(function(){t(n("to62"))}.bind(null,n)).catch(n.oe)}},{path:"/create-team",name:"create-team",component:function(t){Promise.all([n.e(0),n.e(3)]).then(function(){t(n("vDDD"))}.bind(null,n)).catch(n.oe)}},{path:"/get-started",name:"get-started",component:function(t){n.e(11).then(function(){t(n("SYbK"))}.bind(null,n)).catch(n.oe)}},{path:"/user-profile/:id",name:"user-profile",component:function(t){Promise.all([n.e(0),n.e(6)]).then(function(){t(n("ec7E"))}.bind(null,n)).catch(n.oe)}},{path:"/sections",name:"sections",component:function(t){n.e(1).then(function(){t(n("MN7i"))}.bind(null,n)).catch(n.oe)}},{path:"/registration",name:"registration",component:function(t){Promise.all([n.e(0),n.e(12)]).then(function(){t(n("mm3c"))}.bind(null,n)).catch(n.oe)}}],mode:"history"}),T=n("Rf8U"),y=n.n(T),x={state:{user:{isLogged:!1,userID:null,username:"",email:"",coins:0,avatarImage:"",gameNickName:"",gender:"",date_joined:null,isModerator:!1,isAdmin:!1,hasTeam:!1,isTeamOwner:!1,teamID:null}},getters:{isLogged:function(t){return t.user.isLogged},getUserData:function(t){var e=t.user;return{userID:e.userID,username:e.username,dateJoined:e.dateJoined,email:e.email,coins:e.coins,avatar:e.avatarImage,gameNickName:e.gameNickName,gender:e.gender,hasTeam:e.hasTeam,teamID:e.teamID,isTeamOwner:e.isTeamOwner}},isMainUser:function(t){return function(e){return t.user.userID===e}}},actions:{login:function(t,e){return o.a.post("http://0.0.0.0:5000/authentication/api-token-auth/",e).then(function(e){sessionStorage.setItem("auth_token",e.data.token),t.commit("setAuthToken"),t.dispatch("fetchUser")})},fetchUser:function(t){var e=t.commit;return o.a.get("/users/get-user/").then(function(t){var n=t.data;e("setUserData",n)}).catch(function(t){console.log(t)})},register:function(t,e){return o.a.post("http://0.0.0.0:5000/authentication/register/",e).then(function(e){var n=e.data.auth_token;sessionStorage.setItem("auth_token",n),t.commit("setAuthToken"),t.dispatch("fetchUser")})}},mutations:{setAuthToken:function(t){t.user.isLogged=Boolean(sessionStorage.getItem("auth_token")),o.a.defaults.headers.post.Authorization="Token "+sessionStorage.getItem("auth_token"),o.a.defaults.headers.get.Authorization="Token "+sessionStorage.getItem("auth_token"),o.a.defaults.headers.delete.Authorization="Token "+sessionStorage.getItem("auth_token"),o.a.defaults.headers.patch.Authorization="Token "+sessionStorage.getItem("auth_token")},setUserData:function(t,e){t.user.userID=e.pk,t.user.username=e.username,t.user.email=e.email,t.user.avatarImage=e.avatar,t.user.gender=e.gender,t.user.gameNickName=e.game_nickname,t.user.dateJoined=new Date(e.date_joined),t.user.hasTeam=e.has_team,t.user.teamID=e.team_id,t.user.isTeamOwner=e.is_team_owner},logout:function(t){sessionStorage.removeItem("auth_token"),t.user.isLogged=!1}}},w={state:{id:null,totalMembers:0,owner:{avatar:"",username:"",gameNickname:"",pk:null},members:[],name:"",description:"",baseInfo:"",avatar:"",createdDate:""},getters:{isHasTeam:function(t,e,n){return n.authentication.user.hasTeam},isTeamOwner:function(t,e,n){return function(t){return n.authentication.user.isTeamOwner&&n.authentication.user.teamID===+t}},getTeam:function(t){return t},getTeamDescription:function(t){return t.description},getTeamAvatar:function(t){return t.avatar},getTeamName:function(t){return t.name}},actions:{getTeamData:function(t,e){var n=t.commit;t.state;return o.a.get("teams/"+e+"/").then(function(t){switch(t.status){case 200:n("setTeamData",t.data)}})}},mutations:{setTeamData:function(t,e){t.id=e.id,t.totalMembers=e.total_members,t.owner.avatar=e.owner.avatar,t.owner.username=e.owner.username,t.owner.gameNickname=e.owner.game_nickname,t.owner.pk=e.owner.pk,t.members=e.members,t.name=e.name,t.description=e.description,t.baseInfo=e.base_info,t.avatar=e.avatar,t.createdDate=e.created_at}}};a.default.use(y.a,o.a),a.default.use(u.a);var D=new u.a.Store({state:{},getters:{},actions:{},mutations:{},modules:{authentication:x,team:w}}),S=n("ESwS"),I=n.n(S),$=n("TX8X"),C=n.n($),V=n("rifk"),L=n.n(V),N={name:"VueBootstrapTypeaheadListItem",props:{data:{},htmlText:{type:String},backgroundVariant:{type:String},textVariant:{type:String}},data:function(){return{active:!1}},computed:{textClasses:function(){var t="";return t+=this.active?"active":"",t+=this.backgroundVariant?" bg-"+this.backgroundVariant:"","vbst-item list-group-item list-group-item-action "+(t+=this.textVariant?" text-"+this.textVariant:"")}}},A={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("a",{class:t.textClasses,attrs:{tabindex:"0",href:"#"},on:{mouseover:function(e){t.active=!0},mouseout:function(e){t.active=!1}}},[t._t("suggestion",[n("span",{domProps:{innerHTML:t._s(t.htmlText)}})],null,{data:t.data,htmlText:t.htmlText})],2)},staticRenderFns:[]};function z(t){return t.replace(/</g,"&lt;").replace(/>/g,"&gt;")}var M={name:"VueBootstrapTypeaheadList",components:{VueBootstrapTypeaheadListItem:n("VU/8")(N,A,!1,null,null,null).exports},props:{data:{type:Array,required:!0,validator:function(t){return t instanceof Array}},query:{type:String,default:""},backgroundVariant:{type:String},textVariant:{type:String},maxMatches:{type:Number,default:10},minMatchingChars:{type:Number,default:2}},computed:{highlight:function(){var t=this;return function(e){if(e=z(e),0===t.query.length)return e;var n=new RegExp(t.escapedQuery,"gi");return e.replace(n,"<strong>$&</strong>")}},escapedQuery:function(){return z(this.query).replace(/[.*+?^${}()|[\]\\]/g,"\\$&")},matchedItems:function(){if(0===this.query.length||this.query.length<this.minMatchingChars)return[];var t=new RegExp(this.escapedQuery,"gi");return this.data.filter(function(e){return null!==e.text.match(t)}).sort(function(e,n){var a=e.text.indexOf(e.text.match(t)[0]),i=n.text.indexOf(n.text.match(t)[0]);return a<i?-1:a>i?1:0}).slice(0,this.maxMatches)}},methods:{handleHit:function(t,e){this.$emit("hit",t),e.preventDefault()}}},U={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"list-group shadow"},t._l(t.matchedItems,function(e,a){return n("vue-bootstrap-typeahead-list-item",{key:a,attrs:{data:e.data,"html-text":t.highlight(e.text),"background-variant":t.backgroundVariant,"text-variant":t.textVariant},nativeOn:{click:function(n){return t.handleHit(e,n)}},scopedSlots:t._u([{key:"suggestion",fn:function(e){var n=e.data,a=e.htmlText;return t.$scopedSlots.suggestion?[t._t("suggestion",null,null,{data:n,htmlText:a})]:void 0}}],null,!0)})}),1)},staticRenderFns:[]},F=n("VU/8")(M,U,!1,null,null,null).exports,O=n("z+gd"),P={name:"VueBootstrapTypehead",components:{VueBootstrapTypeaheadList:F},props:{size:{type:String,default:null,validator:function(t){return["lg","sm"].indexOf(t)>-1}},value:{type:String},data:{type:Array,required:!0,validator:function(t){return t instanceof Array}},serializer:{type:Function,default:function(t){return t},validator:function(t){return t instanceof Function}},backgroundVariant:String,textVariant:String,inputClass:{type:String,default:""},maxMatches:{type:Number,default:10},minMatchingChars:{type:Number,default:2},placeholder:String,prepend:String,append:String},computed:{sizeClasses:function(){return this.size?"input-group input-group-"+this.size:"input-group"},formattedData:function(){var t=this;return this.data instanceof Array?this.data.map(function(e,n){return{id:n,data:e,text:t.serializer(e)}}):[]}},methods:{resizeList:function(t){var e=t.getBoundingClientRect(),n=this.$refs.list.$el.style;if(n.width=e.width+"px",this.$refs.prependDiv){var a=this.$refs.prependDiv.getBoundingClientRect();n.marginLeft=a.width+"px"}},handleHit:function(t){void 0!==this.value&&this.$emit("input",t.text),this.inputValue=t.text,this.$emit("hit",t.data),this.$refs.input.blur(),this.isFocused=!1},handleBlur:function(t){var e=t.relatedTarget;e&&e.classList.contains("vbst-item")||(this.isFocused=!1)},handleInput:function(t){this.inputValue=t,void 0!==this.value&&this.$emit("input",t)}},data:function(){return{isFocused:!1,inputValue:""}},mounted:function(){var t=this;this.$_ro=new O.a(function(e){t.resizeList(t.$refs.input)}),this.$_ro.observe(this.$refs.input),this.$_ro.observe(this.$refs.list.$el)},beforeDestroy:function(){this.$_ro.disconnect()}},R={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[n("div",{class:t.sizeClasses},[t.$slots.prepend||t.prepend?n("div",{ref:"prependDiv",staticClass:"input-group-prepend"},[t._t("prepend",[n("span",{staticClass:"input-group-text"},[t._v(t._s(t.prepend))])])],2):t._e(),t._v(" "),n("input",{ref:"input",class:"form-control "+t.inputClass,attrs:{type:"search",placeholder:t.placeholder,"aria-label":t.placeholder,autocomplete:"off"},domProps:{value:t.inputValue},on:{focus:function(e){t.isFocused=!0},blur:t.handleBlur,input:function(e){return t.handleInput(e.target.value)}}}),t._v(" "),t.$slots.append||t.append?n("div",{staticClass:"input-group-append"},[t._t("append",[n("span",{staticClass:"input-group-text"},[t._v(t._s(t.append))])])],2):t._e()]),t._v(" "),n("vue-bootstrap-typeahead-list",{directives:[{name:"show",rawName:"v-show",value:t.isFocused&&t.data.length>0,expression:"isFocused && data.length > 0"}],ref:"list",staticClass:"vbt-autcomplete-list",attrs:{query:t.inputValue,data:t.formattedData,"background-variant":t.backgroundVariant,"text-variant":t.textVariant,maxMatches:t.maxMatches,minMatchingChars:t.minMatchingChars},on:{hit:t.handleHit},scopedSlots:t._u([t._l(t.$scopedSlots,function(e,n){return{key:n,fn:function(e){var a=e.data,i=e.htmlText;return[t._t(n,null,null,{data:a,htmlText:i})]}}})],null,!0)})],1)},staticRenderFns:[]};var H=n("VU/8")(P,R,!1,function(t){n("eh44")},"data-v-a0e87de4",null).exports,q=n("3EgV"),B=n.n(q);n("7zck");a.default.use(B.a);var E=new B.a({}),j=n("6J2T"),J=n.n(j);a.default.use(J.a),a.default.use(L.a),a.default.use(C.a),a.default.use(I.a),a.default.use(f.a),a.default.component("vue-bootstrap-typeahead",H),a.default.config.productionTip=!1,o.a.defaults.baseURL="http://0.0.0.0:5000/api/",sessionStorage.getItem("auth_token")&&(o.a.defaults.headers.post.Authorization="Token "+sessionStorage.getItem("auth_token"),o.a.defaults.headers.get.Authorization="Token "+sessionStorage.getItem("auth_token"),o.a.defaults.headers.delete.Authorization="Token "+sessionStorage.getItem("auth_token"),o.a.defaults.headers.patch.Authorization="Token "+sessionStorage.getItem("auth_token")),new a.default({el:"#app",router:k,store:D,vuetify:E,components:{App:m},template:"<App/>"})},XSaP:function(t,e){},a0PA:function(t,e){},eh44:function(t,e){}},["NHnr"]);
//# sourceMappingURL=app.d9aca2b87377887364de.js.map