<script setup>
  import { useAuthStore } from '@/utils/store';
  import { useRouter } from 'vue-router';
  // const authStore = useAuthStore();
</script>

<template>
  <div class="main">
    <v-btn class="btn font-weight-bold"
      prepend-icon="mdi-account-plus-outline"
      stacked
      to="/menu/matricular/"
    >
      Matricular
    </v-btn>

    <v-btn class="btn font-weight-bold"
      prepend-icon="mdi-account-plus-outline"
      stacked
      to="/menu/matricular/"
    >
      Cadastrar Responsável
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
      to="/menu/area-administrativa/"
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