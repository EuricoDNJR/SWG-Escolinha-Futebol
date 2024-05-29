<script setup>
  import { ref, reactive, onMounted } from 'vue';
  import { fetchPost, createCelula, fetchGet } from '../utils/common'
  import { useAuthStore } from '../utils/store';
  import { useRouter } from 'vue-router';
  import PageForm from '../components/PageForm.vue'
  
  const router = useRouter();
  const authStore = useAuthStore();

  const alunos = ref([]);
  const reload = ref(true);

  const customBtns = ref([
    {text: 'Voltar', variant: 'text', icon: undefined, color: undefined, clickEvent: 'voltar', needFormData: false, loading: false},
    {text: 'Registrar', variant: 'flat', icon: 'mdi-account-plus', color: 'green-darken-1', clickEvent: 'registrar', needFormData: true, loading: false},
  ]);

  const eventFunctions = {
    voltar: () => router.push('/menu/pagamentos/'),
    registrar: (body) => requestRegistrarPagamento(body),
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
  
  async function requestAllStudents(){
    try{
      const url = `http://127.0.0.1:8003/v1/list_all_students/?page=${1}&page_size=${100}`;
      const token = authStore.getToken;
      
      const response = await fetchGet(url, token);

      if(response.status != 204){
        const responseJson = await response.json();

        if(response.status === 200){
          alunos.value = responseJson.students;
          reload.value = !reload.value; 
        }
      }
    }catch(e){
      console.log(e);
    }
  }

  async function requestRegistrarPagamento(body){
    const btn = customBtns.value.find((btn) => btn.clickEvent == "registrar");
    btn.loading = true;

    message.isVisible = false;
    console.log(body);
    try{
        const url = "http://127.0.0.1:8003/v1/signup/";
        const token = authStore.getToken;
        
        const response = await fetchPost(url, body, token);
        const responseJson = await response.json();
        
        if(response.status === 201){       
          printMessage("Pagamento registrado com sucesso", "success");
        }else{
          printMessage("Erro ao registrar pagamento", "warning");
        }
    }catch(e){
        console.log(e);
        printMessage("Falha ao registrar pagamento", "warning");
    }        

    btn.loading = false;
  }
  
  onMounted(() => {
    requestAllStudents();
  });
</script>

<template>
  <PageForm :key="reload"
    title="Registrar Pagamento"
    :configs="[
      [createCelula({key:'id', title:'Aluno', type: 'autocomplete', required:true}),],
      [createCelula({key:'file', title:'Comprovante', type: 'file', required:true}),],
    ]"
    :fixies="[
      ['Aluno.items', alunos],
      ['Aluno.itemsTitle', 'nome'],
      ['Aluno.itemsValue', 'id'],
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
