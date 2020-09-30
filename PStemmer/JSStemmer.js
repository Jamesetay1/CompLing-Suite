const inputString = "roll"
let v = inputString.toLowerCase();
console.log(v)

v = v.replace(/([^aeiou])y/g, "$1Y")
// Y is the vowel, y is the consonant

function repl(a, b) {
  const V = '[aeiouY]'
  const C = '[^aeiouY]'
  if (typeof a === 'string') {
    a = a.replace(/V/g, V).replace(/C/g, C);
    a = new RegExp(a);
  }
  if (a.test(v)) {
    v = v.replace(a, b);
    return true;
  }
  return false;
}

//step 5a
repl('(C*(V+C+){2,}V*)e$', "$1") || repl('(C*(V+[b-df-hj-np-tvz]+)V*)e$', "$1")
//step 5b
repl('(C*(V+C+){1,}V+)ll$', "$1l")

console.log(v)