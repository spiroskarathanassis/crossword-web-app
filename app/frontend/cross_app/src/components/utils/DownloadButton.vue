<template>
  <div>

    <div class="btn-group" dropdown dropdown-append-to-body>
      <div>
        <div @click="() => isDownloadExpanded = !isDownloadExpanded" 
          class="btn btn-primary"
          :style="isDownloadExpanded && 'border-radius: 2px 2px 0 0;'"
        >
          Download as
          <span class="caret"></span>
        </div>
        <ul v-if="isDownloadExpanded" class="dropdown-menu">
          <li @click="downloadPdf">
            <span>Pdf</span>
          </li>
          <!-- <li @click="downloadPuz">
            <span>Puzzle</span>
          </li> -->
        </ul>
      </div>
    </div>
    
  </div>
</template>

<script>
import { ref } from 'vue';

import { jsPDF } from 'jspdf';
import { toJpeg } from 'html-to-image';

export default {
  name: 'DownloadButton',
  props: ['htmlSchema', 'theme', 'clues_ans'],
  setup(props) {
    const isDownloadExpanded = ref(false);
    const pdfDoc = ref(null);

    const setFirstPagePdf = async (theme) => {
      // Set fonts
      pdfDoc.value.setFont('times');
      pdfDoc.value.setFontSize(12);
      
      pdfDoc.value.setPage(1);

      // Personal Infos
      pdfDoc.value.text('Spiros Karathanassis'        , 10, 15); // Full name
      pdfDoc.value.text('Kalamogdarti 8A, 26222'      , 10, 20); // Adress
      pdfDoc.value.text('Patras, Greece'              , 10, 25); // City
      pdfDoc.value.text('skarathanassisdev@gmail.com' , 10, 30); // email
      
      // Title - Theme
      const themeWidth = pdfDoc.value.getTextWidth(theme);
      const colStart = Math.floor(220/2 - themeWidth/2);
      pdfDoc.value.text(theme, colStart, 45);
      
      // Image
      await toJpeg(props.htmlSchema)
        .then((dataUrl) => {
          const img = new Image();
          img.src = dataUrl;

          pdfDoc.value.addImage(img, 'JPEG', 40, 70, 130, 130);
        })
        .catch(e => console.log(e));
    }

    const addCluesOnPdf = (clues) => {
      // Set fonts
      pdfDoc.value.setFont('times');
      pdfDoc.value.setFontSize(10);
      
      // Set Page start
      let currentPage = 2;
      pdfDoc.value.addPage();
      pdfDoc.value.setPage(currentPage); // Start across in 2nd page

      let answerCounter = 0; // break page per 25 answers
      let dimHeaderMarginBottomPixel = 20;
      let startPoint = 20;
      let currentColumnPixel = 0;
      let isPageIncludesHead = false;

      ['across', 'down'].forEach(dim => {
        // ACROSS or DOWN
        pdfDoc.value.text(dim.toUpperCase(), 10, startPoint + currentColumnPixel);
        startPoint += dimHeaderMarginBottomPixel + (dim !== 'across' ? 10 : 0);
        isPageIncludesHead = true;

        clues[dim].forEach(ans => {
          currentColumnPixel = answerCounter * 10 + startPoint;
          answerCounter++;

          // 3 columns of pointer, answers and clues
          pdfDoc.value.text(ans.pointer.toString(),   10,  currentColumnPixel);
          pdfDoc.value.text(ans.clue,                 20,  currentColumnPixel);
          pdfDoc.value.text(ans.answer.toUpperCase(), 170, currentColumnPixel);
    
          // 25 answers split page with header dimension or 27
          const compareAnswerNumberPerPage = isPageIncludesHead ? 24 : 27;

          if (answerCounter == compareAnswerNumberPerPage) {
            answerCounter = 0;
            currentPage++;
            startPoint = 20;

            pdfDoc.value.addPage();
            pdfDoc.value.setPage(currentPage);
            isPageIncludesHead = false;
          }
        });
      });
    }

    // Capitilize theme
    const adjustedTheme = () => {
      let theme = props.theme.split('');
      theme[0] = theme[0].toUpperCase();
      return theme.join('');
    }

    const generatePdf = async () => {
      pdfDoc.value = new jsPDF();
      const theme = adjustedTheme();
      await setFirstPagePdf(theme);
      
      addCluesOnPdf(props.clues_ans);
    }
    
    const downloadPdf = async() => {
      if (!props.htmlSchema || !props.theme)
        return;
      // needs a loader
      await generatePdf();
      const lastname = 'Karathanassis';
      const puzzleTheme = adjustedTheme();
      pdfDoc.value.save(`${lastname}_${puzzleTheme}.pdf`);

      isDownloadExpanded.value = !isDownloadExpanded.value;
    }

    return {
      isDownloadExpanded,
      downloadPdf
    }
  }
}
</script>

<style lang="scss" scoped>
  $dropdown-bg: rgba(0, 0, 0, 0.8);
  $font-color: #dcdad7;

  .btn-group {
    position: relative;
    width: max-content;
    margin: 0 10px;
    box-shadow: 0 1px 5px rgba(0,0,0,.4);
    cursor: pointer;
  }
  .caret {
    display: inline-block;
    width: 0;
    height: 0;
    margin-left: 2px;
    vertical-align: middle;
    border-top: 4px dashed;
    border-right: 4px solid transparent;
    border-left: 4px solid transparent;
  }

  .dropdown-menu {
    position: absolute;
    z-index: 10;
    width: 100%;
    list-style-type: none;
    background-color: $dropdown-bg;
    border: none;
    border-radius: 0 0 2px 2px;
    margin-top: 0;
    margin-block-start: 0;
    margin-block-end: 0;
    padding-inline-start: 0;
    
    li {
      border-top: 1px solid $font-color;
      padding: 8px 20px;

      &:hover, &:focus, &:active, &:active &:focus {
        background: rgb(56 60 62);
        border-radius: 0 0 2px 2px;
      }

      span {
        color: $font-color;
      }
    }
  }

  .btn {
    border: 1px solid rgba(0,0,0,0);
    border-radius: 2px;
    padding: 10px 20px;
    
    &:hover, &:focus, &:active, &:active &:focus {
      border: 1px solid rgba(0,0,0,0);
      outline: none !important;
    }
  }

  .btn-primary {
    background-color: $dropdown-bg;
    color: $font-color;
  }
</style>