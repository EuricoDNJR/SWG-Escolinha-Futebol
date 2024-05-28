import {createRouter, createWebHistory} from 'vue-router';

const Login = () => import('../pages/Login.vue');
const Menu = () => import('../pages/Menu.vue');
const Inicio = () => import('../pages/Inicio.vue');
const Matricular = () => import('../pages/Matricular.vue');
const CadastrarResponsavel = () => import('../pages/CadastrarResponsavel.vue');
const AreaAdministrativa = () => import('../pages/AreaAdministrativa.vue');
const CadastrarUsuario = () => import('../pages/CadastrarUsuario.vue');

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
        path: 'cadastrar-responsavel', 
        name: 'cadastrar-responsavel', 
        component: CadastrarResponsavel,
      },
      { 
        path: 'area-administrativa', 
        name: 'area-administrativa', 
        component: AreaAdministrativa,
      },
      { 
        path: 'area-administrativa/cadastrar-usuario', 
        name: 'cadastrar-usuario', 
        component: CadastrarUsuario,
      },
    ]
  },
];

const router = createRouter({
    routes,
    history: createWebHistory(import.meta.env.BASE_URL),
});

export default router;