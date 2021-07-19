<template>
  <div class="cross-container">
    <h1>Crossword Web Generator</h1>

    <section>
      <div class="grid-container">
        <div class="message">
          <p v-if="message.isEnabled" class="msg-p">
            <img src="../assets/images/error.svg" alt="">
            <span>{{ message.text }}</span>
          </p>

          <div v-else-if="!isScreenSmall" class="clue-text">
            <p>
              <span :class="activeCell.blockDimension && 'point'">
                {{ activeCell.blockDimension ? (activeCell.blockDimension == 'down' ? 'D' : 'A') : 'Select a block' }}
                {{ activeCell.clueNumbher }}
              </span>
              <span class="clue">{{ activeCell.clue }}</span>
            </p>

            <download-button :htmlSchema="gridSchema" :theme="theme" :clues_ans="ans_and_clues"></download-button>
          </div>
        </div>
        <div class="grid-wrapper" :style="`grid-template-columns: repeat(${grid.size}, auto);`" ref="crossword">
          <div v-for="(box, i) in gridBoxes" :key="i" class="box">
            <div v-if="box.cell == '#'" class="input-wrapper">
              <input type="text" class="blackbox" disabled="true">
            </div>
            <div v-else class="input-wrapper">
              <span v-if="box.dimensions.includes('down') || box.dimensions.includes('across')" 
                class="point-block"
                :class="box.isDimensionEnable && 'active-opacity'"
              >{{ box.pointer }}</span>
              <input type="text"
                :value="box.cell"
                :class="box.isVisible && 'box-visible'"
                @input="(e) => adjustInput(e, i)"
                @keyup.delete=" (e) => box.cell = '' "
                @click="pointToBlock(i)" >
            </div>
          </div>
        </div>
      </div>
      
      <div class="clue-container" v-if="!isScreenSmall && ans_and_clues.across.length > 0">
        <div class="clue-dimension">
          <h3>Across</h3>
          <div class="clue-list-wrapper">
            <ol class="clue-list" ref="acrossList">
              <li v-for="across in ans_and_clues.across" :key="across.id"
                :id="across.id"
                :class="(activeCell.blockId == across.id) && 'active'"
                @click="() => setActiveAnswer('across', across.id)"
              >
                <span class="clue-pointer">{{ across.pointer }}</span>
                <span>{{ across.clue }}</span>
              </li>
            </ol>
          </div>
        </div>
        <div class="clue-dimension">
          <h3>Down</h3>
          <div class="clue-list-wrapper">
            <ol class="clue-list" ref="downList">
              <li v-for="down in ans_and_clues.down" :key="down.id"
                :id="down.id"
                :class="(activeCell.blockId == down.id) && 'active'"
                @click="() => setActiveAnswer('down', down.id)"
              >
                <span class="clue-pointer">{{ down.pointer }}</span>
                <span>{{ down.clue }}</span>
              </li>
            </ol>
          </div>
        </div>
      </div>

      <div class="clue-container" v-else>
        <div class="clue-dimension" v-if="activeCell.blockDimension">
          <h3>{{ activeCell.blockDimension == 'across' ? 'Across' : 'Down' }}</h3>
          <div class="clue-list-wrapper">
            <ol class="clue-list">
              <li v-for="dim in ans_and_clues.across.concat(ans_and_clues.down)"
                :key="dim.id"
                v-show="activeCell.blockId == dim.id"
              >
                <span class="clue-pointer">{{ dim.pointer }}</span>
                <span>{{ dim.clue }}</span>
              </li>
            </ol>
          </div>
        </div>
      </div>

    </section>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed, onBeforeUnmount, getCurrentInstance } from 'vue';

import DownloadButton from './utils/DownloadButton.vue';

