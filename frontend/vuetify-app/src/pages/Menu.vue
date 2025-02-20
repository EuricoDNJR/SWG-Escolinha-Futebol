<script setup>
  import { useAuthStore } from '@/utils/store';
  import { useRouter } from 'vue-router';

  const router = useRouter();

  const authStore = useAuthStore();

  async function logout() {
    authStore.reset();

    router.push('/');
  }
</script>

<template>
  <div>
    <v-app-bar :elevation="2"  color="grey-darken-4" class="app-bar">
      <template v-slot:prepend>
        <img src="@/assets/logo-farp.svg" alt="logo farp" class="logo-farp">
      </template>

      <template v-slot:append>
        <v-btn
          variant="flat"
          type="submit"
          color="red-darken-4"
          block
          prepend-icon="mdi-logout"
          @click="logout"
        >
          Sair
        </v-btn>
      </template>
    </v-app-bar>
  </div>

  <div class="router-view">
    <router-view/>
  </div>
</template>

<style>
.logo-farp{
  height: 90%;
}

.router-view{
  height: 100%;
}
</style>