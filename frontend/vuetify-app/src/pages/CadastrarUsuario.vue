<script setup>
  import { ref, reactive } from 'vue';
  import { fetchPost, createCelula } from '../utils/common'
  import { useAuthStore } from '../utils/store';
  import { useRouter } from 'vue-router';
  import PageForm from '../components/PageForm.vue'
  
  const router = useRouter();
  const authStore = useAuthStore();

  const cargos = ref([
    {nome: "Administrador"},
    {nome: "Professor"}
  ]);

  const customBtns = ref([
    {text: 'Voltar', variant: 'text', icon: undefined, color: undefined, clickEvent: 'voltar', needFormData: false, loading: false},
    {text: 'Cadastrar', variant: 'flat', icon: 'mdi-account-plus', color: 'green-darken-1', clickEvent: 'cadastrar', needFormData: true, loading: false},
  ]);

  const eventFunctions = {
    voltar: () => router.push('/menu/area-administrativa/'),
    cadastrar: (body) => requestCadastrarUsuario(body),
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

  async function requestCadastrarUsuario(body){
    const btn = customBtns.value.find((btn) => btn.clickEvent == "cadastrar");
    btn.loading = true;

    message.isVisible = false;

    try{
        const url = "http://127.0.0.1:8003/v1/signup/";
        const token = authStore.getToken;
        
        const response = await fetchPost(url, body, token);
        const responseJson = await response.json();

        if(response.status === 201){       
          printMessage("Cadastro realizado com sucesso", "success");
        }else{
          printMessage(responseJson.detail, "warning");
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
    title="Cadastrar Usuário"
    :configs="[
      [createCelula({key:'nome', title:'Nome', required:true}), createCelula({key:'password', title:'Senha', required:true})],
      [createCelula({key:'email', title:'Email', required:true}), createCelula({key:'cargo', title:'Cargo', type: 'select', required:true, initialValue: ''})],
    ]"
    :fixies="[
      ['Cargo.items', cargos],
      ['Cargo.itemsTitle', 'nome'],
      ['Cargo.itemsValue', 'nome'],
    ]"
    :customBtns="customBtns"
    @clicked="btnClicked"
    textAlert="*Senha precisa de no mínimo 6 caracteres."
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
