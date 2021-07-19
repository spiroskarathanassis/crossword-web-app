<template>
  <div class="home-pg">
    <h1>The new generation Crossword</h1>
    <div class="main-section">
      <div class="img-container"></div>
      <div class="modal-form">
        <div class="form-container">
          
          <h4>
            Welcome, generate your own Crossword
          </h4>
          <form @submit="generateGrid">
            
            <div class="input-fields">
              <div class="field">
                <label for="">Crossword Theme</label>
                <input type="text" placeholder="word" autofocus v-model="theme.text"/>
              </div>
              <div class="field">
                <label for="">Grid Dimensions</label>
                <select name="Level" id="" v-model="dimensions.text">
                  <option v-show="level.text == 'Hard'" value="21">21 x 21</option>
                  <option v-show="level.text != 'Easy'"  value="17">17 x 17</option>
                  <option value="15">15 x 15</option>
                  <option value="13">13 x 13</option>
                  <option value="11">11 x 11</option>
                  <option value="9">9 x 9</option>
                  <option value="7">7 x 7</option>
                </select>
              </div>
              <div class="field">
                <label for="">Difficulty Level</label>
                <select name="Level" id="" v-model="level.text">
                  <option value="Easy">Easy</option>
                  <option value="Medium">Medium</option>
                  <option value="Hard">Hard</option>
                </select>
              </div>
            </div>
            <div class="preview-fields">
              <ul>
                <li>
                  <div class="img">
                    <img v-show="theme.isValid" src="../../assets/images/checkmark.svg" alt="" width="15">
                  </div>
                  <span>{{ theme.text ? theme.text : 'eg. sports' }}</span>
                </li>
                <li>
                  <div class="img">
                    <img v-show="level.isValid" src="../../assets/images/checkmark.svg" alt="" width="15">
                  </div>
                  <span>{{ level.text }}</span>
                </li>
                <li>
                  <div class="img">
                    <img v-show="dimensions.isValid" src="../../assets/images/checkmark.svg" alt="" width="15">
                  </div>
                  <span>{{ dimensions.text }} x {{ dimensions.text }}</span>
                </li>
              </ul>
            </div>

          </form>
          <div class="footer">
            <button type="submit"
              @click="generateGrid"
              :disabled="isBtnDisabled"
              :class="isBtnDisabled && 'btn-disabled'"
            >Generate</button>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, watchEffect } from 'vue';

const LEVELS = ['Easy', 'Medium', 'Hard'];
const DIMENSIONS = [5, 7, 9, 11, 13, 15, 17, 21];

export default {
  name: 'Home',
  setup(_, {emit}) {
    const isBtnDisabled = ref(true);
    const theme = reactive({
      text: '',
      isValid: false
    });
    const level = reactive({
      text: 'Easy',
      isValid: false
    });
    const dimensions = reactive({
      text: 15,
      isValid: false
    });

    
    const checkInput = (inputData) => {
      const isEmpty = !inputData.theme.trim('');
      const themeTrimed = inputData.theme.trim();
      const isWord = themeTrimed.split(' ').length > 0
        && themeTrimed.length > 2;
      const isLevelCorrect = LEVELS.includes(inputData.level);
      const dimExists = DIMENSIONS.includes(+inputData.dims);

      if (!isEmpty && isWord) {
        theme.isValid = true;
      }
      if (isLevelCorrect) {
        level.isValid = true;
      }
      if (dimExists) {
        dimensions.isValid = true;
      }

      if (isEmpty || !isWord || !isLevelCorrect || !dimExists) {
        return false;
      }
      return true;
    }
    
    const generateGrid = () => {
      const isInputDataValid = checkInput({
        'theme': theme.text,
        'level': level.text,
        'dims': dimensions.text
      });

      if (!isInputDataValid) {
        console.log('an input was invalid');
        // do something
        return;
      }

      emit('generate-grid', {
        'theme': theme.text,
        'level': level.text,
        'dimensions': +dimensions.text
      });
    }

    watchEffect(() => {
      const canGenerate = checkInput({
        'theme': theme.text,
        'level': level.text,
        'dims': dimensions.text
      });

      isBtnDisabled.value = !canGenerate ? true : false;
    });

    return {
      isBtnDisabled,
      theme,
      level,
      dimensions,
      generateGrid
    }
  }
}
</script>

<style lang="scss" scoped>
  @import '../../assets/styles/home.scss';
</style>