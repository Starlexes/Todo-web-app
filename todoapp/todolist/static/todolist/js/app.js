
let tasksConts = document.querySelectorAll('.tasks-cont');
let body = document.querySelector('.tasks-list');

let importances = {'critical':[], 'high':[], 'medium':[], 'low':[]};

let options = document.getElementById('ordering');
let importance = options[0].innerText;
let finished = options[1].innerText;
let noFinished = options[2].innerText;



let orderByNotFinished = [];
let orderByFinished = [];

for (elem of tasksConts) {
    let textElem = elem.querySelector('.task-finished').innerText;
    let imp = elem.querySelector('.task-finish-date').firstChild.className;

    if (textElem.includes('❌')) {
        orderByNotFinished.push(elem.innerHTML);
    }

    else {
        orderByFinished.push(elem.innerHTML);
    }
  
    if (imp.includes('critical')) {
        importances['critical'].push(elem.innerHTML);
    }

    else if (imp.includes('high')) {
        importances['high'].push(elem.innerHTML);
    }

    else if (imp.includes('medium')) {
        importances['medium'].push(elem.innerHTML);
    }

    else {
        importances['low'].push(elem.innerHTML);
    }
}


options.addEventListener('click', function() {
    switch (options.value) {
        case finished:
            getFinished();
            break;
        case noFinished:
            getNotFinished();
            break;
        case importance:
            getImportance();
            break;
        default:
            break;
    }
});


function getNotFinished() {
    body.innerHTML = '';
    for (elem of orderByNotFinished) {
    
        body.innerHTML +=elem;
    }
}

function getFinished() {
    body.innerHTML = '';
    for (elem of orderByFinished) {
        
        body.innerHTML +=elem;
    }
}

function getImportance() {
    let impArr = [];
    body.innerHTML = '';
    for (named in importances ) {
        impArr.push(...importances[named]);
    }
  
    for (elem of impArr) {
        body.innerHTML+=elem;
    }
}
    
