<script setup>
  import { ref, onMounted } from 'vue';
  import { fetchGet, getFormatedDate, getColorDate } from '../utils/common'
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
    { title: 'Idade', key: 'idade' },
    { title: 'Responsável', key: 'responsavel' },
    { title: '', key: 'data-table-expand' },
  ]);
  const expandedHeader = ref([
    { title: 'Nome', key: 'nome' },
    { title: 'Responsável', key: 'responsavel' },
    { title: 'Email do Responsável', key: 'email_responsavel' },
    { title: 'Email', key: 'email' },
    { title: 'Contato', key: 'contato' },
    { title: 'Cpf', key: 'cpf' },
    { title: 'Idade', key: 'idade' },
    { title: 'Especial', key: 'especial' },
    { title: 'Equipe', key: 'equipe' },
    { title: 'Situação', key: 'situacao' },
    { title: 'Data de Nascimento', key: 'data_nascimento' },
  ]);

  const alunos = ref([]);

  let debouncedRequestAllStudents = () => null;
  
  async function requestAllStudents(){
    loadingDataTable.value = true;
    
    try{
      const url = `http://127.0.0.1:8003/v1/list_all_students/?page=${page.value}&page_size=${10}`;
      const token = authStore.getToken;
      
      const response = await fetchGet(url, token);

      if(response.status != 204){
        const responseJson = await response.json();

        if(response.status === 200){
          qtdTotalPaginas.value = Math.ceil(responseJson.total/10);

          alunos.value = responseJson.students;

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
    requestAllStudents();

    debouncedRequestAllStudents = debounce(requestAllStudents);
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
    :items="alunos"
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
    @update:model-value="debouncedRequestAllStudents"
    :disabled="loadingDataTable"
  ></v-pagination>

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
