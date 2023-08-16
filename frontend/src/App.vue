<script setup>

import { onMounted,ref } from 'vue'
import  Loader  from './components/Loader.vue'

const data = ref({answer:"", steps:""})
const inputData = ref()
const answerReceived = ref(true)
const connection = new WebSocket("ws://localhost:8000/ws")


function submit()  {
  connection.send(inputData.value)
  answerReceived.value = false
}
onMounted(() => {
  
  connection.onmessage = function(e){
   
    let resp = JSON.parse(e.data)
    data.value = resp
    answerReceived.value = true
    console.log(answerReceived, resp)
  }

})

</script>

<template>
  <div class="container"> 
    <img class="sidebar" src="./assets/sidebar.png" /> 
    <div>
      <div class="header">
        <span class="heading"> Hackathon > Insights </span>
      </div>
      <div class="mainapp">
        <div>
          <input class="inputField" type="text" v-model="inputData" @keyup.enter="submit()">
        </div>
        <div>
          <br/>
          <button @click="submit()">Ask Talon</button>
        </div>
        <br/>
        <div v-if="answerReceived">
          <h1>{{data.answer}}</h1>
          <p v-if="data.answer"> How the AI came up with the answer: </p>
          <span v-if="answerReceived">{{data.steps.toString()}}</span>
        </div>
        <div class="loading" v-else>
          <Loader />
        </div>
      </div>
    </div>
    
  </div>
</template>

<style scoped>

  .inputField {
      width: 1000px;
      height: 3rem;
      font-size: 1.5rem;
  }
  .sidebar {
    height: 100vh;
  }
  .header {
    display: block;
    height: 4rem;
    border-bottom: 1px solid #e2e5e9;
    width: 2220px;
    /* align-self: center; */
    align-items: center;
    justify-self: start;
  }
  .heading {
    float: left;
    padding: 20px 0 0 20px;
  }
  .container {
    display: flex;
    flex-direction: row;
    justify-content: start;
    align-items: stretch;
  }

  .mainapp {
    display: block;
    position: absolute;
    left: 55%;
    top: 50%;
    -webkit-transform: translate(-50%, -50%);
    transform: translate(-50%, -50%);
  }
  .loading {
    display: block;
    position: absolute;
    left: 45%;
  }
  
</style>
