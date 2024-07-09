/**
 * plugins/index.js
 *
 * Automatically included in `./src/main.js`
 */

// Plugins
import vuetify from './vuetify'
import pinia from './pinia'
import router from './router'
import { useAuthStore } from '../utils/store';



export function registerPlugins (app) {
  app
    .use(vuetify)
    .use(pinia);

  const authStore = useAuthStore();
  
  router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth) && !authStore.getToken) {
      next('/login');
    } else {
      next();
    }
  });

  app.use(router);
}
