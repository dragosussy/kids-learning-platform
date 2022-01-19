import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

import Vue from 'vue'
import VueRouter from 'vue-router'

import App from './App.vue'
import Home from './pages/Home.vue'
import Login from './pages/Login.vue'
import AdminLogin from './pages/AdminLogin.vue'
import AdminView from './pages/AdminView.vue'
import VueCookies from 'vue-cookies'
import VueApexCharts from 'vue-apexcharts'
import VueMoment from "vue-moment"

//import Compress from 'compress.js'
//window.compressor = new Compress();

Vue.use(VueRouter);
Vue.use(VueCookies);
Vue.use(VueApexCharts);
Vue.use(VueMoment);

Vue.component('apexchart', VueApexCharts);

const routes = [
  { path: '/', component: Login },
  { path: '/login', component: Login },
  { path: '/home', component: Home },
  { path: '/adminLogin', component: AdminLogin },
  { path: '/admin', component: AdminView }
];
const router = new VueRouter({
  routes: routes,
  mode: 'history'
});

new Vue({
  router,
  el: '#app',
  components:{
    App
  },
  render: h => h(App),
});