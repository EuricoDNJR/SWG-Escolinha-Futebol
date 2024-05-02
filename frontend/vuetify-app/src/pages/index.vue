<script setup>
  import { ref, reactive } from 'vue';
  import { fetchPost } from '../utils/common'
  import { useAuthStore } from '../utils/store';
  import { useRouter } from 'vue-router';

  const router = useRouter();

  const authStore = useAuthStore();

  const email = ref('');
  const senha = ref('');
  const message = reactive({
    text: '',
    type: 'error',
    isVisible: false,
  });
  const showPassword = ref(false);

  const loginBtnLoaderIsVisible = ref(false);

  function getDadosLoginForm() {
    return {
      email: email.value,
      password: senha.value
    };
  }

  async function requestLogin(data){   
      let userData = null;

      loginBtnLoaderIsVisible.value = true;
      
      try {
        const response = await fetchPost("http://127.0.0.1:8003/v1/login/", data);
        const responseJson = await response.json();
        
        if(response.status === 200){
          printLoginSuccessfulMessage();

          userData = {
              token: responseJson.token,
          };
        }else{
          const errorMessage = responseJson.detail[0].msg;
          printErrorMessage("Falha no login");
        }
      } catch (error) {
        console.log(error);
        printErrorMessage("Erro inesperado, tente novamente");
      }

      loginBtnLoaderIsVisible.value = false;

      return userData;
  }

  function resetMessage() {
    message.isVisible = false;
  }

  function printMessage(msg){
    message.text = msg;
    message.isVisible = true;
  }

  function printErrorMessage(msg){
    message.type = "error";
    printMessage(msg);
  }

  function printLoginSuccessfulMessage(){
    message.type = "success";
    printMessage("Login efetuado com sucesso");
  }

  async function handleLogin() {
    resetMessage();

    const data = getDadosLoginForm();
    
    // const formatedData = formatDadosLogin(data);

    const userData = await requestLogin(data);

    if(userData){
      authStore.successfulLogin({...userData});

      router.push('/tela-inicial');

      console.log("User TOKEN: " + authStore.getToken + "           index.vue in handleLogin function");
    } 
  }
</script>

<template>
  <div class="elipse"></div> 

  <div class="login-conteiner">
    <div class="login-box-intermediario">
      <img src="../assets/logo-farp.svg" alt="logo farp" class="logo-image">
      
      <div class="login-form">
        <form @submit.prevent="handleLogin">
          <v-text-field class="input-field"
            v-model="email"
            label="Email" 
            variant="outlined"></v-text-field>

          <v-text-field  class="input-field"
            v-model="senha"
            label="Senha" 
            variant="outlined"
            :type="showPassword ? 'text' : 'password'"
            :append-inner-icon="showPassword ? 'mdi-eye':'mdi-eye-off'"
            @click:append-inner="showPassword = !showPassword"
          ></v-text-field>
          
          <v-alert
            :text="message.text"
            :type="message.type"
            variant="tonal"
            v-show="message.isVisible"
            density="compact"
            class="w-100 text-center"
          ></v-alert>

          <v-btn
            :loading="loginBtnLoaderIsVisible"
            variant="flat"
            type="submit"
            color="grey-darken-4"
            block
            prepend-icon="mdi-login"
          >
            Entrar
          </v-btn>
        </form>
      </div>
    </div>
  </div>

  
</template>

<style lang="css">
  .logo-image{
    position: relative;
    width: 20vmin;
    transform: translateY(30%);
  }

  .elipse{
    background-color: #FFD601;
    width:100%;
    height:65%;
    border-radius: 0% 0% 50% 50%;;
    box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.5);
  }

  .login-conteiner{
    top: 0px;
    display: flex;
    flex-direction: column;
    position: absolute;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
  }

  .login-box-intermediario{
    width: 95%;
    display: flex;
    flex-direction: column;
    position: absolute;
    justify-content: center;
    align-items: center;
    transform: translateY(-6vmin);
  }

  .login-form{
    display: flex;
    flex-direction: column;
    justify-content: center;
    width: 90%;
    background-color: white;
    border-radius: 20px;
    padding: 10vmin 15px 15px 15px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.25);
  }
</style>
