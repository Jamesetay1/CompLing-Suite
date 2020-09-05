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
//Mr. & Dr.?
//Quotation marks? Include as optional in all quotation marks
//Followed optionally my a quatation mark --
function parseSentences() {
  console.log("Now parsing text...")

  sentencesStar = text.replace(/(Mr|Dr|Mrs|Ms|e\.g|e\.t\.c|i\.e)\./g, "$1***")
  console.log(sentencesStar)
  sentencesStarParsed = sentencesStar.replace(/([.?!]"?)(\s*)("?[A-Z0-9])/g, "$1|$2$3")
  console.log(sentencesStarParsed)
  sentencesParsed = sentencesStarParsed.replace(/(\*\*\*)/g, ".")
  console.log(sentencesParsed)

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
