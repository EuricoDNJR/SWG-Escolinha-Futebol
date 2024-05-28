<script setup>
    import { ref, toRaw } from 'vue'
    import { createFormFields, emptyStringToNull } from '../utils/common';


    const props = defineProps(['title', 'configs', 'fixies', 
                            'customBtns', 'loadingCard', 'textAlert']);
    const emit = defineEmits(['clicked']);

    let [fieldsObj, formFields] = createFormFields(
        props.configs,
        props.fixies,
    );
    formFields = ref(formFields);

    function isValid(){
        let isValidReturn = true;

        for(let title in fieldsObj){
            if(fieldsObj[title].required){
                fieldsObj[title].error.value = (fieldsObj[title].obj.value.length <= 0);
            }
            if(fieldsObj[title].error.value){
                isValidReturn = false;
            }
        }

        return isValidReturn;
    }

    function create(){
        const something = {};
        
        for(let title in fieldsObj){
            something[fieldsObj[title].key] = fieldsObj[title].obj.value.trim();
        }

        return something;
    }

    function get(){
        let something = null;

        if(isValid()){
            something = create();

            for(let key in something){
                something[key] = emptyStringToNull(something[key]);
            }
        }

        return something;
    }

    function emitClicked(eventClick, needFormData){
        if(needFormData){
            const body = get();

            if(body){
                emit('clicked', {'event': eventClick, 'body': body});
            }
        }else{
            emit('clicked', {'event': eventClick});
        }
    }
</script>

<template>
    <div v-if="props.title">
        <h2 class="titulo">{{ props.title }}</h2>
    </div>

    <v-divider></v-divider>
    
    
  <h4 class="text-alert">{{ props.textAlert }}</h4>

    <v-card 
        class="elevation-0"
        :loading="loadingCard"
    >
        <v-card-text>
            <v-row v-for="(formLine, i) in formFields" :key="i">
                <v-col v-for="(field, j) in formLine" :key="i">
                    <div v-if="field.readonly && field.card">
                        <v-card variant="tonal" :color="field.card.color">
                            <v-card-title>
                                {{ field.title }}
                            </v-card-title>
                            <v-card-text>
                                <v-row>
                                    <v-col cols="auto">
                                        <v-icon >{{ field.card.icon }}</v-icon>
                                    </v-col>
                                    <v-col>
                                        <h2>{{ field.obj.replace('.', ',') }}</h2>
                                    </v-col>
                                </v-row>
                            </v-card-text>
                        </v-card>        
                    </div>
                    <div v-else>
                        <v-text-field v-if="['text', 'number', 'date'].includes(field.type)"
                            v-model="field.obj"
                            :label="field.title"
                            :type="field.type"
                            :error-messages="field.error ? ['Campo obrigatório.'] : []"
                            hide-details="auto"
                            :readonly="field.readonly"
                            :variant="field.variant"
                        ></v-text-field>
                        <v-select v-if="field.type == 'select'"
                            v-model="field.obj"
                            :label="field.title"
                            :items="field.items"
                            :item-title="field.itemsTitle"
                            :item-value="field.itemsValue"
                            :error-messages="field.error ? ['Campo obrigatório.'] : []"
                            hide-details="auto"
                            :readonly="field.readonly"
                            :variant="field.variant"
                        ></v-select>
                        <v-autocomplete v-if="field.type == 'autocomplete'"
                            v-model="field.obj"
                            :label="field.title"
                            :items="field.items"
                            :item-title="field.itemsTitle"
                            :item-value="field.itemsValue"
                            :error-messages="field.error ? ['Campo obrigatório.'] : []"
                            hide-details="auto"
                            :readonly="field.readonly"
                            :variant="field.variant"
                        ></v-autocomplete>
                    </div>
                </v-col>
            </v-row>
        </v-card-text>
    </v-card>

    <v-divider></v-divider>   

    <div class=btns>
        <v-btn v-for="(btn, i) in props.customBtns" :key="i"  
            :color="btn.color"
            :variant="btn.variant"
            :prepend-icon="btn.icon"
            :loading="btn.loading"
            @click="() => emitClicked(btn.clickEvent, btn.needFormData)"
            class="btn"
            
        >
            {{ btn.text }}
        </v-btn>    
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
