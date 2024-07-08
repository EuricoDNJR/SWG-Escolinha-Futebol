<script setup>
  import { ref, reactive, watch, onMounted } from 'vue';
  import { fetchGet, getFormatedDate, getColorDate } from '../utils/common'
  import { useAuthStore } from '../utils/store';
  import { useRouter } from 'vue-router';
  import PageForm from '../components/PageForm.vue'
  
  const router = useRouter();
  const authStore = useAuthStore();

  const expanded = ref([]);
  const qtdTotalPayments = ref(0);
  const page = ref(1);

  const pagamentos = ref([]);
  const reload = ref(true);

  const loadingDataTable = ref(false);

  const headers = ref([
    { title: 'Aluno', key: 'aluno' },
    { title: 'Data de Vencimento', key: 'data_vencimento' },
    { title: 'Status', key: 'status' },
    { title: '', key: 'data-table-expand' },
  ]);

  const searchText = ref('');

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
  
  async function requestAllPayments(){
    loadingDataTable.value = true;
    
    try{
      const url = `http://127.0.0.1:8003/v1/list_all/?page=${page.value}&page_size=${10}`;
      const token = authStore.getToken;
      
      const response = await fetchGet(url, token);

      if(response.status != 204){
        const responseJson = await response.json();

        if(response.status === 200){
          qtdTotalPayments.value = Math.ceil(responseJson.total/10); // Quantidade de páginas necessárias
          pagamentos.value = responseJson.payments;
          reload.value = !reload.value; 
        }
      }
    }catch(e){
      console.log(e);
    }

    loadingDataTable.value = false;
  }


  onMounted(() => {
    requestAllPayments();
  });
</script>

<template>
  <v-text-field 
    v-model="searchText"
    label="Buscar"
    prepend-inner-icon="mdi-magnify"
    variant="solo"
    hide-details
  ></v-text-field>

  <v-data-table-virtual :key="reload"
    v-model:expanded="expanded"
    :headers="headers"
    :items="pagamentos"
    item-value="id"
    :search="searchText"
    :loading="loadingDataTable"
    show-expand
  >
    <template v-slot:item.data_vencimento="{ item }">
      <v-chip :color="getColorDate(item)">
        {{ getFormatedDate(item.data_vencimento) }}
      </v-chip>
    </template>

    <template v-slot:expanded-row="{ columns, item }">
      <tr>
        <td :colspan="columns.length">
          More info about {{ item.valor }}
        </td>
      </tr>
    </template>
  </v-data-table-virtual>

  <v-pagination :key="reload"
    v-model="page"
    :length="qtdTotalPayments" 
    @update:model-value="requestAllPayments"
  ></v-pagination>

  <v-btn 
      color="grey-lighter-1"
      variant="flat"
      @click="() => router.push('/menu/pagamentos/')"
      class="btn"
  >
      Voltar
  </v-btn>   
</template>

<style lang="css">
 .btn{
    margin-top: 3vh;
    display: flex;
    width: 100%;
    height: 10vh;
    flex-grow: 1;
  } 
</style>
