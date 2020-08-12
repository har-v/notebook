var date = new Date();
var monthsArr = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP',
                'OCT', 'DEC'];
var month = monthsArr[date.getMonth()];
var year = date.getFullYear();
var day = date.getDate();

document.getElementById('day').textContent = day;
document.getElementById('month').textContent = month;
document.getElementById('year').textContent = year;

function checkTime(i) {
    if (i < 10) {
        i = "0" + i;
    }
    return i;
}

function startTime() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();

    // add a zero in front of numbers<10
    m = checkTime(m);

    document.getElementById('time').innerHTML = h + ":" + m ;
    t = setTimeout(function() {
        startTime()
    }, 500);
}
startTime();
