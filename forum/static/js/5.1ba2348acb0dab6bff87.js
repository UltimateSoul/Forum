webpackJsonp([5],{"4CgW":function(t,e){},EAzr:function(t,e,s){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var a=s("7+uW"),i=s("mtWM"),n=s.n(i),o=s("Rf8U"),c=s.n(o);a.default.use(c.a,n.a);var r={name:"Conversation",data:function(){return{loading:!1,topics:[],testQuantity:2,section:this.$route.params.section}},created:function(){this.loading=!0,this.getData()},methods:{getData:function(){var t=this;n.a.get("topics/by-section/",{params:{section:this.section.toUpperCase()}}).then(function(e){t.topics=e.data}).finally(function(){t.loading=!1})},createTopic:function(){this.$router.push({name:"topic-creation"})},moveToTopic:function(t){this.$router.push({name:"topic",params:{section:this.section,topicID:t}})}},filters:{getDateFormat:function(t){return new Date(t).toLocaleDateString()}}},l={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",[s("div",{staticClass:"row"},[t._m(0),t._v(" "),s("div",{staticClass:"col-lg-4"},[t.$store.getters.isLogged?s("button",{staticClass:"btn btn-dark",on:{click:t.createTopic}},[t._v("\n        Create Topic\n      ")]):t._e()])]),t._v(" "),s("div",{staticClass:"row"},[s("div",{staticClass:"col-lg-12 col-md-10 col-xs-5"},[t.loading?t._e():s("table",{staticClass:"table"},[t._m(1),t._v(" "),s("transition-group",{tag:"tbody",attrs:{name:"slide"}},t._l(t.topics,function(e,a){return s("tr",{key:a,staticClass:"clickable",on:{click:function(s){return t.moveToTopic(e.id)}}},[s("th",[t._v("\n              "+t._s(e.title)+"\n          ")]),t._v(" "),s("td",[t._v(t._s(e.posts_quantity))]),t._v(" "),s("td",[t._v(t._s(e.author.username))]),t._v(" "),s("td",[t._v(t._s(t._f("getDateFormat")(e.created_date)))])])}),0)],1)])])])},staticRenderFns:[function(){var t=this.$createElement,e=this._self._c||t;return e("div",{staticClass:"col-lg-8"},[e("h1",[this._v("Conversation")])])},function(){var t=this.$createElement,e=this._self._c||t;return e("thead",[e("tr",[e("th",{attrs:{scope:"col"}},[this._v("Topic")]),this._v(" "),e("th",{attrs:{scope:"col"}},[this._v("Responses")]),this._v(" "),e("th",{attrs:{scope:"col"}},[this._v("Author")]),this._v(" "),e("th",{attrs:{scope:"col"}},[this._v("Created Date")])])])}]};var u=s("VU/8")(r,l,!1,function(t){s("4CgW")},"data-v-a8eab0ca",null);e.default=u.exports}});
//# sourceMappingURL=5.1ba2348acb0dab6bff87.js.map