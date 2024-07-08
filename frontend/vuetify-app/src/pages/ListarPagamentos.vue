<script setup>
  import { ref, reactive, watch, onMounted } from 'vue';
  import { fetchGet, getFormatedDate, getColorDate } from '../utils/common'
  import { useAuthStore } from '../utils/store';
  import { useRouter } from 'vue-router';
  
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
  const expandedHeader = ref([
    {title: 'Aluno', key: 'aluno'}, 
    {title: 'Valor', key: 'valor'}, 
    {title: 'Status', key: 'status'}, 
    {title: 'Data de Vencimento', key: 'data_vencimento'}, 
    {title: 'Data de Pagamento', key: 'data_pagamento'}, 
    {title: 'Número da Parcela', key: 'parcela'}, 
  ]);

  const searchText = ref('');
 
  let debouncedRequestAllPayments = () => null;


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

  function debounce(func, timeout = 300){
    let timer;
    return (...args) => {
      clearTimeout(timer);
      timer = setTimeout(() => { func.apply(this, args); }, timeout);
    };
  } 

  onMounted(() => {
    requestAllPayments();

    debouncedRequestAllPayments = debounce(requestAllPayments);
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
    class="max-width-100"
  >
    <template v-slot:item.data_vencimento="{ item }">
      <v-chip :color="getColorDate(item)">
        {{ getFormatedDate(item.data_vencimento) }}
      </v-chip>
    </template>

    <template v-slot:expanded-row="{ columns, item }">
      <div class="d-flex flex-wrap">
        <v-card
          v-for="(obj, index) in expandedHeader"            
          :key="index" 
          class="ma-2"
        >
          <v-card-subtitle> {{obj.title}}</v-card-subtitle>

          <v-card-text>{{ item[obj.key] }}</v-card-text>
        </v-card>
      </div>
    </template>
  </v-data-table-virtual>

  <v-pagination :key="reload"
    v-model="page"
    :length="qtdTotalPayments" 
    @update:model-value="debouncedRequestAllPayments"
    :disabled="loadingDataTable"
  ></v-pagination>

  <v-btn 
      color="grey-lighter-1"
      variant="flat"
      @click="() => router.push('/menu/pagamentos/')"
      class="btn-voltar"
  >
      Voltar
  </v-btn>   
</template>

<style scoped lang="css">
 .btn-voltar{
    margin-top: 3vh;
    display: flex;
    width: 100%;
    height: 10vh;
    flex-grow: 1;
  } 

  .max-width-100{
    max-width: 100%;
  }
</style>
