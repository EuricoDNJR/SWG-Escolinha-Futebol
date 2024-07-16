<script setup>
  import { ref, reactive, onMounted, toRaw } from 'vue';
  import { fetchGet, fetchPost, createCelula } from '../utils/common'
  import { useAuthStore } from '../utils/store';
  import { useRouter } from 'vue-router';
  import PageForm from '../components/PageForm.vue'
  
  const router = useRouter();
  const authStore = useAuthStore();

  const especialOpcoes = ref([
    {nome: "Sim", valor: "true"},
    {nome: "Não", valor: "false"}
  ]);
  let equipes = ref([]);
  let responsaveis = ref([]);
  const reload = ref(true);

  const customBtns = ref([
    {text: 'Voltar', variant: 'text', icon: undefined, color: undefined, clickEvent: 'voltar', needFormData: false, loading: false},
    {text: 'Matricular', variant: 'flat', icon: 'mdi-account-plus', color: 'blue-darken-1', clickEvent: 'matricular', needFormData: true, loading: false},
  ]);

  const eventFunctions = {
    voltar: () => router.push('/menu/inicio/'),
    matricular: (body) => requestMatricularAluno(body),
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

  async function requestAllEquipes(){
    try{
      const url = "http://127.0.0.1:8003/v1/all_teams/";
      const token = authStore.getToken;
      
      const response = await fetchGet(url, token);

      if(response.status != 204){
        const responseJson = await response.json();

        if(response.status === 200){
          equipes.value = responseJson;
          reload.value = !reload.value; 
        }
      }
    }catch(e){
      console.log(e);
    }
  }

  async function requestAllResponsaveis(){
    try{
      const url = "http://127.0.0.1:8003/v1/all_responsible/";
      const token = authStore.getToken;
      
      const response = await fetchGet(url, token);

      if(response.status != 204){
        const responseJson = await response.json();

        if(response.status === 200){
          responsaveis.value = responseJson;
          reload.value = !reload.value; 
        }
      }
    }catch(e){
      console.log(e);
    }
  }

  async function requestCriarPagamento(body){  
    try{
      const url = "http://127.0.0.1:8003/v1/payment_generate/";
      const token = authStore.getToken;

      await fetchPost(url, body, token);
    }catch(e){
      console.log(e);
      printMessage("Falha ao criar pagamento", "warning");
    }        
  }

  async function requestMatricularAluno(body){
    const btn = customBtns.value.find((btn) => btn.clickEvent == "matricular");
    btn.loading = true;

    message.isVisible = false;

    try{
      body.situacao = "Ativo";
      
      if(body.especial == "true"){
        body.especial = true;
      }else{
        body.especial = false;
      }

      const bodyPayment = {
        valor: undefined,
        aluno: undefined,
        quant_parcelas: undefined,
      }

      bodyPayment.valor = body["valor"];
      delete body["valor"];
      bodyPayment.quant_parcelas = body["quant_parcelas"];
      delete body["quant_parcelas"];

      const url = "http://127.0.0.1:8003/v1/student/";
      const token = authStore.getToken;

      const response = await fetchPost(url, body, token);
      const responseJson = await response.json();

      if(response.status === 201){    
        bodyPayment.aluno = responseJson.uuid; 

        await requestCriarPagamento(bodyPayment);
        
        printMessage("Matrícula realizada com sucesso", "success");
      }else{
        printMessage("Erro ao realizar matrícula", "warning");
      }
    }catch(e){
      console.log(e);
      printMessage("Falha ao realizar matrícula", "warning");
    }        

    btn.loading = false;
  }
    
  onMounted(() => {
    requestAllResponsaveis();
    requestAllEquipes();
  });
</script>

<template>
  <PageForm :key="reload"
    title="Matricular Aluno"
    :configs="[
      [createCelula({key:'nome', title:'Nome', required:true}), createCelula({key:'idade', title:'Idade', type:'number'})],
      [createCelula({key:'cpf', title:'Cpf'}), createCelula({key:'contato', title:'Telefone'})],
      [createCelula({key:'data_nascimento', title:'Data de Nascimento', type: 'date'}), createCelula({key:'email', title:'Email'})],
      [createCelula({key:'especial', title:'Especial', type: 'select', required:true, initialValue: ''}), createCelula({key:'equipe', title:'Equipe', type: 'select', required:true, initialValue: ''})],
      [createCelula({key:'valor', title:'Valor da Mensalidade', type: 'number',  required:true}), createCelula({key:'responsavel', title:'Responsavel', type: 'select', required:true, initialValue: ''})],
      [createCelula({key:'ano_escolar', title:'Ano escolar'}), createCelula({key:'quant_parcelas', title:'Quantidade de Parcelas', type: 'number',  required:true})],
    ]"
    :fixies="[
      ['Especial.items', especialOpcoes],
      ['Especial.itemsTitle', 'nome'],
      ['Especial.itemsValue', 'valor'],
      ['Equipe.items', equipes],
      ['Equipe.itemsTitle', 'nome'],
      ['Equipe.itemsValue', 'id'],
      ['Responsavel.items', responsaveis],
      ['Responsavel.itemsTitle', 'nome'],
      ['Responsavel.itemsValue', 'id'],
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
