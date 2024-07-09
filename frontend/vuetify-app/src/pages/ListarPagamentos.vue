<script setup>
  import { ref, reactive, onMounted } from 'vue';
  import { fetchGet, fetchGetFile, getFormatedDate, getColorDate } from '../utils/common'
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
  const downloading = reactive({});

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
          responseJson.payments.forEach((item) => {
            downloading[item.id] = false;
          });

          reload.value = !reload.value; 
        }
      }
    }catch(e){
      console.log(e);
    }

    loadingDataTable.value = false;
  }

  async function downloadComprovante(id_pagamento){
    downloading[id_pagamento] = true;

    try{
      const url = `http://127.0.0.1:8003/v1/download_comprovante/${id_pagamento}`;
      const token = authStore.getToken;
      
      const response = await fetchGetFile(url, token);
      const responseBlob = await response.blob();
      const imageURL = URL.createObjectURL(responseBlob)

      const contentDisposition = response.headers.get('Content-Disposition');

      let fileName = 'downloaded_file'; // Nome padrão caso não seja encontrado no cabeçalho
      if (contentDisposition && contentDisposition.indexOf('attachment') !== -1) {
        const matches = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(contentDisposition);

        if (matches != null && matches[1]) { 
          fileName = matches[1]; 
        }
      }
      
      //Solução Temporária, futuramente o backend vai me enviar o formato da iamgem
      fileName += ".png"
      const link = document.createElement('a')
      link.href = imageURL
      link.download = fileName
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }catch(e){
      console.log(e);
    }

    downloading[id_pagamento] = false;
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

        <v-card v-if="item.status=='Pago'"
          class="ma-2"
        >
          <v-card-subtitle> Data de Pagamento </v-card-subtitle>

          <v-card-text> {{ item.data_pagamento }} </v-card-text>
        </v-card>

        <v-card v-if="item.status=='Pago'"
          class="ma-2"
        >
          <v-card-subtitle> Comprovante </v-card-subtitle>
          
          <v-btn 
            prepend-icon="mdi-download" 
            class="ma-2"
            @click="() => downloadComprovante(item.id)"
            :loading="downloading[item.id]"
          >
            Download
          </v-btn>
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
    height: 8vh;
    flex-grow: 1;
  } 

  .max-width-100{
    max-width: 100%;
  }
</style>
