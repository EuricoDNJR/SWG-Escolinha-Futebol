<script setup>
    import { ref, reactive, onMounted } from 'vue';
    import { fetchPatchFile, createCelula, fetchGet, createFormFields, emptyStringToNull  } from '../utils/common'
    import { useAuthStore } from '../utils/store';
    import { useRouter } from 'vue-router';

    const router = useRouter();
    const authStore = useAuthStore();

    const primeiros10alunos = ref([]);
    const alunos = ref([]);
    const aluno = reactive({
        id: undefined,
        error: false,
    });
    const comprovante = reactive({
        arquivo: undefined,
        error: false,
    });
    const reload = ref(true);
    const loadingData = ref(true);
    const loadingAutocomplete = ref(false);


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

    //////////////////////////
    function isValid(){
        let isValidReturn = true;

        aluno.error = (aluno.id == undefined);
        comprovante.error = (comprovante.arquivo == undefined);

        if(aluno.error || comprovante.error){
            isValidReturn = false;
        }

        return isValidReturn;
    }

    function get(){
        let something = null;

        if(isValid()){
            something = {
                id: aluno.id,
                file: comprovante.arquivo,
            };
        }

        return something;
    }
    //////////////////////////

    function btnClicked(event, needFormData){
        const eventFunction = eventFunctions[event];

        if(needFormData){
            const body = get();

            if(body){ // se os dados do formulário forem válidos
                eventFunction(body);
            }
        }else{
            eventFunction();
        }   
    }

    async function requestFirst10Students(){
        try{
            const url = `http://127.0.0.1:8003/v1/list_all_students/?page=${1}&page_size=${10}`;
            const token = authStore.getToken;
            
            const response = await fetchGet(url, token);

            if(response.status != 204){
            const responseJson = await response.json();

            if(response.status === 200){
                alunos.value = primeiros10alunos.value = responseJson.students;
                reload.value = !reload.value; 
                loadingData.value = false;
            }
            }
        }catch(e){
            console.log(e);
        }
    }

    async function requestSearchStudentsByName(name){
        loadingAutocomplete.value = true;

        try{
            const url = `http://127.0.0.1:8003/v1/search_students_by_name/${name}`;
            const token = authStore.getToken;
            
            const response = await fetchGet(url, token);

            if(response.status != 204){
                const responseJson = await response.json();

                if(response.status === 200){
                    alunos.value = responseJson;
                    reload.value = !reload.value; 
                }else{
                    alunos.value = primeiros10alunos.value
                }
            }
        }catch(e){
            console.log(e);
        }

        loadingAutocomplete.value = false;
    }

    async function requestRegistrarPagamento(body){
        const btn = customBtns.value.find((btn) => btn.clickEvent == "registrar");
        btn.loading = true;

        message.isVisible = false;

        try{
            const url = `http://127.0.0.1:8003/v1/update_status/${body.id}`;
            const token = authStore.getToken;
            let form = new FormData();

            form.append("file", body.file);

            const response = await fetchPatchFile(url, form, token);
            
            if(response.status === 200){       
                printMessage("Pagamento registrado com sucesso", "success");
            }else if(response.status === 404){
                printMessage("Todos os pagamentos já foram registrados", "info");
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
        requestFirst10Students();
    });
</script>

<template>
    <v-skeleton-loader v-if="loadingData"
    type="heading, image, heading"
    ></v-skeleton-loader>

    <div v-if="!loadingData">
        <h2 class="titulo">Registrar Pagamento</h2>

        <v-divider></v-divider>

        <v-card 
            class="elevation-0"
        >
            <v-card-text>
                <v-row>
                    <v-col>
                        <v-autocomplete
                            v-model="aluno.id"
                            label="Nome do Aluno"
                            :items="alunos"
                            item-title="nome"
                            item-value="id"
                            :error-messages="aluno.error ? ['Campo obrigatório.'] : []"
                            hide-details="auto"
                            @update:search="requestSearchStudentsByName"
                            :loading="loadingAutocomplete"
                        ></v-autocomplete>
                    </v-col>
                </v-row>

                <v-row>
                    <v-col>
                        <v-file-input
                            v-model="comprovante.arquivo"
                            label="Comprovante"
                            :error-messages="comprovante.error ? ['Campo obrigatório.'] : []"
                            hide-details="auto"
                            show-size
                            accept="image/*"
                        ></v-file-input>
                    </v-col>
                </v-row>
            </v-card-text>
        </v-card>

        <v-divider></v-divider>   

        <div class=btns>
            <v-btn v-for="(btn, i) in customBtns" :key="i"  
                :color="btn.color"
                :variant="btn.variant"
                :prepend-icon="btn.icon"
                :loading="btn.loading"
                @click="() => btnClicked(btn.clickEvent, btn.needFormData)"
                class="btn"
                
            >
                {{ btn.text }}
            </v-btn>    
        </div>

        <v-alert
            :text="message.text"
            :type="message.type"
            variant="tonal"
            v-show="message.isVisible"
            density="compact"
            class="w-100 text-center"
        ></v-alert>
    </div>
</template>

<style scoped>
.titulo{
    width: 100%;
    text-align: center;
    margin-top: 2vh;
}

.btns{
    margin-top: 3vh;
    display: flex;
    width: 100%;
}

.btn{
    height: 8vh;
    flex-grow: 1;
}

.text-alert{
  color: gray;
  text-align: center;
  width: 100%;
}
</style>
