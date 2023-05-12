const fs = require('fs');

// Read input from file
const input = fs.readFileSync('input.txt', 'utf8').trim().split('\n').map(line => line.split(','));

// Find and replace common expressions
for (let i = 0; i < input.length; i++) {
  for (let j = i + 1; j < input.length; j++) {
    if (input[i][1] === input[j][1]) {
      for (let d = 0; d < input.length; d++) {
        const right = input[d][1];
        const left = input[d][0];
        const b = Array.from(right).map(() => right.length);

        for (let z = 0; z < b[d]; z++) {
          if (right[z] === input[j][0]) {
            const x = Array.from(right);
            x[z] = input[i][0];
            const l = x.join('');
            input[d][1] = right.replace(input[j][0], input[i][0]);
          }
        }
      }
      input[j][0] = input[i][0];
    }
  }
}

// Write intermediate output to file
let output = input.map(line => line.join(',')).join('\n');
fs.writeFileSync('output.txt', output);

// Remove redundant code
output = fs.readFileSync('output.txt', 'utf8').trim().split('\n').map(line => line.split(','));
let i = 0;
let j = 1;
while (j < output.length) {
  if (output[i][1] === output[j][1]) {
    if (output[i][0] === output[j][0]) {
      output.splice(j, 1);
      i += 2;
      j = i + 1;
    } else {
      i += 1;
    }
  } else {
    j += 1;
  }
  if (j === output.length) {
    i = i + 1;
    j = i + 1;
  }
  if (i === output.length) {
    j = output.length;
  }
}

// Write intermediate output to file
output = output.map(line => line.join(',')).join('\n');
fs.writeFileSync('output.txt', output);

// Remove dead code
output = fs.readFileSync('output.txt', 'utf8').trim().split('\n').map(line => line.split(','));
let count = 0;
i = 0;
j = 0;
while (j < output.length && i < output.length) {
  const b = Array.from(output[j][1]).map(() => output[j][1].length);

  for (let z = 0; z < b[0]; z++) {
    if (output[j][1][z] === output[i][0]) {
      count = 1;
    }
  }
  j += 1;

  if (j === output.length) {
    if (count !== 1) {
      output.splice(i, 1);
      i = 0;
      j = 0;
    } else {
      i += 1;
      j = 0;
    }
  }
}

// Write final output to file
output = output.map(line => line.join('=')).join('\n');
fs.writeFileSync('output.txt', output);

// Print final output to console
console.log('The final optimized code is...');
console.log(output);
