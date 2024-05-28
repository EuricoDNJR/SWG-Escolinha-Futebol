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
    {text: 'Cadastrar', variant: 'flat', icon: 'mdi-account-plus', color: 'green-darken-1', clickEvent: 'cadastrar', needFormData: true, loading: false},
  ]);

  const eventFunctions = {
    voltar: () => router.push('/menu/inicio/'),
    cadastrar: (body) => requestCadastrarResponsavel(body),
  };

  const message = reactive({
    text: '',
    type: 'error',
    isVisible: false,
  });

  function printMessage(msg, type){
    message.text = msg;
    message.type = type;
    message.isVisible = true;
  }

  function btnClicked({event, body}){
    const eventFunction = eventFunctions[event];

    if(body){
      eventFunction(body);
    }else{
      eventFunction();
    }   
  }

  async function requestCadastrarResponsavel(body){
    const btn = customBtns.value.find((btn) => btn.clickEvent == "cadastrar");
    btn.loading = true;

    try{
        const url = "http://127.0.0.1:8003/v1/responsible/";
        const token = authStore.getToken;
        
        const response = await fetchPost(url, body, token);
        const responseJson = await response.json();

        if(response.status === 201){       
          printMessage("Cadastro realizado com sucesso", "success");
        }else{
          printMessage("Erro ao realizar cadastro", "warning");
        }
    }catch(e){
        console.log(e);
        printMessage("Falha ao realizar cadastro", "warning");
    }        

    btn.loading = false;
  }
  
</script>

<template>
  <PageForm 
    title="Cadastrar Responsável"
    :configs="[
      [createCelula({key:'nome', title:'Nome', required:true}), createCelula({key:'cpf', title:'Cpf', required:true}),],
      [createCelula({key:'contato', title:'Telefone', required:true}), createCelula({key:'data_nascimento', title:'Data de Nascimento', type: 'date', required:true})],
      [createCelula({key:'email', title:'Email', required:true})],
    ]"
    :fixies="[]"
    :customBtns="customBtns"
    @clicked="btnClicked"
  />

  <v-alert
    :text="message.text"
    :type="message.type"
    variant="tonal"
    v-show="message.isVisible"
    density="compact"
    class="w-100 text-center"
  ></v-alert>
</template>

<style lang="css">
</style>
