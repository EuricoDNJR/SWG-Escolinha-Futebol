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

  <div class="main">
    <v-btn class="btn font-weight-bold"
      prepend-icon="mdi-account-plus-outline"
      stacked
    >
      Matricular
    </v-btn>

    <v-btn class="btn font-weight-bold"
      prepend-icon="mdi-credit-card-outline"
      stacked
    >
      Pagamentos
    </v-btn>

    <v-btn class="btn font-weight-bold"
      prepend-icon="mdi-account-multiple-outline"
      stacked
    >
      Área Administrativa
    </v-btn>

    <v-btn class="btn font-weight-bold"
      prepend-icon="mdi-view-dashboard-outline"
      stacked
    >
      Dashboard
    </v-btn>
  </div>
</template>

<style>


.logo-farp{
  height: 90%;
}

.main{
  display: flex;
  flex-direction: column;
  background-color: #F5F5F5;
  height: 100%;
  padding: 20px;
}

.btn{
  margin-bottom: 10px;
}
</style>