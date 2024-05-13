import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
    id: 'auth',
    state: () => ({
        token: null,
    }),
    getters: {
        getToken() {
          return this.token;
        },
      },
    actions: {
      successfulLogin({token}) {
        this.token = token;
      },
      reset() {
        this.token = null;
      }
    }
});

// export const useSnackbarStore = defineStore('snackbar', {
//   id:'snackbar',

//   state: () => ({
//     wasActivated: false,
//     wasClosed: false,
//     text: "",
//     messageType: 'info',
//   }),
//   getters: {
//     getWasActivated(){
//       return this.wasActivated;
//     },
//     getWasClosed(){
//       return this.wasClosed;
//     },
//     getText(){
//       return this.text;
//     },
//     getMessageType(){
//       return this.messageType;
//     },
//   },
//   actions: {
//     set(text, messageType){
//       this.wasActivated = !this.wasActivated;
//       this.text = text;
//       this.messageType = messageType;
//     },
//     close(){
//       this.wasClosed = !this.wasClosed;
//     }
//   }
// });
