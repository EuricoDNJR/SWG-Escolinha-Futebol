<script setup>
  import { ref, reactive } from 'vue';
  import { fetchPost, createCelula } from '../utils/common'
  import { useAuthStore } from '../utils/store';
  import { useRouter } from 'vue-router';
  import PageForm from '../components/PageForm.vue'
  
  const router = useRouter();
  const authStore = useAuthStore();

  const professores = ref([]);
  const reload = ref(true);

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

  // async function requestAllProfessores(){
  //   try{
  //     const url = "http://127.0.0.1:8003/v1/all_teams/";
  //     const token = authStore.getToken;
      
  //     const response = await fetchGet(url, token);
  //     console.log(response);
  //     if(response.status != 204){
  //       const responseJson = await response.json();

  //       if(response.status === 200){
  //         equipes.value = responseJson;
  //         reload.value = !reload.value; 
  //       }
  //     }
  //   }catch(e){
  //     console.log(e);
  //   }
  // }

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
  <PageForm :key="reload"
    title="Cadastrar Turma"
    :configs="[
      [createCelula({key:'nome', title:'Nome', required:true}), createCelula({key:'professor', title:'Professor', type: 'autocomplete', required:true}),],
      [createCelula({key:'idade_minima', title:'Idade Mínima', type: 'number', required:true}), createCelula({key:'idade_maxima', title:'Idade Máxima', type: 'number', required:true})],
      [createCelula({key:'horario_inicio', title:'Horário de Início', required:true}), createCelula({key:'horario_fim', title:'Horário de Término', required:true})],
      [createCelula({key:'dias_semana', title:'Dias da Semana', required:true})],
    ]"
    :fixies="[
      ['Professor.items', professores],
      ['Professor.itemsTitle', 'nome'],
      ['Professor.itemsValue', 'id'],
    ]"
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
