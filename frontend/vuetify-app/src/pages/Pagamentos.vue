<script setup>
</script>

<template>
  <div class="main">
    <v-btn class="btn font-weight-bold"
      prepend-icon="mdi-account-plus-outline"
      stacked
      to="/menu/pagamentos/registrar-pagamento/"
    >
      Registrar Pagamento
    </v-btn>

    <v-btn class="btn font-weight-bold"
      prepend-icon="mdi-plus-box-outline"
      stacked
    >
      Listar Pagamentos
    </v-btn>

    <v-btn class="btn font-weight-bold"
      prepend-icon="mdi-keyboard-return"
      stacked
      to="/menu/inicio/"
      color="grey-lighten-2"
    >
      Voltar
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