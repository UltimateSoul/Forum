webpackJsonp([7],{"95qr":function(e,t,s){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var a=s("Dd8w"),r=s.n(a),n=s("NYxO"),o={name:"Login",data:function(){return{username:"",password:"",dangerShow:!1}},methods:{loginClick:function(){var e=this,t={username:this.username,password:this.password};this.$store.dispatch("login",t).then(function(){e.isLogged&&e.homePageClick}).catch(function(t){e.dangerShow=!0})},homePageClick:function(){this.$router.push({name:"home"})}},computed:r()({},Object(n.b)(["isLogged"]))},i={render:function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("div",{staticClass:"row login-container"},[s("div",{staticClass:"col-lg-12 col-md-6 col-sm-3 justify-content-center"},[e.dangerShow?s("div",{staticClass:"alert alert-danger",attrs:{role:"alert"}},[e._v("\n      An error occurred during the authentication process. Try again!\n    ")]):e._e(),e._v(" "),e.isLogged?s("div",{staticClass:"alert alert-success",attrs:{role:"alert"}},[e._v("\n      You've successfully logged in!\n    ")]):e._e(),e._v(" "),e.isLogged?e._e():s("form",[s("div",{staticClass:"form-group"},[s("label",{attrs:{for:"exampleInputEmail1"}},[e._v("Username")]),e._v(" "),s("input",{directives:[{name:"model",rawName:"v-model",value:e.username,expression:"username"}],staticClass:"form-control",attrs:{type:"text",id:"exampleInputEmail1","aria-describedby":"emailHelp",placeholder:"Enter Username"},domProps:{value:e.username},on:{input:function(t){t.target.composing||(e.username=t.target.value)}}}),e._v(" "),s("small",{staticClass:"form-text text-muted",attrs:{id:"emailHelp"}},[e._v("We'll never share your password with anyone else.")])]),e._v(" "),s("div",{staticClass:"form-group"},[s("label",{attrs:{for:"exampleInputPassword1"}},[e._v("Password")]),e._v(" "),s("input",{directives:[{name:"model",rawName:"v-model",value:e.password,expression:"password"}],staticClass:"form-control",attrs:{type:"password",id:"exampleInputPassword1",placeholder:"Password"},domProps:{value:e.password},on:{input:function(t){t.target.composing||(e.password=t.target.value)}}})]),e._v(" "),s("button",{staticClass:"btn btn-primary",attrs:{pre:""},on:{click:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"submit",void 0,t.key,void 0)?null:(t.preventDefault(),e.loginClick(t))}}},[e._v("Login")]),e._v(" "),s("router-link",{attrs:{to:{name:"registration"}}},[s("button",{staticClass:"btn btn-primary"},[e._v("\n          Register\n        ")])])],1)])])},staticRenderFns:[]};var l=s("VU/8")(o,i,!1,function(e){s("gKOW")},"data-v-60c2194f",null);t.default=l.exports},gKOW:function(e,t){}});
//# sourceMappingURL=7.7044628ed5d9d00f8add.js.map