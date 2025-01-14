var el = document.getElementsByClassName('myamount');
var sum = 0;

for (var element of el) {
    value = element.innerText.trim()
    sum += parseFloat(value) || 0;
    console.log(sum)
}

document.write(sum);