export default {
  name: 'Grid',
  props: ['gridData'],
  components: {  
    DownloadButton
  },
  setup(props) {
    const theme = ref('');
    const crossword = ref(null);
    const gridSchema = ref(null);
    const gridBoxes = ref([]);
    const acrossList = ref(null);
    const downList = ref(null);
    const isScreenSmall = ref(window.matchMedia('(max-width: 540px)').matches);
    
    const activeCell = reactive({
      blockId: null,
      blockDimension: null,
      index: null,
      clue: null,
      clueNumbher: null
    })
    const message = reactive({
      isEnabled: false,
      text: ""
    });
    const grid = reactive({
      size: computed(() => props.gridData.grid.length),
      boxLength: computed(() => Math.pow(grid.size, 2)),
    });
    const ans_and_clues = reactive({
      across: [],
      down: []
    });

    const internalInstance = getCurrentInstance();

    const displayTimedMessage = (msg) => {
      message.isEnabled = true;
      message.text = msg;

      setTimeout(() => {
        message.isEnabled = false;
        message.text = "";
      }, 3000);
    }
    
    const seperateCluesByDimensions = (ansData) => {
      ansData.forEach(ans => {
        ans_and_clues[ans.dimension].push(ans);
      });
    }

    const adjustInput = (e, index) => {
      let lastLetter = e.data;
      let boxValue = e.target.value;
      const isEmptyString = (lastLetter == " ") && (boxValue.length < 1);

      if (!lastLetter && !boxValue || isEmptyString) {
        return;
      }

      lastLetter = lastLetter.toUpperCase();

      if (!lastLetter.match(/[A-Z]/)) {
        const msg = `Letter ${lastLetter} is invalid.`
        displayTimedMessage(msg);
        e.target.value = boxValue.toUpperCase().replace(lastLetter, "");
        return;
      }

      const value = (boxValue.length == 1) ? boxValue.toUpperCase() : lastLetter;
      e.target.value = value;
      gridBoxes.value[index].cell = value;
    }

    const sortAnsClues = (dim) => {
      ans_and_clues[dim].sort((prev, next) => prev.pointer - next.pointer);
    }

    const findExistingBlock = (dimension, index) => {
      const blockRow = Math.floor(index / grid.size);
      const blockCol = index % grid.size;

      return ans_and_clues[dimension].find(ans => {
        const [row, col] = ans.spot;

        if (dimension == 'across') {
          const isSameRow = row === blockRow;
          const isBetweenCols = (col <= blockCol) && (col + ans['length'] > blockCol);
          
          return isSameRow && isBetweenCols;
        } else {
          const isBetweenRows = (row <= blockRow) && (row + ans['length'] > blockRow);
          const isSameCol = col === blockCol;

          return isBetweenRows && isSameCol;
        }
      });
    }

    const adjustPointerDimensionCell = (boxes) => {
      let counter = 0;

      return boxes.map((ans, i) => {
        if (ans.dimensions.length !== 0) {
          const pointer = ++counter;
          
          // adjust pointer to clues
          for (const dim of ans.dimensions) {
            const currBlock = findExistingBlock(dim, i);
            currBlock.pointer = pointer;
          }

          return {
            ...ans,
            "pointer": pointer
          };
        }
        
        return ans;
      })
    }

    const pointToBlock = (index) => {
      let block;
      let dim = 'across';

      if (index != activeCell.index) {
        block = findExistingBlock(dim, index);
      } else {
        dim = (activeCell.blockDimension != "across") ? "across" : "down";
        block = findExistingBlock(dim, index);
      }

      activeCell.blockId = block.id;
      activeCell.index = index;

      enableActiveBlock(block);
      if (!isScreenSmall.value) {
        scrollClueIntoView(block);
      }
    }

    // scroll clue to screen view
    const scrollClueIntoView = (block) => {
      const scrollIntoViewOptions = { behavior: 'smooth', block: 'start' };
      const li = (block.dimension == 'across')
        ? Array.from(acrossList.value.children).find(el => el.id == block.id)
        : Array.from(downList.value.children).find(el => el.id == block.id);
      
      li.scrollIntoView(scrollIntoViewOptions);
    }

    const setActiveAnswer = (dim, id) => {
      const block = ans_and_clues[dim].find(ans => ans.id == id);
      enableActiveBlock(block);
      activeCell.blockId = id;
    }

    const enableActiveBlock = (block) => {
      const [row, col] = block.spot;
      let cellNumbers = [];

      for (let i = 0; i < block['length']; i++) {
        const cell = (block.dimension == 'across')
          ? row * grid.size + (col + i)
          : (row + i) * grid.size + col;

        cellNumbers.push(cell);
      }

      gridBoxes.value = gridBoxes.value.map((box, index) => ({
        ...box,
        isVisible: cellNumbers.includes(index),
        isDimensionEnable: box.pointer == block.pointer
      }));

      activeCell.clue = block.clue;
      activeCell.clueNumbher = block.pointer;
      activeCell.blockDimension = block.dimension;
    }

    const adjustInitializedBoxes = (currGrid) => {
      const isAdmin = internalInstance.appContext.config.globalProperties.is_admin; // globalproperties
      let boxes = [];

      // adjust cell value
      for (let i=0; i < grid.size; i++) {
        for (let j=0; j < grid.size; j++) {
          // print answers for admin
          const cell = isAdmin 
            ? currGrid[i][j]
            : (currGrid[i][j] == '#' ? '#' : '');
          
          boxes[i * grid.size + j] = {
            "cell": cell,
            "dimensions": []
          }
        }
      }

      // adjust box dimension answers
      ans_and_clues.across.concat(ans_and_clues.down)
        .forEach(ans => {
          const [row, col] = ans.spot;
          boxes[row * grid.size + col].dimensions.push(ans.dimension);
        });

      gridBoxes.value = adjustPointerDimensionCell(boxes);
      sortAnsClues('across');
      sortAnsClues('down');
    }

    const resizeListener = () => {
      isScreenSmall.value = window.matchMedia('(max-width: 540px)').matches;
    }

    onMounted(async () => {
      const { answers, grid } = props.gridData;
      seperateCluesByDimensions(answers);
      adjustInitializedBoxes(grid);

      gridSchema.value = crossword.value;
      theme.value = props.gridData.theme;

      // listeners
      window.addEventListener("resize", resizeListener);
    });
    onBeforeUnmount(() => window.removeEventListener("resize", resizeListener));
    
    return {
      crossword,
      isScreenSmall,
      message,
      acrossList,
      downList,
      gridBoxes,
      gridSchema,
      theme,
      
      grid,
      activeCell,
      ans_and_clues,

      adjustInput,
      setActiveAnswer,
      pointToBlock
    }
  },
}
</script>

<style lang="scss" scoped>
  @import '../assets/styles/grid.scss';
</style>
