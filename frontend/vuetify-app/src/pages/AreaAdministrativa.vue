<script setup>
</script>

<template>
  <div class="main">
    <v-btn class="btn font-weight-bold"
      prepend-icon="mdi-account-plus-outline"
      stacked
      to="/menu/area-administrativa/cadastrar-usuario/"
    >
      Cadastrar Usuário 
    </v-btn>

    <v-btn class="btn font-weight-bold"
      prepend-icon="mdi-plus-box-outline"
      stacked
      to="/menu/area-administrativa/cadastrar-turma/"
    >
      Cadastrar Turma
    </v-btn>

    <v-btn class="btn font-weight-bold"
      prepend-icon="mdi-account-group"
      stacked
    >
      Listar Alunos
    </v-btn>

    <v-btn class="btn font-weight-bold"
      prepend-icon="mdi-list-box-outline"
      stacked
    >
      Listar Turmas
    </v-btn>

    <v-btn class="btn font-weight-bold"
      prepend-icon="mdi-account-multiple"
      stacked
    >
      Listar Usuários
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