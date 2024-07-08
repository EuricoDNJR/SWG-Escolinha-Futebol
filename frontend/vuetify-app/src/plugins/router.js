import {createRouter, createWebHistory} from 'vue-router';


const Login = () => import('../pages/Login.vue');
const Menu = () => import('../pages/Menu.vue');
const Inicio = () => import('../pages/Inicio.vue');
const Matricular = () => import('../pages/Matricular.vue');
const CadastrarResponsavel = () => import('../pages/CadastrarResponsavel.vue');
const AreaAdministrativa = () => import('../pages/AreaAdministrativa.vue');
const CadastrarUsuario = () => import('../pages/CadastrarUsuario.vue');
const CadastrarTurma = () => import('../pages/CadastrarTurma.vue');
const Pagamentos = () => import('../pages/Pagamentos.vue'); 
const RegistrarPagamento = () => import('../pages/RegistrarPagamento.vue'); 

const routes = [
  { 
    path: '/', 
    redirect: { name: 'login' },
  },
  { 
    path: '/login', 
    name: 'login', 
    component: Login,
    meta: { requiresAuth: false },
  },
  { 
    path: '/menu', 
    name: 'menu', 
    component: Menu,
    meta: { requiresAuth: true },
    children: [
      { 
        path: 'inicio', 
        name: 'inicio', 
        component: Inicio,
        meta: { requiresAuth: true },
      },
      { 
        path: 'matricular', 
        name: 'matricular', 
        component: Matricular,
        meta: { requiresAuth: true },
      },
      { 
        path: 'cadastrar-responsavel', 
        name: 'cadastrar-responsavel', 
        component: CadastrarResponsavel,
        meta: { requiresAuth: true },
      },
      { 
        path: 'area-administrativa', 
        name: 'area-administrativa', 
        component: AreaAdministrativa,
        meta: { requiresAuth: true },
      },
      { 
        path: 'area-administrativa/cadastrar-usuario', 
        name: 'cadastrar-usuario', 
        component: CadastrarUsuario,
        meta: { requiresAuth: true },
      },
      { 
        path: 'area-administrativa/cadastrar-turma', 
        name: 'cadastrar-turma', 
        component: CadastrarTurma,
      },
      { 
        path: 'pagamentos', 
        name: 'pagamentos', 
        component: Pagamentos,
      },
      { 
        path: 'pagamentos/registrar-pagamento', 
        name: 'registrar-pagamento', 
        component: RegistrarPagamento,
      },
    ]
  },
];

const router = createRouter({
    routes,
    history: createWebHistory(import.meta.env.BASE_URL),
});

export default router;