<script setup>
  import { ref, reactive, onMounted } from 'vue';
  import { fetchGet, fetchGetFile, getFormatedDate, getColorDate } from '../utils/common'
  import { useAuthStore } from '../utils/store';
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  const authStore = useAuthStore();

  const expanded = ref([]);
  const qtdTotalPaginas = ref(0);
  const page = ref(1);

  const reload = ref(true);
  const loadingDataTable = ref(false);

  const searchText = ref('');

  const headers = ref([
    { title: 'Nome', key: 'nome' },
    { title: 'Cargo', key: 'cargo' },
    { title: '', key: 'data-table-expand' },
  ]);
  const expandedHeader = ref([
    {title: 'Nome', key: 'nome'}, 
    {title: 'Email', key: 'email'}, 
    {title: 'Cargo', key: 'cargo'}, 
  ]);

  const usuarios = ref([]);
  const slicedUsers = ref([]);
  // Será utilizado quando ocorrer a implementação da paginação no back-end
  // let debouncedRequestAllUsers = () => null;
  

  async function requestAllUsers(){
    loadingDataTable.value = true;
    
    try{
      const url = `http://127.0.0.1:8003/v1/all_users/`;
      const token = authStore.getToken;
      
      const response = await fetchGet(url, token);

      if(response.status != 204){
        const responseJson = await response.json();

        if(response.status === 200){
          qtdTotalPaginas.value = Math.ceil(responseJson.length/10); // Quantidade de páginas necessárias

          usuarios.value = responseJson;
          slicedUsers.value =  usuarios.value.slice(0, 10);
        
          reload.value = !reload.value; 
        }
      }
    }catch(e){
      console.log(e);
    }

    loadingDataTable.value = false;
  }

  function fakeLoading(){
    loadingDataTable.value = true;

    setTimeout(sliceUsers, 500);
  }

  function sliceUsers(){
    const fim = page.value * 10;
    const inicio = fim - 10;
    
    slicedUsers.value = usuarios.value.slice(inicio, fim);

    loadingDataTable.value = false;
  }

  // function debounce(func, timeout = 300){
  //   let timer;
  //   return (...args) => {
  //     clearTimeout(timer);
  //     timer = setTimeout(() => { func.apply(this, args); }, timeout);
  //   };
  // } 

  onMounted(() => {
    requestAllUsers();

    // debouncedRequestAllPayments = debounce(requestAllPayments);
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
    :items="slicedUsers"
    item-value="id"
    :search="searchText"
    :loading="loadingDataTable"
    show-expand
    class="max-width-100"
    expand-on-click
  >
    <template v-slot:expanded-row="{ columns, item }">
      <tr>
        <td :colspan="columns.length">
          <div class="d-flex flex-wrap">
            <v-card
              v-for="(obj, index) in expandedHeader"
              :key="index"
              class="ma-2"
            >
              <v-card-subtitle>{{ obj.title }}</v-card-subtitle>
              <v-card-text>{{ item[obj.key] }}</v-card-text>
            </v-card>
          </div>
        </td>
      </tr>
    </template>
  </v-data-table-virtual>

  <v-pagination :key="reload"
    v-model="page"
    :length="qtdTotalPaginas" 
    @update:model-value="fakeLoading"
    :disabled="loadingDataTable"
  ></v-pagination>
  <!-- @update:model-value="debouncedRequestAllPayments" -->
  <v-btn 
      color="grey-lighter-1"
      variant="flat"
      @click="() => router.push('/menu/area-administrativa/')"
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
