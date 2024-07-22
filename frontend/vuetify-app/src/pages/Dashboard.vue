<script setup>
  import { ref, onMounted, reactive } from 'vue';
  import { fetchGet } from '../utils/common';
  import { useAuthStore } from '../utils/store';
  import { Chart, registerables } from 'chart.js';

  Chart.register(...registerables);

  const plugin = {
    id: 'customCanvasBackgroundColor',
    beforeDraw: (chart, args, options) => {
      const {ctx} = chart;
      ctx.save();
      ctx.globalCompositeOperation = 'destination-over';
      ctx.fillStyle = options.color || '#99ffff'; //#F5F5F5
      ctx.fillRect(0, 0, chart.width, chart.height);
      ctx.restore();
    }
  };

  const authStore = useAuthStore();
  
  const paymentsReceivableMonth = ref("R$ 0,00");
  const paymentsReceivableOverdue = ref("R$ 0,00");
  const paymentsReceivedMonth = ref("R$ 0,00");

  const isVisible = reactive({
    paymentsReceivableMonth: false,
    paymentsReceivableOverdue: false,
    paymentsReceivedMonth: false,
    pieChartTeams: false,
    pieChartStudents: false,
  });

  const formatCurrency = (value) => {
    const formatter = new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    });
    return formatter.format(value);
  };
    
  async function requestPaymentsReceivableMonth(){
    try{
      const url = "http://127.0.0.1:8003/v1/payments_receivable_month/"
      const token = authStore.getToken;
      
      const response = await fetchGet(url, token);

      if(response.status != 204){
        const responseJson = await response.json();

        if(response.status === 200){
          paymentsReceivableMonth.value = formatCurrency(responseJson.total);
        }
      }
    }catch(e){
      console.log(e);
    }

    isVisible.paymentsReceivableMonth = true;
  } 

  async function requestPaymentsReceivableOverdue(){
    try{
      const url = "http://127.0.0.1:8003/v1/payments_receivable_overdue/"
      const token = authStore.getToken;
      
      const response = await fetchGet(url, token);

      if(response.status != 204){
        const responseJson = await response.json();

        if(response.status === 200){
          paymentsReceivableOverdue.value = formatCurrency(responseJson.total);
        }
      }
    }catch(e){
      console.log(e);
    }

    isVisible.paymentsReceivableOverdue = true;
  } 

  async function requestPaymentsReceivedMonth(){
    try{
      const url = "http://127.0.0.1:8003/v1/payments_received_month/"
      const token = authStore.getToken;
      
      const response = await fetchGet(url, token);

      if(response.status != 204){
        const responseJson = await response.json();

        if(response.status === 200){
          paymentsReceivedMonth.value = formatCurrency(responseJson.total);
        }
      }
    }catch(e){
      console.log(e);
    }

    isVisible.paymentsReceivedMonth = true;
  } 

  async function requestStudentsPerTeam(){
    let studentsPerTeam = [];

    try{
      const url = "http://127.0.0.1:8003/v1/students_per_team/"
      const token = authStore.getToken;
      
      const response = await fetchGet(url, token);
      
      if(response.status != 204){
        const responseJson = await response.json();
        
        if(response.status === 200){
          studentsPerTeam = responseJson;
        }
      }
    }catch(e){
      console.log(e);
    }

    return studentsPerTeam;
  } 

  async function requestStudentsActiveInactive(){
    let studentsActiveInactive = [];

    try{
      const url = "http://127.0.0.1:8003/v1/students_active_inactive/"
      const token = authStore.getToken;
      
      const response = await fetchGet(url, token);
      
      if(response.status != 204){
        const responseJson = await response.json();

        if(response.status === 200){
          studentsActiveInactive = responseJson;
        }
      }
    }catch(e){
      console.log(e);
    }

    return studentsActiveInactive;
  } 
  

  function createChart({id, type, data, options}){
    const ctx = document.getElementById(id).getContext('2d');

    new Chart(ctx, {
      type: type,
      data: data,
      options: options,
      plugins: [plugin],
    });
  }

  async function createPieChartTeams(){
    const studentsPerTeam = await requestStudentsPerTeam();

    if(studentsPerTeam){
      const data = {
        labels: [],
        datasets: [{
          data: [],
        }]
      };

      studentsPerTeam.forEach((studentPerTeam) => {
        data.labels.push(studentPerTeam.equipe);
        data.datasets[0].data.push(Number(studentPerTeam.total));
      });

      const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: 'Número de Estudantes por Turma',
            font: {
              size: 18
            },
          },
          customCanvasBackgroundColor: {
            color: 'white',
          },
          tooltip: {
            callbacks: {
              label: function(context){
                return `${context.parsed} Alunos`;
              },
            }
          },
        },
        devicePixelRatio: 4,
      };

      createChart({
        id: 'pieChartTeams', 
        type: 'pie', 
        data: data, 
        options: options,
      });

      isVisible.pieChartTeams = true;
    }
  }

  async function createPieChartStudents(){
    const studentsActiveInactive = await requestStudentsActiveInactive();

    if(studentsActiveInactive){
      const data = {
        labels: [],
        datasets: [{
          data: [],
        }]
      };

      studentsActiveInactive.forEach((studentActiveInactive) => {
        data.labels.push(studentActiveInactive.situacao);
        data.datasets[0].data.push(Number(studentActiveInactive.total));
      });

      const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: 'Número de Alunos Ativos e Inativos',
            font: {
              size: 18
            },
          },
          customCanvasBackgroundColor: {
            color: 'white',
          },
          tooltip: {
            callbacks: {
              label: function(context){
                return `${context.parsed} Alunos`;
              },
            }
          },
        },
        devicePixelRatio: 4,
      };

      createChart({
        id: 'pieChartStudents', 
        type: 'pie', 
        data: data, 
        options: options,
      });

      isVisible.pieChartStudents = true;
    }
  }

  onMounted(() => {
    requestPaymentsReceivableMonth();
    requestPaymentsReceivableOverdue();
    requestPaymentsReceivedMonth();
    createPieChartTeams();
    createPieChartStudents();
  });
