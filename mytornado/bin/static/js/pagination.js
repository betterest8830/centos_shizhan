
function firstPage(){
    hide();
    currPageNum = 1;
    showCurrPage(currPageNum);
    showTotalPage();
    for(i = 1; i < pageCount + 1; i++){
        blockTable.rows[i].style.display = "";
    }

    firstText();
    preText();
    nextLink();
    lastLink();
}

function prePage(){
    hide();
    currPageNum--;
    showCurrPage(currPageNum);
    showTotalPage();
    var firstR = firstRow(currPageNum);
    var lastR = lastRow(firstR);
    for(i = firstR; i < lastR; i++){
        blockTable.rows[i].style.display = "";
    }

    if(1 == currPageNum){
        firstText();
        preText();
        nextLink();
        lastLink();
    }else if(pageNum == currPageNum){
        preLink();
        firstLink();
        nextText();
        lastText();
    }else{
        firstLink();
        preLink();
        nextLink();
        lastLink();
    }

}

function nextPage(){
    hide();
    currPageNum++;
    showCurrPage(currPageNum);
    showTotalPage();
    var firstR = firstRow(currPageNum);
    var lastR = lastRow(firstR);
    for(i = firstR; i < lastR; i ++){
        blockTable.rows[i].style.display = "";
    }

    if(1 == currPageNum){
        firstText();
        preText();
        nextLink();
        lastLink();
    }else if(pageNum == currPageNum){
        preLink();
        firstLink();
        nextText();
        lastText();
    }else{
        firstLink();
        preLink();
        nextLink();
        lastLink();
    }
}

function lastPage(){
    hide();
    currPageNum = pageNum;
    showCurrPage(currPageNum);
    showTotalPage();
    var firstR = firstRow(currPageNum);
    for(i = firstR; i < numCount + 1; i++){
        blockTable.rows[i].style.display = "";
    }

    firstLink();
    preLink();
    nextText();
    lastText();
}

function firstRow(currPageNum){
    return pageCount*(currPageNum - 1) + 1;
}

function lastRow(firstRow){
    var lastRow = firstRow + pageCount;
    if(lastRow > numCount + 1){
        lastRow = numCount + 1;
    }
    return lastRow;
}

function showCurrPage(cpn){
    currPageSpan.innerHTML = cpn;
}

function showTotalPage(){
    pageNumSpan.innerHTML = pageNum;
}

function hide(){
    for(var i = 1; i < numCount + 1; i ++){
        blockTable.rows[i].style.display = "none";
    }
}

function firstLink(){firstSpan.innerHTML = "<a href='javascript:firstPage();'>First</a>";}
function firstText(){firstSpan.innerHTML = "First";}

function preLink(){preSpan.innerHTML = "<a href='javascript:prePage();'>Pre</a>";}
function preText(){preSpan.innerHTML = "Pre";}

function nextLink(){nextSpan.innerHTML = "<a href='javascript:nextPage();'>Next</a>";}
function nextText(){nextSpan.innerHTML = "Next";}

function lastLink(){lastSpan.innerHTML = "<a href='javascript:lastPage();'>Last</a>";}
function lastText(){lastSpan.innerHTML = "Last";}