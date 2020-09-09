var text = null

function init() {
  document.getElementById('inputfile')
    .addEventListener('change', function() {

      var fr = new FileReader();
      fr.onload = function() {
        document.getElementById('output')
          .textContent = fr.result;
        text = fr.result
        console.log(fr)
      }

      fr.readAsText(this.files[0]);
    })
}

function parseSentences() {
  console.log("Now parsing text...")

  sentencesStar = text.replace(/(Mr|Dr|Mrs|Ms|U\.S|e\.g|e\.t\.c|i\.e)\./g, "$1***")
  sentencesStarParsed = sentencesStar.replace(/([.?!]"?)(\s*)("?[A-Z0-9])/g, "$1|$2$3")
  sentencesParsed = sentencesStarParsed.replace(/(\*\*\*)/g, ".")

  //Output here
  download("parsedDocument.txt", sentencesParsed);
}

function download(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}