</script>

<template>
  <div class="main">
    <v-row style="max-height: 100px;">
      <v-col>
        <v-card :loading="!isVisible.paymentsReceivableMonth">
          <v-card-subtitle>Valor a Receber Este Mês</v-card-subtitle>
          <v-card-text>
            <v-chip color="green"> 
              {{ paymentsReceivableMonth }}
            </v-chip>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col>
        <v-card :loading="!isVisible.paymentsReceivableOverdue">
          <v-card-subtitle>Valor a Receber por Pagamentos Atrasados</v-card-subtitle>
          <v-card-text>
            <v-chip color="green"> 
              {{ paymentsReceivableOverdue }}
            </v-chip>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col>
        <v-card  :loading="!isVisible.paymentsReceivedMonth">
          <v-card-subtitle>Valor Recebido no Mês Atual</v-card-subtitle>
          <v-card-text>
            <v-chip color="green"> 
              {{ paymentsReceivableOverdue }}
            </v-chip>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row style="max-height: 500px;">
      <v-col>
        <v-skeleton-loader 
          type="image"
          v-if="!isVisible.pieChartTeams"
        ></v-skeleton-loader>
        
        <div id="pie-chart" v-show="isVisible.pieChartTeams"
          color="grey-lighten-4"
          style="min-height: 100px; height: 450px;"
        >
          <canvas  
            id="pieChartTeams"
            width="50"
            height="50"
            class="elevation-2 rounded">
          </canvas>
        </div> 
      </v-col>
      
      <v-col>
        <v-skeleton-loader 
          type="image"
          v-if="!isVisible.pieChartStudents"
        ></v-skeleton-loader>
        
        <div id="pie-chart" v-show="isVisible.pieChartStudents"
          color="grey-lighten-4"
          style="min-height: 100px; height: 450px;"
        >
          <canvas  
            id="pieChartStudents"
            width="50"
            height="50"
            class="elevation-2 rounded">
          </canvas>
        </div> 
      </v-col>
    </v-row>

      <v-btn 
        variant="flat"
        to="/menu/inicio/"
        class="btn-voltar"
    >
        Voltar
    </v-btn> 
  </div>
</template>

<style scoped>
.main{
  display: flex;
  flex-direction: column;
  background-color: #F5F5F5;
  height: 100%;
  padding: 20px;
}

.btn-voltar{
    width: 100%;
    height: 7vh;
    background-color: #F5F5F5;
  } 
</style>