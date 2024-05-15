import {createRouter, createWebHistory} from 'vue-router';

const Login = () => import('../pages/Login.vue');
const Menu = () => import('../pages/Menu.vue');
const Inicio = () => import('../pages/Inicio.vue');
const Matricular = () => import('../pages/Matricular.vue');
const AreaAdministrativa = () => import('../pages/AreaAdministrativa.vue');

const routes = [
  { 
    path: '/', 
    name: 'login', 
    component: Login,
  },
  { 
    path: '/menu', 
    name: 'menu', 
    component: Menu,
    children: [
      { 
        path: 'inicio', 
        name: 'inicio', 
        component: Inicio,
      },
      { 
        path: 'matricular', 
        name: 'matricular', 
        component: Matricular,
      },
      { 
        path: 'area-administrativa', 
        name: 'area-administrativa', 
        component: AreaAdministrativa,
      },
    ]
  },
];

const router = createRouter({
    routes,
    history: createWebHistory(import.meta.env.BASE_URL),
});

export default router;