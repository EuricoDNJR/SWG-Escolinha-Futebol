<script setup>
  import { ref, reactive, onMounted } from 'vue';
  import { fetchGet, fetchPost, createCelula } from '../utils/common'
  import { useAuthStore } from '../utils/store';
  import { useRouter } from 'vue-router';
  import PageForm from '../components/PageForm.vue'
  
  const router = useRouter();
  const authStore = useAuthStore();

  const customBtns = ref([
    {text: 'Fechar', variant: 'text', icon: undefined, color: undefined, clickEvent: 'fechar', needFormData: false, loading: false},
    {text: 'Renovar', variant: 'flat', icon: 'mdi-autorenew', color: 'blue-darken-1', clickEvent: 'renovar', needFormData: true, loading: false},
  ]);

  const eventFunctions = {
    fechar: () => {
      dialog.value = false;

      message.isVisible = false;
    },
    renovar: (body) => requestRenovarMatricula(body),
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

  const expanded = ref([]);
  const qtdTotalPaginas = ref(0);
  const page = ref(1);

  const reload = ref(true);
  const loadingDataTable = ref(false);

  const searchText = ref('');

  const dialog = ref(false);

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
    { title: 'Endereço', key: 'endereco_responsavel' },
    { title: 'Email', key: 'email' },
    { title: 'Contato', key: 'contato' },
    { title: 'Cpf', key: 'cpf' },
    { title: 'Idade', key: 'idade' },
    { title: 'Especial', key: 'especial' },
    { title: 'Equipe', key: 'equipe' },
    { title: 'Situação', key: 'situacao' },
    { title: 'Data de Nascimento', key: 'data_nascimento' },
    { title: 'Ano Escolar', key: 'ano_escolar' },
  ]);

  const alunos = ref([]);
  const aluno = ref(undefined);

  let debouncedRequestAllStudents = () => null;

  function btnClicked({event, body}){
    const eventFunction = eventFunctions[event];

    if(body){
      eventFunction(body);
    }else{
      eventFunction();
    }   
  }

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

  async function requestRenovarMatricula(body){  
    const btn = customBtns.value.find((btn) => btn.clickEvent == "renovar");
    btn.loading = true;

    message.isVisible = false;

    try{
      const url = "http://127.0.0.1:8003/v1/add_installments/";
      const token = authStore.getToken;

      body.aluno = aluno.value;
      console.log(body);

      const response = await fetchPost(url, body, token);

      if(response.status == 200){
        printMessage("Renovação realizada com sucesso", "success");
      }else{
        printMessage("Erro ao realizar renovação", "warning");
      }
    }catch(e){
      console.log(e);
      printMessage("Falha ao renovar matricula", "warning");
    }        

    btn.loading = false;
  }

  function debounce(func, timeout = 300){
    let timer;
    return (...args) => {
      clearTimeout(timer);
      timer = setTimeout(() => { func.apply(this, args); }, timeout);
    };
  } 

  function openDialog(item){
    aluno.value = item.id;

    dialog.value = true;
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
            
            <v-card
              class="ma-2"
            >
              <v-card-subtitle> Matricula </v-card-subtitle>
              
              <v-btn
                class="ma-2"
                prepend-icon="mdi-autorenew"
                v-bind="activatorProps"
                @click="() => openDialog(item)"
              >
                Renovar
              </v-btn>

              <v-dialog
                v-model="dialog"
              >
                <v-card>
                  <v-card-text>
                    <PageForm :key="reload"
                      title="Renovar Matrícula"
                      :configs="[
                        [createCelula({key:'valor', title:'Valor', type:'number', required:true}), createCelula({key:'quant_parcelas', title:'Quantidade de Parcelas', type:'number', required:true})],
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
                  </v-card-text>
                </v-card>
              </v-dialog>
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
