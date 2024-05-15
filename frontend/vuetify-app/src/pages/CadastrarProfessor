<script setup>
  import { ref, reactive } from 'vue';
  import { fetchPost, createCelula } from '../utils/common'
  import { useAuthStore } from '../utils/store';
  import { useRouter } from 'vue-router';
  import PageForm from '../components/PageForm.vue'
  
  const router = useRouter();
  const authStore = useAuthStore();

  const customBtns = ref([
    {text: 'Voltar', variant: 'text', icon: undefined, color: undefined, clickEvent: 'voltar', needFormData: false, loading: false},
    {text: 'Matricular', variant: 'flat', icon: 'mdi-account-plus', color: 'blue-darken-1', clickEvent: 'matricular', needFormData: true, loading: false},
  ]);
  const eventFunctions = {
    voltar: () => router.push('/menu/inicio/'),
    matricular: (body) => {
      emit('cadastrarPessoa', body);
    },
  };

  function btnClicked({event, body}){
    const func = eventFunctions[event];

    if(body){
        func(body);
    }else{
        func();
    }   
  }
  
</script>

<template>
  <PageForm 
    title="Matricular Aluno"
    :configs="[
      [createCelula({key:'nome', title:'Nome', required:true}), createCelula({key:'senha', title:'Senha', required:true})],
      [createCelula({key:'telefone', title:'Telefone', required:true}), createCelula({key:'email', title:'Email', required:true})],
      [createCelula({key:'dataNascimento', title:'Data de Nascimento', type: 'date', required:true}), createCelula({key:'cpf', title:'CPF', required:true})],
      [createCelula({key:'endereco', title:'Endereço', required:true}), createCelula({key:'cargo', title:'Cargo', type: 'select', required:true, initialValue: ''})]
    ]"
    :fixies="[
      ['Cargo.items', cargos],
      ['Cargo.itemsTitle', 'nome'],
      ['Cargo.itemsValue', 'nome'],
    ]"
    :customBtns="customBtns"
    @clicked="btnClicked"
  />
</template>

<style lang="css">
</style>
